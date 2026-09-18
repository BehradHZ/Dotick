from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import F
from django.http import Http404
from django.utils import timezone
from rest_framework.exceptions import APIException

from dotick.identity.models import UserPreferences
from dotick.organization.concurrency import (
    increment_locked_version,
    lock_owned_versioned_resource,
)
from dotick.organization.models import Column, Folder, List

DEFAULT_COLUMN_TITLE = "Items"
UNSET = object()


class ChildResolutionRequired(APIException):
    status_code = 409
    default_detail = "Choose how active descendant Items should be handled."
    default_code = "child_resolution_required"


class ImmutableInbox(APIException):
    status_code = 409
    default_detail = "Inbox cannot be renamed or deleted."
    default_code = "immutable_inbox"


class ImmutableDefaultColumn(APIException):
    status_code = 409
    default_detail = "The default Column cannot be deleted."
    default_code = "immutable_default_column"


def _normalized_title(title):
    normalized = title.strip()
    if not normalized:
        raise ValueError("Title must not be empty.")
    return normalized


@transaction.atomic
def create_folder(*, owner, title, position=None):
    if position is None:
        position = Folder.objects.filter(owner=owner, is_trashed=False).count()
    return Folder.objects.create(
        owner=owner,
        title=_normalized_title(title),
        position=position,
    )


def list_folders(*, actor_id):
    return Folder.objects.filter(owner_id=actor_id, is_trashed=False).order_by(
        "position", "created_at", "id"
    )


def get_folder(*, actor_id, folder_id, for_update=False):
    rows = Folder.objects.filter(owner_id=actor_id, is_trashed=False)
    if for_update:
        rows = rows.select_for_update()
    try:
        return rows.get(pk=folder_id)
    except Folder.DoesNotExist as error:
        raise Http404 from error


@transaction.atomic
def update_folder(*, actor_id, folder_id, version, title=UNSET, position=UNSET):
    row = lock_owned_versioned_resource(
        model=Folder,
        actor_id=actor_id,
        resource_id=folder_id,
        expected_version=version,
        scope_filters={"is_trashed": False},
    )
    updates = {}
    if title is not UNSET:
        updates["title"] = _normalized_title(title)
    if position is not UNSET:
        updates["position"] = position
    return increment_locked_version(
        row=row,
        actor_id=actor_id,
        expected_version=version,
        updates=updates,
    )


@transaction.atomic
def trash_folder(*, actor_id, folder_id, version, item_resolution=None):
    from dotick.items.models import Item

    row = lock_owned_versioned_resource(
        model=Folder,
        actor_id=actor_id,
        resource_id=folder_id,
        expected_version=version,
        scope_filters={"is_trashed": False},
    )
    child_lists = list(
        List.objects.select_for_update()
        .filter(owner_id=actor_id, folder=row, is_trashed=False)
        .order_by("id")
    )
    active_items = Item.objects.select_for_update().filter(
        owner_id=actor_id,
        column__list__in=child_lists,
        is_trashed=False,
    )
    item_ids = list(active_items.values_list("id", flat=True))
    if item_ids and item_resolution not in {"move_to_inbox", "trash"}:
        raise ChildResolutionRequired

    now = timezone.now()
    if item_ids:
        try:
            inbox_column = Column.objects.get(
                list__owner_id=actor_id,
                list__is_inbox=True,
                list__is_trashed=False,
                is_default=True,
            )
        except Column.DoesNotExist as error:
            raise ChildResolutionRequired from error
        if item_resolution == "move_to_inbox":
            Item.objects.filter(pk__in=item_ids).update(
                column=inbox_column,
                version=F("version") + 1,
                updated_at=now,
            )
        else:
            Item.objects.filter(pk__in=item_ids).update(
                column=inbox_column,
                is_trashed=True,
                trashed_at=now,
                trash_origin_column_id=F("column_id"),
                version=F("version") + 1,
                updated_at=now,
            )

    if child_lists:
        List.objects.filter(pk__in=[child.pk for child in child_lists]).update(
            is_trashed=True,
            trashed_at=now,
            version=F("version") + 1,
            updated_at=now,
        )
    increment_locked_version(
        row=row,
        actor_id=actor_id,
        expected_version=version,
        updates={"is_trashed": True, "trashed_at": now},
    )


