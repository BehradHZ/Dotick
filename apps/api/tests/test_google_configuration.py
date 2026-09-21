import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

from rest_framework.test import APIClient

REPO_ROOT = Path(__file__).resolve().parents[3]
ENV_EXAMPLE = REPO_ROOT / ".env.example"


def test_google_oauth_client_id_is_environment_driven():
    environment = {
        **os.environ,
        "GOOGLE_OAUTH_CLIENT_ID": " google-client-id.apps.googleusercontent.com ",
    }
    result = subprocess.run(
        [
            sys.executable,
            "apps/api/manage.py",
            "shell",
            "-c",
            (
                "import config.settings as s; "
                "assert s.GOOGLE_OAUTH_CLIENT_ID == "
                "'google-client-id.apps.googleusercontent.com'"
            ),
        ],
        cwd=REPO_ROOT,
        env=environment,
        capture_output=True,
        text=True,
        timeout=10,
    )

    assert result.returncode == 0, result.stderr


def test_example_declares_backend_and_public_google_client_ids_without_a_public_secret():
    configured_names = {
        line.split("=", 1)[0]
        for line in ENV_EXAMPLE.read_text(encoding="utf-8").splitlines()
        if line and not line.startswith("#") and "=" in line
    }

    assert "GOOGLE_OAUTH_CLIENT_ID" in configured_names
    assert "EXPO_PUBLIC_GOOGLE_CLIENT_ID" in configured_names
    assert not {
        name for name in configured_names if name.startswith("EXPO_PUBLIC_") and "SECRET" in name
    }


def test_missing_google_client_id_returns_clean_unavailable_response_without_contacting_google(
    settings,
):
    settings.GOOGLE_OAUTH_CLIENT_ID = ""

    with patch("dotick.identity.google_identity.id_token.verify_oauth2_token") as verifier:
        response = APIClient().post(
            "/api/v1/auth/google",
            {"credential": "untrusted-google-id-credential"},
            format="json",
        )

    verifier.assert_not_called()
    assert response.status_code == 503
    assert response.json() == {
        "error": {
            "code": "provider_unavailable",
            "details": {"detail": "External authentication provider is unavailable."},
        }
    }
