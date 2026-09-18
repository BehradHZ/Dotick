import uuid

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from dotick.identity.sessions import create_auth_session
from dotick.items.models import Item, ItemSource
from dotick.organization.application import create_list
from dotick.organization.models import Column, List
from rest_framework.test import APIClient

LISTS_URL = "/api/v1/lists"
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


def _create_column(client, parent_list_id, title, **extra):
    payload = {"title": title, "operation_id": str(uuid.uuid4()), **extra}
    return client.post(f"{LISTS_URL}/{parent_list_id}/columns", payload, format="json")


def _delete_column(client, column_id, version, *, items=None):
    url = f"/api/v1/columns/{column_id}"
    if items is not None:
        url += f"?items={items}"
    return client.delete(url, HTTP_IF_MATCH=str(version))


def test_column_create_list_get_and_update_follow_the_public_contract():
    user = _user("column-crud@example.test")
    client = _authenticated_client(user)
    row, default_column = create_list(owner=user, title="Project")
    columns_url = f"{LISTS_URL}/{row.id}/columns"

    first = _create_column(client, row.id, "  Doing  ")
    duplicate = _create_column(client, row.id, "Doing")

    assert first.status_code == 201
    assert duplicate.status_code == 201
    assert first.json()["id"] != duplicate.json()["id"]
    assert first.json() == {
        "id": str(Column.objects.get(pk=first.json()["id"]).id),
        "list_id": str(row.id),
        "title": "Doing",
        "position": 1,
        "version": 1,
        "is_default": False,
    }
    assert duplicate.json()["title"] == "Doing"
    assert duplicate.json()["position"] == 2
    assert duplicate.json()["version"] == 1

    listed = client.get(columns_url)
    retrieved = client.get(f"/api/v1/columns/{first.json()['id']}")
    updated = client.patch(
        f"/api/v1/columns/{first.json()['id']}",
        {"version": 1, "title": "Done", "position": 7},
        format="json",
    )

    assert listed.status_code == 200
    assert [column["id"] for column in listed.json()["results"]] == [
        str(default_column.id),
        first.json()["id"],
        duplicate.json()["id"],
    ]
    assert retrieved.status_code == 200
    assert retrieved.json() == first.json()
    assert updated.status_code == 200
    assert updated.json()["title"] == "Done"
    assert updated.json()["position"] == 7
    assert updated.json()["version"] == 2


def test_column_update_requires_version_and_rejects_stale_write():
    user = _user("column-version-update@example.test")
    client = _authenticated_client(user)
    row, _ = create_list(owner=user, title="Project")
    column = Column.objects.create(list=row, title="Doing", position=1)
    url = f"/api/v1/columns/{column.id}"

    missing = client.patch(url, {"title": "Missing"}, format="json")
    first = client.patch(url, {"version": 1, "title": "Current"}, format="json")
    stale = client.patch(url, {"version": 1, "title": "Stale"}, format="json")

    assert missing.status_code == 400
    assert first.status_code == 200
    assert first.json()["version"] == 2
    assert stale.status_code == 409
    assert stale.json()["error"]["code"] == "version_conflict"
    column.refresh_from_db()
    assert column.title == "Current"
    assert column.version == 2


def test_column_input_and_parent_list_are_validated():
    owner = _user("column-validation@example.test")
    other = _user("column-validation-other@example.test")
    client = _authenticated_client(owner)
    foreign_list, _ = create_list(owner=other, title="Foreign")
    trashed_list, _ = create_list(owner=owner, title="Trashed")
    List.objects.filter(pk=trashed_list.pk).update(
        is_trashed=True,
        trashed_at=timezone.now(),
    )

    assert APIClient().get(f"{LISTS_URL}/{foreign_list.id}/columns").status_code == 401
    assert client.get(f"{LISTS_URL}/{foreign_list.id}/columns").status_code == 404
    assert client.get(f"{LISTS_URL}/{trashed_list.id}/columns").status_code == 404
    assert _create_column(client, foreign_list.id, "Rejected").status_code == 404

    row, _ = create_list(owner=owner, title="Owned")
    assert _create_column(client, row.id, "  ").status_code == 400
    assert (
        _create_column(
            client,
            row.id,
            "Valid",
            list_id=str(row.id),
        ).status_code
        == 400
    )
    column_id = _create_column(client, row.id, "Valid").json()["id"]
    assert client.patch(f"/api/v1/columns/{column_id}", {}, format="json").status_code == 400
    assert (
        client.patch(
            f"/api/v1/columns/{column_id}",
            {"version": 1},
            format="json",
        ).status_code
        == 400
    )
    assert (
        client.patch(
            f"/api/v1/columns/{column_id}",
            {"version": 1, "position": -1},
            format="json",
        ).status_code
        == 400
    )


def test_column_reads_and_writes_are_owner_scoped_and_hide_trashed_list_columns():
    owner = _user("column-owner@example.test")
    other = _user("column-other@example.test")
    active_list, private = create_list(owner=owner, title="Private")
    trashed_list, hidden = create_list(owner=other, title="Trashed")
    List.objects.filter(pk=trashed_list.pk).update(
        is_trashed=True,
        trashed_at=timezone.now(),
    )
    client = _authenticated_client(other)

    assert client.get(f"/api/v1/columns/{private.id}").status_code == 404
    assert (
        client.patch(
            f"/api/v1/columns/{private.id}",
            {"version": 1, "title": "Taken"},
            format="json",
        ).status_code
        == 404
    )
    assert _delete_column(client, private.id, 1).status_code == 404
    assert client.get(f"/api/v1/columns/{hidden.id}").status_code == 404
    assert _delete_column(client, hidden.id, 1).status_code == 404
    private.refresh_from_db()
    assert private.title == "Items"
    assert private.version == 1
    assert active_list.is_trashed is False


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


