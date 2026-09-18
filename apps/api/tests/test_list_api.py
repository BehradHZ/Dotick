import uuid
from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from dotick.identity.sessions import create_auth_session
from dotick.items.models import Item, ItemSource
from dotick.organization.application import create_list as _create_list
from dotick.organization.models import Column, Folder, List
from rest_framework.test import APIClient

BOOTSTRAP_URL = "/api/v1/account/bootstrap"
FOLDERS_URL = "/api/v1/folders"
LISTS_URL = "/api/v1/lists"
TRASHED_LISTS_URL = "/api/v1/trash/lists"
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


def _create_folder(client, title):
    return client.post(
        FOLDERS_URL,
        {"title": title, "operation_id": str(uuid.uuid4())},
        format="json",
    )


def _create_public_list(client, title, **extra):
    payload = {"title": title, "operation_id": str(uuid.uuid4()), **extra}
    return client.post(LISTS_URL, payload, format="json")


def _trash_list(client, list_id, version, *, items=None):
    url = f"{LISTS_URL}/{list_id}"
    if items is not None:
        url += f"?items={items}"
    return client.delete(url, HTTP_IF_MATCH=str(version))


def _restore_list(client, list_id, version):
    return client.post(
        f"{LISTS_URL}/{list_id}/restore",
        {"version": version},
        format="json",
    )


def test_list_create_list_get_and_update_follow_the_public_contract():
    user = _user("list-crud@example.test")
    client = _authenticated_client(user)
    inbox = client.put(
        BOOTSTRAP_URL,
        {"timezone": "Europe/Berlin"},
        format="json",
    ).json()["inbox"]
    first_folder = _create_folder(client, "First").json()
    second_folder = _create_folder(client, "Second").json()

    first = _create_public_list(
        client,
        "  Personal  ",
        folder_id=first_folder["id"],
    )
    duplicate = _create_public_list(client, "Personal")

    assert first.status_code == 201
    assert duplicate.status_code == 201
    assert first.json()["id"] != duplicate.json()["id"]
    assert first.json()["title"] == duplicate.json()["title"] == "Personal"
    assert first.json()["folder_id"] == first_folder["id"]
    assert duplicate.json()["folder_id"] is None
    assert first.json()["position"] == 1
    assert first.json()["version"] == 1
    assert first.json()["is_inbox"] is False
    assert first.json()["is_trashed"] is False
    assert first.json()["trashed_at"] is None
    assert first.json()["default_column"]["is_default"] is True
    assert Column.objects.filter(list_id=first.json()["id"], is_default=True).count() == 1

    listed = client.get(LISTS_URL)
    retrieved = client.get(f"{LISTS_URL}/{first.json()['id']}")
    updated = client.patch(
        f"{LISTS_URL}/{first.json()['id']}",
        {
            "version": 1,
            "title": "Projects",
            "folder_id": second_folder["id"],
            "position": 9,
        },
        format="json",
    )
    folderless = client.patch(
        f"{LISTS_URL}/{first.json()['id']}",
        {"version": 2, "folder_id": None},
        format="json",
    )

    assert listed.status_code == 200
    assert [row["id"] for row in listed.json()["results"]] == [
        inbox["id"],
        first.json()["id"],
        duplicate.json()["id"],
    ]
    assert retrieved.status_code == 200
    assert retrieved.json() == first.json()
    assert updated.status_code == 200
    assert updated.json()["title"] == "Projects"
    assert updated.json()["folder_id"] == second_folder["id"]
    assert updated.json()["position"] == 9
    assert updated.json()["version"] == 2
    assert folderless.status_code == 200
    assert folderless.json()["folder_id"] is None
    assert folderless.json()["version"] == 3


