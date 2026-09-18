from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model

from dotick.items.models import Item, ItemSource
from dotick.organization.application import create_list, restore_list, trash_list
from dotick.organization.models import Column, List

pytestmark = pytest.mark.django_db


def _user(email):
    return get_user_model().objects.create_user(
        email=email,
        password="Only-for-automated-tests-8!",
    )


def _item(*, owner, column, operation_id):
    row = Item.objects.create(
        kind=Item.Kind.TASK,
        owner=owner,
        created_by=owner,
        column=column,
        title="Atomic child",
        creation_operation_id=operation_id,
        creation_intent_digest="0" * 64,
    )
    ItemSource.objects.create(item=row, platform=ItemSource.Platform.MANUAL)
    return row


def _inbox(owner):
    inbox = List.objects.create(owner=owner, title="Inbox", is_inbox=True)
    return Column.objects.create(list=inbox, title="Items", is_default=True)


def test_list_trash_rolls_back_task_mutations_when_parent_version_write_fails():
    owner = _user("list-atomic-trash@example.test")
    inbox_column = _inbox(owner)
    row, column = create_list(owner=owner, title="Project")
    item = _item(
        owner=owner,
        column=column,
        operation_id="00000000-0000-0000-0000-000000000591",
    )

    with patch(
        "dotick.organization.application.increment_locked_version",
        side_effect=RuntimeError("parent write failed"),
    ):
        with pytest.raises(RuntimeError, match="parent write failed"):
            trash_list(
                actor_id=owner.id,
                list_id=row.id,
                version=1,
                item_resolution="trash",
            )

    row.refresh_from_db()
    item.refresh_from_db()
    assert row.is_trashed is False
    assert row.version == 1
    assert item.column_id == column.id
    assert item.column_id != inbox_column.id
    assert item.is_trashed is False
    assert item.version == 1


def test_list_restore_rolls_back_task_mutations_when_parent_version_write_fails():
    owner = _user("list-atomic-restore@example.test")
    _inbox(owner)
    row, column = create_list(owner=owner, title="Project")
    item = _item(
        owner=owner,
        column=column,
        operation_id="00000000-0000-0000-0000-000000000592",
    )
    trash_list(
        actor_id=owner.id,
        list_id=row.id,
        version=1,
        item_resolution="trash",
    )

    with patch(
        "dotick.organization.application.increment_locked_version",
        side_effect=RuntimeError("parent write failed"),
    ):
        with pytest.raises(RuntimeError, match="parent write failed"):
            restore_list(actor_id=owner.id, list_id=row.id, version=2)

    row.refresh_from_db()
    item.refresh_from_db()
    assert row.is_trashed is True
    assert row.version == 2
    assert item.is_trashed is True
    assert item.version == 2
