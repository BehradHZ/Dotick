import hashlib
import json

from django.db import IntegrityError, transaction
from django.http import Http404
from rest_framework.exceptions import APIException

from dotick.organization.application import DEFAULT_COLUMN_TITLE
from dotick.organization.models import Column, Folder, List, OrganizationCreateOperation

UNSET = object()


class IdempotencyConflict(APIException):
    status_code = 409
    default_detail = "The operation ID was already used for a different creation intent."
    default_code = "idempotency_conflict"


def _normalized_title(title):
    normalized = title.strip()
    if not normalized:
        raise ValueError("Title must not be empty.")
    return normalized


def _intent_digest(payload):
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    return hashlib.sha256(encoded.encode()).hexdigest()


def _list_creation_intent_digest(*, title, folder_id, position=UNSET):
    payload = {
        "title": title,
        "folder_id": str(folder_id) if folder_id is not None else None,
    }
    if position is not UNSET:
        payload["position"] = position
    return _intent_digest(payload)


def _get_create_operation(*, actor_id, resource_type, operation_id):
    return OrganizationCreateOperation.objects.filter(
        owner_id=actor_id,
        resource_type=resource_type,
        operation_id=operation_id,
    ).first()


def _resolve_list_retry(*, actor_id, operation, intent_digest):
    if operation.intent_digest != intent_digest:
        raise IdempotencyConflict
    try:
        row = List.objects.get(pk=operation.resource_id, owner_id=actor_id)
        default_column = Column.objects.get(list=row, is_default=True)
    except (List.DoesNotExist, Column.DoesNotExist) as error:
        raise Http404 from error
    return row, default_column, False


@transaction.atomic
def create_list(
    *,
    actor_id,
    title,
    operation_id,
    folder_id=None,
    position=UNSET,
):
    normalized_title = _normalized_title(title)
    intent_digest = _list_creation_intent_digest(
        title=normalized_title,
        folder_id=folder_id,
        position=position,
    )
    resource_type = OrganizationCreateOperation.ResourceType.LIST
    existing = _get_create_operation(
        actor_id=actor_id,
        resource_type=resource_type,
        operation_id=operation_id,
    )
    if existing is not None:
        return _resolve_list_retry(
            actor_id=actor_id,
            operation=existing,
            intent_digest=intent_digest,
        )

    try:
        with transaction.atomic():
            folder = None
            if folder_id is not None:
                try:
                    folder = Folder.objects.select_for_update().get(
                        pk=folder_id,
                        owner_id=actor_id,
                        is_trashed=False,
                    )
                except Folder.DoesNotExist as error:
                    raise Http404 from error

            resolved_position = (
                List.objects.filter(owner_id=actor_id, is_trashed=False).count()
                if position is UNSET
                else position
            )
            row = List.objects.create(
                owner_id=actor_id,
                folder=folder,
                title=normalized_title,
                position=resolved_position,
            )
            default_column = Column.objects.create(
                list=row,
                title=DEFAULT_COLUMN_TITLE,
                position=0,
                is_default=True,
            )
            OrganizationCreateOperation.objects.create(
                owner_id=actor_id,
                resource_type=resource_type,
                operation_id=operation_id,
                intent_digest=intent_digest,
                resource_id=row.id,
            )
    except IntegrityError:
        existing = _get_create_operation(
            actor_id=actor_id,
            resource_type=resource_type,
            operation_id=operation_id,
        )
        if existing is None:
            raise
        return _resolve_list_retry(
            actor_id=actor_id,
            operation=existing,
            intent_digest=intent_digest,
        )

    return row, default_column, True
