from django.conf import settings
from rest_framework.test import APIClient

TASK_URL = "/api/v1/tasks/00000000-0000-0000-0000-000000000001"
TRUSTED_ORIGIN = "http://localhost:8081"
UNTRUSTED_ORIGIN = "https://untrusted.example"


def _preflight(origin):
    return APIClient().options(
        TASK_URL,
        HTTP_ORIGIN=origin,
        HTTP_ACCESS_CONTROL_REQUEST_METHOD="DELETE",
        HTTP_ACCESS_CONTROL_REQUEST_HEADERS="authorization,content-type,if-match",
    )


def test_trusted_origin_preflight_allows_task_if_match_without_credentials():
    response = _preflight(TRUSTED_ORIGIN)

    assert response.status_code == 200
    assert response["Access-Control-Allow-Origin"] == TRUSTED_ORIGIN
    allowed_headers = {
        header.strip().lower() for header in response["Access-Control-Allow-Headers"].split(",")
    }
    assert {"authorization", "content-type", "if-match"} <= allowed_headers
    assert "Access-Control-Allow-Credentials" not in response


def test_untrusted_origin_is_not_granted_cross_origin_access():
    response = _preflight(UNTRUSTED_ORIGIN)

    assert response.status_code == 200
    assert "Access-Control-Allow-Origin" not in response


def test_cors_configuration_is_an_explicit_origin_allowlist():
    assert settings.CORS_ALLOWED_ORIGINS
    assert "*" not in settings.CORS_ALLOWED_ORIGINS
    assert settings.CORS_ALLOW_ALL_ORIGINS is False