@transaction.atomic
def restore_folder(*, actor_id, folder_id, version):
    from dotick.items.models import Item

    row = lock_owned_versioned_resource(
        model=Folder,
        actor_id=actor_id,
        resource_id=folder_id,
        expected_version=version,
        scope_filters={"is_trashed": True},
    )
    deletion_time = row.trashed_at
    child_lists = list(
        List.objects.select_for_update().filter(
            owner_id=actor_id,
            folder=row,
            is_trashed=True,
            trashed_at=deletion_time,
        )
    )
    origin_column_ids = list(
        Column.objects.filter(list__in=child_lists).values_list("id", flat=True)
    )
    trashed_items = Item.objects.select_for_update().filter(
        owner_id=actor_id,
        is_trashed=True,
        trashed_at=deletion_time,
        trash_origin_column_id__in=origin_column_ids,
    )
    item_ids = list(trashed_items.values_list("id", flat=True))
    now = timezone.now()
    if child_lists:
        List.objects.filter(pk__in=[child.pk for child in child_lists]).update(
            is_trashed=False,
            trashed_at=None,
            version=F("version") + 1,
            updated_at=now,
        )
    if item_ids:
        Item.objects.filter(pk__in=item_ids).update(
            column_id=F("trash_origin_column_id"),
            is_trashed=False,
            trashed_at=None,
            trash_origin_column_id=None,
            version=F("version") + 1,
            updated_at=now,
        )
    return increment_locked_version(
        row=row,
        actor_id=actor_id,
        expected_version=version,
        updates={"is_trashed": False, "trashed_at": None},
    )


def list_trashed_folders(*, actor_id):
    return Folder.objects.filter(owner_id=actor_id, is_trashed=True).order_by(
        "-trashed_at", "-id"
    )


def _resolve_folder(*, owner, folder):
    if folder is None:
        return None
    return Folder.objects.get(pk=folder.pk, owner=owner, is_trashed=False)


@transaction.atomic
def create_list_with_default_column(
    *,
    owner,
    title,
    folder=None,
    position=None,
    is_inbox=False,
):
    folder = _resolve_folder(owner=owner, folder=folder)
    if position is None:
        position = List.objects.filter(owner=owner, is_trashed=False).count()

    row = List.objects.create(
        owner=owner,
        folder=folder,
        title=_normalized_title(title),
        position=position,
        is_inbox=is_inbox,
    )
    default_column = Column.objects.create(
        list=row,
        title=DEFAULT_COLUMN_TITLE,
        position=0,
        is_default=True,
    )
    return row, default_column


def create_list(*, owner, title, folder=None, position=None):
    return create_list_with_default_column(
        owner=owner,
        title=title,
        folder=folder,
        position=position,
    )


def list_lists(*, actor_id):
    return (
        List.objects.filter(owner_id=actor_id, is_trashed=False)
        .prefetch_related("columns")
        .order_by("-is_inbox", "position", "created_at", "id")
    )


def get_list(*, actor_id, list_id, for_update=False):
    rows = List.objects.filter(owner_id=actor_id, is_trashed=False).prefetch_related("columns")
    if for_update:
        rows = rows.select_for_update()
    try:
        return rows.get(pk=list_id)
    except List.DoesNotExist as error:
        raise Http404 from error


@transaction.atomic
def update_list(
    *,
    actor_id,
    list_id,
    version,
    title=UNSET,
    folder_id=UNSET,
    position=UNSET,
):
    row = lock_owned_versioned_resource(
        model=List,
        actor_id=actor_id,
        resource_id=list_id,
        expected_version=version,
        scope_filters={"is_trashed": False},
    )
    if row.is_inbox and title is not UNSET:
        raise ImmutableInbox

    updates = {}
    if title is not UNSET:
        updates["title"] = _normalized_title(title)
    if folder_id is not UNSET:
        updates["folder"] = (
            None
            if folder_id is None
            else get_folder(
                actor_id=actor_id,
                folder_id=folder_id,
                for_update=True,
            )
        )
    if position is not UNSET:
        updates["position"] = position
    return increment_locked_version(
        row=row,
        actor_id=actor_id,
        expected_version=version,
        updates=updates,
    )


@transaction.atomic
def trash_list(*, actor_id, list_id, version, item_resolution=None):
    from dotick.items.models import Item

    row = lock_owned_versioned_resource(
        model=List,
        actor_id=actor_id,
        resource_id=list_id,
        expected_version=version,
        scope_filters={"is_trashed": False},
    )
    if row.is_inbox:
        raise ImmutableInbox
    active_items = Item.objects.select_for_update().filter(
        owner_id=actor_id,
        column__list=row,
        is_trashed=False,
    )
    item_ids = list(active_items.values_list("id", flat=True))
    if item_ids and item_resolution not in {"move_to_inbox", "trash"}:
        raise ChildResolutionRequired
    now = timezone.now()
    if item_ids:
        try:
            inbox_column = Column.objects.get(
                list__owner_id=actor_id,
                list__is_inbox=True,
                list__is_trashed=False,
                is_default=True,
            )
        except Column.DoesNotExist as error:
            raise ChildResolutionRequired from error
        if item_resolution == "move_to_inbox":
            Item.objects.filter(pk__in=item_ids).update(
                column=inbox_column,
                version=F("version") + 1,
                updated_at=now,
            )
        else:
            Item.objects.filter(pk__in=item_ids).update(
                column=inbox_column,
                is_trashed=True,
                trashed_at=now,
                trash_origin_column_id=F("column_id"),
                version=F("version") + 1,
                updated_at=now,
            )
    increment_locked_version(
        row=row,
        actor_id=actor_id,
        expected_version=version,
        updates={"is_trashed": True, "trashed_at": now},
    )


