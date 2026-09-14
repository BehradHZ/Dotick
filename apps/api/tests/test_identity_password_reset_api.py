import re

import pytest
from django.contrib.auth import get_user_model
from django.core import mail
from django.utils import timezone
from dotick.identity.models import VerificationChallenge
from rest_framework.test import APIClient

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.usefixtures("_email_backend"),
]

RESET_REQUEST_URL = "/api/v1/auth/password/reset/request"


@pytest.fixture
def _email_backend(settings):
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"


def _delivered_code(message):
    return re.search(r"\b[0-9]{6}\b", message.body).group()


def test_password_reset_request_sends_digest_backed_code_to_eligible_account():
    user = get_user_model().objects.create_user(
        email="reset@example.test",
        password="Long-unique-password-for-tests-8!",
        email_verified_at=timezone.now(),
    )

    response = APIClient().post(
        RESET_REQUEST_URL,
        {"email": "RESET@EXAMPLE.TEST"},
        format="json",
    )

    assert response.status_code == 202
    assert response.json() == {"status": "accepted"}
    assert len(mail.outbox) == 1
    code = _delivered_code(mail.outbox[0])
    challenge = VerificationChallenge.objects.get(
        user=user,
        purpose=VerificationChallenge.Purpose.PASSWORD_RESET,
    )
    assert challenge.code_digest != code
    assert code not in response.content.decode()


@pytest.mark.parametrize("account_state", ["unknown", "unverified", "inactive"])
def test_password_reset_request_hides_ineligible_account_state(account_state):
    email = f"{account_state}-reset@example.test"
    if account_state != "unknown":
        user = get_user_model().objects.create_user(
            email=email,
            password="Long-unique-password-for-tests-8!",
            email_verified_at=timezone.now(),
        )
        if account_state == "unverified":
            user.email_verified_at = None
            user.save(update_fields=["email_verified_at"])
        else:
            user.is_active = False
            user.save(update_fields=["is_active"])

    response = APIClient().post(
        RESET_REQUEST_URL,
        {"email": email},
        format="json",
    )

    assert response.status_code == 202
    assert response.json() == {"status": "accepted"}
    assert len(mail.outbox) == 0


def test_password_reset_request_hides_challenge_cooldown():
    email = "reset-cooldown@example.test"
    get_user_model().objects.create_user(
        email=email,
        password="Long-unique-password-for-tests-8!",
        email_verified_at=timezone.now(),
    )
    client = APIClient()

    first = client.post(RESET_REQUEST_URL, {"email": email}, format="json")
    blocked = client.post(RESET_REQUEST_URL, {"email": email}, format="json")

    assert first.status_code == blocked.status_code == 202
    assert first.json() == blocked.json() == {"status": "accepted"}
    assert len(mail.outbox) == 1
