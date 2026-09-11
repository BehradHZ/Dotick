import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
OPENAPI_PATH = REPO_ROOT / "docs" / "design" / "openapi.json"

SYNCABLE_RESOURCES = ("Folder", "List", "Column", "Task")
RESTORABLE_RESOURCES = {
    "Folder": "/api/v1/folders/{folder_id}/restore",
    "List": "/api/v1/lists/{list_id}/restore",
    "Task": "/api/v1/tasks/{task_id}/restore",
}
PUBLIC_OPERATIONS = {
    ("/api/v1/auth/register", "post"),
    ("/api/v1/auth/email/resend", "post"),
    ("/api/v1/auth/email/verify", "post"),
    ("/api/v1/auth/token", "post"),
    ("/api/v1/auth/token/refresh", "post"),
    ("/api/v1/auth/password/reset/request", "post"),
    ("/api/v1/auth/password/reset/confirm", "post"),
    ("/api/v1/auth/google", "post"),
    ("/api/v1/auth/passkeys/authentication/options", "post"),
    ("/api/v1/auth/passkeys/authentication/verify", "post"),
}
HTTP_METHODS = {"get", "post", "put", "patch", "delete"}


def _load_openapi():
    return json.loads(OPENAPI_PATH.read_text(encoding="utf-8"))


def _schema(contract, name):
    return contract["components"]["schemas"][name]


def _request_schema(contract, request_body_name):
    request_body = contract["components"]["requestBodies"][request_body_name]
    ref = request_body["content"]["application/json"]["schema"]["$ref"]
    return _schema(contract, ref.rsplit("/", 1)[-1])


def _parameter_refs(operation):
    return {
        parameter.get("$ref", "").rsplit("/", 1)[-1]
        for parameter in operation.get("parameters", [])
        if isinstance(parameter, dict)
    }


def test_increment_1_persisted_resource_ids_are_stable_uuids():
    contract = _load_openapi()
    schemas = contract["components"]["schemas"]

    for resource in SYNCABLE_RESOURCES:
        identifier = schemas[resource]["properties"]["id"]
        assert identifier == {"type": "string", "format": "uuid"}

    path_parameters = contract["components"]["parameters"]
    for parameter_name in ("FolderId", "ListId", "ColumnId", "TaskId"):
        identifier = path_parameters[parameter_name]["schema"]
        assert identifier == {"type": "string", "format": "uuid"}


def test_task_foundation_has_versioned_idempotent_mutations():
    contract = _load_openapi()
    paths = contract["paths"]

    create_schema = _request_schema(contract, "TaskCreate")
    assert "operation_id" in create_schema["required"]
    assert create_schema["properties"]["operation_id"] == {
        "type": "string",
        "format": "uuid",
    }

    task_schema = _schema(contract, "Task")
    assert "version" in task_schema["required"]
    assert task_schema["properties"]["version"]["minimum"] == 1

    update_schema = _request_schema(contract, "TaskUpdate")
    assert "version" in update_schema["required"]
    assert update_schema["properties"]["version"]["minimum"] == 1

    update_responses = paths["/api/v1/tasks/{task_id}"]["patch"]["responses"]
    assert "409" in update_responses

    delete_operation = paths["/api/v1/tasks/{task_id}"]["delete"]
    assert "IfMatch" in _parameter_refs(delete_operation)
    assert "409" in delete_operation["responses"]

    restore_operation = paths["/api/v1/tasks/{task_id}/restore"]["post"]
    assert restore_operation["requestBody"]["$ref"].endswith("/Version")
    assert "409" in restore_operation["responses"]


def test_recoverable_delete_keeps_identity_and_has_restore_surface():
    contract = _load_openapi()
    schemas = contract["components"]["schemas"]
    paths = contract["paths"]

    for resource, restore_path in RESTORABLE_RESOURCES.items():
        schema = schemas[resource]
        assert "id" in schema["required"]
        assert "is_trashed" in schema["properties"]
        assert "trashed_at" in schema["properties"]
        assert restore_path in paths

    assert "/api/v1/trash/folders" in paths
    assert "/api/v1/trash/lists" in paths
    assert "/api/v1/trash/tasks" in paths