def test_list_update_requires_version_and_rejects_stale_writes():
    user = _user("list-version-update@example.test")
    client = _authenticated_client(user)
    created = _create_public_list(client, "Original").json()

    missing = client.patch(
        f"{LISTS_URL}/{created['id']}",
        {"title": "Missing version"},
        format="json",
    )
    first = client.patch(
        f"{LISTS_URL}/{created['id']}",
        {"version": 1, "title": "Current"},
        format="json",
    )
    stale = client.patch(
        f"{LISTS_URL}/{created['id']}",
        {"version": 1, "title": "Stale overwrite"},
        format="json",
    )

    assert missing.status_code == 400
    assert first.status_code == 200
    assert first.json()["version"] == 2
    assert stale.status_code == 409
    assert stale.json()["error"]["code"] == "version_conflict"
    row = List.objects.get(pk=created["id"])
    assert row.title == "Current"
    assert row.version == 2


def test_list_input_and_folder_references_are_validated():
    owner = _user("list-validation@example.test")
    other = _user("list-validation-other@example.test")
    client = _authenticated_client(owner)
    foreign_folder = Folder.objects.create(owner=other, title="Foreign")
    trashed_folder = Folder.objects.create(
        owner=owner,
        title="Trashed",
        is_trashed=True,
        trashed_at="2026-09-15T00:00:00Z",
    )

    assert APIClient().get(LISTS_URL).status_code == 401
    assert _create_public_list(client, "  ").status_code == 400
    assert (
        _create_public_list(
            client,
            "Valid",
            owner_user_id=str(owner.id),
        ).status_code
        == 400
    )
    assert (
        _create_public_list(
            client,
            "Foreign",
            folder_id=str(foreign_folder.id),
        ).status_code
        == 404
    )
    assert (
        _create_public_list(
            client,
            "Trashed",
            folder_id=str(trashed_folder.id),
        ).status_code
        == 404
    )

    created = _create_public_list(client, "Valid").json()
    assert client.patch(f"{LISTS_URL}/{created['id']}", {}, format="json").status_code == 400
    assert (
        client.patch(
            f"{LISTS_URL}/{created['id']}",
            {"version": 1},
            format="json",
        ).status_code
        == 400
    )
    assert (
        client.patch(
            f"{LISTS_URL}/{created['id']}",
            {"version": 1, "position": -1},
            format="json",
        ).status_code
        == 400
    )


def test_list_reads_and_writes_are_owner_scoped_and_hide_trashed_rows():
    owner = _user("list-owner@example.test")
    other = _user("list-other@example.test")
    private = List.objects.create(owner=owner, title="Private")
    Column.objects.create(list=private, title="Items", is_default=True)
    trashed = List.objects.create(
        owner=other,
        title="Trashed",
        is_trashed=True,
        trashed_at="2026-09-15T00:00:00Z",
    )
    Column.objects.create(list=trashed, title="Items", is_default=True)
    client = _authenticated_client(other)

    assert client.get(f"{LISTS_URL}/{private.id}").status_code == 404
    assert (
        client.patch(
            f"{LISTS_URL}/{private.id}",
            {"version": 1, "title": "Taken"},
            format="json",
        ).status_code
        == 404
    )
    assert _trash_list(client, private.id, 1).status_code == 404
    assert _restore_list(client, private.id, 1).status_code == 404
    assert client.get(f"{LISTS_URL}/{trashed.id}").status_code == 404
    assert client.get(LISTS_URL).json() == {"results": []}
    private.refresh_from_db()
    assert private.title == "Private"
    assert private.version == 1


def test_inbox_cannot_be_renamed_or_trashed():
    user = _user("immutable-inbox@example.test")
    client = _authenticated_client(user)
    inbox = client.put(
        BOOTSTRAP_URL,
        {"timezone": "Europe/Berlin"},
        format="json",
    ).json()["inbox"]
    row = List.objects.get(pk=inbox["id"])

    renamed = client.patch(
        f"{LISTS_URL}/{inbox['id']}",
        {"version": row.version, "title": "Renamed"},
        format="json",
    )
    deleted = _trash_list(client, inbox["id"], row.version)

    assert renamed.status_code == 409
    assert renamed.json()["error"]["code"] == "immutable_inbox"
    assert deleted.status_code == 409
    assert deleted.json()["error"]["code"] == "immutable_inbox"
    row.refresh_from_db()
    assert row.title == "Inbox"
    assert row.version == 1
    assert row.is_trashed is False


