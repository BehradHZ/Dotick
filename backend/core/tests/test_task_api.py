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
