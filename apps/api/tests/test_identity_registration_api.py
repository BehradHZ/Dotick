import re
from datetime import timedelta

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

REGISTER_URL = "/api/v1/auth/register"
RESEND_URL = "/api/v1/auth/email/resend"
VERIFY_URL = "/api/v1/auth/email/verify"


@pytest.fixture
def _email_backend(settings):
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"


def _valid_registration(**overrides):
    payload = {
        "email": "person@example.test",
        "password": "Long-unique-password-for-tests-8!",
        "handle": "person_1",
        "display_name": "Test Person",
    }
    payload.update(overrides)
    return payload


def _delivered_code(message):
    return re.search(r"\b[0-9]{6}\b", message.body).group()


def test_registration_creates_inactive_account_and_sends_digest_backed_code():
    client = APIClient()
    payload = _valid_registration(email="  Person@Example.TEST  ")

    response = client.post(REGISTER_URL, payload, format="json")

    assert response.status_code == 202
    assert response.json() == {"status": "accepted"}
    user = get_user_model().objects.get()
    account_id = user.id
    assert user.email == "person@example.test"
    assert user.handle == payload["handle"]
    assert user.display_name == payload["display_name"]
    assert user.check_password(payload["password"])
    assert user.is_active is False
    assert user.email_verified_at is None

    assert len(mail.outbox) == 1
    code = _delivered_code(mail.outbox[0])
    challenge = VerificationChallenge.objects.get()
    assert challenge.code_digest != code
    assert code not in response.content.decode()

    verified = client.post(
        VERIFY_URL,
        {"email": "PERSON@example.test", "code": code},
        format="json",
    )

    assert verified.status_code == 204
    user.refresh_from_db()
    challenge.refresh_from_db()
    assert user.id == account_id
    assert user.is_active is True
    assert user.email_verified_at is not None
    assert challenge.consumed_at is not None


def test_registration_response_does_not_disclose_existing_email():
    client = APIClient()
    payload = _valid_registration()

    first = client.post(REGISTER_URL, payload, format="json")
    duplicate = client.post(
        REGISTER_URL,
        _valid_registration(email="PERSON@EXAMPLE.TEST", handle="different_handle"),
        format="json",
    )

    assert first.status_code == duplicate.status_code == 202
    assert first.json() == duplicate.json() == {"status": "accepted"}
    assert get_user_model().objects.count() == 1
    assert len(mail.outbox) == 1


def test_registration_rejects_case_insensitive_handle_collision():
    get_user_model().objects.create_user(
        email="existing@example.test",
        handle="Reserved_Handle",
        display_name="Existing User",
    )
    client = APIClient()

    response = client.post(
        REGISTER_URL,
        _valid_registration(handle="reserved_handle"),
        format="json",
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "validation_error"
    assert response.json()["error"]["details"] == {"handle": ["This handle is unavailable."]}
    assert get_user_model().objects.count() == 1


@pytest.mark.parametrize("handle", ["ab", "contains-hyphen", "x" * 31])
def test_registration_rejects_invalid_handle(handle):
    response = APIClient().post(
        REGISTER_URL,
        _valid_registration(handle=handle),
        format="json",
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "validation_error"
    assert get_user_model().objects.count() == 0


def test_registration_rejects_blank_display_name_and_unknown_fields():
    client = APIClient()

    blank_name = client.post(
        REGISTER_URL,
        _valid_registration(display_name="   "),
        format="json",
    )
    unknown_field = client.post(
        REGISTER_URL,
        {**_valid_registration(), "is_active": True},
        format="json",
    )

    assert blank_name.status_code == 400
    assert unknown_field.status_code == 400
    assert unknown_field.json()["error"]["details"] == {"input": "Unknown fields are not accepted."}
    assert get_user_model().objects.count() == 0


def test_registration_applies_django_password_validation():
    response = APIClient().post(
        REGISTER_URL,
        _valid_registration(password="short"),
        format="json",
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "validation_error"
    assert "password" in response.json()["error"]["details"]
    assert get_user_model().objects.count() == 0


def test_incorrect_expired_and_replayed_codes_share_failure_surface():
    client = APIClient()
    payload = _valid_registration()
    client.post(REGISTER_URL, payload, format="json")
    code = _delivered_code(mail.outbox[0])

    incorrect = client.post(
        VERIFY_URL,
        {"email": payload["email"], "code": "000000" if code != "000000" else "111111"},
        format="json",
    )
    VerificationChallenge.objects.update(expires_at=timezone.now() - timedelta(seconds=1))
    expired = client.post(
        VERIFY_URL,
        {"email": payload["email"], "code": code},
        format="json",
    )

    VerificationChallenge.objects.update(expires_at=timezone.now() + timedelta(minutes=10))
    accepted = client.post(
        VERIFY_URL,
        {"email": payload["email"], "code": code},
        format="json",
    )
    replayed = client.post(
        VERIFY_URL,
        {"email": payload["email"], "code": code},
        format="json",
    )

    assert incorrect.status_code == expired.status_code == replayed.status_code == 400
    assert {
        incorrect.json()["error"]["code"],
        expired.json()["error"]["code"],
        replayed.json()["error"]["code"],
    } == {"invalid_verification_code"}
    assert accepted.status_code == 204


def test_fifth_incorrect_code_consumes_challenge_and_keeps_account_inactive():
    client = APIClient()
    payload = _valid_registration(email="locked@example.test", handle="locked_user")
    client.post(REGISTER_URL, payload, format="json")
    code = _delivered_code(mail.outbox[0])
    wrong_code = "000000" if code != "000000" else "111111"

    for _ in range(5):
        response = client.post(
            VERIFY_URL,
            {"email": payload["email"], "code": wrong_code},
            format="json",
        )
        assert response.status_code == 400
        assert response.json()["error"]["code"] == "invalid_verification_code"

    challenge = VerificationChallenge.objects.get()
    user = get_user_model().objects.get()
    assert challenge.failed_attempts == 5
    assert challenge.consumed_at is not None
    assert user.is_active is False
    assert user.email_verified_at is None
    assert (
        client.post(
            VERIFY_URL,
            {"email": payload["email"], "code": code},
            format="json",
        ).status_code
        == 400
    )


def test_resend_replaces_old_challenge_after_cooldown():
    client = APIClient()
    payload = _valid_registration()
    client.post(REGISTER_URL, payload, format="json")
    old_challenge = VerificationChallenge.objects.get()
    VerificationChallenge.objects.filter(pk=old_challenge.pk).update(
        created_at=timezone.now() - timedelta(seconds=61)
    )

    response = client.post(
        RESEND_URL,
        {"email": "PERSON@EXAMPLE.TEST"},
        format="json",
    )

    assert response.status_code == 202
    assert response.json() == {"status": "accepted"}
    assert len(mail.outbox) == 2
    old_challenge.refresh_from_db()
    assert old_challenge.consumed_at is not None
    assert VerificationChallenge.objects.count() == 2


def test_resend_for_unknown_email_is_indistinguishable_and_sends_nothing():
    response = APIClient().post(
        RESEND_URL,
        {"email": "missing@example.test"},
        format="json",
    )

    assert response.status_code == 202
    assert response.json() == {"status": "accepted"}
    assert len(mail.outbox) == 0
