from django.db import connection
from django.test import Client, TransactionTestCase


class ReadyEndpointTests(TransactionTestCase):
    def test_ready_reports_available_when_postgresql_responds(self):
        response = Client().get("/ready")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ready"})

    def test_ready_reports_unavailable_without_connection_details(self):
        original_port = connection.settings_dict["PORT"]
        connection.close()
        connection.settings_dict["PORT"] = "1"

        try:
            response = Client().get("/ready")
        finally:
            connection.close()
            connection.settings_dict["PORT"] = original_port

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json(), {"status": "unavailable"})
