from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from dotick.identity.sessions import create_auth_session
from dotick.items.models import Item, ItemSource
from dotick.organization.application import create_list
from dotick.organization.models import Column, Folder, List
from rest_framework.test import APIClient

FOLDERS_URL = "/api/v1/folders"
TRASHED_FOLDERS_URL = "/api/v1/trash/folders"
pytestmark = pytest.mark.django_db


def _user(email):
    return get_user_model().objects.create_user(
        email=email,
        password="Only-for-automated-tests-8!",
    )


def _authenticated_client(user):
    _, pair = create_auth_session(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {pair.access}")
    return client


def _trash_folder(client, folder_id, version, *, items=None):
    url = f"{FOLDERS_URL}/{folder_id}"
    if items is not None:
        url += f"?items={items}"
    return client.delete(url, HTTP_IF_MATCH=str(version))


def _restore_folder(client, folder_id, version):
    return client.post(
        f"{FOLDERS_URL}/{folder_id}/restore",
        {"version": version},
        format="json",
    )


def test_folder_create_list_get_and_update_follow_the_public_contract():
    user = _user("folder-crud@example.test")
    client = _authenticated_client(user)

    first = client.post(FOLDERS_URL, {"title": "  Work  "}, format="json")
    second = client.post(FOLDERS_URL, {"title": "Work"}, format="json")

    assert first.status_code == 201
    assert second.status_code == 201
    assert first.json() == {
        "id": str(Folder.objects.get(owner=user, position=0).id),
        "title": "Work",
        "position": 0,
        "version": 1,
        "is_trashed": False,
        "trashed_at": None,
    }
    assert second.json()["id"] != first.json()["id"]
    assert second.json()["position"] == 1
    assert second.json()["version"] == 1

    listed = client.get(FOLDERS_URL)
    retrieved = client.get(f"{FOLDERS_URL}/{first.json()['id']}")
    updated = client.patch(
        f"{FOLDERS_URL}/{first.json()['id']}",
        {"version": 1, "title": "Projects", "position": 7},
        format="json",
    )

    assert listed.status_code == 200
    assert [row["id"] for row in listed.json()["results"]] == [
        first.json()["id"],
        second.json()["id"],
    ]
    assert retrieved.status_code == 200
    assert retrieved.json() == first.json()
    assert updated.status_code == 200
    assert updated.json()["title"] == "Projects"
    assert updated.json()["position"] == 7
    assert updated.json()["version"] == 2


def test_folder_update_requires_version_and_rejects_invalid_input():
    user = _user("folder-validation@example.test")
    client = _authenticated_client(user)

    assert APIClient().get(FOLDERS_URL).status_code == 401
    assert client.post(FOLDERS_URL, {"title": "  "}, format="json").status_code == 400
    assert (
        client.post(
            FOLDERS_URL,
            {"title": "Valid", "owner_user_id": str(user.id)},
            format="json",
        ).status_code
        == 400
    )

    folder_id = client.post(FOLDERS_URL, {"title": "Valid"}, format="json").json()["id"]
    assert client.patch(f"{FOLDERS_URL}/{folder_id}", {}, format="json").status_code == 400
    assert (
        client.patch(
            f"{FOLDERS_URL}/{folder_id}",
            {"title": "Missing version"},
            format="json",
        ).status_code
        == 400
    )
    assert (
        client.patch(
            f"{FOLDERS_URL}/{folder_id}",
            {"version": 1},
            format="json",
        ).status_code
        == 400
    )
    assert (
        client.patch(
            f"{FOLDERS_URL}/{folder_id}",
            {"version": 1, "position": -1},
            format="json",
        ).status_code
        == 400
    )


def test_folder_update_rejects_stale_version_without_overwrite():
    user = _user("folder-stale-update@example.test")
    client = _authenticated_client(user)
    created = client.post(FOLDERS_URL, {"title": "Original"}, format="json").json()

    first_update = client.patch(
        f"{FOLDERS_URL}/{created['id']}",
        {"version": 1, "title": "Current"},
        format="json",
    )
    stale = client.patch(
        f"{FOLDERS_URL}/{created['id']}",
        {"version": 1, "title": "Stale overwrite"},
        format="json",
    )

    assert first_update.status_code == 200
    assert first_update.json()["version"] == 2
    assert stale.status_code == 409
    assert stale.json()["error"]["code"] == "version_conflict"
    assert stale.json()["error"]["details"]["current"] == {
        "id": created["id"],
        "version": 2,
    }
    row = Folder.objects.get(pk=created["id"])
    assert row.title == "Current"
    assert row.version == 2


def test_folder_reads_and_writes_are_owner_scoped_and_hide_trashed_rows():
    owner = _user("folder-owner@example.test")
    other = _user("folder-other@example.test")
    folder = Folder.objects.create(owner=owner, title="Private")
    Folder.objects.create(
        owner=owner,
        title="Trashed",
        is_trashed=True,
        trashed_at="2026-09-15T00:00:00Z",
    )
    client = _authenticated_client(other)

    assert client.get(f"{FOLDERS_URL}/{folder.id}").status_code == 404
    assert (
        client.patch(
            f"{FOLDERS_URL}/{folder.id}",
            {"version": 1, "title": "Taken"},
            format="json",
        ).status_code
        == 404
    )
    assert _trash_folder(client, folder.id, 1).status_code == 404
    assert _restore_folder(client, folder.id, 1).status_code == 404
    assert client.get(FOLDERS_URL).json() == {"results": []}
    folder.refresh_from_db()
    assert folder.title == "Private"
    assert folder.version == 1
    assert folder.is_trashed is False


def test_folder_trash_and_restore_require_versions_and_increment_them():
    user = _user("folder-trash@example.test")
    client = _authenticated_client(user)
    created = client.post(FOLDERS_URL, {"title": "Recoverable"}, format="json").json()

    missing_precondition = client.delete(f"{FOLDERS_URL}/{created['id']}")
    assert missing_precondition.status_code == 400

    deleted = _trash_folder(client, created["id"], created["version"])

    assert deleted.status_code == 204
    assert deleted.content == b""
    assert client.get(f"{FOLDERS_URL}/{created['id']}").status_code == 404
    assert client.get(FOLDERS_URL).json() == {"results": []}
    row = Folder.objects.get(pk=created["id"])
    assert row.is_trashed is True
    assert row.trashed_at is not None
    assert row.version == 2

    assert (
        client.post(
            f"{FOLDERS_URL}/{created['id']}/restore",
            {},
            format="json",
        ).status_code
        == 400
    )

    restored = _restore_folder(client, created["id"], row.version)

    assert restored.status_code == 200
    assert restored.json()["id"] == created["id"]
    assert restored.json()["is_trashed"] is False
    assert restored.json()["trashed_at"] is None
    assert restored.json()["version"] == 3
    assert client.get(f"{FOLDERS_URL}/{created['id']}").status_code == 200


def test_folder_trash_rejects_stale_version_without_mutation():
    user = _user("folder-stale-trash@example.test")
    client = _authenticated_client(user)
    created = client.post(FOLDERS_URL, {"title": "Project"}, format="json").json()
    updated = client.patch(
        f"{FOLDERS_URL}/{created['id']}",
        {"version": 1, "title": "Current"},
        format="json",
    ).json()

    stale = _trash_folder(client, created["id"], 1)

    assert stale.status_code == 409
    assert stale.json()["error"]["code"] == "version_conflict"
    assert stale.json()["error"]["details"]["current"]["version"] == 2
    row = Folder.objects.get(pk=created["id"])
    assert row.is_trashed is False
    assert row.version == updated["version"] == 2


def test_folder_restore_rejects_stale_version_without_mutation():
    user = _user("folder-stale-restore@example.test")
    client = _authenticated_client(user)
    created = client.post(FOLDERS_URL, {"title": "Project"}, format="json").json()
    assert _trash_folder(client, created["id"], 1).status_code == 204

    stale = _restore_folder(client, created["id"], 1)

    assert stale.status_code == 409
    assert stale.json()["error"]["code"] == "version_conflict"
    assert stale.json()["error"]["details"]["current"]["version"] == 2
    row = Folder.objects.get(pk=created["id"])
    assert row.is_trashed is True
    assert row.version == 2


def test_folder_trash_and_restore_are_state_and_owner_scoped():
    owner = _user("folder-trash-owner@example.test")
    other = _user("folder-trash-other@example.test")
    folder = Folder.objects.create(owner=owner, title="Private")
    other_client = _authenticated_client(other)

    assert _trash_folder(other_client, folder.id, 1).status_code == 404
    assert _restore_folder(other_client, folder.id, 1).status_code == 404
    folder.refresh_from_db()
    assert folder.is_trashed is False

    owner_client = _authenticated_client(owner)
    assert _trash_folder(owner_client, folder.id, 1).status_code == 204
    assert _trash_folder(owner_client, folder.id, 2).status_code == 404
    assert (
        owner_client.post(
            f"{FOLDERS_URL}/{folder.id}/restore",
            {"version": 2, "unexpected": True},
            format="json",
        ).status_code
        == 400
    )
    assert _restore_folder(other_client, folder.id, 2).status_code == 404


def test_trashed_folder_listing_is_owned_separate_and_newest_first():
    owner = _user("trashed-folder-list@example.test")
    other = _user("trashed-folder-list-other@example.test")
    client = _authenticated_client(owner)
    older = Folder.objects.create(
        owner=owner,
        title="Older",
        is_trashed=True,
        trashed_at=timezone.now() - timedelta(days=1),
        version=2,
    )
    newer = Folder.objects.create(
        owner=owner,
        title="Newer",
        is_trashed=True,
        trashed_at=timezone.now(),
        version=3,
    )
    Folder.objects.create(
        owner=other,
        title="Foreign",
        is_trashed=True,
        trashed_at=timezone.now(),
    )
    Folder.objects.create(owner=owner, title="Active")

    response = client.get(TRASHED_FOLDERS_URL)

    assert response.status_code == 200
    assert [row["id"] for row in response.json()["results"]] == [
        str(newer.id),
        str(older.id),
    ]
    assert [row["version"] for row in response.json()["results"]] == [3, 2]
    assert all(row["is_trashed"] is True for row in response.json()["results"])
    assert all(row["trashed_at"] is not None for row in response.json()["results"])
    assert APIClient().get(TRASHED_FOLDERS_URL).status_code == 401


def _item(*, owner, column, title, operation_id):
    row = Item.objects.create(
        kind=Item.Kind.TASK,
        owner=owner,
        created_by=owner,
        column=column,
        title=title,
        creation_operation_id=operation_id,
        creation_intent_digest="0" * 64,
    )
    ItemSource.objects.create(item=row, platform=ItemSource.Platform.MANUAL)
    return row


def test_folder_delete_preserves_child_resolution_and_versions_affected_lists():
    user = _user("folder-move-items@example.test")
    client = _authenticated_client(user)
    client.put("/api/v1/account/bootstrap", {"timezone": "Europe/Berlin"}, format="json")
    inbox_column = Column.objects.get(list__owner=user, list__is_inbox=True, is_default=True)
    folder = Folder.objects.create(owner=user, title="Project")
    child_list, child_column = create_list(owner=user, folder=folder, title="Launch")
    item = _item(
        owner=user,
        column=child_column,
        title="Ship",
        operation_id="00000000-0000-0000-0000-000000000401",
    )

    missing = _trash_folder(client, folder.id, 1)
    invalid = _trash_folder(client, folder.id, 1, items="delete")

    assert missing.status_code == 409
    assert missing.json()["error"]["code"] == "child_resolution_required"
    assert invalid.status_code == 409
    folder.refresh_from_db()
    child_list.refresh_from_db()
    item.refresh_from_db()
    assert folder.is_trashed is False
    assert folder.version == 1
    assert child_list.is_trashed is False
    assert child_list.version == 1
    assert item.column_id == child_column.id
    assert item.version == 1

    moved = _trash_folder(client, folder.id, 1, items="move_to_inbox")

    assert moved.status_code == 204
    folder.refresh_from_db()
    child_list.refresh_from_db()
    item.refresh_from_db()
    assert folder.is_trashed is True
    assert folder.version == 2
    assert child_list.is_trashed is True
    assert child_list.version == 2
    assert item.is_trashed is False
    assert item.column_id == inbox_column.id
    assert item.version == 2

    restored = _restore_folder(client, folder.id, 2)
    assert restored.status_code == 200
    assert restored.json()["version"] == 3
    child_list.refresh_from_db()
    item.refresh_from_db()
    assert child_list.is_trashed is False
    assert child_list.version == 3
    assert item.column_id == inbox_column.id
    assert item.version == 2


def test_folder_delete_can_trash_and_restore_its_item_subtree_with_versions():
    user = _user("folder-trash-items@example.test")
    client = _authenticated_client(user)
    client.put("/api/v1/account/bootstrap", {"timezone": "Europe/Berlin"}, format="json")
    inbox_column = Column.objects.get(list__owner=user, list__is_inbox=True, is_default=True)
    folder = Folder.objects.create(owner=user, title="Project")
    child_list, child_column = create_list(owner=user, folder=folder, title="Launch")
    item = _item(
        owner=user,
        column=child_column,
        title="Recover me",
        operation_id="00000000-0000-0000-0000-000000000402",
    )

    deleted = _trash_folder(client, folder.id, 1, items="trash")

    assert deleted.status_code == 204
    folder.refresh_from_db()
    child_list.refresh_from_db()
    item.refresh_from_db()
    assert folder.version == 2
    assert child_list.is_trashed is True
    assert child_list.version == 2
    assert item.is_trashed is True
    assert item.trashed_at is not None
    assert item.trash_origin_column_id == child_column.id
    assert item.column_id == inbox_column.id
    assert item.version == 2

    restored = _restore_folder(client, folder.id, 2)

    assert restored.status_code == 200
    assert restored.json()["version"] == 3
    child_list.refresh_from_db()
    item.refresh_from_db()
    assert child_list.is_trashed is False
    assert child_list.version == 3
    assert item.is_trashed is False
    assert item.trashed_at is None
    assert item.trash_origin_column_id is None
    assert item.column_id == child_column.id
    assert item.version == 3


def test_folder_restore_does_not_revive_or_reversion_earlier_trashed_children():
    user = _user("folder-restore-scope@example.test")
    client = _authenticated_client(user)
    folder = Folder.objects.create(owner=user, title="Project")
    child_list, _ = create_list(owner=user, folder=folder, title="Already trashed")
    earlier = timezone.now() - timedelta(days=1)
    List.objects.filter(pk=child_list.pk).update(is_trashed=True, trashed_at=earlier)

    assert _trash_folder(client, folder.id, 1).status_code == 204
    assert _restore_folder(client, folder.id, 2).status_code == 200

    child_list.refresh_from_db()
    assert child_list.is_trashed is True
    assert child_list.trashed_at == earlier
    assert child_list.version == 1
