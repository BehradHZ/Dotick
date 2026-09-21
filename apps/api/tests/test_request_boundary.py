import json

from config.middleware import JsonRequestBoundaryMiddleware
from django.conf import settings
from django.http import JsonResponse
from django.test import Client, RequestFactory

TOKEN_URL = "/api/v1/auth/token"


def test_product_api_rejects_oversized_json_before_view_dispatch():
    response = Client().generic(
        "POST",
        TOKEN_URL,
        data=b"{" + (b" " * settings.API_MAX_JSON_BODY_BYTES),
        content_type="application/json",
    )

    assert response.status_code == 413
    assert json.loads(response.content) == {
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
    assert json.loads(response.content) == {
        "error": {
            "code": "unsupported_media_type",
            "details": {"detail": "Use application/json for API request bodies."},
        }
    }


def test_non_api_operational_endpoint_is_outside_json_boundary():
    response = Client().post("/health", data="plain text", content_type="text/plain")

    assert response.status_code == 200


def test_product_api_rejects_malformed_json_with_stable_envelope():
    response = Client().generic(
        "POST",
        TOKEN_URL,
        data=b'{"email":',
        content_type="application/json",
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "parse_error"


def test_product_api_rejects_malformed_content_length():
    request = RequestFactory().post(
        TOKEN_URL,
        data=b"{}",
        content_type="application/json",
    )
    request.META["CONTENT_LENGTH"] = "not-a-number"
    middleware = JsonRequestBoundaryMiddleware(lambda request: JsonResponse({"ok": True}))

    response = middleware(request)

    assert response.status_code == 400
    assert json.loads(response.content) == {
        "error": {
            "code": "bad_request",
            "details": {"detail": "Malformed Content-Length header."},
        }
    }


def test_product_api_checks_actual_body_size_when_declared_length_is_false():
    request = RequestFactory().post(
        TOKEN_URL,
        data=b"{" + (b" " * settings.API_MAX_JSON_BODY_BYTES),
        content_type="application/json",
    )
    request.META["CONTENT_LENGTH"] = "1"
    middleware = JsonRequestBoundaryMiddleware(lambda request: JsonResponse({"ok": True}))

    response = middleware(request)

    assert response.status_code == 413
    assert json.loads(response.content)["error"]["code"] == "payload_too_large"
