from datetime import timedelta
from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from dotick.identity.google_identity import (
    InvalidGoogleCredential,
    verify_google_id_credential,
)
from dotick.identity.sessions import create_auth_session
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db

PASSWORD_URL = "/api/v1/auth/password"
TOKEN_URL = "/api/v1/auth/token"


def _authenticated_client(user, *, session_age=timedelta(0)):
    session, pair = create_auth_session(user=user)
    if session_age:
        session.created_at = timezone.now() - session_age
        session.save(update_fields=["created_at"])
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {pair.access}")
    return client, session


def test_google_style_account_can_add_password_fallback_after_recent_authentication():
    user = get_user_model().objects.create_user(
        email="google-only@example.test",
        password=None,
        email_verified_at=timezone.now(),
    )
    assert not user.has_usable_password()
    client, _ = _authenticated_client(user)
    new_password = "Independent-password-fallback-8!"

    response = client.put(
        PASSWORD_URL,
        {"password": new_password},
        format="json",
    )

    assert response.status_code == 204
    user.refresh_from_db()
    assert user.check_password(new_password)
    login = APIClient().post(
        TOKEN_URL,
        {"email": user.email, "password": new_password},
        format="json",
    )
    assert login.status_code == 200


def test_password_fallback_requires_recent_authentication():
    user = get_user_model().objects.create_user(
        email="stale-google-only@example.test",
        password=None,
        email_verified_at=timezone.now(),
    )
    client, _ = _authenticated_client(user, session_age=timedelta(minutes=11))

    response = client.put(
        PASSWORD_URL,
        {"password": "Independent-password-fallback-8!"},
        format="json",
    )

    assert response.status_code == 403
    assert response.json()["error"]["code"] == "recent_auth_required"
    user.refresh_from_db()
    assert not user.has_usable_password()


@pytest.mark.parametrize("current_password", [None, "Wrong-current-password-9!"])
def test_existing_password_change_requires_current_password(current_password):
    original = "Original-current-password-8!"
    replacement = "Quartz-Lantern-Cedar-5729!"
    user = get_user_model().objects.create_user(
        email="password-change@example.test",
        password=original,
        email_verified_at=timezone.now(),
    )
    client, _ = _authenticated_client(user)
    payload = {"password": replacement}
    if current_password is not None:
        payload["current_password"] = current_password

    response = client.put(PASSWORD_URL, payload, format="json")

    assert response.status_code == 400
    assert "current_password" in response.json()["error"]["details"]
    user.refresh_from_db()
    assert user.check_password(original)
    assert not user.check_password(replacement)


def test_existing_password_change_requires_recent_auth_and_revokes_other_sessions():
    original = "Original-current-password-8!"
    replacement = "Quartz-Lantern-Cedar-5729!"
    user = get_user_model().objects.create_user(
        email="protected-password-change@example.test",
        password=original,
        email_verified_at=timezone.now(),
    )
    stale_client, _ = _authenticated_client(user, session_age=timedelta(minutes=11))
    rejected = stale_client.put(
        PASSWORD_URL,
        {"password": replacement, "current_password": original},
        format="json",
    )
    assert rejected.status_code == 403

    client, current_session = _authenticated_client(user)
    other_session, _ = create_auth_session(user=user)
    response = client.put(
        PASSWORD_URL,
        {"password": replacement, "current_password": original},
        format="json",
    )

    assert response.status_code == 204
    user.refresh_from_db()
    current_session.refresh_from_db()
    other_session.refresh_from_db()
    assert user.check_password(replacement)
    assert current_session.revoked_at is None
    assert other_session.revoked_at is not None


def test_google_id_credential_is_verified_for_configured_audience(settings):
    settings.GOOGLE_OAUTH_CLIENT_ID = "dotick-google-client-id"
    verified_claims = {
        "sub": "google-subject-123",
        "email": "Person@Example.TEST",
        "email_verified": True,
        "name": "Test Person",
        "picture": "https://example.test/person.png",
    }

    with patch(
        "dotick.identity.google_identity.id_token.verify_oauth2_token",
        return_value=verified_claims,
    ) as verifier:
        claims = verify_google_id_credential("signed-google-id-credential")

    assert claims.subject == "google-subject-123"
    assert claims.email == "person@example.test"
    assert claims.display_name == "Test Person"
    verifier.assert_called_once()
    assert verifier.call_args.kwargs["audience"] == "dotick-google-client-id"


def test_google_id_credential_requires_verified_email(settings):
    settings.GOOGLE_OAUTH_CLIENT_ID = "dotick-google-client-id"
    with patch(
        "dotick.identity.google_identity.id_token.verify_oauth2_token",
        return_value={
            "sub": "google-subject-123",
            "email": "person@example.test",
            "email_verified": False,
        },
    ):
        with pytest.raises(InvalidGoogleCredential):
            verify_google_id_credential("signed-google-id-credential")
