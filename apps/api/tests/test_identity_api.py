import json
import re
from pathlib import Path

import pytest
from django.core import mail
from django.urls import get_resolver
from openapi_spec_validator import validate
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db
REGISTER_URL = "/api/v1/auth/register"
VERIFY_URL = "/api/v1/auth/email/verify"
RESEND_URL = "/api/v1/auth/email/resend"
TOKEN_URL = "/api/v1/auth/token"
REFRESH_URL = "/api/v1/auth/token/refresh"
SESSIONS_URL = "/api/v1/auth/sessions"
LOGOUT_URL = "/api/v1/auth/logout"
PASSWORD_RESET_REQUEST_URL = "/api/v1/auth/password/reset/request"
PASSWORD_RESET_CONFIRM_URL = "/api/v1/auth/password/reset/confirm"


def _register_and_verify(client, *, email, password, handle):
    client.post(
        REGISTER_URL,
        {"email": email, "password": password, "handle": handle, "display_name": handle},
        format="json",
    )
    code = re.search(r"\b\d{6}\b", mail.outbox[-1].body).group()
    return client.post(VERIFY_URL, {"email": email, "code": code}, format="json")


def test_verified_email_enables_password_sign_in(settings):
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
    client = APIClient()
    credentials = {
        "email": "person@example.test",
        "password": "Long-unique-password-for-tests-8!",
    }

    registered = client.post(
        REGISTER_URL,
        {
            **credentials,
            "handle": "person",
            "display_name": "Test Person",
        },
        format="json",
    )
    assert registered.status_code == 202
    assert registered.json() == {"status": "accepted"}
    assert client.post(TOKEN_URL, credentials, format="json").status_code == 401

    code = re.search(r"\b\d{6}\b", mail.outbox[0].body).group()
    verified = client.post(
        VERIFY_URL,
        {"email": credentials["email"], "code": code},
        format="json",
    )
    assert verified.status_code == 204

    signed_in = client.post(TOKEN_URL, credentials, format="json")
    assert signed_in.status_code == 200
    assert set(signed_in.json()) == {"access", "refresh", "user"}
    assert signed_in.json()["user"] == {
        "email": credentials["email"],
        "handle": "person",
        "display_name": "Test Person",
    }


def test_email_verification_code_locks_after_five_failures(settings):
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
    client = APIClient()
    credentials = {
        "email": "locked@example.test",
        "password": "Another-long-password-for-tests-9!",
    }
    client.post(
        REGISTER_URL,
        {**credentials, "handle": "locked", "display_name": "Locked Person"},
        format="json",
    )
    actual_code = re.search(r"\b\d{6}\b", mail.outbox[0].body).group()
    wrong_code = "000000" if actual_code != "000000" else "111111"

    for _ in range(5):
        response = client.post(
            VERIFY_URL,
            {"email": credentials["email"], "code": wrong_code},
            format="json",
        )
        assert response.status_code == 400
        assert response.json()["error"]["code"] == "invalid_verification_code"

    assert (
        client.post(
            VERIFY_URL,
            {"email": credentials["email"], "code": actual_code},
            format="json",
        ).status_code
        == 400
    )
    assert client.post(TOKEN_URL, credentials, format="json").status_code == 401


def test_refresh_rotates_token_and_logout_revokes_the_session(settings):
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
    client = APIClient()
    credentials = {
        "email": "session@example.test",
        "password": "Session-password-for-tests-8!",
    }
    client.post(
        REGISTER_URL,
        {**credentials, "handle": "session", "display_name": "Session Person"},
        format="json",
    )
    code = re.search(r"\b\d{6}\b", mail.outbox[0].body).group()
    client.post(
        VERIFY_URL,
        {"email": credentials["email"], "code": code},
        format="json",
    )
    tokens = client.post(TOKEN_URL, credentials, format="json").json()

    renewed = client.post(REFRESH_URL, {"refresh": tokens["refresh"]}, format="json")
    assert renewed.status_code == 200
    assert renewed.json()["access"] != tokens["access"]
    assert renewed.json()["refresh"] != tokens["refresh"]
    assert (
        client.post(REFRESH_URL, {"refresh": tokens["refresh"]}, format="json").status_code == 401
    )

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {renewed.json()['access']}")
    sessions = client.get(SESSIONS_URL)
    assert sessions.status_code == 200
    assert len(sessions.json()["results"]) == 1
    assert sessions.json()["results"][0]["current"] is True
    assert client.post(LOGOUT_URL, {}, format="json").status_code == 204
    assert client.get(SESSIONS_URL).status_code == 401
    client.credentials()
    assert (
        client.post(REFRESH_URL, {"refresh": renewed.json()["refresh"]}, format="json").status_code
        == 401
    )


