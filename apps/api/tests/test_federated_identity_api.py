from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
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
