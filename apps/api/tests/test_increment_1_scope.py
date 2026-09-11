import json
from pathlib import Path

from django.apps import apps

REPO_ROOT = Path(__file__).resolve().parents[3]
OPENAPI_PATH = REPO_ROOT / "docs" / "design" / "openapi.json"

I1_API_TAGS = {"Identity", "Account", "Organization", "Tasks"}
I1_TASK_STATUSES = {"todo", "done", "wont_do"}

FORBIDDEN_PATH_FRAGMENTS = {
    "/audit",
    "/comments",
    "/dependencies",
    "/events",
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
    "/tags",
}

FORBIDDEN_SCHEMA_PREFIXES = (
    "Audit",
    "Comment",
    "ContentBlock",
    "DailyRing",
    "Event",
    "Goal",
    "Group",
    "Notification",
    "Recurrence",
    "Reminder",
    "Routine",
    "Share",
    "Sync",
    "Tag",
)

FORBIDDEN_MODEL_NAMES = {
    "AccessGrant",
    "AuditLog",
    "ChangeRecord",
    "Comment",
    "ContentBlock",
    "DailyAction",
    "DailyRing",
    "Event",
    "Goal",
    "Group",
    "GroupMembership",
    "ItemDependency",
    "ItemRelation",
    "Notification",
    "RecurrenceRule",
    "Reminder",
    "ResourceShare",
    "RingGroup",
    "Routine",
    "RoutineCompletion",
    "SyncOperation",
    "SyncState",
    "Tag",
}

FORBIDDEN_FIELD_NAMES = {
    "all_day_date",
    "blocked_by",
    "blocked_by_ids",
    "comments",
    "content_blocks",
    "day_boundary_offset_minutes",
    "deadline_at",
    "description",
    "description_id",
    "due_at",
    "end_at",
    "grace_period_days",
    "goal_id",
    "group_id",
    "location",
    "parent_item_id",
    "priority",
    "recurrence_rule",
    "reminders",
    "start_at",
    "tags",
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


def test_increment_1_openapi_has_no_later_increment_surface():
    contract = _load_openapi()

    declared_tags = {tag["name"] for tag in contract.get("tags", [])}
    unexpected_tags = declared_tags - I1_API_TAGS
    assert not unexpected_tags, f"Increment 2+ API tags leaked into I1: {unexpected_tags}"

    leaked_paths = {
        path
        for path in contract.get("paths", {})
        if any(fragment in path for fragment in FORBIDDEN_PATH_FRAGMENTS)
    }
    assert not leaked_paths, f"Increment 2+ endpoints leaked into I1: {leaked_paths}"

    schemas = contract.get("components", {}).get("schemas", {})
    leaked_schemas = {
        name for name in schemas if name.startswith(FORBIDDEN_SCHEMA_PREFIXES)
    }
    assert not leaked_schemas, f"Increment 2+ schemas leaked into I1: {leaked_schemas}"

    leaked_properties = set(_property_names(schemas)) & FORBIDDEN_FIELD_NAMES
    assert not leaked_properties, (
        f"Increment 2+ fields leaked into the I1 API contract: {leaked_properties}"
    )


def test_increment_1_task_contract_uses_only_basic_task_states():
    schemas = _load_openapi().get("components", {}).get("schemas", {})
    task_status_enums = []

    for name, schema in schemas.items():
        if "Task" not in name or not isinstance(schema, dict):
            continue
        status_schema = schema.get("properties", {}).get("status")
        if isinstance(status_schema, dict) and "enum" in status_schema:
            task_status_enums.append(set(status_schema["enum"]))

    assert task_status_enums, "The I1 OpenAPI contract must expose a basic Task status enum."
    assert all(statuses == I1_TASK_STATUSES for statuses in task_status_enums), (
        "Increment 1 Task status must remain exactly Todo/Done/Won't_Do."
    )


def test_increment_1_django_schema_has_no_later_increment_models_or_fields():
    dotick_models = [
        model for model in apps.get_models() if model.__module__.startswith("dotick.")
    ]

    leaked_models = {
        model.__name__ for model in dotick_models if model.__name__ in FORBIDDEN_MODEL_NAMES
    }
    assert not leaked_models, f"Increment 2+ models leaked into I1: {leaked_models}"

    leaked_fields = {}
    for model in dotick_models:
        field_names = {field.name for field in model._meta.get_fields()}
        forbidden = field_names & FORBIDDEN_FIELD_NAMES
        if forbidden:
            leaked_fields[model.__name__] = sorted(forbidden)

    assert not leaked_fields, f"Increment 2+ fields leaked into I1 schema: {leaked_fields}"
