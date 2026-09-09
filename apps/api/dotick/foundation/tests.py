import base64
from unittest.mock import patch

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
