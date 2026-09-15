import hashlib

from django.db import IntegrityError, transaction
from django.http import Http404
from rest_framework.exceptions import APIException

from dotick.items.models import Item, ItemSource
from dotick.organization.models import Column
from dotick.tasks.models import Task


class IdempotencyConflict(APIException):
    status_code = 409
    default_detail = "The operation ID was already used for a different Task creation."
    default_code = "idempotency_conflict"


def _creation_intent_digest(*, title, column_id):
    value = f"{title.strip()}\0{column_id or 'inbox'}"
    return hashlib.sha256(value.encode()).hexdigest()


def _get_task_by_operation(*, actor_id, operation_id):
    try:
        return (
            Item.objects.select_related("task", "source")
            .filter(owner_id=actor_id, kind=Item.Kind.TASK)
            .get(creation_operation_id=operation_id)
        )
    except Item.DoesNotExist as error:
        raise Http404 from error


def _resolve_creation_retry(*, actor_id, operation_id, intent_digest):
    existing = _get_task_by_operation(actor_id=actor_id, operation_id=operation_id)
    if existing.creation_intent_digest != intent_digest:
        raise IdempotencyConflict
    return existing, False


@transaction.atomic
def create_task(*, actor_id, title, operation_id, column_id=None):
    normalized_title = title.strip()
    intent_digest = _creation_intent_digest(title=normalized_title, column_id=column_id)
    existing = (
        Item.objects.filter(
            owner_id=actor_id,
            creation_operation_id=operation_id,
            kind=Item.Kind.TASK,
        )
        .select_related("task", "source")
        .first()
    )
    if existing is not None:
        return _resolve_creation_retry(
            actor_id=actor_id,
            operation_id=operation_id,
            intent_digest=intent_digest,
        )

    try:
        if column_id is None:
            destination = Column.objects.select_related("list").get(
                list__owner_id=actor_id,
                list__is_inbox=True,
                list__is_trashed=False,
                is_default=True,
            )
        else:
            destination = Column.objects.select_related("list").get(
                pk=column_id,
                list__owner_id=actor_id,
                list__is_trashed=False,
            )
    except Column.DoesNotExist as error:
        raise Http404("The destination Column is unavailable.") from error

    try:
        with transaction.atomic():
            item = Item.objects.create(
                kind=Item.Kind.TASK,
                owner_id=actor_id,
                created_by_id=actor_id,
                column=destination,
                title=normalized_title,
                creation_operation_id=operation_id,
                creation_intent_digest=intent_digest,
            )
            Task.objects.create(item=item)
            ItemSource.objects.create(item=item, platform=ItemSource.Platform.MANUAL)
    except IntegrityError:
        return _resolve_creation_retry(
            actor_id=actor_id,
            operation_id=operation_id,
            intent_digest=intent_digest,
        )

    return (
        Item.objects.select_related("task", "source").get(pk=item.pk),
        True,
    )
