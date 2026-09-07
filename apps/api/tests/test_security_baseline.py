import json
import logging
import os
import subprocess
import sys
from pathlib import Path

import pytest
from config.observability import JsonFormatter
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction

TEST_JWT_SIGNING_KEY = "test-only-jwt-key-which-is-longer-than-fifty-characters-123456"


@pytest.mark.django_db
def test_password_is_argon2_and_email_is_unique_ignoring_case(signed_in):
    _, user = signed_in()
    assert user.password.startswith("argon2$")
    assert user.check_password("Only-for-automated-tests-8!")
    with pytest.raises(IntegrityError), transaction.atomic():
        get_user_model().objects.create(email=user.email.upper(), password="!")


def test_log_format_drops_arbitrary_message_exception_and_sensitive_extras():
    record = logging.LogRecord(
        "test", logging.ERROR, "", 1, "password=should-never-appear", (), None
    )
    record.authorization = "Bearer secret"
    record.event = "http_request"
    output = JsonFormatter().format(record)
    assert set(json.loads(output)) == {"timestamp", "level", "service", "event"}
    assert "secret" not in output
    assert "password" not in output


@pytest.mark.django_db
def test_oversized_body_is_rejected_before_persistence(signed_in):
    client, _ = signed_in()
    response = client.post("/api/v1/foundation/checkpoints", {"text": "x" * 20000}, format="json")
    assert response.status_code == 413
    assert client.get("/api/v1/foundation/checkpoints").json() == {"results": []}


def test_health_response_has_correlation_and_no_cache(client):
    response = client.get("/health")
    assert response["X-Request-ID"]
    assert response["Cache-Control"] == "no-store"


def test_untrusted_origin_is_not_granted_cross_origin_access(client):
    response = client.options(
        "/health", HTTP_ORIGIN="https://untrusted.example", HTTP_ACCESS_CONTROL_REQUEST_METHOD="GET"
    )
    assert "Access-Control-Allow-Origin" not in response


def test_production_process_refuses_to_enable_the_developer_workbench():
    root = Path(__file__).resolve().parents[3]
    result = subprocess.run(
        [sys.executable, "apps/api/manage.py", "check"],
        cwd=root,
        env={
            **os.environ,
            "DOTICK_ENV": "production",
            "DOTICK_FOUNDATION_ENABLED": "1",
            "DJANGO_JWT_SIGNING_KEY": TEST_JWT_SIGNING_KEY,
        },
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode != 0
    assert "foundation workbench is only available in local/test" in result.stderr


def test_production_requires_a_separate_jwt_signing_key():
    root = Path(__file__).resolve().parents[3]
    result = subprocess.run(
        [sys.executable, "apps/api/manage.py", "check"],
        cwd=root,
        env={
            **os.environ,
            "DOTICK_ENV": "production",
            "DOTICK_FOUNDATION_ENABLED": "0",
            "DJANGO_JWT_SIGNING_KEY": "",
        },
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode != 0
    assert "DJANGO_JWT_SIGNING_KEY must contain at least 50 characters" in result.stderr
