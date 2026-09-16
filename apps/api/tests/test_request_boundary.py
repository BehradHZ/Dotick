from django.conf import settings
from django.test import Client

TOKEN_URL = "/api/v1/auth/token"


def test_product_api_rejects_oversized_json_before_view_dispatch():
    response = Client().generic(
        "POST",
        TOKEN_URL,
        data=b"{" + (b" " * settings.API_MAX_JSON_BODY_BYTES),
        content_type="application/json",
    )

    assert response.status_code == 413
    assert response.json() == {
        "error": {
            "code": "payload_too_large",
            "details": {"detail": "Request body exceeds the 16 KiB limit."},
        }
    }


def test_product_api_rejects_non_json_request_body():
    response = Client().generic(
        "POST",
        TOKEN_URL,
        data=b"email=user@example.test",
        content_type="application/x-www-form-urlencoded",
    )

    assert response.status_code == 415
    assert response.json() == {
        "error": {
            "code": "unsupported_media_type",
            "details": {"detail": "Use application/json for API request bodies."},
        }
    }


def test_non_api_operational_endpoint_is_outside_json_boundary():
    response = Client().post("/health", data="plain text", content_type="text/plain")

    assert response.status_code == 200
