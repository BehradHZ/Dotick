from datetime import timedelta
from types import SimpleNamespace
from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from dotick.identity.google_identity import (
    GoogleIdentityClaims,
    InvalidGoogleCredential,
    verify_google_id_credential,
)
from dotick.identity.models import ExternalIdentity, PasskeyChallenge, PasskeyCredential
from dotick.identity.sessions import create_auth_session
from rest_framework.test import APIClient
from webauthn.helpers import base64url_to_bytes, bytes_to_base64url
from webauthn.helpers.structs import CredentialDeviceType

pytestmark = pytest.mark.django_db

PASSWORD_URL = "/api/v1/auth/password"
TOKEN_URL = "/api/v1/auth/token"
GOOGLE_URL = "/api/v1/auth/google"
GOOGLE_LINK_URL = "/api/v1/auth/google/link"
PASSKEY_REGISTRATION_OPTIONS_URL = "/api/v1/auth/passkeys/registration/options"
PASSKEY_REGISTRATION_VERIFY_URL = "/api/v1/auth/passkeys/registration/verify"
PASSKEY_AUTHENTICATION_OPTIONS_URL = "/api/v1/auth/passkeys/authentication/options"
PASSKEY_AUTHENTICATION_VERIFY_URL = "/api/v1/auth/passkeys/authentication/verify"
PASSKEYS_URL = "/api/v1/auth/passkeys"


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


def _google_claims(*, subject="google-subject-123", email="google@example.test"):
    return GoogleIdentityClaims(
        subject=subject,
        email=email,
        display_name="Google Person",
        picture_url="https://example.test/google-person.png",
    )


def test_google_sign_in_creates_google_only_account_and_session():
    with patch(
        "dotick.identity.application.verify_google_id_credential",
        return_value=_google_claims(),
    ):
        response = APIClient().post(
            GOOGLE_URL,
            {"credential": "signed-google-id-credential"},
            format="json",
            HTTP_USER_AGENT="Google test client",
        )

    assert response.status_code == 200
    user = get_user_model().objects.get(email="google@example.test")
    assert user.is_active
    assert user.email_verified_at is not None
    assert not user.has_usable_password()
    assert ExternalIdentity.objects.get(user=user).subject == "google-subject-123"
    assert user.auth_sessions.get().user_agent == "Google test client"
    assert response.json()["user"]["email"] == user.email
    assert response.json()["fallback_recommended"] is True


def test_google_sign_in_resolves_existing_linked_identity():
    user = get_user_model().objects.create_user(
        email="linked@example.test",
        password="Independent-password-fallback-8!",
        email_verified_at=timezone.now(),
    )
    ExternalIdentity.objects.create(
        user=user,
        provider=ExternalIdentity.Provider.GOOGLE,
        subject="linked-google-subject",
    )
    with patch(
        "dotick.identity.application.verify_google_id_credential",
        return_value=_google_claims(
            subject="linked-google-subject",
            email="changed-at-google@example.test",
        ),
    ):
        response = APIClient().post(
            GOOGLE_URL,
            {"credential": "signed-google-id-credential"},
            format="json",
        )

    assert response.status_code == 200
    assert get_user_model().objects.count() == 1
    assert response.json()["user"]["email"] == user.email
    assert response.json()["fallback_recommended"] is False


def test_authenticated_user_can_explicitly_link_google_identity():
    user = get_user_model().objects.create_user(
        email="link-target@example.test",
        password="Independent-password-fallback-8!",
        email_verified_at=timezone.now(),
    )
    client, _ = _authenticated_client(user)
    with patch(
        "dotick.identity.application.verify_google_id_credential",
        return_value=_google_claims(
            subject="explicit-link-subject",
            email="different-google-email@example.test",
        ),
    ):
        response = client.post(
            GOOGLE_LINK_URL,
            {"credential": "signed-google-id-credential"},
            format="json",
        )

    assert response.status_code == 204
    assert get_user_model().objects.count() == 1
    assert ExternalIdentity.objects.get(
        provider=ExternalIdentity.Provider.GOOGLE,
        subject="explicit-link-subject",
    ).user == user


