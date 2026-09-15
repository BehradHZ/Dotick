from uuid import uuid4

import pytest
from django.contrib.auth import get_user_model
from dotick.identity.sessions import create_auth_session
from dotick.items.models import Item, ItemSource
from dotick.organization.application import create_list
from dotick.tasks.models import Task
from rest_framework.test import APIClient

BOOTSTRAP_URL = "/api/v1/account/bootstrap"
TASKS_URL = "/api/v1/tasks"
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


def test_task_create_persists_composed_rows_in_the_inbox():
    user = _user("task-create@example.test")
    client = _authenticated_client(user)
    workspace = client.put(
        BOOTSTRAP_URL,
        {"timezone": "Europe/Berlin"},
        format="json",
    ).json()

    response = client.post(
        TASKS_URL,
        {
            "title": "  خرید نان  ",
            "operation_id": "00000000-0000-0000-0000-000000000801",
        },
        format="json",
    )

    assert response.status_code == 201
    body = response.json()
    item = Item.objects.select_related("task", "source").get(pk=body["id"])
    assert body == {
        "id": str(item.id),
        "title": "خرید نان",
        "status": "todo",
        "version": 1,
        "column_id": workspace["inbox"]["default_column"]["id"],
        "owner_user_id": str(user.id),
        "created_by_user_id": str(user.id),
        "source": {
            "platform": "manual",
            "external_account_id": None,
            "external_id": None,
        },
        "created_at": item.created_at.isoformat().replace("+00:00", "Z"),
        "updated_at": item.updated_at.isoformat().replace("+00:00", "Z"),
    }
    assert Task.objects.filter(pk=item.id).count() == 1
    assert ItemSource.objects.filter(pk=item.id).count() == 1


def test_task_create_accepts_only_an_owned_active_destination_column():
    owner = _user("task-create-owner@example.test")
    other = _user("task-create-other@example.test")
    owner_client = _authenticated_client(owner)
    owned_list, owned_column = create_list(owner=owner, title="Owned")
    _, foreign_column = create_list(owner=other, title="Foreign")

    created = owner_client.post(
        TASKS_URL,
        {
            "title": "Placed",
            "operation_id": "00000000-0000-0000-0000-000000000802",
            "column_id": str(owned_column.id),
        },
        format="json",
    )
    foreign = owner_client.post(
        TASKS_URL,
        {
            "title": "Rejected",
            "operation_id": "00000000-0000-0000-0000-000000000803",
            "column_id": str(foreign_column.id),
        },
        format="json",
    )
    owned_list.is_trashed = True
    owned_list.trashed_at = owned_list.updated_at
    owned_list.save(update_fields=["is_trashed", "trashed_at", "updated_at"])
    trashed = owner_client.post(
        TASKS_URL,
        {
            "title": "Rejected",
            "operation_id": "00000000-0000-0000-0000-000000000804",
            "column_id": str(owned_column.id),
        },
        format="json",
    )

    assert created.status_code == 201
    assert created.json()["column_id"] == str(owned_column.id)
    assert foreign.status_code == 404
    assert trashed.status_code == 404


def test_task_create_is_idempotent_per_owner_and_rejects_changed_intent():
    user = _user("task-create-idempotent@example.test")
    client = _authenticated_client(user)
    client.put(BOOTSTRAP_URL, {"timezone": "Europe/Berlin"}, format="json")
    payload = {
        "title": "Write proposal",
        "operation_id": "00000000-0000-0000-0000-000000000805",
    }

    first = client.post(TASKS_URL, payload, format="json")
    repeated = client.post(TASKS_URL, payload, format="json")
    conflicting = client.post(
        TASKS_URL,
        {**payload, "title": "Different intent"},
        format="json",
    )

    assert first.status_code == 201
    assert repeated.status_code == 200
    assert repeated.json() == first.json()
    assert conflicting.status_code == 409
    assert conflicting.json()["error"]["code"] == "idempotency_conflict"
    assert Item.objects.filter(owner=user).count() == 1


