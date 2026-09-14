from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from threading import Barrier

import pytest
from django.contrib.auth import get_user_model
from django.db import close_old_connections
from django.utils import timezone
from dotick.identity.authentication import SessionJWTAuthentication
from dotick.identity.models import AuthSession
from dotick.identity.sessions import create_auth_session, revoke_session
from dotick.identity.tokens import issue_token_pair
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

pytestmark = pytest.mark.django_db

TOKEN_URL = "/api/v1/auth/token"
REFRESH_URL = "/api/v1/auth/token/refresh"
LOGOUT_URL = "/api/v1/auth/logout"
SESSIONS_URL = "/api/v1/auth/sessions"


def test_jwt_access_and_refresh_lifetimes():
    user = get_user_model().objects.create_user(
        email="token-lifetime@example.test",
        password="Long-unique-password-for-tests-8!",
    )

    refresh = RefreshToken.for_user(user)
    access = refresh.access_token

    assert refresh["exp"] - refresh["iat"] == int(timedelta(days=30).total_seconds())
    assert access["exp"] - access["iat"] == int(timedelta(minutes=5).total_seconds())


def test_access_and_refresh_tokens_include_session_id():
    user = get_user_model().objects.create_user(
        email="token-session@example.test",
        password="Long-unique-password-for-tests-8!",
    )
    session_id = user.id

    pair = issue_token_pair(user=user, session_id=session_id)

    assert RefreshToken(pair.refresh)["sid"] == str(session_id)
    assert AccessToken(pair.access)["sid"] == str(session_id)


def test_session_persists_only_current_refresh_jti():
    user = get_user_model().objects.create_user(
        email="stored-refresh@example.test",
        password="Long-unique-password-for-tests-8!",
    )

    session, pair = create_auth_session(user=user, user_agent="Test client")

    refresh = RefreshToken(pair.refresh)
    session.refresh_from_db()
    assert session.refresh_jti == refresh["jti"]
    assert session.user_agent == "Test client"
    field_names = {field.name for field in AuthSession._meta.get_fields()}
    assert "refresh_token" not in field_names
    assert "access_token" not in field_names
    assert pair.refresh not in str(session.__dict__)
    assert pair.access not in str(session.__dict__)


def test_verified_account_can_log_in_with_email_and_password():
    password = "Long-unique-password-for-tests-8!"
    user = get_user_model().objects.create_user(
        email="login@example.test",
        password=password,
        handle="login_user",
        display_name="Login User",
        email_verified_at=timezone.now(),
    )

    response = APIClient().post(
        TOKEN_URL,
        {"email": "LOGIN@EXAMPLE.TEST", "password": password},
        format="json",
        HTTP_USER_AGENT="Dotick test client",
    )

    assert response.status_code == 200
    assert response.json()["user"] == {
        "email": user.email,
        "handle": user.handle,
        "display_name": user.display_name,
    }
    session = AuthSession.objects.get(user=user)
    assert session.user_agent == "Dotick test client"
    assert AccessToken(response.json()["access"])["sid"] == str(session.id)
    assert RefreshToken(response.json()["refresh"])["sid"] == str(session.id)


@pytest.mark.parametrize("account_state", ["unknown", "wrong_password", "unverified", "inactive"])
def test_login_failures_share_one_surface(account_state):
    password = "Long-unique-password-for-tests-8!"
    email = f"{account_state}@example.test"
    submitted_password = password

    if account_state != "unknown":
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            email_verified_at=timezone.now(),
        )
        if account_state == "wrong_password":
            submitted_password = "Different-long-password-for-tests-9!"
        elif account_state == "unverified":
            user.email_verified_at = None
            user.save(update_fields=["email_verified_at"])
        elif account_state == "inactive":
            user.is_active = False
            user.save(update_fields=["is_active"])

    response = APIClient().post(
        TOKEN_URL,
        {"email": email, "password": submitted_password},
        format="json",
    )

    assert response.status_code == 401
    assert response.json()["error"]["code"] == "invalid_credentials"
    assert AuthSession.objects.count() == 0