def test_google_linking_requires_recent_authentication():
    user = get_user_model().objects.create_user(
        email="stale-link-target@example.test",
        password="Independent-password-fallback-8!",
        email_verified_at=timezone.now(),
    )
    client, _ = _authenticated_client(user, session_age=timedelta(minutes=11))
    with patch(
        "dotick.identity.application.verify_google_id_credential",
        return_value=_google_claims(subject="stale-link-subject"),
    ) as verifier:
        response = client.post(
            GOOGLE_LINK_URL,
            {"credential": "signed-google-id-credential"},
            format="json",
        )

    assert response.status_code == 403
    assert response.json()["error"]["code"] == "recent_auth_required"
    assert not ExternalIdentity.objects.exists()
    verifier.assert_not_called()


def test_google_subject_is_authoritative_when_claimed_email_matches_another_account():
    subject_owner = get_user_model().objects.create_user(
        email="subject-owner@example.test",
        password=None,
        email_verified_at=timezone.now(),
    )
    email_owner = get_user_model().objects.create_user(
        email="claimed-email-owner@example.test",
        password="Independent-password-fallback-8!",
        email_verified_at=timezone.now(),
    )
    ExternalIdentity.objects.create(
        user=subject_owner,
        provider=ExternalIdentity.Provider.GOOGLE,
        subject="authoritative-google-subject",
    )
    with patch(
        "dotick.identity.application.verify_google_id_credential",
        return_value=_google_claims(
            subject="authoritative-google-subject",
            email=email_owner.email,
        ),
    ):
        response = APIClient().post(
            GOOGLE_URL,
            {"credential": "signed-google-id-credential"},
            format="json",
        )

    assert response.status_code == 200
    assert response.json()["user"]["email"] == subject_owner.email
    assert subject_owner.auth_sessions.count() == 1
    assert email_owner.auth_sessions.count() == 0


def test_google_sign_in_never_auto_links_existing_account_by_email():
    existing = get_user_model().objects.create_user(
        email="existing-google-email@example.test",
        password="Independent-password-fallback-8!",
        email_verified_at=timezone.now(),
    )
    with patch(
        "dotick.identity.application.verify_google_id_credential",
        return_value=_google_claims(
            subject="unlinked-google-subject",
            email=existing.email,
        ),
    ):
        response = APIClient().post(
            GOOGLE_URL,
            {"credential": "signed-google-id-credential"},
            format="json",
        )

    assert response.status_code == 409
    assert response.json()["error"]["code"] == "account_link_required"
    assert not ExternalIdentity.objects.exists()
    assert not existing.auth_sessions.exists()


def test_google_only_account_can_sign_in_without_password_or_passkey():
    user = get_user_model().objects.create_user(
        email="google-only-returning@example.test",
        password=None,
        email_verified_at=timezone.now(),
    )
    ExternalIdentity.objects.create(
        user=user,
        provider=ExternalIdentity.Provider.GOOGLE,
        subject="google-only-returning-subject",
    )
    with patch(
        "dotick.identity.application.verify_google_id_credential",
        return_value=_google_claims(
            subject="google-only-returning-subject",
            email=user.email,
        ),
    ):
        response = APIClient().post(
            GOOGLE_URL,
            {"credential": "signed-google-id-credential"},
            format="json",
        )

    assert response.status_code == 200
    assert not user.has_usable_password()
    assert response.json()["user"]["email"] == user.email


def test_google_sign_in_recommends_fallback_only_when_none_exists():
    user = get_user_model().objects.create_user(
        email="google-passkey-fallback@example.test",
        password=None,
        email_verified_at=timezone.now(),
    )
    ExternalIdentity.objects.create(
        user=user,
        provider=ExternalIdentity.Provider.GOOGLE,
        subject="google-passkey-fallback-subject",
    )
    PasskeyCredential.objects.create(
        user=user,
        credential_id=b"fallback-passkey-id",
        public_key=b"fallback-public-key",
        name="Fallback passkey",
    )
    with patch(
        "dotick.identity.application.verify_google_id_credential",
        return_value=_google_claims(
            subject="google-passkey-fallback-subject",
            email=user.email,
        ),
    ):
        response = APIClient().post(
            GOOGLE_URL,
            {"credential": "signed-google-id-credential"},
            format="json",
        )

    assert response.status_code == 200
    assert response.json()["fallback_recommended"] is False