def test_list_trash_and_restore_require_versions_and_increment_them():
    user = _user("list-trash@example.test")
    client = _authenticated_client(user)
    folder = _create_folder(client, "Projects").json()
    created = _create_public_list(
        client,
        "Recoverable",
        folder_id=folder["id"],
    ).json()

    assert client.delete(f"{LISTS_URL}/{created['id']}").status_code == 400
    deleted = _trash_list(client, created["id"], 1)
    assert deleted.status_code == 204
    row = List.objects.get(pk=created["id"])
    assert row.is_trashed is True
    assert row.trashed_at is not None
    assert row.version == 2

    missing_restore = client.post(f"{LISTS_URL}/{created['id']}/restore", {}, format="json")
    stale_restore = _restore_list(client, created["id"], 1)
    restored = _restore_list(client, created["id"], 2)

    assert missing_restore.status_code == 400
    assert stale_restore.status_code == 409
    assert stale_restore.json()["error"]["code"] == "version_conflict"
    assert restored.status_code == 200
    assert restored.json()["id"] == created["id"]
    assert restored.json()["folder_id"] == folder["id"]
    assert restored.json()["version"] == 3
    assert restored.json()["is_trashed"] is False
    assert restored.json()["trashed_at"] is None


def test_list_trash_and_restore_protect_ownership_and_state():
    owner = _user("list-trash-owner@example.test")
    other = _user("list-trash-other@example.test")
    owner_client = _authenticated_client(owner)
    other_client = _authenticated_client(other)
    row, _ = _create_list(owner=owner, title="Private")

    assert _trash_list(other_client, row.id, 1).status_code == 404
    assert _restore_list(other_client, row.id, 1).status_code == 404

    assert _trash_list(owner_client, row.id, 1).status_code == 204
    assert _trash_list(owner_client, row.id, 2).status_code == 404
    assert (
        owner_client.post(
            f"{LISTS_URL}/{row.id}/restore",
            {"version": 2, "unexpected": True},
            format="json",
        ).status_code
        == 400
    )
    assert _restore_list(other_client, row.id, 2).status_code == 404


def test_restoring_a_list_detaches_it_from_a_still_trashed_folder():
    user = _user("list-restore-folder@example.test")
    client = _authenticated_client(user)
    folder = Folder.objects.create(owner=user, title="Trashed parent")
    row, _ = _create_list(owner=user, folder=folder, title="Child")

    assert _trash_list(client, row.id, 1).status_code == 204
    Folder.objects.filter(pk=folder.pk).update(
        is_trashed=True,
        trashed_at=timezone.now(),
    )

    restored = _restore_list(client, row.id, 2)

    assert restored.status_code == 200
    assert restored.json()["folder_id"] is None
    assert restored.json()["version"] == 3


def test_trashed_list_listing_is_owned_separate_and_newest_first():
    owner = _user("trashed-list-listing@example.test")
    other = _user("trashed-list-listing-other@example.test")
    client = _authenticated_client(owner)
    older, _ = _create_list(owner=owner, title="Older")
    newer, _ = _create_list(owner=owner, title="Newer")
    foreign, _ = _create_list(owner=other, title="Foreign")
    _create_list(owner=owner, title="Active")
    older_time = timezone.now() - timedelta(days=1)
    newer_time = timezone.now()
    List.objects.filter(pk=older.pk).update(is_trashed=True, trashed_at=older_time)
    List.objects.filter(pk=newer.pk).update(is_trashed=True, trashed_at=newer_time)
    List.objects.filter(pk=foreign.pk).update(is_trashed=True, trashed_at=newer_time)

    response = client.get(TRASHED_LISTS_URL)

    assert response.status_code == 200
    assert [row["id"] for row in response.json()["results"]] == [
        str(newer.id),
        str(older.id),
    ]
    assert all(row["version"] == 1 for row in response.json()["results"])
    assert all(row["is_trashed"] is True for row in response.json()["results"])
    assert all(row["trashed_at"] is not None for row in response.json()["results"])
    assert all(row["default_column"]["is_default"] is True for row in response.json()["results"])
    assert APIClient().get(TRASHED_LISTS_URL).status_code == 401


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


