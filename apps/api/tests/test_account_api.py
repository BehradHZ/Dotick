from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.core import mail
from django.utils import timezone
from dotick.identity.contact_challenges import issue_contact_challenge
from dotick.identity.models import AccountContact, ContactVerificationChallenge
from dotick.identity.sessions import create_auth_session
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db

CONTACTS_URL = "/api/v1/account/contacts"
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
    issue_contact_challenge(contact=contact)
    client = _authenticated_client(user)

    response = client.post(
        CONTACT_VERIFY_URL,
        {"contact_id": str(contact.id), "code": "000000"},
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
