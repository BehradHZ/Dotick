import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.core import mail
from dotick.identity.sessions import create_auth_session
from rest_framework.test import APIClient

REPO_ROOT = Path(__file__).resolve().parents[3]
SMTP_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
LOCMEM_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
TEST_JWT_SIGNING_KEY = "test-only-jwt-key-which-is-longer-than-fifty-characters-123456"
CONTACTS_URL = "/api/v1/account/contacts"


def _production_environment(**overrides):
    environment = {
        **os.environ,
        "DOTICK_ENV": "production",
        "DJANGO_ALLOWED_HOSTS": "api.example.test",
        "DJANGO_CORS_ORIGINS": "https://app.example.test",
        "DJANGO_CSRF_TRUSTED_ORIGINS": "https://app.example.test",
        "DJANGO_JWT_SIGNING_KEY": TEST_JWT_SIGNING_KEY,
        "WEBAUTHN_ORIGIN": "https://app.example.test",
        "DJANGO_EMAIL_BACKEND": SMTP_BACKEND,
        "DJANGO_EMAIL_HOST": "smtp.example.test",
        "DJANGO_EMAIL_PORT": "465",
        "DJANGO_EMAIL_HOST_USER": "mailer@example.test",
        "DJANGO_EMAIL_HOST_PASSWORD": "test-only-mail-secret",
        "DJANGO_EMAIL_USE_TLS": "0",
        "DJANGO_EMAIL_USE_SSL": "1",
        "DJANGO_DEFAULT_FROM_EMAIL": "Dotick <noreply@example.test>",
    }
    environment.update(overrides)
    return environment


def _run_settings_command(command, *, environment):
    return subprocess.run(
        [sys.executable, "apps/api/manage.py", "shell", "-c", command],
        cwd=REPO_ROOT,
        env=environment,
        capture_output=True,
        text=True,
        timeout=10,
    )


def _authenticated_client(user):
    _, pair = create_auth_session(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {pair.access}")
    return client


def test_external_email_provider_settings_are_environment_driven():
    command = (
        "import config.settings as s; "
        f"assert s.EMAIL_BACKEND == {SMTP_BACKEND!r}; "
        "assert s.EMAIL_HOST == 'smtp.example.test'; "
        "assert s.EMAIL_PORT == 465; "
        "assert s.EMAIL_HOST_USER == 'mailer@example.test'; "
        "assert s.EMAIL_HOST_PASSWORD == 'test-only-mail-secret'; "
        "assert s.EMAIL_USE_TLS is False; assert s.EMAIL_USE_SSL is True; "
        "assert s.DEFAULT_FROM_EMAIL == 'Dotick <noreply@example.test>'"
    )

    result = _run_settings_command(command, environment=_production_environment())

    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize(
    ("overrides", "expected_error"),
    [
        ({"DJANGO_EMAIL_PORT": "not-a-port"}, "DJANGO_EMAIL_PORT must be an integer port"),
        ({"DJANGO_EMAIL_PORT": "70000"}, "DJANGO_EMAIL_PORT must be between 1 and 65535"),
        (
            {"DJANGO_EMAIL_USE_TLS": "1", "DJANGO_EMAIL_USE_SSL": "1"},
            "DJANGO_EMAIL_USE_TLS and DJANGO_EMAIL_USE_SSL are mutually exclusive",
        ),
        (
            {"DJANGO_EMAIL_HOST_PASSWORD": ""},
            "DJANGO_EMAIL_HOST_USER and DJANGO_EMAIL_HOST_PASSWORD must be configured together",
        ),
    ],
)
def test_invalid_email_provider_configuration_is_rejected(overrides, expected_error):
    result = _run_settings_command(
        "import config.settings",
        environment=_production_environment(**overrides),
    )

    assert result.returncode != 0
    assert expected_error in result.stderr


@pytest.mark.django_db
def test_locmem_email_backend_does_not_require_external_provider_settings(settings):
    settings.EMAIL_BACKEND = LOCMEM_BACKEND
    settings.EMAIL_HOST = ""
    settings.DEFAULT_FROM_EMAIL = ""
    user = get_user_model().objects.create_user(
        email="local-email-backend@example.test",
        password="Only-for-automated-tests-8!",
    )

    response = _authenticated_client(user).post(
        CONTACTS_URL,
        {"kind": "email", "value": "secondary@example.test"},
        format="json",
    )

    assert response.status_code == 202
    assert len(mail.outbox) == 1


@pytest.mark.django_db
def test_unconfigured_smtp_delivery_returns_unavailable(settings):
    settings.EMAIL_BACKEND = SMTP_BACKEND
    settings.EMAIL_HOST = ""
    settings.DEFAULT_FROM_EMAIL = ""
    user = get_user_model().objects.create_user(
        email="unconfigured-email@example.test",
        password="Only-for-automated-tests-8!",
    )

    response = _authenticated_client(user).post(
        CONTACTS_URL,
        {"kind": "email", "value": "secondary-unconfigured@example.test"},
        format="json",
    )

    assert response.status_code == 503
    assert response.json()["error"]["code"] == "contact_delivery_unavailable"


@pytest.mark.django_db
def test_unexpected_email_error_is_not_mislabeled_as_provider_unavailable(settings):
    settings.EMAIL_BACKEND = LOCMEM_BACKEND
    user = get_user_model().objects.create_user(
        email="unexpected-email-error@example.test",
        password="Only-for-automated-tests-8!",
    )
    client = _authenticated_client(user)

    with patch("dotick.identity.contacts.send_mail", side_effect=ValueError("programming defect")):
        with pytest.raises(ValueError, match="programming defect"):
            client.post(
                CONTACTS_URL,
                {"kind": "email", "value": "secondary-unexpected@example.test"},
                format="json",
            )
