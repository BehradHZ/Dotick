from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import F
from django.http import Http404
from django.utils import timezone
from rest_framework.exceptions import APIException

from dotick.organization.models import Column, Folder, List, UserPreferences, trash_list

UNSET = object()


class ImmutableInbox(APIException):
    status_code = 409
    default_detail = "Inbox cannot be renamed or deleted."
    default_code = "immutable_inbox"


class ImmutableDefaultColumn(APIException):
    status_code = 409
    default_detail = "The default Column cannot be deleted."
    default_code = "immutable_default_column"


class ChildResolutionRequired(APIException):
    status_code = 409
    default_detail = "Choose how active child resources should be handled."
    default_code = "child_resolution_required"


@transaction.atomic
def bootstrap_account(*, actor_id, timezone):
    user = get_user_model().objects.select_for_update().get(id=actor_id)
    preferences, _ = UserPreferences.objects.get_or_create(
        user=user,
        defaults={"timezone": timezone},
    )
    inbox, _ = List.objects.get_or_create(
        owner=user,
        is_inbox=True,
        defaults={"title": "Inbox", "position": 0},
    )
    default_column, _ = Column.objects.get_or_create(
        list=inbox,
        is_default=True,
        defaults={"title": "not_sectioned", "position": 0},
    )
    return preferences, inbox, default_column


def list_lists(*, actor_id):
    return (
        List.objects.filter(owner_id=actor_id, is_trashed=False)
        .prefetch_related("columns")
        .order_by("-is_inbox", "position", "created_at")
    )


def list_folders(*, actor_id):
    return Folder.objects.filter(owner_id=actor_id, is_trashed=False).order_by(
        "position", "created_at"
    )


@transaction.atomic
def create_folder(*, actor_id, title):
    return Folder.objects.create(
        owner_id=actor_id,
        title=title.strip(),
        position=Folder.objects.filter(owner_id=actor_id, is_trashed=False).count(),
    )


def get_folder(*, actor_id, folder_id, for_update=False):
    rows = Folder.objects.filter(owner_id=actor_id, is_trashed=False)
    if for_update:
        rows = rows.select_for_update()
    try:
        return rows.get(id=folder_id)
    except Folder.DoesNotExist as error:
        raise Http404 from error


@transaction.atomic
def update_folder(*, actor_id, folder_id, title=UNSET, position=UNSET):
    row = get_folder(actor_id=actor_id, folder_id=folder_id, for_update=True)
    changed_fields = ["updated_at"]
    if title is not UNSET:
        row.title = title.strip()
        changed_fields.append("title")
    if position is not UNSET:
        row.position = position
        changed_fields.append("position")
    row.save(update_fields=changed_fields)
    return row


@transaction.atomic
def delete_folder(*, actor_id, folder_id, item_resolution=None):
    row = get_folder(actor_id=actor_id, folder_id=folder_id, for_update=True)
    child_lists = list(
        List.objects.select_for_update().filter(folder=row, is_trashed=False).order_by("id")
    )
    if child_lists and item_resolution not in {"move_to_inbox", "trash"}:
        raise ChildResolutionRequired
    for child in child_lists:
        delete_list(
            actor_id=actor_id,
            list_id=child.id,
            item_resolution=item_resolution,
        )
    row.is_trashed = True
    row.trashed_at = timezone.now()
    row.save(update_fields=["is_trashed", "trashed_at", "updated_at"])


@transaction.atomic
def create_list(*, actor_id, title, folder_id=None):
    folder = None
    if folder_id is not None:
        try:
            folder = Folder.objects.filter(owner_id=actor_id, is_trashed=False).get(id=folder_id)
        except Folder.DoesNotExist as error:
            raise Http404 from error
    row = List.objects.create(
        owner_id=actor_id,
        folder=folder,
        title=title.strip(),
        position=List.objects.filter(owner_id=actor_id, is_trashed=False).count(),
    )
    Column.objects.create(list=row, title="not_sectioned", is_default=True)
    return get_list(actor_id=actor_id, list_id=row.id)


def get_list(*, actor_id, list_id, for_update=False):
    rows = List.objects.filter(owner_id=actor_id, is_trashed=False).prefetch_related("columns")
    if for_update:
        rows = rows.select_for_update()
    try:
        return rows.get(id=list_id)
    except List.DoesNotExist as error:
        raise Http404 from error


@transaction.atomic
def update_list(*, actor_id, list_id, title=UNSET, folder_id=UNSET, position=UNSET):
    row = get_list(actor_id=actor_id, list_id=list_id, for_update=True)
    if row.is_inbox and title is not UNSET:
        raise ImmutableInbox
    changed_fields = ["updated_at"]
    if title is not UNSET:
        row.title = title.strip()
        changed_fields.append("title")
    if folder_id is not UNSET:
        if folder_id is None:
            row.folder = None
        else:
            row.folder = get_folder(actor_id=actor_id, folder_id=folder_id, for_update=True)
        changed_fields.append("folder")
    if position is not UNSET:
        row.position = position
        changed_fields.append("position")
    row.save(update_fields=changed_fields)
    return get_list(actor_id=actor_id, list_id=row.id)