def test_refresh_rotates_token_pair_for_locked_session():
    user = get_user_model().objects.create_user(
        email="rotate@example.test",
        password="Long-unique-password-for-tests-8!",
        email_verified_at=timezone.now(),
    )
    session, original_pair = create_auth_session(user=user)
    original_jti = session.refresh_jti

    response = APIClient().post(
        REFRESH_URL,
        {"refresh": original_pair.refresh},
        format="json",
    )

    assert response.status_code == 200
    session.refresh_from_db()
    rotated_refresh = RefreshToken(response.json()["refresh"])
    rotated_access = AccessToken(response.json()["access"])
    assert session.refresh_jti == rotated_refresh["jti"]
    assert session.refresh_jti != original_jti
    assert rotated_refresh["sid"] == rotated_access["sid"] == str(session.id)


def test_refresh_rejects_reuse_without_invalidating_current_token():
    user = get_user_model().objects.create_user(
        email="refresh-reuse@example.test",
        password="Long-unique-password-for-tests-8!",
        email_verified_at=timezone.now(),
    )
    _, original_pair = create_auth_session(user=user)
    client = APIClient()

    rotated = client.post(
        REFRESH_URL,
        {"refresh": original_pair.refresh},
        format="json",
    )
    replayed = client.post(
        REFRESH_URL,
        {"refresh": original_pair.refresh},
        format="json",
    )
    current = client.post(
        REFRESH_URL,
        {"refresh": rotated.json()["refresh"]},
        format="json",
    )

    assert rotated.status_code == 200
    assert replayed.status_code == 401
    assert replayed.json()["error"]["code"] == "token_not_valid"
    assert current.status_code == 200


@pytest.mark.django_db(transaction=True)
def test_concurrent_refresh_rotation_accepts_token_once():
    user = get_user_model().objects.create_user(
        email="concurrent-refresh@example.test",
        password="Long-unique-password-for-tests-8!",
        email_verified_at=timezone.now(),
    )
    _, pair = create_auth_session(user=user)
    barrier = Barrier(2)

    def refresh_once():
        close_old_connections()
        try:
            barrier.wait()
            return APIClient().post(
                REFRESH_URL,
                {"refresh": pair.refresh},
                format="json",
            ).status_code
        finally:
            close_old_connections()

    with ThreadPoolExecutor(max_workers=2) as executor:
        statuses = list(executor.map(lambda _: refresh_once(), range(2)))

    assert sorted(statuses) == [200, 401]


def test_access_authentication_requires_active_server_session():
    user = get_user_model().objects.create_user(
        email="authenticated-session@example.test",
        password="Long-unique-password-for-tests-8!",
        email_verified_at=timezone.now(),
    )
    session, pair = create_auth_session(user=user)
    request = APIRequestFactory().get(
        "/protected",
        HTTP_AUTHORIZATION=f"Bearer {pair.access}",
    )

    authenticated_user, _ = SessionJWTAuthentication().authenticate(request)

    assert authenticated_user == user
    assert request.auth_session == session

    session.revoked_at = timezone.now()
    session.save(update_fields=["revoked_at"])
    revoked_request = APIRequestFactory().get(
        "/protected",
        HTTP_AUTHORIZATION=f"Bearer {pair.access}",
    )
    with pytest.raises(AuthenticationFailed) as rejected:
        SessionJWTAuthentication().authenticate(revoked_request)
    assert rejected.value.get_codes() == "token_not_valid"


def test_access_authentication_rejects_missing_session_claim():
    user = get_user_model().objects.create_user(
        email="missing-session-claim@example.test",
        password="Long-unique-password-for-tests-8!",
        email_verified_at=timezone.now(),
    )
    access = RefreshToken.for_user(user).access_token
    request = APIRequestFactory().get(
        "/protected",
        HTTP_AUTHORIZATION=f"Bearer {access}",
    )

    with pytest.raises(AuthenticationFailed) as rejected:
        SessionJWTAuthentication().authenticate(request)

    assert rejected.value.get_codes() == "token_not_valid"