def test_passkey_registration_options_use_persisted_challenge_and_account_identity():
    user = get_user_model().objects.create_user(
        email="registration-options@example.test",
        password=None,
        display_name="Registration Options User",
        email_verified_at=timezone.now(),
    )
    client, _ = _authenticated_client(user)

    response = client.post(
        PASSKEY_REGISTRATION_OPTIONS_URL,
        {"name": "Laptop passkey"},
        format="json",
    )

    assert response.status_code == 200
    payload = response.json()
    challenge = user.passkey_challenges.get(id=payload["challenge_id"])
    public_key = payload["public_key"]
    assert base64url_to_bytes(public_key["challenge"]) == bytes(challenge.challenge)
    assert base64url_to_bytes(public_key["user"]["id"]) == user.id.bytes
    assert public_key["user"]["name"] == user.email
    assert challenge.name == "Laptop passkey"


def test_passkey_registration_verification_persists_verified_credential():
    user = get_user_model().objects.create_user(
        email="registration-verify@example.test",
        password=None,
        email_verified_at=timezone.now(),
    )
    client, _ = _authenticated_client(user)
    options = client.post(
        PASSKEY_REGISTRATION_OPTIONS_URL,
        {"name": "Phone passkey"},
        format="json",
    ).json()
    credential = {
        "id": "credential-id",
        "response": {"transports": ["internal", "hybrid"]},
    }
    verification = SimpleNamespace(
        credential_id=b"verified-credential-id",
        credential_public_key=b"verified-public-key",
        sign_count=7,
        credential_device_type=CredentialDeviceType.MULTI_DEVICE,
        credential_backed_up=True,
    )

    with patch(
        "dotick.identity.passkeys.verify_registration_response",
        return_value=verification,
    ) as verifier:
        response = client.post(
            PASSKEY_REGISTRATION_VERIFY_URL,
            {
                "challenge_id": options["challenge_id"],
                "credential": credential,
            },
            format="json",
        )

    assert response.status_code == 201
    passkey = PasskeyCredential.objects.get(user=user)
    challenge = user.passkey_challenges.get(id=options["challenge_id"])
    assert bytes(passkey.credential_id) == b"verified-credential-id"
    assert bytes(passkey.public_key) == b"verified-public-key"
    assert passkey.sign_count == 7
    assert passkey.device_type == "multi_device"
    assert passkey.backed_up is True
    assert passkey.transports == ["internal", "hybrid"]
    assert passkey.name == "Phone passkey"
    assert challenge.consumed_at is not None
    assert verifier.call_args.kwargs["expected_challenge"] == bytes(challenge.challenge)
    assert verifier.call_args.kwargs["require_user_verification"] is True

    replay = client.post(
        PASSKEY_REGISTRATION_VERIFY_URL,
        {
            "challenge_id": options["challenge_id"],
            "credential": credential,
        },
        format="json",
    )
    assert replay.status_code == 400
    assert replay.json()["error"]["code"] == "invalid_passkey_ceremony"


def test_passkey_authentication_options_are_discoverable_and_public():
    response = APIClient().post(
        PASSKEY_AUTHENTICATION_OPTIONS_URL,
        {},
        format="json",
    )

    assert response.status_code == 200
    payload = response.json()
    challenge = PasskeyChallenge.objects.get(id=payload["challenge_id"])
    public_key = payload["public_key"]
    assert challenge.user is None
    assert challenge.purpose == PasskeyChallenge.Purpose.AUTHENTICATION
    assert base64url_to_bytes(public_key["challenge"]) == bytes(challenge.challenge)
    assert public_key.get("allowCredentials") in (None, [])
    assert public_key["userVerification"] == "required"


