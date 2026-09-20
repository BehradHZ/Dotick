import hashlib
import json
from datetime import timedelta

from django.db import IntegrityError, transaction
from django.db.models import F
from django.http import Http404
from django.utils import timezone
from rest_framework.exceptions import APIException, ValidationError

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
            "priority": item.task.priority,
            "due_at": item.task.due_at,
            "end_at": item.task.end_at,
            "is_all_day": item.task.is_all_day,
            "deadline_at": item.task.deadline_at,
            "grace_period_days": item.task.grace_period_days,
            "version": item.version,
            "column_id": str(item.column_id),
        }
        super().__init__("The Task changed after the supplied version.")


def _creation_intent_digest(**intent):
    value = json.dumps(intent, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(value.encode()).hexdigest()


def _validate_schedule(*, due_at, end_at, is_all_day, deadline_at, grace_period_days):
    errors = {}
    if end_at is not None and due_at is None:
        errors["end_at"] = "A duration end requires due_at."
    elif end_at is not None and end_at < due_at:
        errors["end_at"] = "end_at must be at or after due_at."
    if deadline_at is not None and due_at is not None and deadline_at < due_at:
        errors["deadline_at"] = "deadline_at must be at or after due_at."
    if deadline_at is not None and end_at is not None and deadline_at < end_at:
        errors["deadline_at"] = "deadline_at must be at or after end_at."
    if is_all_day and due_at is None:
        errors["is_all_day"] = "An all-day Task requires due_at."
    if deadline_at is None and grace_period_days != 0:
        errors["grace_period_days"] = "A nonzero grace period requires deadline_at."
    if errors:
        raise ValidationError(errors)


def task_time_status(*, task, now):
    if task.deadline_at is not None and now >= task.deadline_at:
        grace_ends_at = task.deadline_at + timedelta(days=task.grace_period_days)
        if task.grace_period_days == 0 or now >= grace_ends_at:
            return Task.Status.SKIPPED
        return Task.Status.MISSED
    if task.due_at is not None and now >= task.due_at:
        return Task.Status.OVERDUE
    return Task.Status.TODO


@transaction.atomic
def advance_task_lifecycle(*, now=None):
    evaluation_time = now or timezone.now()
    mutable_statuses = [Task.Status.TODO, Task.Status.OVERDUE, Task.Status.MISSED]
    items = (
        Item.objects.select_for_update(of=("self",))
        .select_related("task")
        .filter(
            task__status__in=mutable_statuses,
            is_trashed=False,
            column__list__is_trashed=False,
        )
        .order_by("id")
    )
    changed = 0
    for item in items:
        task = item.task
        target = task_time_status(task=task, now=evaluation_time)
        if target == task.status:
            continue
        Task.objects.filter(pk=item.pk).update(status=target)
        Item.objects.filter(pk=item.pk).update(
            version=F("version") + 1,
            updated_at=evaluation_time,
        )
        changed += 1
    return changed


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
def update_task(
    *,
    actor_id,
    task_id,
    version,
    title=UNSET,
    status=UNSET,
    column_id=UNSET,
    priority=UNSET,
    due_at=UNSET,
    end_at=UNSET,
    is_all_day=UNSET,
    deadline_at=UNSET,
    grace_period_days=UNSET,
):
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

    schedule = {
        "due_at": item.task.due_at if due_at is UNSET else due_at,
        "end_at": item.task.end_at if end_at is UNSET else end_at,
        "is_all_day": item.task.is_all_day if is_all_day is UNSET else is_all_day,
        "deadline_at": item.task.deadline_at if deadline_at is UNSET else deadline_at,
        "grace_period_days": (
            item.task.grace_period_days if grace_period_days is UNSET else grace_period_days
        ),
    }
    _validate_schedule(**schedule)

    task_changes = {}
    for field, value in {
        "status": status,
        "priority": priority,
        "due_at": due_at,
        "end_at": end_at,
        "is_all_day": is_all_day,
        "deadline_at": deadline_at,
        "grace_period_days": grace_period_days,
    }.items():
        if value is not UNSET:
            task_changes[field] = value
    if task_changes:
        Task.objects.filter(pk=item.pk).update(**task_changes)

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
def create_task(
    *,
    actor_id,
    title,
    operation_id,
    column_id=None,
    priority=Task.Priority.NONE,
    due_at=None,
    end_at=None,
    is_all_day=False,
    deadline_at=None,
    grace_period_days=0,
):
    normalized_title = title.strip()
    _validate_schedule(
        due_at=due_at,
        end_at=end_at,
        is_all_day=is_all_day,
        deadline_at=deadline_at,
        grace_period_days=grace_period_days,
    )
    intent_digest = _creation_intent_digest(
        title=normalized_title,
        column_id=column_id or "inbox",
        priority=priority,
        due_at=due_at,
        end_at=end_at,
        is_all_day=is_all_day,
        deadline_at=deadline_at,
        grace_period_days=grace_period_days,
    )
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
            Task.objects.create(
                item=item,
                priority=priority,
                due_at=due_at,
                end_at=end_at,
                is_all_day=is_all_day,
                deadline_at=deadline_at,
                grace_period_days=grace_period_days,
            )
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
