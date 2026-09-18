import hashlib
import json

from django.db import IntegrityError, transaction
from django.http import Http404
from rest_framework.exceptions import APIException

from dotick.organization.application import DEFAULT_COLUMN_TITLE
from dotick.organization.models import Column, Folder, List, OrganizationCreateOperation
from dotick.organization.operation_locks import lock_create_operation_scope

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


def _column_creation_intent_digest(*, list_id, title):
    return _intent_digest(
        {
            "list_id": str(list_id),
            "title": title,
        }
    )


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


def _resolve_column_retry(*, actor_id, operation, intent_digest):
    if operation.intent_digest != intent_digest:
        raise IdempotencyConflict
    try:
        row = Column.objects.get(
            pk=operation.resource_id,
            list__owner_id=actor_id,
        )
    except Column.DoesNotExist as error:
        raise Http404 from error
    return row, False


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
    lock_create_operation_scope(
        actor_id=actor_id,
        resource_type=resource_type,
        operation_id=operation_id,
    )
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


@transaction.atomic
def create_column(*, actor_id, list_id, title, operation_id):
    normalized_title = _normalized_title(title)
    intent_digest = _column_creation_intent_digest(
        list_id=list_id,
        title=normalized_title,
    )
    resource_type = OrganizationCreateOperation.ResourceType.COLUMN
    lock_create_operation_scope(
        actor_id=actor_id,
        resource_type=resource_type,
        operation_id=operation_id,
    )
    existing = _get_create_operation(
        actor_id=actor_id,
        resource_type=resource_type,
        operation_id=operation_id,
    )
    if existing is not None:
        return _resolve_column_retry(
            actor_id=actor_id,
            operation=existing,
            intent_digest=intent_digest,
        )

    try:
        with transaction.atomic():
            try:
                parent = List.objects.select_for_update().get(
                    pk=list_id,
                    owner_id=actor_id,
                    is_trashed=False,
                )
            except List.DoesNotExist as error:
                raise Http404 from error

            row = Column.objects.create(
                list=parent,
                title=normalized_title,
                position=parent.columns.count(),
                is_default=False,
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
        return _resolve_column_retry(
            actor_id=actor_id,
            operation=existing,
            intent_digest=intent_digest,
        )

    return row, True
