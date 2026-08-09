"""
Stage 2 — Event model and status (ROADMAP.md §4.2, §4.5).

Seam under test: core.models.Event — a CTI child of BaseEvent,
independent of Task. Events use a purely time-driven three-state model
with no stored status field at all.
"""

from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from core.models import BaseEvent, Event


class EventCTITests(TestCase):
    def test_event_is_created_with_a_backing_base_event_row(self):
        start = timezone.now() + timedelta(hours=1)
        end = start + timedelta(hours=2)
        event = Event.objects.create(title="Standup", start_time=start, end_time=end)

        self.assertTrue(BaseEvent.objects.filter(pk=event.pk).exists())
        self.assertEqual(BaseEvent.objects.get(pk=event.pk).title, "Standup")


class EventStatusTests(TestCase):
    """
    §4.5: UPCOMING (now < start_time), ONGOING (start_time <= now <=
    end_time), PAST (now > end_time). Fully computed, no stored status
    field.
    """

    def _make_event(self, start_time, end_time):
        return Event.objects.create(title="e", start_time=start_time, end_time=end_time)

    def test_upcoming_when_start_time_in_future(self):
        start = timezone.now() + timedelta(hours=1)
        end = start + timedelta(hours=1)
        event = self._make_event(start, end)
        self.assertEqual(event.status, Event.Status.UPCOMING)

    def test_ongoing_when_now_between_start_and_end(self):
        start = timezone.now() - timedelta(minutes=30)
        end = timezone.now() + timedelta(minutes=30)
        event = self._make_event(start, end)
        self.assertEqual(event.status, Event.Status.ONGOING)

    def test_past_when_end_time_has_passed(self):
        start = timezone.now() - timedelta(hours=2)
        end = timezone.now() - timedelta(hours=1)
        event = self._make_event(start, end)
        self.assertEqual(event.status, Event.Status.PAST)

    def test_boundary_exactly_at_start_time_is_ongoing_not_upcoming(self):
        """§4.5: ONGOING condition is `start_time <= now` (inclusive)."""
        start = timezone.now() + timedelta(seconds=5)
        end = start + timedelta(hours=1)
        event = self._make_event(start, end)
        event.start_time = timezone.now()
        event.save()
        self.assertEqual(event.status, Event.Status.ONGOING)

    def test_boundary_exactly_at_end_time_is_ongoing_not_past(self):
        """§4.5: ONGOING condition is `now <= end_time` (inclusive), PAST is `now > end_time`."""
        start = timezone.now() - timedelta(hours=1)
        end = timezone.now() + timedelta(seconds=5)
        event = self._make_event(start, end)
        self.assertEqual(event.status, Event.Status.ONGOING)

    def test_event_has_no_stored_status_field(self):
        """§4.5: no stored status field at all — status is a property, not a db column."""
        event_fields = {f.name for f in Event._meta.get_fields()}
        self.assertNotIn("status", event_fields)
        self.assertNotIn("user_status", event_fields)
