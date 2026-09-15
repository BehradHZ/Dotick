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


def test_column_create_list_get_and_update_follow_the_public_contract():
    user = _user("column-crud@example.test")
    client = _authenticated_client(user)
    row, default_column = create_list(owner=user, title="Project")
    columns_url = f"{LISTS_URL}/{row.id}/columns"

    first = client.post(columns_url, {"title": "  Doing  "}, format="json")
    duplicate = client.post(columns_url, {"title": "Doing"}, format="json")

    assert first.status_code == 201
    assert duplicate.status_code == 201
    assert first.json()["id"] != duplicate.json()["id"]
    assert first.json() == {
        "id": str(Column.objects.get(pk=first.json()["id"]).id),
        "list_id": str(row.id),
        "title": "Doing",
        "position": 1,
        "is_default": False,
    }
    assert duplicate.json()["title"] == "Doing"
    assert duplicate.json()["position"] == 2

    listed = client.get(columns_url)
    retrieved = client.get(f"/api/v1/columns/{first.json()['id']}")
    updated = client.patch(
        f"/api/v1/columns/{first.json()['id']}",
        {"title": "Done", "position": 7},
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
    assert (
        client.post(
            f"{LISTS_URL}/{foreign_list.id}/columns",
            {"title": "Rejected"},
            format="json",
        ).status_code
        == 404
    )

    row, _ = create_list(owner=owner, title="Owned")
    columns_url = f"{LISTS_URL}/{row.id}/columns"
    assert client.post(columns_url, {"title": "  "}, format="json").status_code == 400
    assert (
        client.post(
            columns_url,
            {"title": "Valid", "list_id": str(row.id)},
            format="json",
        ).status_code
        == 400
    )
    column_id = client.post(columns_url, {"title": "Valid"}, format="json").json()["id"]
    assert client.patch(f"/api/v1/columns/{column_id}", {}, format="json").status_code == 400
    assert (
        client.patch(
            f"/api/v1/columns/{column_id}",
            {"position": -1},
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
            {"title": "Taken"},
            format="json",
        ).status_code
        == 404
    )
    assert client.get(f"/api/v1/columns/{hidden.id}").status_code == 404
    private.refresh_from_db()
    assert private.title == "Items"
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


def test_empty_nondefault_column_can_be_deleted_but_default_column_cannot():
    user = _user("column-delete@example.test")
    client = _authenticated_client(user)
    row, default_column = create_list(owner=user, title="Project")
    column = Column.objects.create(list=row, title="Doing", position=1)

    protected = client.delete(f"/api/v1/columns/{default_column.id}")
    deleted = client.delete(f"/api/v1/columns/{column.id}")

    assert protected.status_code == 409
    assert protected.json()["error"]["code"] == "immutable_default_column"
    assert deleted.status_code == 204
    assert deleted.content == b""
    assert not Column.objects.filter(pk=column.id).exists()
    assert client.get(f"/api/v1/columns/{column.id}").status_code == 404


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

    assert client.delete(f"/api/v1/columns/{private.id}").status_code == 404
    assert client.delete(f"/api/v1/columns/{hidden.id}").status_code == 404
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

    missing = client.delete(f"/api/v1/columns/{column.id}")
    invalid = client.delete(f"/api/v1/columns/{column.id}?items=move_to_inbox")

    assert missing.status_code == 409
    assert missing.json()["error"]["code"] == "child_resolution_required"
    assert invalid.status_code == 409
    assert Column.objects.filter(pk=column.id).exists()
    item.refresh_from_db()
    assert item.column_id == column.id
    assert item.version == 1

    moved = client.delete(f"/api/v1/columns/{column.id}?items=move_to_default")

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

    deleted = client.delete(f"/api/v1/columns/{column.id}?items=trash")

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

    deleted = client.delete(f"/api/v1/columns/{column.id}")

    assert deleted.status_code == 204
    item.refresh_from_db()
    assert item.is_trashed is True
    assert item.trashed_at == trashed_at
    assert item.trash_origin_column_id == column.id
    assert item.column_id == default_column.id
    assert item.version == 2
