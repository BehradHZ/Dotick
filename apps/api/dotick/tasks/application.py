import hashlib

from django.db import IntegrityError, transaction
from django.db.models import F
from django.http import Http404
from django.utils import timezone
from rest_framework.exceptions import APIException

from dotick.items.models import Item, ItemSource
from dotick.organization.models import Column
from dotick.tasks.models import Task

UNSET = object()


class IdempotencyConflict(APIException):
    status_code = 409
    default_detail = "The operation ID was already used for a different Task creation."
    default_code = "idempotency_conflict"


class VersionConflict(APIException):
    status_code = 409
    default_code = "version_conflict"

    def __init__(self, item):
        self.current = {
            "id": str(item.id),
            "title": item.title,
            "status": item.task.status,
            "version": item.version,
            "column_id": str(item.column_id),
        }
        super().__init__("The Task changed after the supplied version.")


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


def list_tasks(*, actor_id, column_id=None):
    rows = Item.objects.select_related("task", "source").filter(
        owner_id=actor_id,
        is_trashed=False,
        kind=Item.Kind.TASK,
        column__list__is_trashed=False,
    )
    if column_id is not None:
        rows = rows.filter(column_id=column_id)
    return rows.order_by("-updated_at", "-id")


def list_trashed_tasks(*, actor_id):
    return (
        Item.objects.select_related("task", "source")
        .filter(
            owner_id=actor_id,
            is_trashed=True,
            kind=Item.Kind.TASK,
        )
        .order_by("-trashed_at", "-id")
    )


def get_task(*, actor_id, task_id):
    try:
        return (
            Item.objects.select_related("task", "source")
            .filter(
                owner_id=actor_id,
                is_trashed=False,
                kind=Item.Kind.TASK,
                column__list__is_trashed=False,
            )
            .get(pk=task_id)
        )
    except Item.DoesNotExist as error:
        raise Http404 from error


@transaction.atomic
def update_task(*, actor_id, task_id, version, title=UNSET, status=UNSET, column_id=UNSET):
    try:
        item = (
            Item.objects.select_for_update(of=("self",))
            .select_related("task", "source")
            .filter(
                owner_id=actor_id,
                is_trashed=False,
                kind=Item.Kind.TASK,
                column__list__is_trashed=False,
            )
            .get(pk=task_id)
        )
    except Item.DoesNotExist as error:
        raise Http404 from error

    if item.version != version:
        raise VersionConflict(item)

    destination = None
    if column_id is not UNSET:
        try:
            destination = Column.objects.get(
                pk=column_id,
                list__owner_id=actor_id,
                list__is_trashed=False,
            )
        except Column.DoesNotExist as error:
            raise Http404("The destination Column is unavailable.") from error

    if status is not UNSET:
        Task.objects.filter(pk=item.pk).update(status=status)

    item_changes = {
        "version": F("version") + 1,
        "updated_at": timezone.now(),
    }
    if title is not UNSET:
        item_changes["title"] = title.strip()
    if destination is not None:
        item_changes["column"] = destination
    updated = Item.objects.filter(pk=item.pk, version=version).update(**item_changes)
    if updated != 1:
        item.refresh_from_db()
        raise VersionConflict(item)
    return get_task(actor_id=actor_id, task_id=task_id)


@transaction.atomic
def delete_task(*, actor_id, task_id, version):
    try:
        item = (
            Item.objects.select_for_update(of=("self",))
            .select_related("task")
            .filter(
                owner_id=actor_id,
                is_trashed=False,
                kind=Item.Kind.TASK,
                column__list__is_trashed=False,
            )
            .get(pk=task_id)
        )
    except Item.DoesNotExist as error:
        raise Http404 from error

    if item.version != version:
        raise VersionConflict(item)

    now = timezone.now()
    updated = Item.objects.filter(pk=item.pk, version=version).update(
        is_trashed=True,
        trashed_at=now,
        trash_origin_column_id=F("column_id"),
        version=F("version") + 1,
        updated_at=now,
    )
    if updated != 1:
        item.refresh_from_db()
        raise VersionConflict(item)


@transaction.atomic
def restore_task(*, actor_id, task_id, version):
    try:
        item = (
            Item.objects.select_for_update(of=("self",))
            .select_related("task")
            .filter(
                owner_id=actor_id,
                is_trashed=True,
                kind=Item.Kind.TASK,
            )
            .get(pk=task_id)
        )
    except Item.DoesNotExist as error:
        raise Http404 from error

    if item.version != version:
        raise VersionConflict(item)

    destination = Column.objects.filter(
        pk=item.trash_origin_column_id,
        list__owner_id=actor_id,
        list__is_trashed=False,
    ).first()
    if destination is None:
        try:
            destination = Column.objects.get(
                list__owner_id=actor_id,
                list__is_inbox=True,
                list__is_trashed=False,
                is_default=True,
            )
        except Column.DoesNotExist as error:
            raise Http404("The Inbox default Column is unavailable.") from error

    now = timezone.now()
    updated = Item.objects.filter(
        pk=item.pk,
        version=version,
        is_trashed=True,
    ).update(
        column=destination,
        is_trashed=False,
        trashed_at=None,
        trash_origin_column_id=None,
        version=F("version") + 1,
        updated_at=now,
    )
    if updated != 1:
        item.refresh_from_db()
        raise VersionConflict(item)
    return get_task(actor_id=actor_id, task_id=task_id)


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