def test_task_create_requires_authentication_and_strict_valid_input():
    user = _user("task-create-validation@example.test")
    client = _authenticated_client(user)
    client.put(BOOTSTRAP_URL, {"timezone": "Europe/Berlin"}, format="json")

    assert APIClient().post(TASKS_URL, {}, format="json").status_code == 401
    assert (
        client.post(
            TASKS_URL,
            {
                "title": "  ",
                "operation_id": "00000000-0000-0000-0000-000000000806",
            },
            format="json",
        ).status_code
        == 400
    )
    assert (
        client.post(
            TASKS_URL,
            {
                "title": "Valid",
                "operation_id": "00000000-0000-0000-0000-000000000807",
                "status": "done",
            },
            format="json",
        ).status_code
        == 400
    )


def test_task_list_returns_only_owned_active_tasks_in_active_lists_newest_first():
    owner = _user("task-list-owner@example.test")
    other = _user("task-list-other@example.test")
    client = _authenticated_client(owner)
    client.put(BOOTSTRAP_URL, {"timezone": "Europe/Berlin"}, format="json")
    other_client = _authenticated_client(other)
    other_client.put(BOOTSTRAP_URL, {"timezone": "Europe/Berlin"}, format="json")

    first = client.post(
        TASKS_URL,
        {
            "title": "First",
            "operation_id": "00000000-0000-0000-0000-000000000808",
        },
        format="json",
    ).json()
    second = client.post(
        TASKS_URL,
        {
            "title": "Second",
            "operation_id": "00000000-0000-0000-0000-000000000809",
        },
        format="json",
    ).json()
    foreign = other_client.post(
        TASKS_URL,
        {
            "title": "Foreign",
            "operation_id": "00000000-0000-0000-0000-000000000810",
        },
        format="json",
    ).json()
    hidden_item = Item.objects.get(pk=first["id"])
    hidden_item.is_trashed = True
    hidden_item.trashed_at = hidden_item.updated_at
    hidden_item.save(update_fields=["is_trashed", "trashed_at", "updated_at"])
    hidden_list, hidden_column = create_list(owner=owner, title="Trashed List")
    hidden = client.post(
        TASKS_URL,
        {
            "title": "Hidden by List",
            "operation_id": "00000000-0000-0000-0000-000000000811",
            "column_id": str(hidden_column.id),
        },
        format="json",
    ).json()
    hidden_list.is_trashed = True
    hidden_list.trashed_at = hidden_list.updated_at
    hidden_list.save(update_fields=["is_trashed", "trashed_at", "updated_at"])

    response = client.get(TASKS_URL)

    assert response.status_code == 200
    assert [task["id"] for task in response.json()["results"]] == [second["id"]]
    returned_ids = {task["id"] for task in response.json()["results"]}
    assert foreign["id"] not in returned_ids
    assert hidden["id"] not in returned_ids
    assert first["id"] not in returned_ids
    assert APIClient().get(TASKS_URL).status_code == 401


