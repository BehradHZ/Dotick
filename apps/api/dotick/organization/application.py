from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import F
from django.http import Http404
from django.utils import timezone
from rest_framework.exceptions import APIException

from dotick.identity.models import UserPreferences
from dotick.organization.models import Column, Folder, List

DEFAULT_COLUMN_TITLE = "Items"
UNSET = object()


class ChildResolutionRequired(APIException):
    status_code = 409
    default_detail = "Choose how active descendant Items should be handled."
    default_code = "child_resolution_required"


class ImmutableInbox(APIException):
    status_code = 409
    default_detail = "Inbox cannot be renamed."
    default_code = "immutable_inbox"


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
def update_folder(*, actor_id, folder_id, title=UNSET, position=UNSET):
    row = get_folder(actor_id=actor_id, folder_id=folder_id, for_update=True)
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
def trash_folder(*, actor_id, folder_id, item_resolution=None):
    from dotick.items.models import Item

    row = get_folder(actor_id=actor_id, folder_id=folder_id, for_update=True)
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
            updated_at=now,
        )
    row.is_trashed = True
    row.trashed_at = now
    row.save(update_fields=["is_trashed", "trashed_at", "updated_at"])


@transaction.atomic
def restore_folder(*, actor_id, folder_id):
    from dotick.items.models import Item

    try:
        row = Folder.objects.select_for_update().get(
            pk=folder_id,
            owner_id=actor_id,
            is_trashed=True,
        )
    except Folder.DoesNotExist as error:
        raise Http404 from error
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
    if child_lists:
        List.objects.filter(pk__in=[child.pk for child in child_lists]).update(
            is_trashed=False,
            trashed_at=None,
            updated_at=timezone.now(),
        )
    if item_ids:
        Item.objects.filter(pk__in=item_ids).update(
            column_id=F("trash_origin_column_id"),
            is_trashed=False,
            trashed_at=None,
            trash_origin_column_id=None,
            version=F("version") + 1,
            updated_at=timezone.now(),
        )
    row.is_trashed = False
    row.trashed_at = None
    row.save(update_fields=["is_trashed", "trashed_at", "updated_at"])
    return row


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
def update_list(*, actor_id, list_id, title=UNSET, folder_id=UNSET, position=UNSET):
    row = get_list(actor_id=actor_id, list_id=list_id, for_update=True)
    if row.is_inbox and title is not UNSET:
        raise ImmutableInbox

    changed_fields = ["updated_at"]
    if title is not UNSET:
        row.title = _normalized_title(title)
        changed_fields.append("title")
    if folder_id is not UNSET:
        row.folder = (
            None
            if folder_id is None
            else get_folder(
                actor_id=actor_id,
                folder_id=folder_id,
                for_update=True,
            )
        )
        changed_fields.append("folder")
    if position is not UNSET:
        row.position = position
        changed_fields.append("position")
    row.save(update_fields=changed_fields)
    return get_list(actor_id=actor_id, list_id=row.id)


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