def test_password_reset_revokes_existing_sessions(settings):
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
    client = APIClient()
    credentials = {
        "email": "reset@example.test",
        "password": "Original-password-for-tests-8!",
    }
    client.post(
        REGISTER_URL,
        {**credentials, "handle": "reset_user", "display_name": "Reset Person"},
        format="json",
    )
    verification_code = re.search(r"\b\d{6}\b", mail.outbox[-1].body).group()
    client.post(
        VERIFY_URL,
        {"email": credentials["email"], "code": verification_code},
        format="json",
    )
    old_tokens = client.post(TOKEN_URL, credentials, format="json").json()

    requested = client.post(
        PASSWORD_RESET_REQUEST_URL,
        {"email": credentials["email"]},
        format="json",
    )
    assert requested.status_code == 202
    assert requested.json() == {"status": "accepted"}
    reset_code = re.search(r"\b\d{6}\b", mail.outbox[-1].body).group()
    new_password = "Replacement-password-for-tests-9!"
    confirmed = client.post(
        PASSWORD_RESET_CONFIRM_URL,
        {"email": credentials["email"], "code": reset_code, "password": new_password},
        format="json",
    )
    assert confirmed.status_code == 204

    assert client.post(TOKEN_URL, credentials, format="json").status_code == 401
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {old_tokens['access']}")
    assert client.get(SESSIONS_URL).status_code == 401
    client.credentials()
    assert (
        client.post(REFRESH_URL, {"refresh": old_tokens["refresh"]}, format="json").status_code
        == 401
    )
    assert (
        client.post(
            TOKEN_URL,
            {"email": credentials["email"], "password": new_password},
            format="json",
        ).status_code
        == 200
    )


def test_verification_requests_are_rate_limited_without_account_disclosure(settings):
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
    client = APIClient()
    payload = {
        "email": "limited@example.test",
        "password": "Rate-limited-password-for-tests-8!",
        "handle": "limited",
        "display_name": "Limited Person",
    }
    assert client.post(REGISTER_URL, payload, format="json").status_code == 202
    assert len(mail.outbox) == 1

    assert client.post(REGISTER_URL, payload, format="json").status_code == 202
    assert client.post(RESEND_URL, {"email": payload["email"]}, format="json").status_code == 202
    assert (
        client.post(RESEND_URL, {"email": "missing@example.test"}, format="json").status_code == 202
    )
    assert len(mail.outbox) == 1


def test_verification_code_cannot_be_replayed(settings):
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
    client = APIClient()
    email = "single-use@example.test"
    client.post(
        REGISTER_URL,
        {
            "email": email,
            "password": "Single-use-password-for-tests-8!",
            "handle": "single_use",
            "display_name": "Single Use",
        },
        format="json",
    )
    code = re.search(r"\b\d{6}\b", mail.outbox[-1].body).group()
    assert client.post(VERIFY_URL, {"email": email, "code": code}, format="json").status_code == 204
    replayed = client.post(VERIFY_URL, {"email": email, "code": code}, format="json")
    assert replayed.status_code == 400
    assert replayed.json()["error"]["code"] == "invalid_verification_code"


def test_user_can_revoke_one_session_or_all_devices(settings):
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
    anonymous = APIClient()
    credentials = {
        "email": "devices@example.test",
        "password": "Multiple-device-password-for-tests-8!",
    }
    assert (
        _register_and_verify(
            anonymous,
            **credentials,
            handle="devices",
        ).status_code
        == 204
    )
    first_tokens = anonymous.post(
        TOKEN_URL,
        credentials,
        format="json",
        HTTP_USER_AGENT="First browser",
    ).json()
    second_tokens = anonymous.post(
        TOKEN_URL,
        credentials,
        format="json",
        HTTP_USER_AGENT="Second browser",
    ).json()

    first = APIClient()
    first.credentials(HTTP_AUTHORIZATION=f"Bearer {first_tokens['access']}")
    sessions = first.get(SESSIONS_URL).json()["results"]
    assert {row["user_agent"] for row in sessions} == {"First browser", "Second browser"}
    other_id = next(row["id"] for row in sessions if not row["current"])
    assert first.delete(f"{SESSIONS_URL}/{other_id}").status_code == 204

    second = APIClient()
    second.credentials(HTTP_AUTHORIZATION=f"Bearer {second_tokens['access']}")
    assert second.get(SESSIONS_URL).status_code == 401
    assert first.get(SESSIONS_URL).status_code == 200

    third_tokens = anonymous.post(TOKEN_URL, credentials, format="json").json()
    assert first.delete(SESSIONS_URL).status_code == 204
    assert first.get(SESSIONS_URL).status_code == 401
    third = APIClient()
    third.credentials(HTTP_AUTHORIZATION=f"Bearer {third_tokens['access']}")
    assert third.get(SESSIONS_URL).status_code == 401