def test_task_get_returns_only_an_owned_active_task_in_an_active_list():
    owner = _user("task-get-owner@example.test")
    other = _user("task-get-other@example.test")
    client = _authenticated_client(owner)
    other_client = _authenticated_client(other)
    client.put(BOOTSTRAP_URL, {"timezone": "Europe/Berlin"}, format="json")
    other_client.put(BOOTSTRAP_URL, {"timezone": "Europe/Berlin"}, format="json")
    created = client.post(
        TASKS_URL,
        {
            "title": "Readable",
            "operation_id": "00000000-0000-0000-0000-000000000812",
        },
        format="json",
    ).json()

    response = client.get(f"{TASKS_URL}/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created
    assert other_client.get(f"{TASKS_URL}/{created['id']}").status_code == 404
    assert client.get(f"{TASKS_URL}/{uuid4()}").status_code == 404
    assert APIClient().get(f"{TASKS_URL}/{created['id']}").status_code == 401

    item = Item.objects.get(pk=created["id"])
    item.is_trashed = True
    item.trashed_at = item.updated_at
    item.save(update_fields=["is_trashed", "trashed_at", "updated_at"])
    assert client.get(f"{TASKS_URL}/{created['id']}").status_code == 404


def test_task_get_hides_tasks_in_trashed_lists():
    owner = _user("task-get-trashed-list@example.test")
    client = _authenticated_client(owner)
    owned_list, column = create_list(owner=owner, title="Soon trashed")
    created = client.post(
        TASKS_URL,
        {
            "title": "Hidden",
            "operation_id": "00000000-0000-0000-0000-000000000813",
            "column_id": str(column.id),
        },
        format="json",
    ).json()
    owned_list.is_trashed = True
    owned_list.trashed_at = owned_list.updated_at
    owned_list.save(update_fields=["is_trashed", "trashed_at", "updated_at"])

    assert client.get(f"{TASKS_URL}/{created['id']}").status_code == 404


def test_task_title_update_is_trimmed_and_atomically_increments_version():
    user = _user("task-title-update@example.test")
    client = _authenticated_client(user)
    client.put(BOOTSTRAP_URL, {"timezone": "Europe/Berlin"}, format="json")
    created = client.post(
        TASKS_URL,
        {
            "title": "Before",
            "operation_id": "00000000-0000-0000-0000-000000000814",
        },
        format="json",
    ).json()

    response = client.patch(
        f"{TASKS_URL}/{created['id']}",
        {"version": 1, "title": "  After  "},
        format="json",
    )

    assert response.status_code == 200
    assert response.json()["title"] == "After"
    assert response.json()["version"] == 2
    assert response.json()["id"] == created["id"]
    assert response.json()["created_at"] == created["created_at"]
    assert response.json()["updated_at"] > created["updated_at"]
    assert Item.objects.get(pk=created["id"]).version == 2


def test_task_title_update_rejects_stale_invalid_and_unowned_changes():
    owner = _user("task-title-update-owner@example.test")
    other = _user("task-title-update-other@example.test")
    client = _authenticated_client(owner)
    other_client = _authenticated_client(other)
    client.put(BOOTSTRAP_URL, {"timezone": "Europe/Berlin"}, format="json")
    other_client.put(BOOTSTRAP_URL, {"timezone": "Europe/Berlin"}, format="json")
    created = client.post(
        TASKS_URL,
        {
            "title": "Original",
            "operation_id": "00000000-0000-0000-0000-000000000815",
        },
        format="json",
    ).json()
    url = f"{TASKS_URL}/{created['id']}"
    assert client.patch(url, {"version": 1, "title": "First"}, format="json").status_code == 200

    stale = client.patch(url, {"version": 1, "title": "Stale"}, format="json")

    assert stale.status_code == 409
    assert stale.json()["error"]["code"] == "version_conflict"
    assert stale.json()["error"]["details"]["current"]["title"] == "First"
    assert stale.json()["error"]["details"]["current"]["version"] == 2
    assert client.patch(url, {"version": 2, "title": "  "}, format="json").status_code == 400
    assert client.patch(url, {"version": 2}, format="json").status_code == 400
    assert other_client.patch(url, {"version": 2, "title": "No"}, format="json").status_code == 404
    assert Item.objects.get(pk=created["id"]).title == "First"
    assert Item.objects.get(pk=created["id"]).version == 2


def test_task_status_update_supports_only_increment_one_statuses():
    user = _user("task-status-update@example.test")
    client = _authenticated_client(user)
    client.put(BOOTSTRAP_URL, {"timezone": "Europe/Berlin"}, format="json")
    created = client.post(
        TASKS_URL,
        {
            "title": "Status lifecycle",
            "operation_id": "00000000-0000-0000-0000-000000000816",
        },
        format="json",
    ).json()
    url = f"{TASKS_URL}/{created['id']}"

    done = client.patch(url, {"version": 1, "status": "done"}, format="json")
    wont_do = client.patch(url, {"version": 2, "status": "wont_do"}, format="json")
    todo = client.patch(
        url,
        {"version": 3, "status": "todo", "title": "Combined change"},
        format="json",
    )
    invalid = client.patch(url, {"version": 4, "status": "cancelled"}, format="json")

    assert (done.status_code, done.json()["status"], done.json()["version"]) == (200, "done", 2)
    assert (wont_do.status_code, wont_do.json()["status"], wont_do.json()["version"]) == (
        200,
        "wont_do",
        3,
    )
    assert (todo.status_code, todo.json()["status"], todo.json()["version"]) == (200, "todo", 4)
    assert todo.json()["title"] == "Combined change"
    assert invalid.status_code == 400
    item = Item.objects.select_related("task").get(pk=created["id"])
    assert item.version == 4
    assert item.task.status == "todo"