def test_i1_does_not_pretend_optimistic_version_is_branching_history():
    contract = _load_openapi()

    forbidden_path_fragments = ("/history", "/undo", "/changes", "/sync")
    assert not {
        path
        for path in contract["paths"]
        if any(fragment in path for fragment in forbidden_path_fragments)
    }

    forbidden_history_fields = {
        "change_id",
        "parent_change_id",
        "branch_id",
        "field_clock",
        "device_clock",
    }
    for schema in contract["components"]["schemas"].values():
        properties = schema.get("properties", {}) if isinstance(schema, dict) else {}
        assert not (set(properties) & forbidden_history_fields)


def test_revocable_session_surface_is_explicit_and_authenticated():
    contract = _load_openapi()
    paths = contract["paths"]
    bearer = [{"bearerAuth": []}]

    assert paths["/api/v1/auth/logout"]["post"]["security"] == bearer
    assert paths["/api/v1/auth/sessions"]["get"]["security"] == bearer
    assert paths["/api/v1/auth/sessions"]["delete"]["security"] == bearer
    assert paths["/api/v1/auth/sessions/{session_id}"]["delete"]["security"] == bearer
    assert "401" in paths["/api/v1/auth/token/refresh"]["post"]["responses"]


@pytest.mark.xfail(
    strict=True,
    reason=(
        "I6 review blocker: OpenAPI has no global bearer security, so many private I1 "
        "operations are currently described as unauthenticated."
    ),
)
def test_private_i1_operations_inherit_bearer_authentication():
    contract = _load_openapi()
    global_security = contract.get("security")
    assert global_security == [{"bearerAuth": []}]

    for path, path_item in contract["paths"].items():
        for method, operation in path_item.items():
            if method not in HTTP_METHODS:
                continue
            if (path, method) in PUBLIC_OPERATIONS:
                assert operation.get("security") == []
            else:
                assert operation.get("security", global_security) == [{"bearerAuth": []}]


@pytest.mark.xfail(
    strict=True,
    reason=(
        "I6 review blocker: Folder/List/Column contracts do not yet carry the optimistic "
        "version and idempotent-create foundations required before those APIs are implemented."
    ),
)
def test_organization_resources_are_versioned_and_idempotent_before_implementation():
    contract = _load_openapi()
    schemas = contract["components"]["schemas"]
    paths = contract["paths"]

    for resource in ("Folder", "List", "Column"):
        assert "version" in schemas[resource]["required"]
        assert schemas[resource]["properties"]["version"]["minimum"] == 1

    title_create = schemas["TitleRequest"]
    assert "operation_id" in title_create["required"]
    assert title_create["properties"]["operation_id"]["format"] == "uuid"

    list_create = schemas["ListCreateRequest"]
    assert "operation_id" in list_create["required"]
    assert list_create["properties"]["operation_id"]["format"] == "uuid"

    container_update = schemas["ContainerUpdateRequest"]
    assert "version" in container_update["required"]

    list_update = schemas["ListUpdateRequest"]
    assert "version" in list_update["required"]

    organization_paths = (
        "/api/v1/folders/{folder_id}",
        "/api/v1/lists/{list_id}",
        "/api/v1/columns/{column_id}",
    )
    for path in organization_paths:
        assert "IfMatch" in _parameter_refs(paths[path]["delete"])
        assert "409" in paths[path]["delete"]["responses"]

    for restore_path in (
        "/api/v1/folders/{folder_id}/restore",
        "/api/v1/lists/{list_id}/restore",
    ):
        operation = paths[restore_path]["post"]
        assert operation["requestBody"]["$ref"].endswith("/Version")
        assert "409" in operation["responses"]
