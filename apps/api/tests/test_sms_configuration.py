import os
import subprocess
import sys
from pathlib import Path

import pytest
from django.contrib.auth import get_user_model
from dotick.identity.models import AccountContact, ContactVerificationChallenge
from dotick.identity.sessions import create_auth_session
from dotick.identity.sms import SmsDeliveryUnavailable
from rest_framework.test import APIClient

REPO_ROOT = Path(__file__).resolve().parents[3]
CONTACTS_URL = "/api/v1/account/contacts"
CONTACT_VERIFY_URL = "/api/v1/account/contacts/verify"
TEST_ADAPTER = "tests.test_sms_configuration.RecordingSmsDeliveryAdapter"
UNAVAILABLE_ADAPTER = "tests.test_sms_configuration.UnavailableTestSmsDeliveryAdapter"
UNEXPECTED_ERROR_ADAPTER = "tests.test_sms_configuration.BrokenSmsDeliveryAdapter"

delivered_messages = []


class RecordingSmsDeliveryAdapter:
    def send_verification_code(self, *, phone_number, code):
        delivered_messages.append((phone_number, code))


class UnavailableTestSmsDeliveryAdapter:
    def send_verification_code(self, *, phone_number, code):
        raise SmsDeliveryUnavailable


class BrokenSmsDeliveryAdapter:
    def send_verification_code(self, *, phone_number, code):
        raise ValueError("programming defect")


def _authenticated_client(user):
    _, pair = create_auth_session(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {pair.access}")
    return client


def test_sms_delivery_adapter_setting_is_environment_driven():
    environment = {**os.environ, "DOTICK_SMS_DELIVERY_ADAPTER": TEST_ADAPTER}
    result = subprocess.run(
        [
            sys.executable,
            "apps/api/manage.py",
            "shell",
            "-c",
            f"import config.settings as s; assert s.SMS_DELIVERY_ADAPTER == {TEST_ADAPTER!r}",
        ],
        cwd=REPO_ROOT,
        env=environment,
        capture_output=True,
        text=True,
        timeout=10,
    )

    assert result.returncode == 0, result.stderr


def test_blank_sms_delivery_adapter_setting_is_rejected():
    environment = {**os.environ, "DOTICK_SMS_DELIVERY_ADAPTER": " "}
    result = subprocess.run(
        [sys.executable, "apps/api/manage.py", "check"],
        cwd=REPO_ROOT,
        env=environment,
        capture_output=True,
        text=True,
        timeout=10,
    )

    assert result.returncode != 0
    assert "DOTICK_SMS_DELIVERY_ADAPTER may not be blank" in result.stderr


@pytest.mark.django_db
def test_configured_sms_adapter_delivers_code_without_owning_verification(settings):
    settings.SMS_DELIVERY_ADAPTER = TEST_ADAPTER
    delivered_messages.clear()
    user = get_user_model().objects.create_user(
        email="sms-delivery@example.test",
        password="Only-for-automated-tests-8!",
    )
    client = _authenticated_client(user)

    requested = client.post(
        CONTACTS_URL,
        {"kind": "phone", "value": "+49123456783"},
        format="json",
    )

    assert requested.status_code == 202
    contact = AccountContact.objects.get(user=user)
    assert delivered_messages == [(contact.value, delivered_messages[0][1])]
    assert ContactVerificationChallenge.objects.filter(contact=contact).count() == 1
    assert contact.verified_at is None

    verified = client.post(
        CONTACT_VERIFY_URL,
        {"contact_id": str(contact.id), "code": delivered_messages[0][1]},
        format="json",
    )

    assert verified.status_code == 204
    contact.refresh_from_db()
    assert contact.verified_at is not None


@pytest.mark.django_db
def test_unavailable_sms_adapter_returns_expected_response_and_leaves_contact_pending(settings):
    settings.SMS_DELIVERY_ADAPTER = UNAVAILABLE_ADAPTER
    user = get_user_model().objects.create_user(
        email="sms-unavailable@example.test",
        password="Only-for-automated-tests-8!",
    )

    response = _authenticated_client(user).post(
        CONTACTS_URL,
        {"kind": "phone", "value": "+49123456784"},
        format="json",
    )

    assert response.status_code == 503
    assert response.json()["error"]["code"] == "contact_delivery_unavailable"
    assert AccountContact.objects.get(user=user).verified_at is None


@pytest.mark.django_db
def test_unexpected_sms_adapter_error_is_not_mislabeled_as_unavailable(settings):
    settings.SMS_DELIVERY_ADAPTER = UNEXPECTED_ERROR_ADAPTER
    user = get_user_model().objects.create_user(
        email="sms-defect@example.test",
        password="Only-for-automated-tests-8!",
    )

    response = _authenticated_client(user).post(
        CONTACTS_URL,
        {"kind": "phone", "value": "+49123456785"},
        format="json",
    )

    assert response.status_code == 500
    assert response.json()["error"]["code"] == "internal_error"
