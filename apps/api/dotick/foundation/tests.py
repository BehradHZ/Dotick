import base64
import json
import logging
import uuid
from unittest.mock import patch

from config.observability import JsonFormatter
from django.contrib.auth import get_user_model
from django.db import connection
from django.test import Client, TestCase, TransactionTestCase, override_settings
from rest_framework.test import APIClient

from dotick.foundation.models import Checkpoint


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


@override_settings(FOUNDATION_ENABLED=True)
class FoundationCheckpointAPITests(TestCase):
    checkpoint_url = "/api/v1/foundation/checkpoints"
    max_request_body_bytes = 16 * 1024

    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()

        cls.user = user_model.objects.create_user(
            email="foundation-user@example.test",
            password="Foundation-Test-Password-123!",
        )
        cls.other_user = user_model.objects.create_user(
            email="foundation-other@example.test",
            password="Foundation-Other-Password-123!",
        )

    def setUp(self):
        self.client = APIClient()

        credentials = base64.b64encode(
            b"foundation-user@example.test:Foundation-Test-Password-123!"
        ).decode()

        self.client.credentials(HTTP_AUTHORIZATION=f"Basic {credentials}")

    def test_checkpoint_api_requires_authentication(self):
        client = APIClient()

        response = client.get(self.checkpoint_url)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {
                "error": {
                    "code": "not_authenticated",
                    "details": {
                        "detail": "Authentication credentials were not provided.",
                    },
                }
            },
        )

    def test_post_creates_checkpoint_for_authenticated_owner(self):
        response = self.client.post(
            self.checkpoint_url,
            {"text": "Walking skeleton checkpoint"},
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        payload = response.json()
        checkpoint = Checkpoint.objects.get(id=payload["id"])

        self.assertEqual(checkpoint.owner, self.user)
        self.assertEqual(checkpoint.text, "Walking skeleton checkpoint")
        self.assertEqual(payload["text"], "Walking skeleton checkpoint")
        self.assertIn("created_at", payload)

    def test_get_lists_only_authenticated_owners_checkpoints(self):
        own_checkpoint = Checkpoint.objects.create(
            owner=self.user,
            text="Own checkpoint",
        )
        other_checkpoint = Checkpoint.objects.create(
            owner=self.other_user,
            text="Other checkpoint",
        )

        response = self.client.get(self.checkpoint_url)

        self.assertEqual(response.status_code, 200)

        ids = {row["id"] for row in response.json()["results"]}

        self.assertIn(str(own_checkpoint.id), ids)
        self.assertNotIn(str(other_checkpoint.id), ids)

    def test_get_detail_returns_owned_checkpoint(self):
        checkpoint = Checkpoint.objects.create(
            owner=self.user,
            text="Owned checkpoint",
        )

        response = self.client.get(f"{self.checkpoint_url}/{checkpoint.id}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], str(checkpoint.id))
        self.assertEqual(response.json()["text"], "Owned checkpoint")

    def test_get_detail_hides_another_owners_checkpoint(self):
        checkpoint = Checkpoint.objects.create(
            owner=self.other_user,
            text="Private checkpoint",
        )

        response = self.client.get(f"{self.checkpoint_url}/{checkpoint.id}")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(),
            {
                "error": {
                    "code": "not_found",
                    "details": {
                        "detail": "Not found.",
                    },
                }
            },
        )

    def test_post_rejects_blank_text(self):
        response = self.client.post(
            self.checkpoint_url,
            {"text": "   "},
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_post_rejects_text_longer_than_240_characters(self):
        response = self.client.post(
            self.checkpoint_url,
            {"text": "x" * 241},
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_post_rejects_unknown_fields(self):
        response = self.client.post(
            self.checkpoint_url,
            {
                "text": "Checkpoint",
                "unexpected": "value",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "error": {
                    "code": "validation_error",
                    "details": {
                        "input": "Unknown fields are not accepted.",
                    },
                }
            },
        )

    @override_settings(FOUNDATION_ENABLED=False)
    def test_foundation_api_is_hidden_when_disabled(self):
        response = self.client.get(self.checkpoint_url)

        self.assertEqual(response.status_code, 404)

    @patch(
        "dotick.foundation.application.list_checkpoints",
        side_effect=RuntimeError("sensitive internal error"),
    )
    def test_unhandled_api_error_uses_generic_envelope(self, mocked_list):
        response = self.client.get(self.checkpoint_url)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            response.json(),
            {
                "error": {
                    "code": "internal_error",
                }
            },
        )

        self.assertNotIn(
            "sensitive internal error",
            response.content.decode(),
        )

    def test_request_body_below_limit_is_accepted(self):
        response = self._post_json_body(self.max_request_body_bytes - 1)

        self.assertEqual(response.status_code, 201)

    def test_request_body_at_limit_is_accepted(self):
        response = self._post_json_body(self.max_request_body_bytes)

        self.assertEqual(response.status_code, 201)

    def test_request_body_above_limit_returns_stable_413(self):
        with self.assertLogs("dotick.http", level="INFO") as captured:
            response = self._post_json_body(self.max_request_body_bytes + 1)

        self.assertEqual(response.status_code, 413)
        self.assertEqual(
            response.json(),
            {
                "error": {
                    "code": "payload_too_large",
                    "details": {
                        "detail": "Request body exceeds the 16 KiB limit.",
                    },
                }
            },
        )
        self.assertNotIn("Within limit", response.content.decode())

        serialized_logs = "\n".join(JsonFormatter().format(record) for record in captured.records)

        self.assertNotIn("Within limit", serialized_logs)

    def _post_json_body(self, size):
        body = b'{"text":"Within limit"}'
        body += b" " * (size - len(body))

        self.assertEqual(len(body), size)

        return self.client.generic(
            "POST",
            self.checkpoint_url,
            data=body,
            content_type="application/json",
        )


class RequestIDTests(TestCase):
    def test_response_contains_server_generated_request_id(self):
        response = Client().get("/health")

        request_id = response["X-Request-ID"]

        self.assertIsInstance(uuid.UUID(request_id), uuid.UUID)

    def test_each_request_gets_a_different_request_id(self):
        first_response = Client().get("/health")
        second_response = Client().get("/health")

        self.assertNotEqual(
            first_response["X-Request-ID"],
            second_response["X-Request-ID"],
        )

    def test_client_supplied_request_id_is_not_trusted(self):
        response = Client().get(
            "/health",
            HTTP_X_REQUEST_ID="client-controlled-id",
        )

        self.assertNotEqual(
            response["X-Request-ID"],
            "client-controlled-id",
        )

    def test_error_response_contains_request_id(self):
        response = Client().get(
            "/api/v1/foundation/checkpoints",
        )

        self.assertEqual(response.status_code, 401)
        self.assertIn("X-Request-ID", response)

        uuid.UUID(response["X-Request-ID"])


class CacheControlTests(TestCase):
    def test_success_response_disables_caching(self):
        response = Client().get("/health")

        self.assertEqual(response["Cache-Control"], "no-store")

    def test_error_response_disables_caching(self):
        response = Client().get(
            "/api/v1/foundation/checkpoints",
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response["Cache-Control"], "no-store")


class StructuredLoggingTests(TestCase):
    def test_json_formatter_emits_only_allowlisted_fields(self):
        record = logging.LogRecord(
            name="dotick.http",
            level=logging.INFO,
            pathname=__file__,
            lineno=1,
            msg="sensitive message",
            args=(),
            exc_info=None,
        )

        record.event = "http_request"
        record.request_id = "request-id"
        record.route = "api/v1/foundation/checkpoints"
        record.status = 200
        record.duration_ms = 12.5

        record.password = "secret-password"
        record.credential = "secret-credential"
        record.token = "secret-token"
        record.authorization = "Basic secret"
        record.cookie = "sessionid=secret-session"
        record.body = '{"password":"secret"}'
        record.exception_message = "sensitive internal exception"
        record.connection_string = "postgresql://user:password@localhost/database"
        record.secret_key = "sensitive-django-secret-key"
        record.environment = {"PRIVATE_ENVIRONMENT_VALUE": "sensitive-environment-value"}

        payload = json.loads(JsonFormatter().format(record))

        self.assertEqual(
            set(payload),
            {
                "timestamp",
                "level",
                "service",
                "event",
                "request_id",
                "route",
                "status",
                "duration_ms",
            },
        )

        serialized = json.dumps(payload)

        self.assertNotIn("secret-password", serialized)
        self.assertNotIn("secret-credential", serialized)
        self.assertNotIn("secret-token", serialized)
        self.assertNotIn("Basic secret", serialized)
        self.assertNotIn("secret-session", serialized)
        self.assertNotIn("postgresql://", serialized)
        self.assertNotIn("sensitive internal exception", serialized)
        self.assertNotIn("sensitive-django-secret-key", serialized)
        self.assertNotIn("sensitive-environment-value", serialized)
        self.assertNotIn("sensitive message", serialized)

    def test_request_log_contains_response_request_id(self):
        with self.assertLogs("dotick.http", level="INFO") as captured:
            response = Client().get("/health")

        request_log = next(
            record
            for record in captured.records
            if getattr(record, "event", None) == "http_request"
        )

        payload = json.loads(JsonFormatter().format(request_log))

        self.assertEqual(
            payload["request_id"],
            response["X-Request-ID"],
        )
        self.assertEqual(payload["event"], "http_request")
        self.assertEqual(payload["method"], "GET")
        self.assertEqual(payload["route"], "health")
        self.assertEqual(payload["status"], 200)

    def test_request_log_excludes_credentials_cookies_and_body(self):
        with self.assertLogs("dotick.http", level="INFO") as captured:
            response = Client().post(
                "/api/v1/foundation/checkpoints",
                data=b'{"text":"sensitive-request-body"}',
                content_type="application/json",
                HTTP_AUTHORIZATION="Bearer sensitive-auth-token",
                HTTP_COOKIE="sessionid=sensitive-session-secret",
            )

        self.assertEqual(response.status_code, 401)

        serialized_logs = "\n".join(JsonFormatter().format(record) for record in captured.records)

        self.assertNotIn("sensitive-request-body", serialized_logs)
        self.assertNotIn("sensitive-auth-token", serialized_logs)
        self.assertNotIn("sensitive-session-secret", serialized_logs)
