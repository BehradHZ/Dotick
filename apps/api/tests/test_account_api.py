from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.core import mail
from django.utils import timezone
from dotick.identity.models import AccountContact
from dotick.identity.sessions import create_auth_session
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db

CONTACTS_URL = "/api/v1/account/contacts"
PASSWORD_RESET_REQUEST_URL = "/api/v1/auth/password/reset/request"


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
