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
RESET_CONFIRM_URL = "/api/v1/auth/password/reset/confirm"


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


def test_password_reset_confirmation_changes_password_and_consumes_code():
    old_password = "Long-unique-password-for-tests-8!"
    new_password = "Different-long-password-for-tests-9!"
    user = get_user_model().objects.create_user(
        email="reset-confirm@example.test",
        password=old_password,
        email_verified_at=timezone.now(),
    )
    client = APIClient()
    client.post(RESET_REQUEST_URL, {"email": user.email}, format="json")
    code = _delivered_code(mail.outbox[0])

    response = client.post(
        RESET_CONFIRM_URL,
        {"email": user.email, "code": code, "password": new_password},
        format="json",
    )

    assert response.status_code == 204
    user.refresh_from_db()
    assert user.check_password(new_password)
    assert not user.check_password(old_password)
    assert VerificationChallenge.objects.get().consumed_at is not None
    replay = client.post(
        RESET_CONFIRM_URL,
        {"email": user.email, "code": code, "password": new_password},
        format="json",
    )
    assert replay.status_code == 400
    assert replay.json()["error"]["code"] == "invalid_verification_code"


def test_weak_password_does_not_consume_valid_reset_code():
    user = get_user_model().objects.create_user(
        email="reset-policy@example.test",
        password="Long-unique-password-for-tests-8!",
        email_verified_at=timezone.now(),
    )
    client = APIClient()
    client.post(RESET_REQUEST_URL, {"email": user.email}, format="json")
    code = _delivered_code(mail.outbox[0])

    rejected = client.post(
        RESET_CONFIRM_URL,
        {"email": user.email, "code": code, "password": "short"},
        format="json",
    )
    accepted = client.post(
        RESET_CONFIRM_URL,
        {
            "email": user.email,
            "code": code,
            "password": "Different-long-password-for-tests-9!",
        },
        format="json",
    )

    assert rejected.status_code == 400
    assert rejected.json()["error"]["code"] == "validation_error"
    assert accepted.status_code == 204


@pytest.mark.parametrize("code_state", ["incorrect", "expired", "unknown_email"])
def test_invalid_reset_confirmations_share_one_failure(code_state):
    user = get_user_model().objects.create_user(
        email=f"{code_state}-confirm@example.test",
        password="Long-unique-password-for-tests-8!",
        email_verified_at=timezone.now(),
    )
    client = APIClient()
    client.post(RESET_REQUEST_URL, {"email": user.email}, format="json")
    code = _delivered_code(mail.outbox[0])
    submitted_email = user.email
    submitted_code = code
    if code_state == "incorrect":
        submitted_code = "000000" if code != "000000" else "111111"
    elif code_state == "expired":
        VerificationChallenge.objects.update(expires_at=timezone.now())
    else:
        submitted_email = "unknown-confirm@example.test"

    response = client.post(
        RESET_CONFIRM_URL,
        {
            "email": submitted_email,
            "code": submitted_code,
            "password": "Different-long-password-for-tests-9!",
        },
        format="json",
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "invalid_verification_code"
