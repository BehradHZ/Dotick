"""
Stage 2 — Routine model and status (ROADMAP.md §4.2, §4.6).

Seam under test: core.models.Routine — a CTI child of BaseEvent,
independent of Task/Event. Stage 2 supports manually-created single
occurrences only; full recurrence generation is Stage 3 (§4.9).

Each Routine row here represents one occurrence (e.g. "today's" entry
for a daily routine), per the roadmap's own phrasing in §4.6.
"""

from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from core.models import BaseEvent, Routine


class RoutineCTITests(TestCase):
    def test_routine_is_created_with_a_backing_base_event_row(self):
        period_end = timezone.now() + timedelta(hours=12)
        routine = Routine.objects.create(title="Morning stretch", period_end=period_end)

        self.assertTrue(BaseEvent.objects.filter(pk=routine.pk).exists())
        self.assertEqual(BaseEvent.objects.get(pk=routine.pk).title, "Morning stretch")


class RoutineStatusTests(TestCase):
    """
    §4.6: TODO / DONE / WONT_DO (explicit, reversible) / AUTO_WONT_DO
    (period elapsed with no action). No OVERDUE/MISSED distinction,
    unlike Task — a routine occurrence has one period, not a separate
    due date vs. deadline.
    """

    def _make_routine(self, **kwargs):
        kwargs.setdefault("period_end", timezone.now() + timedelta(hours=1))
        return Routine.objects.create(title="r", **kwargs)

    def test_todo_when_occurrence_not_yet_resolved_and_period_not_elapsed(self):
        routine = self._make_routine(period_end=timezone.now() + timedelta(hours=1))
        self.assertEqual(routine.status, Routine.Status.TODO)

    def test_done_when_user_marks_complete(self):
        routine = self._make_routine(user_status=Routine.UserStatus.DONE)
        self.assertEqual(routine.status, Routine.Status.DONE)

    def test_done_even_after_period_elapsed(self):
        past = timezone.now() - timedelta(hours=1)
        routine = self._make_routine(
            period_end=past, user_status=Routine.UserStatus.DONE
        )
        self.assertEqual(routine.status, Routine.Status.DONE)

    def test_wont_do_when_user_explicitly_skips(self):
        routine = self._make_routine(user_status=Routine.UserStatus.WONT_DO)
        self.assertEqual(routine.status, Routine.Status.WONT_DO)

    def test_wont_do_is_reversible_by_clearing_user_status(self):
        routine = self._make_routine(
            period_end=timezone.now() + timedelta(hours=1),
            user_status=Routine.UserStatus.WONT_DO,
        )
        routine.user_status = None
        routine.save()
        self.assertEqual(routine.status, Routine.Status.TODO)

    def test_auto_wont_do_when_period_elapsed_with_no_action(self):
        past = timezone.now() - timedelta(hours=1)
        routine = self._make_routine(period_end=past)
        self.assertEqual(routine.status, Routine.Status.AUTO_WONT_DO)

    def test_boundary_exactly_at_period_end_is_still_todo(self):
        """Mirrors Task's inclusive due_date boundary (§4.3): not yet
        elapsed means `now <= period_end`."""
        routine = self._make_routine(period_end=timezone.now() + timedelta(seconds=5))
        routine.period_end = timezone.now() + timedelta(milliseconds=200)
        routine.save()
        self.assertEqual(routine.status, Routine.Status.TODO)

    def test_no_overdue_or_missed_states_exist(self):
        """§4.6: routines don't have OVERDUE/MISSED — only four statuses total."""
        status_values = {choice.value for choice in Routine.Status}
        self.assertEqual(status_values, {"TODO", "DONE", "WONT_DO", "AUTO_WONT_DO"})
