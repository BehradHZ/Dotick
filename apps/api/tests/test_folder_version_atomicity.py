from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from dotick.organization import application
from dotick.organization.models import Folder, List

pytestmark = pytest.mark.django_db


def _user(email):
    return get_user_model().objects.create_user(
        email=email,
        password="Only-for-automated-tests-8!",
    )


def test_folder_trash_rolls_back_descendant_list_changes_if_folder_write_fails():
    owner = _user("folder-trash-atomic@example.test")
    folder = Folder.objects.create(owner=owner, title="Project")
    child, _ = application.create_list(owner=owner, folder=folder, title="Launch")

    with patch.object(
        application,
        "increment_locked_version",
        side_effect=RuntimeError("folder write failed"),
    ):
        with pytest.raises(RuntimeError, match="folder write failed"):
            application.trash_folder(
                actor_id=owner.id,
                folder_id=folder.id,
                version=1,
            )

    folder.refresh_from_db()
    child.refresh_from_db()
    assert folder.is_trashed is False
    assert folder.version == 1
    assert child.is_trashed is False
    assert child.version == 1


def test_folder_restore_rolls_back_descendant_list_changes_if_folder_write_fails():
    owner = _user("folder-restore-atomic@example.test")
    folder = Folder.objects.create(owner=owner, title="Project")
    child, _ = application.create_list(owner=owner, folder=folder, title="Launch")
    application.trash_folder(
        actor_id=owner.id,
        folder_id=folder.id,
        version=1,
    )

    folder.refresh_from_db()
    child.refresh_from_db()
    assert folder.is_trashed is True
    assert folder.version == 2
    assert child.is_trashed is True
    assert child.version == 2

    with patch.object(
        application,
        "increment_locked_version",
        side_effect=RuntimeError("folder write failed"),
    ):
        with pytest.raises(RuntimeError, match="folder write failed"):
            application.restore_folder(
                actor_id=owner.id,
                folder_id=folder.id,
                version=2,
            )

    folder.refresh_from_db()
    child.refresh_from_db()
    assert folder.is_trashed is True
    assert folder.version == 2
    assert child.is_trashed is True
    assert child.version == 2


def test_folder_restore_only_versions_lists_mutated_by_that_restore():
    owner = _user("folder-restore-list-scope@example.test")
    folder = Folder.objects.create(owner=owner, title="Project")
    active_child, _ = application.create_list(owner=owner, folder=folder, title="Active")
    earlier_child, _ = application.create_list(owner=owner, folder=folder, title="Earlier")
    List.objects.filter(pk=earlier_child.pk).update(
        is_trashed=True,
        trashed_at="2026-09-17T00:00:00Z",
    )

    application.trash_folder(
        actor_id=owner.id,
        folder_id=folder.id,
        version=1,
    )
    application.restore_folder(
        actor_id=owner.id,
        folder_id=folder.id,
        version=2,
    )

    active_child.refresh_from_db()
    earlier_child.refresh_from_db()
    assert active_child.is_trashed is False
    assert active_child.version == 3
    assert earlier_child.is_trashed is True
    assert earlier_child.version == 1
