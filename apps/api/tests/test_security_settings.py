import os
import subprocess
import sys
from pathlib import Path

from django.conf import settings

REPO_ROOT = Path(__file__).resolve().parents[3]
TEST_JWT_SIGNING_KEY = "test-only-jwt-key-which-is-longer-than-fifty-characters-123456"


def test_hosts_and_trusted_origins_are_explicit_allowlists():
    assert settings.ALLOWED_HOSTS
    assert "*" not in settings.ALLOWED_HOSTS
    assert settings.CSRF_TRUSTED_ORIGINS
    assert all(
        origin.startswith(("http://", "https://")) for origin in settings.CSRF_TRUSTED_ORIGINS
    )


def test_production_refuses_missing_host_and_trusted_origin_allowlists():
    result = subprocess.run(
        [sys.executable, "apps/api/manage.py", "check"],
        cwd=REPO_ROOT,
        env={
            **os.environ,
            "DOTICK_ENV": "production",
            "DJANGO_ALLOWED_HOSTS": "",
            "DJANGO_CSRF_TRUSTED_ORIGINS": "",
            "DJANGO_JWT_SIGNING_KEY": TEST_JWT_SIGNING_KEY,
        },
        capture_output=True,
        text=True,
        timeout=10,
    )

    assert result.returncode != 0
    assert "DJANGO_ALLOWED_HOSTS is required outside local/test" in result.stderr


def test_production_like_configuration_enforces_https():
    result = subprocess.run(
        [
            sys.executable,
            "apps/api/manage.py",
            "shell",
            "-c",
            "import config.settings as s; "
            "assert s.SECURE_SSL_REDIRECT; assert s.SESSION_COOKIE_SECURE; "
            "assert s.CSRF_COOKIE_SECURE; assert s.SECURE_HSTS_SECONDS == 31536000; "
            "assert s.SECURE_PROXY_SSL_HEADER == ('HTTP_X_FORWARDED_PROTO', 'https')",
        ],
        cwd=REPO_ROOT,
        env={
            **os.environ,
            "DOTICK_ENV": "production",
            "DJANGO_ALLOWED_HOSTS": "api.example.test",
            "DJANGO_CORS_ORIGINS": "https://app.example.test",
            "DJANGO_CSRF_TRUSTED_ORIGINS": "https://app.example.test",
            "DJANGO_JWT_SIGNING_KEY": TEST_JWT_SIGNING_KEY,
            "WEBAUTHN_ORIGIN": "https://app.example.test",
        },
        capture_output=True,
        text=True,
        timeout=10,
    )

    assert result.returncode == 0, result.stderr