def test_passkey_authentication_verification_updates_counter_and_creates_session():
    user = get_user_model().objects.create_user(
        email="passkey-authentication@example.test",
        password=None,
        email_verified_at=timezone.now(),
    )
    passkey = PasskeyCredential.objects.create(
        user=user,
        credential_id=b"authentication-credential-id",
        public_key=b"authentication-public-key",
        sign_count=3,
        device_type="single_device",
        backed_up=False,
        name="Authentication passkey",
    )
    options = APIClient().post(
        PASSKEY_AUTHENTICATION_OPTIONS_URL,
        {},
        format="json",
    ).json()
    credential = {
        "id": bytes_to_base64url(bytes(passkey.credential_id)),
        "rawId": bytes_to_base64url(bytes(passkey.credential_id)),
        "response": {
            "clientDataJSON": bytes_to_base64url(b"client-data"),
            "authenticatorData": bytes_to_base64url(b"authenticator-data"),
            "signature": bytes_to_base64url(b"signature"),
            "userHandle": bytes_to_base64url(user.id.bytes),
        },
        "type": "public-key",
    }
    verification = SimpleNamespace(
        credential_id=bytes(passkey.credential_id),
        new_sign_count=4,
        credential_device_type=CredentialDeviceType.MULTI_DEVICE,
        credential_backed_up=True,
    )

    with patch(
        "dotick.identity.passkeys.verify_authentication_response",
        return_value=verification,
    ) as verifier:
        response = APIClient().post(
            PASSKEY_AUTHENTICATION_VERIFY_URL,
            {
                "challenge_id": options["challenge_id"],
                "credential": credential,
            },
            format="json",
            HTTP_USER_AGENT="Passkey test client",
        )

    assert response.status_code == 200
    passkey.refresh_from_db()
    challenge = PasskeyChallenge.objects.get(id=options["challenge_id"])
    assert passkey.sign_count == 4
    assert passkey.device_type == "multi_device"
    assert passkey.backed_up is True
    assert passkey.last_used_at is not None
    assert challenge.consumed_at is not None
    assert user.auth_sessions.get().user_agent == "Passkey test client"
    assert response.json()["user"]["email"] == user.email
    assert response.json()["fallback_recommended"] is False
    assert verifier.call_args.kwargs["credential_current_sign_count"] == 3
    assert verifier.call_args.kwargs["require_user_verification"] is True

    replay = APIClient().post(
        PASSKEY_AUTHENTICATION_VERIFY_URL,
        {
            "challenge_id": options["challenge_id"],
            "credential": credential,
        },
        format="json",
    )
    assert replay.status_code == 400


def test_passkey_listing_contains_only_owned_credentials():
    user = get_user_model().objects.create_user(
        email="passkey-list@example.test",
        password=None,
        email_verified_at=timezone.now(),
    )
    other_user = get_user_model().objects.create_user(
        email="other-passkey-list@example.test",
        password=None,
        email_verified_at=timezone.now(),
    )
    owned = PasskeyCredential.objects.create(
        user=user,
        credential_id=b"owned-list-credential",
        public_key=b"owned-list-public-key",
        device_type="multi_device",
        backed_up=True,
        name="Owned passkey",
    )
    PasskeyCredential.objects.create(
        user=other_user,
        credential_id=b"foreign-list-credential",
        public_key=b"foreign-list-public-key",
        name="Foreign passkey",
    )
    client, _ = _authenticated_client(user)

    response = client.get(PASSKEYS_URL)

    assert response.status_code == 200
    assert response.json()["results"] == [
        {
            "id": str(owned.id),
            "name": "Owned passkey",
            "device_type": "multi_device",
            "backed_up": True,
            "created_at": owned.created_at.isoformat().replace("+00:00", "Z"),
            "last_used_at": None,
        }
    ]


def test_passkey_deletion_is_scoped_to_owner():
    user = get_user_model().objects.create_user(
        email="passkey-delete@example.test",
        password=None,
        email_verified_at=timezone.now(),
    )
    other_user = get_user_model().objects.create_user(
        email="other-passkey-delete@example.test",
        password=None,
        email_verified_at=timezone.now(),
    )
    owned = PasskeyCredential.objects.create(
        user=user,
        credential_id=b"owned-delete-credential",
        public_key=b"owned-delete-public-key",
        name="Owned passkey",
    )
    foreign = PasskeyCredential.objects.create(
        user=other_user,
        credential_id=b"foreign-delete-credential",
        public_key=b"foreign-delete-public-key",
        name="Foreign passkey",
    )
    client, _ = _authenticated_client(user)

    hidden = client.delete(f"{PASSKEYS_URL}/{foreign.id}")
    deleted = client.delete(f"{PASSKEYS_URL}/{owned.id}")

    assert hidden.status_code == 404
    assert PasskeyCredential.objects.filter(pk=foreign.id).exists()
    assert deleted.status_code == 204
    assert not PasskeyCredential.objects.filter(pk=owned.id).exists()


def test_passkey_enrollment_requires_recent_authenticated_session():
    user = get_user_model().objects.create_user(
        email="stale-passkey-enrollment@example.test",
        password=None,
        email_verified_at=timezone.now(),
    )
    client, _ = _authenticated_client(user, session_age=timedelta(minutes=11))

    response = client.post(
        PASSKEY_REGISTRATION_OPTIONS_URL,
        {"name": "Stale session passkey"},
        format="json",
    )

    assert response.status_code == 403
    assert response.json()["error"]["code"] == "recent_auth_required"
    assert not PasskeyChallenge.objects.exists()