def test_openapi_contract_covers_published_increment_1_routes():
    root = Path(__file__).resolve().parents[3]
    contract = json.loads((root / "docs/design/openapi.json").read_text(encoding="utf-8"))
    validate(contract)
    assert contract["openapi"] == "3.1.0"
    expected_paths = {
        "/api/v1/auth/register",
        "/api/v1/auth/email/resend",
        "/api/v1/auth/email/verify",
        "/api/v1/auth/token",
        "/api/v1/auth/token/refresh",
        "/api/v1/auth/logout",
        "/api/v1/auth/sessions",
        "/api/v1/auth/sessions/{session_id}",
        "/api/v1/auth/password/reset/request",
        "/api/v1/auth/password/reset/confirm",
        "/api/v1/auth/password",
        "/api/v1/auth/google",
        "/api/v1/auth/google/link",
        "/api/v1/auth/passkeys",
        "/api/v1/auth/passkeys/{passkey_id}",
        "/api/v1/auth/passkeys/registration/options",
        "/api/v1/auth/passkeys/registration/verify",
        "/api/v1/auth/passkeys/authentication/options",
        "/api/v1/auth/passkeys/authentication/verify",
        "/api/v1/account",
        "/api/v1/account/bootstrap",
        "/api/v1/account/contacts",
        "/api/v1/account/contacts/verify",
        "/api/v1/account/contacts/{contact_id}",
        "/api/v1/folders",
        "/api/v1/folders/{folder_id}",
        "/api/v1/folders/{folder_id}/restore",
        "/api/v1/trash/folders",
        "/api/v1/lists",
        "/api/v1/lists/{list_id}",
        "/api/v1/lists/{list_id}/restore",
        "/api/v1/trash/lists",
        "/api/v1/lists/{list_id}/columns",
        "/api/v1/columns/{column_id}",
        "/api/v1/tasks",
        "/api/v1/tasks/{task_id}",
        "/api/v1/tasks/{task_id}/restore",
        "/api/v1/trash/tasks",
    }
    routed_paths = {
        "/" + re.sub(r"<uuid:([^>]+)>", r"{\1}", str(pattern.pattern))
        for pattern in get_resolver().url_patterns
        if str(pattern.pattern).startswith("api/v1/")
        and not str(pattern.pattern).startswith("api/v1/foundation/")
    }
    assert set(contract["paths"]) == expected_paths == routed_paths
    assert contract["components"]["schemas"]["Error"]["required"] == ["error"]


def test_public_token_endpoints_ignore_an_unrelated_bearer_header(settings):
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
    client = APIClient()
    credentials = {
        "email": "header@example.test",
        "password": "Header-password-for-tests-8!",
    }
    assert _register_and_verify(client, **credentials, handle="header_user").status_code == 204
    refresh = client.post(TOKEN_URL, credentials, format="json").json()["refresh"]

    client.credentials(HTTP_AUTHORIZATION="Bearer unrelated-or-stale-token")
    assert client.post(TOKEN_URL, credentials, format="json").status_code == 200
    assert client.post(REFRESH_URL, {"refresh": refresh}, format="json").status_code == 200


def test_rejected_reset_password_does_not_consume_the_code(settings):
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
    client = APIClient()
    credentials = {
        "email": "password-policy@example.test",
        "password": "Original-policy-password-for-tests-8!",
    }
    assert _register_and_verify(client, **credentials, handle="password_policy").status_code == 204
    client.post(PASSWORD_RESET_REQUEST_URL, {"email": credentials["email"]}, format="json")
    code = re.search(r"\b\d{6}\b", mail.outbox[-1].body).group()

    rejected = client.post(
        PASSWORD_RESET_CONFIRM_URL,
        {"email": credentials["email"], "code": code, "password": "short"},
        format="json",
    )
    assert rejected.status_code == 400
    assert rejected.json()["error"]["code"] == "validation_error"

    accepted = client.post(
        PASSWORD_RESET_CONFIRM_URL,
        {
            "email": credentials["email"],
            "code": code,
            "password": "Quasar-Magnolia-7429!River",
        },
        format="json",
    )
    assert accepted.status_code == 204
