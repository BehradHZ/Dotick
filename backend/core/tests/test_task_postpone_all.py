"""
Stage 2 — Postpone All (bulk), ROADMAP.md §4.7.

Seam under test: Task.objects.postpone_all() — applies Task.postpone()
logic to every OVERDUE/MISSED task at once. Reuses the single-task
postpone() method per-row so both entry points share one source of
truth for the branching behavior, logging each affected task
individually (§4.8) with action="postpone_all".
"""

from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from core.models import Task


class PostponeAllTests(TestCase):
    def _overdue_task(self):
        return Task.objects.create(
            title="overdue",
            due_date=timezone.now() - timedelta(days=1),
            deadline_enabled=True,
            deadline=timezone.now() + timedelta(days=5),
        )

    def _missed_task(self):
        return Task.objects.create(
            title="missed",
            due_date=timezone.now() - timedelta(days=10),
            deadline_enabled=True,
            deadline=timezone.now() - timedelta(days=1),
            grace_period=timedelta(days=7),
        )

    def _todo_task(self):
        return Task.objects.create(
            title="todo",
            due_date=timezone.now() + timedelta(days=3),
            deadline_enabled=False,
        )

    def _done_task(self):
        return Task.objects.create(title="done", user_status=Task.UserStatus.DONE)

    def test_postpones_every_overdue_and_missed_task(self):
        overdue = self._overdue_task()
        missed = self._missed_task()

        Task.objects.postpone_all()

        overdue.refresh_from_db()
        missed.refresh_from_db()
        # due_date was shifted to "now" for both — checked via a tight
        # tolerance rather than effective_status, since due_date==now()
        # means effective_status can tick back to OVERDUE within
        # microseconds of the call (real, correct §4.3 behavior, not a
        # bug: postpone sets due_date to the instant it ran, and time
        # keeps moving after that).
        self.assertAlmostEqual(
            overdue.due_date, timezone.now(), delta=timedelta(seconds=5)
        )
        self.assertAlmostEqual(
            missed.due_date, timezone.now(), delta=timedelta(seconds=5)
        )
        # OVERDUE branch: deadline stays enabled.
        self.assertTrue(overdue.deadline_enabled)
        # MISSED branch: deadline gets disabled, value preserved.
        self.assertFalse(missed.deadline_enabled)

    def test_does_not_touch_todo_or_done_or_wont_do_tasks(self):
        todo = self._todo_task()
        done = self._done_task()
        original_todo_due = todo.due_date

        Task.objects.postpone_all()

        todo.refresh_from_db()
        done.refresh_from_db()
        self.assertEqual(todo.due_date, original_todo_due)
        self.assertEqual(done.user_status, Task.UserStatus.DONE)

    def test_returns_the_number_of_tasks_postponed(self):
        self._overdue_task()
        self._missed_task()
        self._todo_task()

        count = Task.objects.postpone_all()

        self.assertEqual(count, 2)

    def test_logs_one_entry_per_postponed_task_with_postpone_all_action(self):
        self._overdue_task()
        self._missed_task()
        self._todo_task()

        with self.assertLogs("dotick.audit", level="INFO") as captured:
            Task.objects.postpone_all()

        self.assertEqual(len(captured.records), 2)
        for record in captured.records:
            self.assertEqual(record.action, "postpone_all")

    def test_empty_when_nothing_needs_postponing(self):
        self._todo_task()
        self._done_task()

        count = Task.objects.postpone_all()

        self.assertEqual(count, 0)