def test_empty_nondefault_column_requires_version_and_default_column_stays_immutable():
    user = _user("column-delete@example.test")
    client = _authenticated_client(user)
    row, default_column = create_list(owner=user, title="Project")
    column = Column.objects.create(list=row, title="Doing", position=1)

    assert client.delete(f"/api/v1/columns/{column.id}").status_code == 400
    protected = _delete_column(client, default_column.id, 1)
    deleted = _delete_column(client, column.id, 1)

    assert protected.status_code == 409
    assert protected.json()["error"]["code"] == "immutable_default_column"
    assert deleted.status_code == 204
    assert deleted.content == b""
    assert not Column.objects.filter(pk=column.id).exists()
    assert client.get(f"/api/v1/columns/{column.id}").status_code == 404


def test_column_delete_rejects_stale_version_without_deleting():
    user = _user("column-stale-delete@example.test")
    client = _authenticated_client(user)
    row, _ = create_list(owner=user, title="Project")
    column = Column.objects.create(list=row, title="Doing", position=1)
    Column.objects.filter(pk=column.pk).update(version=2)

    response = _delete_column(client, column.id, 1)

    assert response.status_code == 409
    assert response.json()["error"]["code"] == "version_conflict"
    column.refresh_from_db()
    assert column.version == 2


def test_column_delete_is_owner_and_active_list_scoped():
    owner = _user("column-delete-owner@example.test")
    other = _user("column-delete-other@example.test")
    owner_list, _ = create_list(owner=owner, title="Private")
    private = Column.objects.create(list=owner_list, title="Private", position=1)
    trashed_list, _ = create_list(owner=other, title="Trashed")
    hidden = Column.objects.create(list=trashed_list, title="Hidden", position=1)
    List.objects.filter(pk=trashed_list.pk).update(
        is_trashed=True,
        trashed_at=timezone.now(),
    )
    client = _authenticated_client(other)

    assert _delete_column(client, private.id, 1).status_code == 404
    assert _delete_column(client, hidden.id, 1).status_code == 404
    assert Column.objects.filter(pk__in=[private.id, hidden.id]).count() == 2


def test_column_delete_requires_item_resolution_and_can_move_to_default():
    user = _user("column-move-items@example.test")
    client = _authenticated_client(user)
    row, default_column = create_list(owner=user, title="Project")
    column = Column.objects.create(list=row, title="Doing", position=1)
    item = _item(
        owner=user,
        column=column,
        title="Ship",
        operation_id="00000000-0000-0000-0000-000000000601",
    )

    missing_version = client.delete(f"/api/v1/columns/{column.id}")
    missing_resolution = _delete_column(client, column.id, 1)
    invalid_resolution = _delete_column(client, column.id, 1, items="move_to_inbox")

    assert missing_version.status_code == 400
    assert missing_resolution.status_code == 409
    assert missing_resolution.json()["error"]["code"] == "child_resolution_required"
    assert invalid_resolution.status_code == 409
    assert Column.objects.filter(pk=column.id).exists()
    item.refresh_from_db()
    assert item.column_id == column.id
    assert item.version == 1

    moved = _delete_column(client, column.id, 1, items="move_to_default")

    assert moved.status_code == 204
    assert not Column.objects.filter(pk=column.id).exists()
    item.refresh_from_db()
    assert item.is_trashed is False
    assert item.column_id == default_column.id
    assert item.version == 2


def test_column_delete_can_trash_its_items_before_hard_deletion():
    user = _user("column-trash-items@example.test")
    client = _authenticated_client(user)
    row, default_column = create_list(owner=user, title="Project")
    column = Column.objects.create(list=row, title="Doing", position=1)
    item = _item(
        owner=user,
        column=column,
        title="Discard",
        operation_id="00000000-0000-0000-0000-000000000602",
    )

    deleted = _delete_column(client, column.id, 1, items="trash")

    assert deleted.status_code == 204
    assert not Column.objects.filter(pk=column.id).exists()
    item.refresh_from_db()
    assert item.is_trashed is True
    assert item.trashed_at is not None
    assert item.trash_origin_column_id == column.id
    assert item.column_id == default_column.id
    assert item.version == 2


def test_column_delete_rehomes_already_trashed_items_without_restoring_them():
    user = _user("column-trashed-items@example.test")
    client = _authenticated_client(user)
    row, default_column = create_list(owner=user, title="Project")
    column = Column.objects.create(list=row, title="Doing", position=1)
    item = _item(
        owner=user,
        column=column,
        title="Already trashed",
        operation_id="00000000-0000-0000-0000-000000000603",
    )
    trashed_at = timezone.now()
    Item.objects.filter(pk=item.pk).update(
        is_trashed=True,
        trashed_at=trashed_at,
        trash_origin_column_id=column.id,
    )

    deleted = _delete_column(client, column.id, 1)

    assert deleted.status_code == 204
    item.refresh_from_db()
    assert item.is_trashed is True
    assert item.trashed_at == trashed_at
    assert item.trash_origin_column_id == column.id
    assert item.column_id == default_column.id
    assert item.version == 2
