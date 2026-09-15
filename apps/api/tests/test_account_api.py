from datetime import timedelta
from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.core import mail
from django.utils import timezone
from dotick.identity.contact_challenges import issue_contact_challenge
from dotick.identity.models import (
    AccountContact,
    ContactVerificationChallenge,
    ExternalIdentity,
    PasskeyCredential,
    UserPreferences,
)
from dotick.identity.sessions import create_auth_session
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db

CONTACTS_URL = "/api/v1/account/contacts"
ACCOUNT_URL = "/api/v1/account"
PASSWORD_RESET_REQUEST_URL = "/api/v1/auth/password/reset/request"
CONTACT_VERIFY_URL = "/api/v1/account/contacts/verify"


def _authenticated_client(user):
    _, pair = create_auth_session(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {pair.access}")
    return client


def test_active_contact_list_returns_only_verified_owned_contacts():
    user = get_user_model().objects.create_user(
        email="contact-owner@example.test",
        password="Only-for-automated-tests-8!",
    )
    other = get_user_model().objects.create_user(
        email="other-contact-owner@example.test",
        password="Only-for-automated-tests-8!",
    )
    verified_at = timezone.now() - timedelta(minutes=1)
    verified = AccountContact.objects.create(
        user=user,
        kind=AccountContact.Kind.EMAIL,
        value="VERIFIED@example.test",
        verified_at=verified_at,
    )
    AccountContact.objects.create(
        user=user,
        kind=AccountContact.Kind.PHONE,
        value="+49123456789",
    )
    AccountContact.objects.create(
        user=other,
        kind=AccountContact.Kind.EMAIL,
        value="foreign@example.test",
        verified_at=verified_at,
    )

    response = _authenticated_client(user).get(CONTACTS_URL)

    assert response.status_code == 200
    assert response.json() == {
        "results": [
            {
                "id": str(verified.id),
                "kind": "email",
                "value": "verified@example.test",
                "verified_at": verified_at.isoformat().replace("+00:00", "Z"),
            }
        ]
    }


def test_pending_contact_cannot_drive_password_reset(settings):
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
    user = get_user_model().objects.create_user(
        email="primary-account@example.test",
        password="Only-for-automated-tests-8!",
        email_verified_at=timezone.now(),
        is_active=True,
    )
    pending = AccountContact.objects.create(
        user=user,
        kind=AccountContact.Kind.EMAIL,
        value="pending-reset@example.test",
    )

    response = APIClient().post(
        PASSWORD_RESET_REQUEST_URL,
        {"email": pending.value},
        format="json",
    )

    assert response.status_code == 202
    assert mail.outbox == []
    assert not user.verification_challenges.exists()


def _delivered_code(message):
    return message.body.split("code is ", 1)[1].split(".", 1)[0]


def test_contact_request_and_verification_activate_email_contact(settings):
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
    user = get_user_model().objects.create_user(
        email="request-contact@example.test",
        password="Only-for-automated-tests-8!",
    )
    client = _authenticated_client(user)

    requested = client.post(
        CONTACTS_URL,
        {"kind": "email", "value": "  SECONDARY@Example.Test "},
        format="json",
    )

    assert requested.status_code == 202
    assert requested.json()["status"] == "pending"
    contact = AccountContact.objects.get(id=requested.json()["id"])
    assert contact.value == "secondary@example.test"
    assert contact.verified_at is None
    challenge = ContactVerificationChallenge.objects.get(contact=contact)
    code = _delivered_code(mail.outbox[0])
    assert code not in challenge.code_digest
    assert client.get(CONTACTS_URL).json() == {"results": []}

    verified = client.post(
        CONTACT_VERIFY_URL,
        {"contact_id": str(contact.id), "code": code},
        format="json",
    )

    assert verified.status_code == 204
    contact.refresh_from_db()
    assert contact.verified_at is not None
    assert client.get(CONTACTS_URL).json()["results"][0]["id"] == str(contact.id)


def test_invalid_contact_code_keeps_contact_pending_and_tracks_attempt():
    user = get_user_model().objects.create_user(
        email="invalid-contact-code@example.test",
        password="Only-for-automated-tests-8!",
    )
    contact = AccountContact.objects.create(
        user=user,
        kind=AccountContact.Kind.PHONE,
        value="+49123456780",
    )
    actual_code = issue_contact_challenge(contact=contact)
    invalid_code = "000000" if actual_code != "000000" else "000001"
    client = _authenticated_client(user)

    response = client.post(
        CONTACT_VERIFY_URL,
        {"contact_id": str(contact.id), "code": invalid_code},
        format="json",
    )

    assert response.status_code == 400
    contact.refresh_from_db()
    challenge = ContactVerificationChallenge.objects.get(contact=contact)
    assert contact.verified_at is None
    assert challenge.failed_attempts == 1


def test_contact_deletion_is_scoped_to_owner():
    user = get_user_model().objects.create_user(
        email="delete-contact@example.test",
        password="Only-for-automated-tests-8!",
    )
    other = get_user_model().objects.create_user(
        email="foreign-delete-contact@example.test",
        password="Only-for-automated-tests-8!",
    )
    owned = AccountContact.objects.create(
        user=user,
        kind=AccountContact.Kind.PHONE,
        value="+49123456781",
    )
    foreign = AccountContact.objects.create(
        user=other,
        kind=AccountContact.Kind.PHONE,
        value="+49123456782",
    )
    client = _authenticated_client(user)

    assert client.delete(f"{CONTACTS_URL}/{foreign.id}").status_code == 404
    assert client.delete(f"{CONTACTS_URL}/{owned.id}").status_code == 204
    assert AccountContact.objects.filter(id=foreign.id).exists()
    assert not AccountContact.objects.filter(id=owned.id).exists()


def test_verified_contact_conflict_does_not_disclose_owner(settings):
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
    owner = get_user_model().objects.create_user(
        email="verified-contact-owner@example.test",
        password="Only-for-automated-tests-8!",
    )
    requester = get_user_model().objects.create_user(
        email="verified-contact-requester@example.test",
        password="Only-for-automated-tests-8!",
    )
    AccountContact.objects.create(
        user=owner,
        kind=AccountContact.Kind.EMAIL,
        value="claimed@example.test",
        verified_at=timezone.now(),
    )

    response = _authenticated_client(requester).post(
        CONTACTS_URL,
        {"kind": "email", "value": "claimed@example.test"},
        format="json",
    )

    assert response.status_code == 409
    assert response.json()["error"]["code"] == "contact_conflict"
    assert "owner" not in str(response.json()).lower()


def test_contact_activation_conflict_keeps_pending_contact_inactive():
    owner = get_user_model().objects.create_user(
        email="activation-owner@example.test",
        password="Only-for-automated-tests-8!",
    )
    requester = get_user_model().objects.create_user(
        email="activation-requester@example.test",
        password="Only-for-automated-tests-8!",
    )
    pending = AccountContact.objects.create(
        user=requester,
        kind=AccountContact.Kind.PHONE,
        value="+49123456784",
    )
    code = issue_contact_challenge(contact=pending)
    AccountContact.objects.create(
        user=owner,
        kind=AccountContact.Kind.PHONE,
        value=pending.value,
        verified_at=timezone.now(),
    )

    response = _authenticated_client(requester).post(
        CONTACT_VERIFY_URL,
        {"contact_id": str(pending.id), "code": code},
        format="json",
    )

    assert response.status_code == 409
    pending.refresh_from_db()
    assert pending.verified_at is None


def test_phone_contact_remains_pending_when_delivery_is_unavailable():
    user = get_user_model().objects.create_user(
        email="phone-delivery@example.test",
        password="Only-for-automated-tests-8!",
    )

    response = _authenticated_client(user).post(
        CONTACTS_URL,
        {"kind": "phone", "value": "+49123456783"},
        format="json",
    )

    assert response.status_code == 503
    assert response.json()["error"]["code"] == "contact_delivery_unavailable"
    contact = AccountContact.objects.get(user=user)
    assert contact.verified_at is None


def test_email_transport_failure_returns_unavailable_and_preserves_pending_contact():
    user = get_user_model().objects.create_user(
        email="email-delivery-failure@example.test",
        password="Only-for-automated-tests-8!",
    )

    with patch("dotick.identity.contacts.send_mail", side_effect=OSError("transport down")):
        response = _authenticated_client(user).post(
            CONTACTS_URL,
            {"kind": "email", "value": "pending-delivery@example.test"},
            format="json",
        )

    assert response.status_code == 503
    contact = AccountContact.objects.get(user=user)
    assert contact.value == "pending-delivery@example.test"
    assert contact.verified_at is None


def test_get_and_patch_current_account():
    user = get_user_model().objects.create_user(
        email="account-detail@example.test",
        password="Only-for-automated-tests-8!",
        handle="account_detail",
        display_name="Before update",
    )
    client = _authenticated_client(user)

    initial = client.get(ACCOUNT_URL)
    updated = client.patch(
        ACCOUNT_URL,
        {"display_name": "After update"},
        format="json",
    )

    assert initial.status_code == 200
    assert initial.json() == {
        "id": str(user.id),
        "email": user.email,
        "handle": "account_detail",
        "display_name": "Before update",
        "profile_picture_url": None,
        "timezone": None,
        "authentication_methods": {"password": True, "google": False, "passkey": False},
    }
    assert updated.status_code == 200
    assert updated.json()["display_name"] == "After update"
    user.refresh_from_db()
    assert user.display_name == "After update"


def test_account_detail_requires_an_active_session():
    response = APIClient().get(ACCOUNT_URL)

    assert response.status_code == 401


@pytest.mark.parametrize("payload", [{}, {"unknown": "value"}])
def test_account_patch_rejects_empty_and_unknown_updates(payload):
    user = get_user_model().objects.create_user(
        email="invalid-account-update@example.test",
        password="Only-for-automated-tests-8!",
    )

    response = _authenticated_client(user).patch(ACCOUNT_URL, payload, format="json")

    assert response.status_code == 400


def test_account_patch_updates_every_mutable_profile_field():
    user = get_user_model().objects.create_user(
        email="mutable-account@example.test",
        password="Only-for-automated-tests-8!",
        handle="before_handle",
        display_name="Before profile update",
    )
    client = _authenticated_client(user)

    response = client.patch(
        ACCOUNT_URL,
        {
            "handle": "after_handle",
            "display_name": "  After profile update  ",
            "profile_picture_url": "https://cdn.example.test/profile.png",
            "timezone": "Europe/Berlin",
        },
        format="json",
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": str(user.id),
        "email": user.email,
        "handle": "after_handle",
        "display_name": "After profile update",
        "profile_picture_url": "https://cdn.example.test/profile.png",
        "timezone": "Europe/Berlin",
        "authentication_methods": {"password": True, "google": False, "passkey": False},
    }
    user.refresh_from_db()
    assert user.handle == "after_handle"
    assert user.display_name == "After profile update"
    assert user.profile_picture_url == "https://cdn.example.test/profile.png"
    assert UserPreferences.objects.get(user=user).timezone == "Europe/Berlin"

    cleared = client.patch(
        ACCOUNT_URL,
        {"profile_picture_url": None, "timezone": "Asia/Tehran"},
        format="json",
    )

    assert cleared.status_code == 200
    assert cleared.json()["profile_picture_url"] is None
    assert cleared.json()["timezone"] == "Asia/Tehran"


def test_account_patch_rejects_case_insensitive_handle_conflict_atomically():
    user = get_user_model().objects.create_user(
        email="handle-requester@example.test",
        password="Only-for-automated-tests-8!",
        handle="requester_handle",
        display_name="Unchanged name",
    )
    get_user_model().objects.create_user(
        email="handle-owner@example.test",
        password="Only-for-automated-tests-8!",
        handle="Claimed_Handle",
    )

    response = _authenticated_client(user).patch(
        ACCOUNT_URL,
        {
            "handle": "claimed_handle",
            "display_name": "Must roll back",
            "timezone": "Europe/Berlin",
        },
        format="json",
    )

    assert response.status_code == 409
    assert response.json()["error"]["code"] == "account_conflict"
    user.refresh_from_db()
    assert user.handle == "requester_handle"
    assert user.display_name == "Unchanged name"
    assert not UserPreferences.objects.filter(user=user).exists()


@pytest.mark.parametrize(
    "payload",
    [
        {"handle": "not valid"},
        {"display_name": "   "},
        {"profile_picture_url": "not-a-url"},
        {"timezone": "Mars/Olympus_Mons"},
    ],
)
def test_account_patch_validates_mutable_profile_fields(payload):
    user = get_user_model().objects.create_user(
        email="profile-validation@example.test",
        password="Only-for-automated-tests-8!",
        handle="valid_handle",
        display_name="Valid name",
    )

    response = _authenticated_client(user).patch(ACCOUNT_URL, payload, format="json")

    assert response.status_code == 400
    user.refresh_from_db()
    assert user.handle == "valid_handle"
    assert user.display_name == "Valid name"
    assert user.profile_picture_url is None
    assert not UserPreferences.objects.filter(user=user).exists()


def test_account_response_returns_enabled_authentication_methods():
    user = get_user_model().objects.create_user(
        email="account-methods@example.test",
        password=None,
    )
    ExternalIdentity.objects.create(
        user=user,
        provider=ExternalIdentity.Provider.GOOGLE,
        subject="account-methods-google-subject",
    )
    PasskeyCredential.objects.create(
        user=user,
        credential_id=b"account-methods-credential",
        public_key=b"account-methods-public-key",
        name="Account methods passkey",
    )

    response = _authenticated_client(user).get(ACCOUNT_URL)

    assert response.status_code == 200
    assert response.json()["authentication_methods"] == {
        "password": False,
        "google": True,
        "passkey": True,
    }
