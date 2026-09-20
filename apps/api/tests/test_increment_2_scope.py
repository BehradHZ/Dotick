import json
from pathlib import Path

from django.apps import apps

REPO_ROOT = Path(__file__).resolve().parents[3]
OPENAPI_PATH = REPO_ROOT / "docs" / "design" / "openapi.json"

I2_API_TAGS = {
    "Identity",
    "Account",
    "Organization",
    "Tasks",
    "Events",
    "Descriptions",
    "Comments",
    "Tags",
    "Audit",
}
I2_TASK_STATUSES = {"todo", "overdue", "missed", "done", "wont_do", "skipped"}

FORBIDDEN_PATH_FRAGMENTS = {
    "/goals",
    "/groups",
    "/history",
    "/notifications",
    "/recurrence",
    "/reminders",
    "/rings",
    "/routines",
    "/shares",
    "/sync",
}

FORBIDDEN_SCHEMA_PREFIXES = (
    "DailyRing",
    "Goal",
    "Group",
    "Notification",
    "Recurrence",
    "Reminder",
    "Routine",
    "Share",
    "Sync",
)

FORBIDDEN_MODEL_NAMES = {
    "AccessGrant",
    "ChangeRecord",
    "DailyAction",
    "DailyRing",
    "Goal",
    "Group",
    "GroupMembership",
    "Notification",
    "RecurrenceRule",
    "Reminder",
    "ResourceShare",
    "RingGroup",
    "Routine",
    "RoutineCompletion",
    "SyncOperation",
    "SyncState",
}

FORBIDDEN_FIELD_NAMES = {
    "day_boundary_offset_minutes",
    "goal_id",
    "group_id",
    "recurrence_rule",
    "reminders",
}


def _property_names(node):
    if isinstance(node, dict):
        properties = node.get("properties")
        if isinstance(properties, dict):
            yield from properties
        for value in node.values():
            yield from _property_names(value)
    elif isinstance(node, list):
        for value in node:
            yield from _property_names(value)


def _load_openapi():
    return json.loads(OPENAPI_PATH.read_text(encoding="utf-8"))


def test_increment_2_openapi_has_no_later_increment_surface():
    contract = _load_openapi()

    declared_tags = {tag["name"] for tag in contract.get("tags", [])}
    unexpected_tags = declared_tags - I2_API_TAGS
    assert not unexpected_tags, f"Increment 3+ API tags leaked into I2: {unexpected_tags}"

    leaked_paths = {
        path
        for path in contract.get("paths", {})
        if any(fragment in path for fragment in FORBIDDEN_PATH_FRAGMENTS)
    }
    assert not leaked_paths, f"Increment 3+ endpoints leaked into I2: {leaked_paths}"

    schemas = contract.get("components", {}).get("schemas", {})
    leaked_schemas = {name for name in schemas if name.startswith(FORBIDDEN_SCHEMA_PREFIXES)}
    assert not leaked_schemas, f"Increment 3+ schemas leaked into I2: {leaked_schemas}"

    leaked_properties = set(_property_names(schemas)) & FORBIDDEN_FIELD_NAMES
    assert not leaked_properties, (
        f"Increment 3+ fields leaked into the I2 API contract: {leaked_properties}"
    )


def test_increment_2_task_contract_uses_full_task_states():
    schemas = _load_openapi().get("components", {}).get("schemas", {})
    task_statuses = set(schemas["Task"]["properties"]["status"]["enum"])
    user_selectable_statuses = set(schemas["TaskUpdateRequest"]["properties"]["status"]["enum"])

    assert task_statuses == I2_TASK_STATUSES
    assert user_selectable_statuses == {"todo", "done", "wont_do"}
    assert {"overdue", "missed", "skipped"}.isdisjoint(user_selectable_statuses)


def test_increment_2_django_schema_has_no_later_increment_models_or_fields():
    dotick_models = [model for model in apps.get_models() if model.__module__.startswith("dotick.")]

    leaked_models = {
        model.__name__ for model in dotick_models if model.__name__ in FORBIDDEN_MODEL_NAMES
    }
    assert not leaked_models, f"Increment 3+ models leaked into I2: {leaked_models}"

    leaked_fields = {}
    for model in dotick_models:
        field_names = {field.name for field in model._meta.get_fields()}
        forbidden = field_names & FORBIDDEN_FIELD_NAMES
        if forbidden:
            leaked_fields[model.__name__] = sorted(forbidden)

    assert not leaked_fields, f"Increment 3+ fields leaked into I2 schema: {leaked_fields}"
