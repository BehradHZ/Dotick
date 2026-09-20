import hashlib
import json
import re
from pathlib import Path

from django.urls import URLPattern, URLResolver, get_resolver
from openapi_spec_validator import validate

REPO_ROOT = Path(__file__).resolve().parents[3]
OPENAPI_PATH = REPO_ROOT / "docs" / "design" / "openapi.json"
HTTP_METHODS = {"get", "post", "put", "patch", "delete", "options", "head", "trace"}
REVIEWED_CONTRACT_SHA256 = "e041ff0c2ec707ab0acee5f243ee59a855e354acb3c114f998b0e8d6aa297c9c"
PUBLISHED_INCREMENT_2_PATHS = {
    "/api/v1/account",
    "/api/v1/account/bootstrap",
    "/api/v1/account/contacts",
    "/api/v1/account/contacts/{contact_id}",
    "/api/v1/account/contacts/verify",
    "/api/v1/auth/email/resend",
    "/api/v1/auth/email/verify",
    "/api/v1/auth/google",
    "/api/v1/auth/google/link",
    "/api/v1/auth/logout",
    "/api/v1/auth/passkeys",
    "/api/v1/auth/passkeys/{passkey_id}",
    "/api/v1/auth/passkeys/authentication/options",
    "/api/v1/auth/passkeys/authentication/verify",
    "/api/v1/auth/passkeys/registration/options",
    "/api/v1/auth/passkeys/registration/verify",
    "/api/v1/auth/password",
    "/api/v1/auth/password/reset/confirm",
    "/api/v1/auth/password/reset/request",
    "/api/v1/auth/register",
    "/api/v1/auth/sessions",
    "/api/v1/auth/sessions/{session_id}",
    "/api/v1/auth/token",
    "/api/v1/auth/token/refresh",
    "/api/v1/columns/{column_id}",
    "/api/v1/folders",
    "/api/v1/folders/{folder_id}",
    "/api/v1/folders/{folder_id}/restore",
    "/api/v1/lists",
    "/api/v1/lists/{list_id}",
    "/api/v1/lists/{list_id}/columns",
    "/api/v1/lists/{list_id}/restore",
    "/api/v1/tasks",
    "/api/v1/tasks/{task_id}",
    "/api/v1/tasks/{task_id}/restore",
    "/api/v1/trash/folders",
    "/api/v1/trash/lists",
    "/api/v1/trash/tasks",
}
EDGE_RATE_LIMITED_OPERATIONS = {
    ("/api/v1/account/contacts", "post"),
    ("/api/v1/account/contacts/verify", "post"),
    ("/api/v1/auth/email/resend", "post"),
    ("/api/v1/auth/email/verify", "post"),
    ("/api/v1/auth/passkeys/authentication/options", "post"),
    ("/api/v1/auth/passkeys/authentication/verify", "post"),
    ("/api/v1/auth/password/reset/confirm", "post"),
    ("/api/v1/auth/password/reset/request", "post"),
    ("/api/v1/auth/register", "post"),
}


def _load_contract():
    return json.loads(OPENAPI_PATH.read_text(encoding="utf-8"))


def _operations(contract):
    for path, path_item in contract["paths"].items():
        for method, operation in path_item.items():
            if method in HTTP_METHODS:
                yield path, method, operation


def _django_routes(patterns, prefix=""):
    for pattern in patterns:
        route = prefix + str(pattern.pattern)
        if isinstance(pattern, URLResolver):
            yield from _django_routes(pattern.url_patterns, route)
        elif isinstance(pattern, URLPattern):
            yield route


def test_published_contract_changes_require_a_reviewed_test_update():
    contract = _load_contract()
    canonical = json.dumps(
        contract,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode()

    assert hashlib.sha256(canonical).hexdigest() == REVIEWED_CONTRACT_SHA256


def test_openapi_document_is_valid_openapi_31():
    validate(_load_contract())


def test_openapi_paths_exactly_match_the_published_increment_2_routes():
    contract_paths = set(_load_contract()["paths"])
    routed_paths = {
        "/" + re.sub(r"<[^:>]+:([^>]+)>", r"{\1}", route)
        for route in _django_routes(get_resolver().url_patterns)
        if route.startswith("api/v1/") and not route.startswith("api/v1/foundation/")
    }

    assert contract_paths == PUBLISHED_INCREMENT_2_PATHS == routed_paths


def test_openapi_is_the_executable_increment_2_contract():
    contract = _load_contract()

    assert contract["openapi"] == "3.1.0"
    assert contract["paths"]
    assert all(path.startswith("/api/v1/") for path in contract["paths"])

    operations = list(_operations(contract))
    assert operations
    assert all(operation.get("operationId") for _, _, operation in operations)
    assert all(operation.get("responses") for _, _, operation in operations)

    request_bodies = contract["components"]["requestBodies"].values()
    assert all(set(body["content"]) == {"application/json"} for body in request_bodies)

    error = contract["components"]["schemas"]["Error"]
    assert error["required"] == ["error"]
    assert set(error["properties"]["error"]["required"]) == {"code", "details"}


def test_identity_ceremonies_declare_their_edge_rate_limit_policy():
    contract = _load_contract()

    for path, method in EDGE_RATE_LIMITED_OPERATIONS:
        operation = contract["paths"][path][method]
        assert operation["x-edge-rate-limit-policy"] == "identity-ceremony"
