import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
TEST_JWT_SIGNING_KEY = "test-only-jwt-key-which-is-longer-than-fifty-characters-123456"


def _production_environment(**overrides):
    environment = {
        **os.environ,
        "DOTICK_ENV": "production",
        "DJANGO_ALLOWED_HOSTS": "api.example.test",
        "DJANGO_CORS_ORIGINS": "https://app.example.test",
        "DJANGO_CSRF_TRUSTED_ORIGINS": "https://app.example.test",
        "DJANGO_JWT_SIGNING_KEY": TEST_JWT_SIGNING_KEY,
        "WEBAUTHN_RP_ID": "example.test",
        "WEBAUTHN_RP_NAME": "Dotick Production",
        "WEBAUTHN_ORIGIN": "https://app.example.test",
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


def test_webauthn_relying_party_settings_are_environment_driven():
    result = _run_settings_command(
        (
            "import config.settings as s; "
            "assert s.WEBAUTHN_RP_ID == 'example.test'; "
            "assert s.WEBAUTHN_RP_NAME == 'Dotick Production'; "
            "assert s.WEBAUTHN_ORIGIN == 'https://app.example.test'"
        ),
        environment=_production_environment(),
    )

    assert result.returncode == 0, result.stderr


def test_localhost_http_webauthn_configuration_remains_available():
    environment = {
        **os.environ,
        "DOTICK_ENV": "test",
        "WEBAUTHN_RP_ID": "localhost",
        "WEBAUTHN_RP_NAME": "Dotick",
        "WEBAUTHN_ORIGIN": "http://localhost:8081",
    }
    result = _run_settings_command(
        (
            "import config.settings as s; "
            "assert s.WEBAUTHN_RP_ID == 'localhost'; "
            "assert s.WEBAUTHN_RP_NAME == 'Dotick'; "
            "assert s.WEBAUTHN_ORIGIN == 'http://localhost:8081'"
        ),
        environment=environment,
    )

    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize(
    ("overrides", "expected_error"),
    [
        ({"WEBAUTHN_RP_ID": ""}, "WEBAUTHN_RP_ID must be a valid domain name"),
        ({"WEBAUTHN_RP_ID": "https://example.test"}, "WEBAUTHN_RP_ID must be a valid domain name"),
        ({"WEBAUTHN_RP_NAME": " "}, "WEBAUTHN_RP_NAME may not be blank"),
        ({"WEBAUTHN_ORIGIN": ""}, "WEBAUTHN_ORIGIN must be a valid origin"),
        (
            {"WEBAUTHN_ORIGIN": "http://app.example.test"},
            "Production WebAuthn origin must use HTTPS",
        ),
        (
            {"WEBAUTHN_ORIGIN": "https://app.example.test/path"},
            "WEBAUTHN_ORIGIN must be a valid origin",
        ),
        (
            {"WEBAUTHN_ORIGIN": "https://unrelated.test"},
            "WEBAUTHN_RP_ID must match the WebAuthn origin domain",
        ),
    ],
)
def test_invalid_production_webauthn_configuration_is_rejected(overrides, expected_error):
    result = _run_settings_command(
        "import config.settings",
        environment=_production_environment(**overrides),
    )

    assert result.returncode != 0
    assert expected_error in result.stderr


def test_http_webauthn_origin_is_limited_to_localhost_development():
    result = _run_settings_command(
        "import config.settings",
        environment={
            **os.environ,
            "DOTICK_ENV": "local",
            "WEBAUTHN_RP_ID": "example.test",
            "WEBAUTHN_RP_NAME": "Dotick Local",
            "WEBAUTHN_ORIGIN": "http://app.example.test",
        },
    )

    assert result.returncode != 0
    assert "HTTP WebAuthn origin is allowed only for localhost development" in result.stderr
