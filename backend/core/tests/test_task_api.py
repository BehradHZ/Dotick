"""
Stage 2 — Task REST API (ROADMAP.md §4, §6 Stage 2: "CRUD endpoints for
Task, Event, and Routine").

Seam under test: HTTP requests against /api/tasks/ — DRF ViewSet
wrapping the Task model, including the domain actions (Postpone,
Postpone All) alongside standard CRUD.
"""

from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from core.models import Task


class TaskCRUDApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_task(self):
        response = self.client.post(
            "/api/tasks/", {"title": "Write the roadmap"}, format="json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["title"], "Write the roadmap")
        self.assertTrue(Task.objects.filter(title="Write the roadmap").exists())

    def test_list_tasks(self):
        Task.objects.create(title="A")
        Task.objects.create(title="B")

        response = self.client.get("/api/tasks/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_task_includes_effective_status(self):
        future = timezone.now() + timedelta(days=1)
        task = Task.objects.create(title="A", due_date=future, deadline_enabled=False)

        response = self.client.get(f"/api/tasks/{task.pk}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["effective_status"], "TODO")

    def test_update_task(self):
        task = Task.objects.create(title="Old title")

        response = self.client.patch(
            f"/api/tasks/{task.pk}/", {"title": "New title"}, format="json"
        )

        self.assertEqual(response.status_code, 200)
        task.refresh_from_db()
        self.assertEqual(task.title, "New title")

    def test_delete_task(self):
        task = Task.objects.create(title="Gone soon")

        response = self.client.delete(f"/api/tasks/{task.pk}/")

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())

    def test_mark_task_done_via_update(self):
        task = Task.objects.create(title="A")

        response = self.client.patch(
            f"/api/tasks/{task.pk}/", {"user_status": "DONE"}, format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["effective_status"], "DONE")


class TaskDueDateDeadlineValidationTests(TestCase):
    """TESTING_PLAN.md §3.7: 'Invalid input (e.g., due_date after
    deadline) is rejected with a clear error, not silently accepted.'"""

    def setUp(self):
        self.client = APIClient()

    def test_create_rejects_due_date_after_deadline_when_deadline_enabled(self):
        due = timezone.now() + timedelta(days=10)
        deadline = timezone.now() + timedelta(days=5)

        response = self.client.post(
            "/api/tasks/",
            {
                "title": "Bad dates",
                "due_date": due.isoformat(),
                "deadline": deadline.isoformat(),
                "deadline_enabled": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("due_date", response.data)
        self.assertFalse(Task.objects.filter(title="Bad dates").exists())

    def test_create_accepts_due_date_after_deadline_when_deadline_disabled(self):
        """§4.3: while deadline_enabled=false the stored deadline is
        inert, so it must not block an unrelated due_date."""
        due = timezone.now() + timedelta(days=10)
        deadline = timezone.now() + timedelta(days=5)

        response = self.client.post(
            "/api/tasks/",
            {
                "title": "Fine for now",
                "due_date": due.isoformat(),
                "deadline": deadline.isoformat(),
                "deadline_enabled": False,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

    def test_create_accepts_due_date_equal_to_deadline(self):
        same = timezone.now() + timedelta(days=5)

        response = self.client.post(
            "/api/tasks/",
            {
                "title": "Same instant",
                "due_date": same.isoformat(),
                "deadline": same.isoformat(),
                "deadline_enabled": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

    def test_partial_update_rejects_due_date_moved_past_existing_deadline(self):
        """A PATCH that only sends due_date must still be checked
        against the task's already-stored deadline."""
        deadline = timezone.now() + timedelta(days=5)
        task = Task.objects.create(
            title="A", deadline_enabled=True, deadline=deadline,
            due_date=timezone.now(),
        )
        bad_due = timezone.now() + timedelta(days=10)

        response = self.client.patch(
            f"/api/tasks/{task.pk}/",
            {"due_date": bad_due.isoformat()},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        task.refresh_from_db()
        self.assertNotEqual(task.due_date, bad_due)

    def test_partial_update_rejects_deadline_moved_before_existing_due_date(self):
        """Same check, triggered from the other side: shrinking
        deadline below an already-stored due_date."""
        due = timezone.now() + timedelta(days=5)
        task = Task.objects.create(
            title="A", deadline_enabled=True, due_date=due,
            deadline=timezone.now() + timedelta(days=10),
        )
        bad_deadline = timezone.now() + timedelta(days=1)

        response = self.client.patch(
            f"/api/tasks/{task.pk}/",
            {"deadline": bad_deadline.isoformat()},
            format="json",
        )

        self.assertEqual(response.status_code, 400)


class TaskPostponeApiTests(TestCase):
    """§4.7 exposed as API actions, per the frontend's need for 'a
    visible way to trigger Postpone / Postpone All'."""

    def setUp(self):
        self.client = APIClient()

    def test_postpone_single_task(self):
        due = timezone.now() - timedelta(days=1)
        deadline = timezone.now() + timedelta(days=5)
        task = Task.objects.create(
            title="A", due_date=due, deadline_enabled=True, deadline=deadline
        )

        response = self.client.post(f"/api/tasks/{task.pk}/postpone/")

        self.assertEqual(response.status_code, 200)
        task.refresh_from_db()
        self.assertAlmostEqual(
            task.due_date, timezone.now(), delta=timedelta(seconds=5)
        )

    def test_postpone_all(self):
        overdue = Task.objects.create(
            title="overdue",
            due_date=timezone.now() - timedelta(days=1),
            deadline_enabled=True,
            deadline=timezone.now() + timedelta(days=5),
        )
        Task.objects.create(
            title="todo",
            due_date=timezone.now() + timedelta(days=3),
            deadline_enabled=False,
        )

        response = self.client.post("/api/tasks/postpone_all/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["postponed_count"], 1)
        overdue.refresh_from_db()
        self.assertAlmostEqual(
            overdue.due_date, timezone.now(), delta=timedelta(seconds=5)
        )