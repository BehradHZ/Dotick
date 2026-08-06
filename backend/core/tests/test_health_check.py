"""
Stage 1 — smoke-test endpoint.

Seam under test: GET /api/health/ (public HTTP interface).
See ROADMAP.md §6 Stage 1: "A minimal health-check or smoke-test
endpoint proving the full path (browser -> Django -> PostgreSQL ->
response) works."

Two seams, tested separately (per project decision):
1. Response shape — this file.
2. Real DB connectivity — test_health_check_db.py.
"""

from django.test import TestCase


class HealthCheckResponseShapeTests(TestCase):
    """The endpoint returns a 200 with the expected JSON shape."""

    def test_returns_200(self):
        response = self.client.get("/api/health/")
        self.assertEqual(response.status_code, 200)

    def test_returns_json_content_type(self):
        response = self.client.get("/api/health/")
        self.assertEqual(response["Content-Type"], "application/json")

    def test_response_body_reports_ok_status(self):
        response = self.client.get("/api/health/")
        self.assertEqual(response.json()["status"], "ok")
