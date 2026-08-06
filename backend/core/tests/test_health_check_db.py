"""
Stage 1 — smoke-test endpoint, DB-connectivity seam.

Separate from test_health_check.py's response-shape seam (per project
decision). This test proves the endpoint reflects a *real* database
check rather than a hardcoded "ok" — if the DB connection is actually
broken, the endpoint must surface that failure instead of silently
reporting success.
"""

from unittest.mock import patch

from django.db import OperationalError
from django.test import TestCase


class HealthCheckDatabaseConnectivityTests(TestCase):
    def test_returns_500_when_database_is_unreachable(self):
        with patch(
            "django.db.backends.utils.CursorWrapper.execute",
            side_effect=OperationalError("simulated connection failure"),
        ):
            response = self.client.get("/api/health/")

        self.assertEqual(response.status_code, 500)

    def test_healthy_response_reflects_a_successful_query(self):
        """
        Sanity check for the happy path: with a real, working DB
        connection (the normal test-database setup), the endpoint
        reports status "ok". Combined with the failure test above,
        this shows "ok" tracks the actual query outcome rather than
        being returned unconditionally.
        """
        response = self.client.get("/api/health/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")