@transaction.atomic
def restore_list(*, actor_id, list_id, version):
    from dotick.items.models import Item

    row = lock_owned_versioned_resource(
        model=List,
        actor_id=actor_id,
        resource_id=list_id,
        expected_version=version,
        scope_filters={"is_trashed": True},
    )
    deletion_time = row.trashed_at
    origin_column_ids = list(Column.objects.filter(list=row).values_list("id", flat=True))
    trashed_items = Item.objects.select_for_update().filter(
        owner_id=actor_id,
        is_trashed=True,
        trashed_at=deletion_time,
        trash_origin_column_id__in=origin_column_ids,
    )
    item_ids = list(trashed_items.values_list("id", flat=True))
    updates = {"is_trashed": False, "trashed_at": None}
    if row.folder_id is not None and row.folder.is_trashed:
        updates["folder"] = None
    now = timezone.now()
    if item_ids:
        Item.objects.filter(pk__in=item_ids).update(
            column_id=F("trash_origin_column_id"),
            is_trashed=False,
            trashed_at=None,
            trash_origin_column_id=None,
            version=F("version") + 1,
            updated_at=now,
        )
    return increment_locked_version(
        row=row,
        actor_id=actor_id,
        expected_version=version,
        updates=updates,
    )


def list_trashed_lists(*, actor_id):
    return (
        List.objects.filter(owner_id=actor_id, is_trashed=True)
        .prefetch_related("columns")
        .order_by("-trashed_at", "-id")
    )


def list_columns(*, actor_id, list_id):
    row = get_list(actor_id=actor_id, list_id=list_id)
    return row.columns.order_by("position", "created_at", "id")


@transaction.atomic
def create_column(*, actor_id, list_id, title):
    row = get_list(actor_id=actor_id, list_id=list_id, for_update=True)
    return Column.objects.create(
        list=row,
        title=_normalized_title(title),
        position=row.columns.count(),
    )


def get_column(*, actor_id, column_id, for_update=False):
    rows = Column.objects.filter(
        list__owner_id=actor_id,
        list__is_trashed=False,
    )
    if for_update:
        rows = rows.select_for_update()
    try:
        return rows.get(pk=column_id)
    except Column.DoesNotExist as error:
        raise Http404 from error


@transaction.atomic
def update_column(*, actor_id, column_id, title=UNSET, position=UNSET):
    row = get_column(actor_id=actor_id, column_id=column_id, for_update=True)
    changed_fields = ["updated_at"]
    if title is not UNSET:
        row.title = _normalized_title(title)
        changed_fields.append("title")
    if position is not UNSET:
        row.position = position
        changed_fields.append("position")
    row.save(update_fields=changed_fields)
    return row


@transaction.atomic
def delete_column(*, actor_id, column_id, item_resolution=None):
    from dotick.items.models import Item

    row = get_column(actor_id=actor_id, column_id=column_id, for_update=True)
    if row.is_default:
        raise ImmutableDefaultColumn

    items = Item.objects.select_for_update().filter(
        owner_id=actor_id,
        column=row,
    )
    active_item_ids = list(items.filter(is_trashed=False).values_list("id", flat=True))
    trashed_item_ids = list(items.filter(is_trashed=True).values_list("id", flat=True))
    if active_item_ids and item_resolution not in {"move_to_default", "trash"}:
        raise ChildResolutionRequired

    default_column = Column.objects.select_for_update().get(
        list_id=row.list_id,
        is_default=True,
    )
    now = timezone.now()
    if active_item_ids and item_resolution == "move_to_default":
        Item.objects.filter(pk__in=active_item_ids).update(
            column=default_column,
            version=F("version") + 1,
            updated_at=now,
        )
    elif active_item_ids:
        Item.objects.filter(pk__in=active_item_ids).update(
            column=default_column,
            is_trashed=True,
            trashed_at=now,
            trash_origin_column_id=F("column_id"),
            version=F("version") + 1,
            updated_at=now,
        )
    if trashed_item_ids:
        Item.objects.filter(pk__in=trashed_item_ids).update(
            column=default_column,
            version=F("version") + 1,
            updated_at=now,
        )
    row.delete()


@transaction.atomic
def bootstrap_account(*, actor_id, timezone):
    user = get_user_model().objects.select_for_update().get(pk=actor_id)
    preferences, _ = UserPreferences.objects.get_or_create(
        user=user,
        defaults={"timezone": timezone},
    )

    inbox = List.objects.filter(owner=user, is_inbox=True).first()
    if inbox is None:
        inbox, default_column = create_list_with_default_column(
            owner=user,
            title="Inbox",
            position=0,
            is_inbox=True,
        )
    else:
        default_column, _ = Column.objects.get_or_create(
            list=inbox,
            is_default=True,
            defaults={"title": DEFAULT_COLUMN_TITLE, "position": 0},
        )

    return preferences, inbox, default_column
