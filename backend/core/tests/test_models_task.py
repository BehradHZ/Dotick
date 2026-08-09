"""
Stage 2 — Core Task, Event, and Routine Management.

Seam under test: core.models (BaseEvent, Task) — Django model layer,
per ROADMAP.md §4.1 (CTI), §4.2 (Task/Event independent types), §4.3
(Task status model).
"""

from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from core.models import BaseEvent, Task


class BaseEventTaskCTITests(TestCase):
    """
    §4.1: base_events holds shared fields; tasks holds a FK back to
    base_events (Django multi-table inheritance) and only task-specific
    fields.
    """

    def test_task_is_created_with_a_backing_base_event_row(self):
        task = Task.objects.create(title="Write the roadmap")

        # Task IS-A BaseEvent via multi-table inheritance: the same pk
        # identifies both rows.
        self.assertTrue(BaseEvent.objects.filter(pk=task.pk).exists())
        self.assertEqual(BaseEvent.objects.get(pk=task.pk).title, "Write the roadmap")

    def test_base_event_shared_fields_are_present(self):
        task = Task.objects.create(title="Write the roadmap", description="Details here")

        base = BaseEvent.objects.get(pk=task.pk)
        self.assertEqual(base.title, "Write the roadmap")
        self.assertEqual(base.description, "Details here")
        self.assertIsNotNone(base.created_at)
        self.assertIsNotNone(base.updated_at)


class TaskEffectiveStatusTests(TestCase):
    """
    ROADMAP.md §4.3 — the six user-visible statuses, computed from
    `user_status` (NULL/DONE/WONT_DO) plus the time-driven fields
    (due_date, deadline, deadline_enabled, grace_period) when
    user_status is NULL.
    """

    def _make_task(self, **kwargs):
        return Task.objects.create(title="t", **kwargs)

    # --- Explicit user_status short-circuits time computation entirely ---

    def test_done_status_is_explicit_regardless_of_time_fields(self):
        past = timezone.now() - timedelta(days=30)
        task = self._make_task(
            user_status=Task.UserStatus.DONE,
            due_date=past,
            deadline_enabled=True,
            deadline=past,
            grace_period=timedelta(days=1),
        )
        self.assertEqual(task.effective_status, Task.Status.DONE)

    def test_wont_do_status_is_explicit_regardless_of_time_fields(self):
        task = self._make_task(user_status=Task.UserStatus.WONT_DO)
        self.assertEqual(task.effective_status, Task.Status.WONT_DO)

    # --- Time-driven states (user_status is NULL) ---

    def test_todo_when_due_date_in_future(self):
        future = timezone.now() + timedelta(days=1)
        task = self._make_task(due_date=future, deadline_enabled=False)
        self.assertEqual(task.effective_status, Task.Status.TODO)

    def test_todo_when_deadline_disabled_even_past_due_date(self):
        past = timezone.now() - timedelta(days=10)
        task = self._make_task(due_date=past, deadline_enabled=False)
        self.assertEqual(task.effective_status, Task.Status.TODO)

    def test_overdue_when_due_date_passed_but_deadline_not_reached(self):
        due = timezone.now() - timedelta(days=1)
        deadline = timezone.now() + timedelta(days=5)
        task = self._make_task(
            due_date=due, deadline_enabled=True, deadline=deadline
        )
        self.assertEqual(task.effective_status, Task.Status.OVERDUE)

    def test_missed_when_deadline_passed_but_within_grace_period(self):
        due = timezone.now() - timedelta(days=10)
        deadline = timezone.now() - timedelta(days=1)
        task = self._make_task(
            due_date=due,
            deadline_enabled=True,
            deadline=deadline,
            grace_period=timedelta(days=7),
        )
        self.assertEqual(task.effective_status, Task.Status.MISSED)

    def test_auto_wont_do_when_grace_period_elapsed(self):
        due = timezone.now() - timedelta(days=30)
        deadline = timezone.now() - timedelta(days=20)
        task = self._make_task(
            due_date=due,
            deadline_enabled=True,
            deadline=deadline,
            grace_period=timedelta(days=7),
        )
        self.assertEqual(task.effective_status, Task.Status.AUTO_WONT_DO)

    def test_boundary_exactly_at_due_date_is_still_todo(self):
        """§4.3: TODO condition is `now <= due_date` (inclusive)."""
        now = timezone.now()
        task = self._make_task(
            due_date=now, deadline_enabled=True, deadline=now + timedelta(days=1)
        )
        # Can't hit the exact instant, but due_date in the very near
        # future with deadline_enabled=True and now still <= due_date
        # must be TODO, not OVERDUE.
        task.due_date = timezone.now() + timedelta(seconds=5)
        task.save()
        self.assertEqual(task.effective_status, Task.Status.TODO)

    def test_boundary_exactly_at_deadline_is_still_overdue_not_missed(self):
        """§4.3: MISSED condition is `deadline < now`, so at/before deadline is OVERDUE."""
        due = timezone.now() - timedelta(days=1)
        deadline = timezone.now() + timedelta(seconds=5)
        task = self._make_task(due_date=due, deadline_enabled=True, deadline=deadline)
        self.assertEqual(task.effective_status, Task.Status.OVERDUE)

    def test_deadline_disabled_can_never_become_missed_or_auto_wont_do(self):
        """§4.3 note: deadline_enabled=false can never be MISSED/AUTO_WONT_DO."""
        long_past = timezone.now() - timedelta(days=365)
        task = self._make_task(
            due_date=long_past,
            deadline_enabled=False,
            deadline=long_past,
            grace_period=timedelta(days=1),
        )
        self.assertEqual(task.effective_status, Task.Status.TODO)
