"""
Stage 2 — Event and Routine REST APIs (ROADMAP.md §6 Stage 2).

Seam under test: HTTP requests against /api/events/ and
/api/routines/ — DRF ViewSets wrapping the respective models.
"""

from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from core.models import Event, Routine


class EventCRUDApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_event(self):
        start = timezone.now() + timedelta(hours=1)
        end = start + timedelta(hours=1)
        response = self.client.post(
            "/api/events/",
            {
                "title": "Standup",
                "start_time": start.isoformat(),
                "end_time": end.isoformat(),
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Event.objects.filter(title="Standup").exists())

    def test_retrieve_event_includes_status(self):
        start = timezone.now() + timedelta(hours=1)
        end = start + timedelta(hours=1)
        event = Event.objects.create(title="Standup", start_time=start, end_time=end)

        response = self.client.get(f"/api/events/{event.pk}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "UPCOMING")

    def test_list_events(self):
        start = timezone.now()
        end = start + timedelta(hours=1)
        Event.objects.create(title="A", start_time=start, end_time=end)
        Event.objects.create(title="B", start_time=start, end_time=end)

        response = self.client.get("/api/events/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_update_event(self):
        start = timezone.now()
        end = start + timedelta(hours=1)
        event = Event.objects.create(title="Old", start_time=start, end_time=end)

        response = self.client.patch(
            f"/api/events/{event.pk}/", {"title": "New"}, format="json"
        )

        self.assertEqual(response.status_code, 200)
        event.refresh_from_db()
        self.assertEqual(event.title, "New")

    def test_delete_event(self):
        start = timezone.now()
        end = start + timedelta(hours=1)
        event = Event.objects.create(title="Gone", start_time=start, end_time=end)

        response = self.client.delete(f"/api/events/{event.pk}/")

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Event.objects.filter(pk=event.pk).exists())


class RoutineCRUDApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_routine(self):
        period_end = timezone.now() + timedelta(hours=12)
        response = self.client.post(
            "/api/routines/",
            {"title": "Morning stretch", "period_end": period_end.isoformat()},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Routine.objects.filter(title="Morning stretch").exists())

    def test_retrieve_routine_includes_status(self):
        period_end = timezone.now() + timedelta(hours=12)
        routine = Routine.objects.create(title="Stretch", period_end=period_end)

        response = self.client.get(f"/api/routines/{routine.pk}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "TODO")

    def test_mark_routine_done(self):
        period_end = timezone.now() + timedelta(hours=12)
        routine = Routine.objects.create(title="Stretch", period_end=period_end)

        response = self.client.patch(
            f"/api/routines/{routine.pk}/", {"user_status": "DONE"}, format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "DONE")

    def test_mark_routine_wont_do_then_reverse_it(self):
        period_end = timezone.now() + timedelta(hours=12)
        routine = Routine.objects.create(title="Stretch", period_end=period_end)

        self.client.patch(
            f"/api/routines/{routine.pk}/", {"user_status": "WONT_DO"}, format="json"
        )
        response = self.client.patch(
            f"/api/routines/{routine.pk}/", {"user_status": None}, format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "TODO")

    def test_delete_routine(self):
        period_end = timezone.now() + timedelta(hours=12)
        routine = Routine.objects.create(title="Gone", period_end=period_end)

        response = self.client.delete(f"/api/routines/{routine.pk}/")

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Routine.objects.filter(pk=routine.pk).exists())
