"""
Stage 2 — Postpone behavior (ROADMAP.md §4.7) and its logging
integration (§4.8).

Seam under test: Task.postpone() — a single-task action. "Postpone All"
(bulk) is layered on top of this in a later cycle.
"""

from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from core.models import Task


class PostponeTodoOrOverdueTests(TestCase):
    """
    §4.7 branch 1: postponing a TODO or OVERDUE task sets due_date=today;
    deadline is untouched.
    """

    def test_postpone_todo_task_sets_due_date_to_today_leaves_deadline_untouched(self):
        original_due = timezone.now() - timedelta(days=1)
        deadline = timezone.now() + timedelta(days=5)
        task = Task.objects.create(
            title="t",
            due_date=original_due,
            deadline_enabled=True,
            deadline=deadline,
        )
        self.assertEqual(task.effective_status, Task.Status.OVERDUE)

        task.postpone()

        task.refresh_from_db()
        self.assertAlmostEqual(
            task.due_date, timezone.now(), delta=timedelta(seconds=5)
        )
        self.assertEqual(task.deadline, deadline)
        self.assertTrue(task.deadline_enabled)

    def test_postpone_plain_todo_task_with_no_deadline_still_shifts_due_date(self):
        original_due = timezone.now() + timedelta(days=3)
        task = Task.objects.create(
            title="t", due_date=original_due, deadline_enabled=False
        )
        self.assertEqual(task.effective_status, Task.Status.TODO)

        task.postpone()

        task.refresh_from_db()
        self.assertAlmostEqual(
            task.due_date, timezone.now(), delta=timedelta(seconds=5)
        )
        self.assertFalse(task.deadline_enabled)


class PostponeMissedTests(TestCase):
    """
    §4.7 branch 2: postponing a MISSED task sets due_date=today AND turns
    deadline_enabled off. The stored deadline value is left untouched —
    not shifted, not cleared (§10.1, resolved).
    """

    def test_postpone_missed_task_sets_due_date_and_disables_deadline(self):
        due = timezone.now() - timedelta(days=10)
        deadline = timezone.now() - timedelta(days=1)
        task = Task.objects.create(
            title="t",
            due_date=due,
            deadline_enabled=True,
            deadline=deadline,
            grace_period=timedelta(days=7),
        )
        self.assertEqual(task.effective_status, Task.Status.MISSED)

        task.postpone()

        task.refresh_from_db()
        self.assertAlmostEqual(
            task.due_date, timezone.now(), delta=timedelta(seconds=5)
        )
        self.assertFalse(task.deadline_enabled)
        # Stored deadline value preserved untouched, not shifted/cleared.
        self.assertEqual(task.deadline, deadline)

    def test_postponed_missed_task_becomes_todo(self):
        due = timezone.now() - timedelta(days=10)
        deadline = timezone.now() - timedelta(days=1)
        task = Task.objects.create(
            title="t",
            due_date=due,
            deadline_enabled=True,
            deadline=deadline,
            grace_period=timedelta(days=7),
        )

        task.postpone()

        self.assertEqual(task.effective_status, Task.Status.TODO)

    def test_deadline_can_be_reenabled_after_missed_postpone_without_reentering_date(self):
        due = timezone.now() - timedelta(days=10)
        deadline = timezone.now() - timedelta(days=1)
        task = Task.objects.create(
            title="t",
            due_date=due,
            deadline_enabled=True,
            deadline=deadline,
            grace_period=timedelta(days=7),
        )
        task.postpone()

        task.deadline_enabled = True
        task.save()

        task.refresh_from_db()
        self.assertEqual(task.deadline, deadline)


class PostponeAutoWontDoTests(TestCase):
    """AUTO_WONT_DO is not TODO/OVERDUE/MISSED; postpone should still
    recover it the same way a MISSED task is recovered, since it's past
    the deadline (the grace period elapsing doesn't change which branch
    applies — deadline has still passed)."""

    def test_postpone_auto_wont_do_task_behaves_like_missed_branch(self):
        due = timezone.now() - timedelta(days=30)
        deadline = timezone.now() - timedelta(days=20)
        task = Task.objects.create(
            title="t",
            due_date=due,
            deadline_enabled=True,
            deadline=deadline,
            grace_period=timedelta(days=7),
        )
        self.assertEqual(task.effective_status, Task.Status.AUTO_WONT_DO)

        task.postpone()

        task.refresh_from_db()
        self.assertFalse(task.deadline_enabled)
        self.assertEqual(task.deadline, deadline)
        self.assertEqual(task.effective_status, Task.Status.TODO)


class PostponeLoggingTests(TestCase):
    """§4.8: every postpone writes a structured audit log entry via
    core.logging_utils.log_deadline_change (Stage 1.5's seam), not a
    domain history table."""

    def test_postpone_single_writes_an_audit_log_entry(self):
        due = timezone.now() - timedelta(days=1)
        deadline = timezone.now() + timedelta(days=5)
        task = Task.objects.create(
            title="t", due_date=due, deadline_enabled=True, deadline=deadline
        )

        with self.assertLogs("dotick.audit", level="INFO") as captured:
            task.postpone()

        self.assertEqual(len(captured.records), 1)
        record = captured.records[0]
        self.assertEqual(record.task_id, task.pk)
        self.assertEqual(record.action, "postpone_single")
        self.assertEqual(record.new_deadline_enabled, True)

    def test_postpone_missed_logs_deadline_enabled_toggle(self):
        due = timezone.now() - timedelta(days=10)
        deadline = timezone.now() - timedelta(days=1)
        task = Task.objects.create(
            title="t",
            due_date=due,
            deadline_enabled=True,
            deadline=deadline,
            grace_period=timedelta(days=7),
        )

        with self.assertLogs("dotick.audit", level="INFO") as captured:
            task.postpone()

        record = captured.records[0]
        self.assertEqual(record.action, "postpone_single")
        self.assertEqual(record.old_deadline_enabled, True)
        self.assertEqual(record.new_deadline_enabled, False)