def test_logout_revokes_current_session_and_access_token():
    user = get_user_model().objects.create_user(
        email="logout@example.test",
        password="Long-unique-password-for-tests-8!",
        email_verified_at=timezone.now(),
    )
    session, pair = create_auth_session(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {pair.access}")

    response = client.post(LOGOUT_URL, format="json")

    assert response.status_code == 204
    session.refresh_from_db()
    assert session.revoked_at is not None
    rejected = client.post(LOGOUT_URL, format="json")
    assert rejected.status_code == 401
    assert rejected.json()["error"]["code"] == "token_not_valid"


def test_active_session_listing_is_owned_and_marks_current_session():
    user = get_user_model().objects.create_user(
        email="session-list@example.test",
        password="Long-unique-password-for-tests-8!",
        email_verified_at=timezone.now(),
    )
    other_user = get_user_model().objects.create_user(
        email="other-session-list@example.test",
        password="Long-unique-password-for-tests-8!",
        email_verified_at=timezone.now(),
    )
    current, current_pair = create_auth_session(user=user, user_agent="Current browser")
    second, _ = create_auth_session(user=user, user_agent="Phone")
    revoked, _ = create_auth_session(user=user, user_agent="Old browser")
    revoke_session(session=revoked)
    create_auth_session(user=other_user, user_agent="Other account")
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {current_pair.access}")

    response = client.get(SESSIONS_URL)

    assert response.status_code == 200
    results = response.json()["results"]
    assert {entry["id"] for entry in results} == {str(current.id), str(second.id)}
    assert {entry["user_agent"] for entry in results} == {"Current browser", "Phone"}
    assert next(entry for entry in results if entry["id"] == str(current.id))["current"] is True
    assert next(entry for entry in results if entry["id"] == str(second.id))["current"] is False


def test_user_can_revoke_one_owned_session_but_not_another_users_session():
    user = get_user_model().objects.create_user(
        email="session-owner@example.test",
        password="Long-unique-password-for-tests-8!",
        email_verified_at=timezone.now(),
    )
    other_user = get_user_model().objects.create_user(
        email="other-session-owner@example.test",
        password="Long-unique-password-for-tests-8!",
        email_verified_at=timezone.now(),
    )
    _, current_pair = create_auth_session(user=user)
    owned, _ = create_auth_session(user=user)
    other, _ = create_auth_session(user=other_user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {current_pair.access}")

    hidden = client.delete(f"{SESSIONS_URL}/{other.id}")
    revoked = client.delete(f"{SESSIONS_URL}/{owned.id}")

    assert hidden.status_code == 404
    other.refresh_from_db()
    assert other.revoked_at is None
    assert revoked.status_code == 204
    owned.refresh_from_db()
    assert owned.revoked_at is not None


def test_user_can_revoke_all_owned_sessions():
    user = get_user_model().objects.create_user(
        email="revoke-all@example.test",
        password="Long-unique-password-for-tests-8!",
        email_verified_at=timezone.now(),
    )
    other_user = get_user_model().objects.create_user(
        email="other-revoke-all@example.test",
        password="Long-unique-password-for-tests-8!",
        email_verified_at=timezone.now(),
    )
    current, current_pair = create_auth_session(user=user)
    second, _ = create_auth_session(user=user)
    other, _ = create_auth_session(user=other_user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {current_pair.access}")

    response = client.delete(SESSIONS_URL)

    assert response.status_code == 204
    current.refresh_from_db()
    second.refresh_from_db()
    other.refresh_from_db()
    assert current.revoked_at is not None
    assert second.revoked_at is not None
    assert other.revoked_at is None
    assert client.get(SESSIONS_URL).status_code == 401
