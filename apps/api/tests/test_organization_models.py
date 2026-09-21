import uuid

import pytest
from django.apps import apps
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from dotick.organization.models import Column, Folder, List

pytestmark = pytest.mark.django_db


def _user(email):
    return get_user_model().objects.create_user(
        email=email,
        password="Only-for-automated-tests-8!",
    )


def test_folder_list_and_column_have_increment_one_persistence_shape():
    user = _user("organization-shape@example.test")
    folder = Folder.objects.create(owner=user, title="Work", position=2)
    row = List.objects.create(owner=user, folder=folder, title="Backend", position=3)
    column = Column.objects.create(list=row, title="Tasks", position=4, is_default=True)

    assert isinstance(folder.id, uuid.UUID)
    assert folder.owner == user
    assert folder.is_trashed is False
    assert folder.trashed_at is None
    assert folder.version == 1
    assert folder.created_at is not None and folder.updated_at is not None

    assert isinstance(row.id, uuid.UUID)
    assert row.owner == user
    assert row.folder == folder
    assert row.is_inbox is False
    assert row.is_trashed is False
    assert row.trashed_at is None
    assert row.version == 1
    assert row.created_at is not None and row.updated_at is not None

    assert isinstance(column.id, uuid.UUID)
    assert column.list == row
    assert column.is_default is True
    assert column.version == 1
    assert column.created_at is not None and column.updated_at is not None


def test_organization_versions_must_remain_positive():
    user = _user("positive-organization-version@example.test")
    folder = Folder.objects.create(owner=user, title="Work")
    row = List.objects.create(owner=user, folder=folder, title="Backend")

    with pytest.raises(IntegrityError), transaction.atomic():
        Folder.objects.create(owner=user, title="Invalid Folder", version=0)

    with pytest.raises(IntegrityError), transaction.atomic():
        List.objects.create(owner=user, title="Invalid List", version=0)

    with pytest.raises(IntegrityError), transaction.atomic():
        Column.objects.create(list=row, title="Invalid Column", version=0)


def test_folder_is_optional_for_lists():
    user = _user("folderless-list@example.test")

    row = List.objects.create(owner=user, title="Folderless")

    assert row.folder is None


def test_database_allows_at_most_one_inbox_per_user():
    user = _user("one-inbox@example.test")
    List.objects.create(owner=user, title="Inbox", is_inbox=True)

    with pytest.raises(IntegrityError), transaction.atomic():
        List.objects.create(owner=user, title="Another Inbox", is_inbox=True)


def test_database_allows_at_most_one_default_column_per_list():
    user = _user("one-default-column@example.test")
    row = List.objects.create(owner=user, title="List")
    Column.objects.create(list=row, title="Default", is_default=True)

    with pytest.raises(IntegrityError), transaction.atomic():
        Column.objects.create(list=row, title="Second default", is_default=True)


def test_tab_and_section_are_not_organization_entities():
    with pytest.raises(LookupError):
        apps.get_model("organization", "Tab")
    with pytest.raises(LookupError):
        apps.get_model("organization", "Section")