def test_list_delete_requires_item_resolution_after_version_precondition():
    user = _user("list-move-items@example.test")
    client = _authenticated_client(user)
    client.put(BOOTSTRAP_URL, {"timezone": "Europe/Berlin"}, format="json")
    inbox_column = Column.objects.get(list__owner=user, list__is_inbox=True, is_default=True)
    row, column = _create_list(owner=user, title="Project")
    item = _item(
        owner=user,
        column=column,
        title="Ship",
        operation_id="00000000-0000-0000-0000-000000000501",
    )

    missing_version = client.delete(f"{LISTS_URL}/{row.id}")
    missing_resolution = _trash_list(client, row.id, 1)
    invalid_resolution = _trash_list(client, row.id, 1, items="delete")

    assert missing_version.status_code == 400
    assert missing_resolution.status_code == 409
    assert missing_resolution.json()["error"]["code"] == "child_resolution_required"
    assert invalid_resolution.status_code == 409
    row.refresh_from_db()
    item.refresh_from_db()
    assert row.is_trashed is False
    assert row.version == 1
    assert item.column_id == column.id
    assert item.version == 1

    moved = _trash_list(client, row.id, 1, items="move_to_inbox")

    assert moved.status_code == 204
    row.refresh_from_db()
    item.refresh_from_db()
    assert row.is_trashed is True
    assert row.version == 2
    assert item.is_trashed is False
    assert item.column_id == inbox_column.id
    assert item.version == 2

    restored = _restore_list(client, row.id, 2)
    assert restored.status_code == 200
    item.refresh_from_db()
    assert restored.json()["version"] == 3
    assert item.column_id == inbox_column.id
    assert item.version == 2


def test_list_delete_can_trash_and_restore_its_items_with_task_versions():
    user = _user("list-trash-items@example.test")
    client = _authenticated_client(user)
    client.put(BOOTSTRAP_URL, {"timezone": "Europe/Berlin"}, format="json")
    inbox_column = Column.objects.get(list__owner=user, list__is_inbox=True, is_default=True)
    row, column = _create_list(owner=user, title="Project")
    item = _item(
        owner=user,
        column=column,
        title="Recover",
        operation_id="00000000-0000-0000-0000-000000000502",
    )

    deleted = _trash_list(client, row.id, 1, items="trash")

    assert deleted.status_code == 204
    row.refresh_from_db()
    item.refresh_from_db()
    assert row.version == 2
    assert item.is_trashed is True
    assert item.trashed_at is not None
    assert item.trash_origin_column_id == column.id
    assert item.column_id == inbox_column.id
    assert item.version == 2

    restored = _restore_list(client, row.id, 2)

    assert restored.status_code == 200
    item.refresh_from_db()
    assert restored.json()["version"] == 3
    assert item.is_trashed is False
    assert item.trashed_at is None
    assert item.trash_origin_column_id is None
    assert item.column_id == column.id
    assert item.version == 3


def test_list_restore_does_not_revive_an_item_trashed_before_the_list():
    user = _user("list-restore-item-scope@example.test")
    client = _authenticated_client(user)
    row, column = _create_list(owner=user, title="Project")
    item = _item(
        owner=user,
        column=column,
        title="Already trashed",
        operation_id="00000000-0000-0000-0000-000000000503",
    )
    earlier = timezone.now() - timedelta(days=1)
    Item.objects.filter(pk=item.pk).update(
        is_trashed=True,
        trashed_at=earlier,
        trash_origin_column_id=column.id,
    )

    assert _trash_list(client, row.id, 1).status_code == 204
    assert _restore_list(client, row.id, 2).status_code == 200

    item.refresh_from_db()
    assert item.is_trashed is True
    assert item.trashed_at == earlier
