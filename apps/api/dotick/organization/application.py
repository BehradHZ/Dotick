from django.db import transaction

from dotick.organization.models import Column, Folder, List

DEFAULT_COLUMN_TITLE = "Items"


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
