import json
from pathlib import Path

from django.conf import settings

REPO_ROOT = Path(__file__).resolve().parents[3]
OPENAPI_PATH = REPO_ROOT / "docs" / "design" / "openapi.json"
TIME_VECTORS_PATH = REPO_ROOT / "docs" / "design" / "time-vectors.json"
CI_PATH = REPO_ROOT / ".github" / "workflows" / "ci.yml"

HTTP_METHODS = {"get", "post", "put", "patch", "delete"}
WRITE_REQUEST_SCHEMAS = {
    "AccountUpdateRequest",
    "BootstrapRequest",
    "ContactRequest",
    "ContactVerifyRequest",
    "TitleRequest",
    "ContainerUpdateRequest",
    "ListCreateRequest",
    "ListUpdateRequest",
    "TaskCreateRequest",
    "TaskUpdateRequest",
}
SERVER_AUTHORITY_FIELDS = {
    "id",
    "owner_user_id",
    "created_by_user_id",
    "source",
    "created_at",
    "updated_at",
    "is_trashed",
    "trashed_at",
}
REVIEW_REQUIRED_MIGRATION_TOKENS = {
    "migrations.DeleteModel(",
    "migrations.RemoveField(",
    "migrations.RenameField(",
    "migrations.RenameModel(",
    "migrations.RunSQL(",
}
MIGRATION_REVIEW_MARKER = "MIGRATION_SAFETY_REVIEWED = True"


def _load_openapi():
    return json.loads(OPENAPI_PATH.read_text(encoding="utf-8"))


def _resolve_local_ref(contract, ref):
    assert ref.startswith("#/"), f"Only local OpenAPI refs are allowed in I1: {ref}"
    node = contract
    for part in ref[2:].split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        node = node[part]
    return node


def _walk_refs(node):
    if isinstance(node, dict):
        ref = node.get("$ref")
        if isinstance(ref, str):
            yield ref
        for value in node.values():
            yield from _walk_refs(value)
    elif isinstance(node, list):
        for value in node:
            yield from _walk_refs(value)


def test_multi_auth_contract_converges_on_one_internal_identity():
    contract = _load_openapi()
    schemas = contract["components"]["schemas"]
    responses = contract["components"]["responses"]
    paths = contract["paths"]

    password_user_ref = schemas["TokenPair"]["properties"]["user"]["$ref"]
    federated_user_ref = schemas["FederatedTokenPair"]["properties"]["user"]["$ref"]
    assert password_user_ref == federated_user_ref == "#/components/schemas/UserIdentity"

    assert (
        paths["/api/v1/auth/google"]["post"]["responses"]["200"]["$ref"]
        == "#/components/responses/FederatedTokenPair"
    )
    assert (
        paths["/api/v1/auth/passkeys/authentication/verify"]["post"]["responses"]["200"]["$ref"]
        == "#/components/responses/FederatedTokenPair"
    )
    assert (
        responses["FederatedTokenPair"]["content"]["application/json"]["schema"]["$ref"]
        == "#/components/schemas/FederatedTokenPair"
    )

    provider_specific_user_schemas = {
        name
        for name in schemas
        if name.lower() in {"googleuser", "passkeyuser", "passworduser", "oauthuser"}
    }
    assert not provider_specific_user_schemas


def test_client_write_contract_cannot_assign_server_authority():
    schemas = _load_openapi()["components"]["schemas"]

    for schema_name in WRITE_REQUEST_SCHEMAS:
        schema = schemas[schema_name]
        assert schema.get("additionalProperties") is False, (
            f"{schema_name} must reject unknown fields to prevent authority smuggling."
        )
        properties = set(schema.get("properties", {}))
        leaked_authority = properties & SERVER_AUTHORITY_FIELDS
        assert not leaked_authority, (
            f"{schema_name} exposes server-owned fields to the client: {leaked_authority}"
        )


def test_openapi_local_refs_and_operation_ids_are_drift_safe():
    contract = _load_openapi()

    for ref in _walk_refs(contract):
        _resolve_local_ref(contract, ref)

    operation_ids = []
    for path_item in contract["paths"].values():
        for method, operation in path_item.items():
            if method not in HTTP_METHODS:
                continue
            operation_id = operation.get("operationId")
            assert operation_id, f"Every I1 operation needs a stable operationId: {operation}"
            operation_ids.append(operation_id)

    assert len(operation_ids) == len(set(operation_ids)), "OpenAPI operationIds must be unique."


def test_timezone_baseline_is_utc_with_executable_iana_dst_vectors():
    assert settings.USE_TZ is True
    assert settings.TIME_ZONE == "UTC"

    vectors = json.loads(TIME_VECTORS_PATH.read_text(encoding="utf-8"))
    zones = {vector["zone"] for vector in vectors["wall_times"]}
    zones.update(vector["zone"] for vector in vectors["all_day"])

    assert "Europe/Berlin" in zones
    assert "America/New_York" in zones
    assert "Asia/Tehran" in zones
    assert {23, 25} <= {
        vector["hours"] for vector in vectors["all_day"] if "hours" in vector
    }
    assert any(vector.get("error") == "ambiguous" for vector in vectors["wall_times"])
    assert any(vector.get("error") == "nonexistent" for vector in vectors["wall_times"])


def test_ci_keeps_postgresql_migration_drift_and_clean_database_gates():
    workflow = CI_PATH.read_text(encoding="utf-8")

    required_controls = (
        "makemigrations --check --dry-run",
        "migrate --noinput",
        "showmigrations",
        "scripts/check_migrations.py",
        "scripts/verify_clean_database.py",
    )
    for control in required_controls:
        assert control in workflow


def test_destructive_or_opaque_migrations_require_explicit_safety_review():
    migration_files = sorted(
        REPO_ROOT.glob("apps/api/dotick/*/migrations/[0-9][0-9][0-9][0-9]_*.py")
    )
    assert migration_files, "At least one executable migration must exist."

    violations = []
    for migration_file in migration_files:
        content = migration_file.read_text(encoding="utf-8")
        risky_tokens = {
            token for token in REVIEW_REQUIRED_MIGRATION_TOKENS if token in content
        }
        if risky_tokens and MIGRATION_REVIEW_MARKER not in content:
            violations.append((migration_file.relative_to(REPO_ROOT), sorted(risky_tokens)))

    assert not violations, (
        "Destructive/opaque migrations require an explicit safety review marker: "
        f"{violations}"
    )
