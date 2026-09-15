from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from dotick.identity.models import AccountContact
from dotick.identity.sessions import create_auth_session
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db

CONTACTS_URL = "/api/v1/account/contacts"


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
