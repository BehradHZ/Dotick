import hashlib

from django.db import IntegrityError, transaction
from django.http import Http404
from rest_framework.exceptions import APIException

from dotick.items.models import Item, ItemSource, trash_item
from dotick.organization.models import Column
from dotick.tasks.models import Task

UNSET = object()


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
        super().__init__("The task changed after the supplied version.")


class IdempotencyConflict(APIException):
    status_code = 409
    default_detail = "The operation ID was already used for a different task creation."
    default_code = "idempotency_conflict"


def _creation_intent_digest(*, title, column_id):
    value = f"{title.strip()}\0{column_id or 'inbox'}"
    return hashlib.sha256(value.encode()).hexdigest()


def _resolve_creation_retry(*, actor_id, operation_id, intent_digest):
    existing = get_task_by_operation(actor_id=actor_id, operation_id=operation_id)
    if existing.creation_intent_digest != intent_digest:
        raise IdempotencyConflict
    return existing, False


@transaction.atomic
def create_task(*, actor_id, title, operation_id, column_id=None):
    intent_digest = _creation_intent_digest(title=title, column_id=column_id)
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
                id=column_id,
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
                title=title.strip(),
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
    return get_task(actor_id=actor_id, task_id=item.id), True


def get_task_by_operation(*, actor_id, operation_id):
    try:
        return (
            Item.objects.select_related("task", "source")
            .filter(owner_id=actor_id, kind=Item.Kind.TASK)
            .get(creation_operation_id=operation_id)
        )
    except Item.DoesNotExist as error:
        raise Http404 from error


def get_task(*, actor_id, task_id):
    try:
        return (
            Item.objects.select_related("task", "source")
            .filter(owner_id=actor_id, is_trashed=False, kind=Item.Kind.TASK)
            .get(id=task_id)
        )
    except Item.DoesNotExist as error:
        raise Http404 from error


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


@transaction.atomic
def update_task(
    *,
    actor_id,
    task_id,
    version,
    title=UNSET,
    status=UNSET,
    column_id=UNSET,
):
    try:
        item = (
            Item.objects.select_for_update(of=("self",))
            .select_related("task", "source")
            .filter(owner_id=actor_id, is_trashed=False, kind=Item.Kind.TASK)
            .get(id=task_id)
        )
    except Item.DoesNotExist as error:
        raise Http404 from error
    if item.version != version:
        raise VersionConflict(item)
    changed_fields = ["version", "updated_at"]
    if title is not UNSET:
        item.title = title.strip()
        changed_fields.append("title")
    if column_id is not UNSET:
        try:
            item.column = Column.objects.filter(
                list__owner_id=actor_id,
                list__is_trashed=False,
            ).get(id=column_id)
        except Column.DoesNotExist as error:
            raise Http404 from error
        changed_fields.append("column")
    if status is not UNSET:
        item.task.status = status
        item.task.save(update_fields=["status"])
    item.version += 1
    item.save(update_fields=changed_fields)
    return get_task(actor_id=actor_id, task_id=item.id)


@transaction.atomic
def delete_task(*, actor_id, task_id, version):
    try:
        item = (
            Item.objects.select_for_update(of=("self",))
            .select_related("task")
            .filter(owner_id=actor_id, is_trashed=False, kind=Item.Kind.TASK)
            .get(id=task_id)
        )
    except Item.DoesNotExist as error:
        raise Http404 from error
    if item.version != version:
        raise VersionConflict(item)
    trash_item(item)


def list_trashed_tasks(*, actor_id):
    return (
        Item.objects.select_related("task", "source")
        .filter(owner_id=actor_id, is_trashed=True, kind=Item.Kind.TASK)
        .order_by("-trashed_at", "-id")
    )


@transaction.atomic
def restore_task(*, actor_id, task_id, version):
    try:
        item = (
            Item.objects.select_for_update(of=("self",))
            .select_related("task", "source", "column__list")
            .filter(owner_id=actor_id, is_trashed=True, kind=Item.Kind.TASK)
            .get(id=task_id)
        )
    except Item.DoesNotExist as error:
        raise Http404 from error
    if item.version != version:
        raise VersionConflict(item)
    changed_fields = [
        "is_trashed",
        "trashed_at",
        "trash_origin_column_id",
        "version",
        "updated_at",
    ]
    destination = None
    if item.trash_origin_column_id is not None:
        destination = (
            Column.objects.filter(
                id=item.trash_origin_column_id,
                list__owner_id=actor_id,
                list__is_trashed=False,
            )
            .select_related("list")
            .first()
        )
    if destination is None:
        try:
            destination = Column.objects.get(
                list__owner_id=actor_id,
                list__is_inbox=True,
                list__is_trashed=False,
                is_default=True,
            )
        except Column.DoesNotExist as error:
            raise Http404("The account Inbox is unavailable.") from error
    if item.column_id != destination.id:
        item.column = destination
        changed_fields.append("column")
    item.is_trashed = False
    item.trashed_at = None
    item.trash_origin_column_id = None
    item.version += 1
    item.save(update_fields=changed_fields)
    return get_task(actor_id=actor_id, task_id=item.id)