@transaction.atomic
def delete_list(*, actor_id, list_id, item_resolution=None):
    row = get_list(actor_id=actor_id, list_id=list_id, for_update=True)
    if row.is_inbox:
        raise ImmutableInbox
    from dotick.items.models import Item

    active_items = Item.objects.filter(column__list=row, is_trashed=False)
    if active_items.exists():
        if item_resolution not in {"move_to_inbox", "trash"}:
            raise ChildResolutionRequired
        inbox_column = Column.objects.get(
            list__owner_id=actor_id,
            list__is_inbox=True,
            list__is_trashed=False,
            is_default=True,
        )
        now = timezone.now()
        if item_resolution == "move_to_inbox":
            active_items.update(column=inbox_column, version=F("version") + 1, updated_at=now)
        else:
            active_items.update(
                column=inbox_column,
                is_trashed=True,
                trashed_at=now,
                trash_origin_column_id=F("column_id"),
                version=F("version") + 1,
                updated_at=now,
            )
    trash_list(row)


def list_trashed_lists(*, actor_id):
    return (
        List.objects.filter(owner_id=actor_id, is_trashed=True)
        .prefetch_related("columns")
        .order_by("-trashed_at", "-id")
    )


def list_trashed_folders(*, actor_id):
    return Folder.objects.filter(owner_id=actor_id, is_trashed=True).order_by("-trashed_at", "-id")


def _restore_list_row(row):
    from dotick.items.models import Item

    if row.folder_id is not None and row.folder.is_trashed:
        row.folder = None
    row.is_trashed = False
    row.trashed_at = None
    row.save(update_fields=["folder", "is_trashed", "trashed_at", "updated_at"])
    columns = list(row.columns.values_list("id", flat=True))
    now = timezone.now()
    Item.objects.filter(
        owner=row.owner,
        is_trashed=True,
        trash_origin_column_id__in=columns,
    ).update(
        column_id=F("trash_origin_column_id"),
        is_trashed=False,
        trashed_at=None,
        trash_origin_column_id=None,
        version=F("version") + 1,
        updated_at=now,
    )


@transaction.atomic
def restore_list(*, actor_id, list_id):
    try:
        row = (
            List.objects.select_for_update()
            .select_related("folder")
            .prefetch_related("columns")
            .get(id=list_id, owner_id=actor_id, is_trashed=True)
        )
    except List.DoesNotExist as error:
        raise Http404 from error
    _restore_list_row(row)
    return get_list(actor_id=actor_id, list_id=row.id)


@transaction.atomic
def restore_folder(*, actor_id, folder_id):
    try:
        row = Folder.objects.select_for_update().get(
            id=folder_id,
            owner_id=actor_id,
            is_trashed=True,
        )
    except Folder.DoesNotExist as error:
        raise Http404 from error
    row.is_trashed = False
    row.trashed_at = None
    row.save(update_fields=["is_trashed", "trashed_at", "updated_at"])
    children = (
        List.objects.select_for_update()
        .select_related("folder")
        .prefetch_related("columns")
        .filter(folder=row, is_trashed=True)
    )
    for child in children:
        _restore_list_row(child)
    return row


def list_columns(*, actor_id, list_id):
    row = get_list(actor_id=actor_id, list_id=list_id)
    return row.columns.order_by("position", "created_at")


@transaction.atomic
def create_column(*, actor_id, list_id, title):
    row = get_list(actor_id=actor_id, list_id=list_id, for_update=True)
    return Column.objects.create(
        list=row,
        title=title.strip(),
        position=row.columns.count(),
    )


def get_column(*, actor_id, column_id, for_update=False):
    rows = Column.objects.filter(list__owner_id=actor_id, list__is_trashed=False)
    if for_update:
        rows = rows.select_for_update()
    try:
        return rows.get(id=column_id)
    except Column.DoesNotExist as error:
        raise Http404 from error


@transaction.atomic
def update_column(*, actor_id, column_id, title=UNSET, position=UNSET):
    row = get_column(actor_id=actor_id, column_id=column_id, for_update=True)
    changed_fields = ["updated_at"]
    if title is not UNSET:
        row.title = title.strip()
        changed_fields.append("title")
    if position is not UNSET:
        row.position = position
        changed_fields.append("position")
    row.save(update_fields=changed_fields)
    return row


@transaction.atomic
def delete_column(*, actor_id, column_id, item_resolution=None):
    row = get_column(actor_id=actor_id, column_id=column_id, for_update=True)
    if row.is_default:
        raise ImmutableDefaultColumn
    from dotick.items.models import Item

    active_items = Item.objects.filter(column=row, is_trashed=False)
    if active_items.exists():
        if item_resolution not in {"move_to_default", "trash"}:
            raise ChildResolutionRequired
        default_column = Column.objects.get(list=row.list, is_default=True)
        now = timezone.now()
        if item_resolution == "move_to_default":
            active_items.update(column=default_column, version=F("version") + 1, updated_at=now)
        else:
            active_items.update(
                column=default_column,
                is_trashed=True,
                trashed_at=now,
                trash_origin_column_id=row.id,
                version=F("version") + 1,
                updated_at=now,
            )
    row.delete()
