from django.contrib.auth import get_user_model
from django.db import transaction
from django.http import Http404
from django.utils import timezone

from dotick.identity.models import UserPreferences
from dotick.organization.models import Column, Folder, List

DEFAULT_COLUMN_TITLE = "Items"
UNSET = object()


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
def trash_folder(*, actor_id, folder_id):
    row = get_folder(actor_id=actor_id, folder_id=folder_id, for_update=True)
    row.is_trashed = True
    row.trashed_at = timezone.now()
    row.save(update_fields=["is_trashed", "trashed_at", "updated_at"])


@transaction.atomic
def restore_folder(*, actor_id, folder_id):
    try:
        row = Folder.objects.select_for_update().get(
            pk=folder_id,
            owner_id=actor_id,
            is_trashed=True,
        )
    except Folder.DoesNotExist as error:
        raise Http404 from error
    row.is_trashed = False
    row.trashed_at = None
    row.save(update_fields=["is_trashed", "trashed_at", "updated_at"])
    return row


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
