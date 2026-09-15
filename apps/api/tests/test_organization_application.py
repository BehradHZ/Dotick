from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model

from dotick.organization.application import (
    DEFAULT_COLUMN_TITLE,
    create_folder,
    create_list,
)
from dotick.organization.models import Column, Folder, List

pytestmark = pytest.mark.django_db


def _user(email):
    return get_user_model().objects.create_user(
        email=email,
        password="Only-for-automated-tests-8!",
    )


def test_create_folder_uses_owned_manual_order_and_normalized_title():
    user = _user("create-folder@example.test")

    folder = create_folder(owner=user, title="  Work  ")

    assert folder.owner == user
    assert folder.title == "Work"
    assert folder.position == 0


def test_create_list_creates_exactly_one_default_column_without_legacy_name():
    user = _user("create-list@example.test")
    folder = create_folder(owner=user, title="Work")

    row, default_column = create_list(owner=user, folder=folder, title="  Backend  ")

    assert row.owner == user
    assert row.folder == folder
    assert row.title == "Backend"
    assert row.columns.count() == 1
    assert default_column.is_default is True
    assert default_column.position == 0
    assert default_column.title == DEFAULT_COLUMN_TITLE
    assert default_column.title != "not_sectioned"


def test_list_and_default_column_creation_is_atomic():
    user = _user("atomic-list@example.test")

    with patch.object(Column.objects, "create", side_effect=RuntimeError("column write failed")):
        with pytest.raises(RuntimeError, match="column write failed"):
            create_list(owner=user, title="Must roll back")

    assert not List.objects.filter(owner=user).exists()


def test_list_cannot_use_another_users_folder():
    owner = _user("list-owner@example.test")
    other = _user("folder-owner@example.test")
    foreign_folder = Folder.objects.create(owner=other, title="Foreign")

    with pytest.raises(Folder.DoesNotExist):
        create_list(owner=owner, title="Rejected", folder=foreign_folder)

    assert not List.objects.filter(owner=owner).exists()
