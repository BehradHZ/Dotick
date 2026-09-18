from collections.abc import Mapping
from typing import Any

from django.db import transaction
from django.db.models import F
from django.http import Http404
from django.utils import timezone
from rest_framework.exceptions import APIException, ValidationError

from dotick.organization.models import Column, Folder, List

VERSION_CONFLICT_CODE = "version_conflict"
EXPECTED_VERSION_ERROR = "Use the current positive integer version."


class OrganizationVersionConflict(APIException):
    status_code = 409
    default_detail = "The organization resource changed after the supplied version."
    default_code = VERSION_CONFLICT_CODE

    def __init__(self, row):
        self.current = {
            "id": str(row.pk),
            "version": row.version,
        }
        super().__init__(self.default_detail, code=self.default_code)


def validate_expected_version(value):
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValidationError(EXPECTED_VERSION_ERROR, code="invalid_version")
    return value


def _require_atomic_version_context():
    if not transaction.get_connection().in_atomic_block:
        raise RuntimeError("Organization version comparison requires an active transaction.")


def _owned_queryset(*, model, actor_id):
    if model is Folder:
        return Folder.objects.filter(owner_id=actor_id)
    if model is List:
        return List.objects.filter(owner_id=actor_id)
    if model is Column:
        return Column.objects.filter(list__owner_id=actor_id)
    raise TypeError("Optimistic organization concurrency supports Folder, List, and Column only.")


def lock_owned_versioned_resource(
    *,
    model,
    actor_id,
    resource_id,
    expected_version,
    scope_filters: Mapping[str, Any] | None = None,
):
    _require_atomic_version_context()
    expected_version = validate_expected_version(expected_version)
    rows = _owned_queryset(model=model, actor_id=actor_id)
    if scope_filters:
        rows = rows.filter(**scope_filters)
    try:
        row = rows.select_for_update().get(pk=resource_id)
    except model.DoesNotExist as error:
        raise Http404 from error
    if row.version != expected_version:
        raise OrganizationVersionConflict(row)
    return row


def increment_locked_version(
    *,
    row,
    actor_id,
    expected_version,
    updates: Mapping[str, Any] | None = None,
):
    _require_atomic_version_context()
    expected_version = validate_expected_version(expected_version)
    changes = dict(updates or {})
    if "version" in changes:
        raise ValueError("version is server-owned and cannot be supplied as mutation state.")
    if row.version != expected_version:
        raise OrganizationVersionConflict(row)

    changes["version"] = F("version") + 1
    changes["updated_at"] = timezone.now()
    rows = _owned_queryset(model=type(row), actor_id=actor_id).filter(
        pk=row.pk,
        version=expected_version,
    )
    if rows.update(**changes) != 1:
        row.refresh_from_db(fields=["version"])
        raise OrganizationVersionConflict(row)

    row.refresh_from_db()
    return row
