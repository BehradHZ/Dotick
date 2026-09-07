import re
from concurrent.futures import ThreadPoolExecutor

import pytest
from django.core import mail
from django.db import close_old_connections
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db
REGISTER_URL = "/api/v1/auth/register"
VERIFY_URL = "/api/v1/auth/email/verify"
TOKEN_URL = "/api/v1/auth/token"
BOOTSTRAP_URL = "/api/v1/account/bootstrap"
FOLDERS_URL = "/api/v1/folders"
LISTS_URL = "/api/v1/lists"
TASKS_URL = "/api/v1/tasks"
TRASH_TASKS_URL = "/api/v1/trash/tasks"
ACCOUNT_URL = "/api/v1/account"


def _authenticated_client(settings, suffix="owner"):
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
    email = f"workspace-{suffix}@example.test"
    password = "Workspace-owner-password-for-tests-8!"
    anonymous = APIClient()
    registered = anonymous.post(
        REGISTER_URL,
        {
            "email": email,
            "password": password,
            "handle": f"workspace_{suffix}",
            "display_name": "Workspace Owner",
        },
        format="json",
    )
    assert registered.status_code == 202
    code = re.search(r"\b\d{6}\b", mail.outbox[-1].body).group()
    verified = anonymous.post(VERIFY_URL, {"email": email, "code": code}, format="json")
    assert verified.status_code == 204
    access = anonymous.post(
        TOKEN_URL,
        {"email": email, "password": password},
        format="json",
    ).json()["access"]
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
    return client, {"email": email, "password": password}


def test_repeated_account_bootstrap_returns_one_inbox_and_default_column(settings):
    client, _ = _authenticated_client(settings)

    first = client.put(BOOTSTRAP_URL, {"timezone": "Europe/Berlin"}, format="json")
    repeated = client.put(BOOTSTRAP_URL, {"timezone": "Europe/Berlin"}, format="json")

    assert first.status_code == 200
    assert repeated.status_code == 200
    assert repeated.json() == first.json()
    assert first.json()["preferences"] == {"timezone": "Europe/Berlin"}
    assert first.json()["inbox"]["title"] == "Inbox"
    assert first.json()["inbox"]["is_inbox"] is True
    assert first.json()["inbox"]["default_column"]["is_default"] is True


@pytest.mark.django_db(transaction=True)
def test_concurrent_account_bootstrap_keeps_one_inbox_and_default_column(settings):
    _, credentials = _authenticated_client(settings, "concurrent_bootstrap")
    anonymous = APIClient()
    tokens = [
        anonymous.post(TOKEN_URL, credentials, format="json").json()["access"] for _ in range(2)
    ]

    def bootstrap(access):
        close_old_connections()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        response = client.put(BOOTSTRAP_URL, {"timezone": "Europe/Berlin"}, format="json")
        close_old_connections()
        return response.status_code, response.json()

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(bootstrap, tokens))

    from dotick.organization.models import Column, List

    assert [status for status, _ in results] == [200, 200]
    assert results[0][1] == results[1][1]
    assert List.objects.filter(owner__email=credentials["email"], is_inbox=True).count() == 1
    assert (
        Column.objects.filter(
            list__owner__email=credentials["email"],
            list__is_inbox=True,
            is_default=True,
        ).count()
        == 1
    )


def test_account_profile_and_timezone_can_be_presented_and_changed(settings):
    owner, _ = _authenticated_client(settings, "profile")
    owner.put(BOOTSTRAP_URL, {"timezone": "Europe/Berlin"}, format="json")

    changed = owner.patch(
        ACCOUNT_URL,
        {
            "handle": "New_Profile_Handle",
            "display_name": "New Name",
            "profile_picture_url": "https://cdn.example.test/avatar.png",
            "timezone": "Asia/Tehran",
        },
        format="json",
    )
    retrieved = owner.get(ACCOUNT_URL)

    assert changed.status_code == 200
    assert retrieved.status_code == 200
    assert retrieved.json() == changed.json()
    assert retrieved.json()["handle"] == "New_Profile_Handle"
    assert retrieved.json()["display_name"] == "New Name"
    assert retrieved.json()["profile_picture_url"].endswith("avatar.png")
    assert retrieved.json()["timezone"] == "Asia/Tehran"
    assert retrieved.json()["authentication_methods"] == {
        "password": True,
        "google": False,
        "passkey": False,
    }

    other, _ = _authenticated_client(settings, "other_profile")
    collision = other.patch(
        ACCOUNT_URL,
        {"handle": "new_profile_handle"},
        format="json",
    )
    invalid_timezone = owner.patch(
        ACCOUNT_URL,
        {"timezone": "Mars/Olympus"},
        format="json",
    )
    assert collision.status_code == 409
    assert collision.json()["error"]["code"] == "handle_unavailable"
    assert invalid_timezone.status_code == 400


def test_unscheduled_task_is_retrieved_after_a_new_sign_in(settings):
    client, credentials = _authenticated_client(settings)
    workspace = client.put(
        BOOTSTRAP_URL,
        {"timezone": "Europe/Berlin"},
        format="json",
    ).json()

    created = client.post(
        TASKS_URL,
        {
            "title": "خرید نان",
            "operation_id": "00000000-0000-0000-0000-000000000101",
        },
        format="json",
    )

    assert created.status_code == 201
    task = created.json()
    assert task["title"] == "خرید نان"
    assert task["status"] == "todo"
    assert task["version"] == 1
    assert task["column_id"] == workspace["inbox"]["default_column"]["id"]
    assert task["owner_user_id"] == task["created_by_user_id"]
    assert task["source"] == {
        "platform": "manual",
        "external_account_id": None,
        "external_id": None,
    }

    anonymous = APIClient()
    access = anonymous.post(TOKEN_URL, credentials, format="json").json()["access"]
    reopened = APIClient()
    reopened.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    retrieved = reopened.get(f"{TASKS_URL}/{task['id']}")

    assert retrieved.status_code == 200
    assert retrieved.json() == task


def test_lists_allow_duplicate_titles_without_a_folder_and_inbox_is_immutable(settings):
    client, _ = _authenticated_client(settings)
    inbox = client.put(
        BOOTSTRAP_URL,
        {"timezone": "Europe/Berlin"},
        format="json",
    ).json()["inbox"]

    first = client.post(LISTS_URL, {"title": "Personal"}, format="json")
    second = client.post(LISTS_URL, {"title": "Personal"}, format="json")

    assert first.status_code == 201
    assert second.status_code == 201
    assert first.json()["id"] != second.json()["id"]
    assert first.json()["title"] == second.json()["title"] == "Personal"
    assert first.json()["folder_id"] is None
    assert first.json()["default_column"]["is_default"] is True

    renamed = client.patch(
        f"{LISTS_URL}/{inbox['id']}",
        {"title": "Renamed"},
        format="json",
    )
    deleted = client.delete(f"{LISTS_URL}/{inbox['id']}")

    assert renamed.status_code == 409
    assert renamed.json()["error"]["code"] == "immutable_inbox"
    assert deleted.status_code == 409
    assert deleted.json()["error"]["code"] == "immutable_inbox"

    listed = client.get(LISTS_URL)
    assert listed.status_code == 200
    assert [row["title"] for row in listed.json()["results"]] == [
        "Inbox",
        "Personal",
        "Personal",
    ]


def test_task_can_move_and_change_title_and_status_without_changing_identity(settings):
    client, _ = _authenticated_client(settings)
    client.put(BOOTSTRAP_URL, {"timezone": "Europe/Berlin"}, format="json")
    destination = client.post(LISTS_URL, {"title": "Work"}, format="json").json()
    created = client.post(
        TASKS_URL,
        {
            "title": "Draft",
            "operation_id": "00000000-0000-0000-0000-000000000102",
        },
        format="json",
    ).json()

    changed = client.patch(
        f"{TASKS_URL}/{created['id']}",
        {
            "version": created["version"],
            "title": "Publish plan",
            "status": "done",
            "column_id": destination["default_column"]["id"],
        },
        format="json",
    )

    assert changed.status_code == 200
    assert changed.json()["id"] == created["id"]
    assert changed.json()["title"] == "Publish plan"
    assert changed.json()["status"] == "done"
    assert changed.json()["column_id"] == destination["default_column"]["id"]
    assert changed.json()["version"] == 2

    empty_title = client.patch(
        f"{TASKS_URL}/{created['id']}",
        {"version": 2, "title": "  "},
        format="json",
    )
    forged_metadata = client.patch(
        f"{TASKS_URL}/{created['id']}",
        {"version": 2, "owner_user_id": "00000000-0000-0000-0000-000000000001"},
        format="json",
    )

    assert empty_title.status_code == 400
    assert forged_metadata.status_code == 400


def test_task_creation_is_idempotent_and_stale_edits_return_current_state(settings):
    client, _ = _authenticated_client(settings)
    client.put(BOOTSTRAP_URL, {"timezone": "Europe/Berlin"}, format="json")
    operation_id = "00000000-0000-0000-0000-000000000103"

    first = client.post(
        TASKS_URL,
        {"title": "Initial", "operation_id": operation_id},
        format="json",
    )
    repeated = client.post(
        TASKS_URL,
        {"title": "Initial", "operation_id": operation_id},
        format="json",
    )
    different_intent = client.post(
        TASKS_URL,
        {"title": "Different", "operation_id": operation_id},
        format="json",
    )

    assert first.status_code == 201
    assert repeated.status_code == 200
    assert repeated.json() == first.json()
    assert different_intent.status_code == 409
    assert different_intent.json()["error"]["code"] == "idempotency_conflict"

    accepted = client.patch(
        f"{TASKS_URL}/{first.json()['id']}",
        {"version": 1, "title": "Accepted"},
        format="json",
    )
    stale = client.patch(
        f"{TASKS_URL}/{first.json()['id']}",
        {"version": 1, "title": "Stale"},
        format="json",
    )

    assert accepted.status_code == 200
    assert stale.status_code == 409
    assert stale.json()["error"]["code"] == "version_conflict"
    assert stale.json()["error"]["details"]["current"]["title"] == "Accepted"
    assert stale.json()["error"]["details"]["current"]["version"] == 2


def test_tasks_and_columns_are_isolated_between_accounts(settings):
    owner, _ = _authenticated_client(settings, "first")
    owner_workspace = owner.put(
        BOOTSTRAP_URL,
        {"timezone": "Europe/Berlin"},
        format="json",
    ).json()
    private_task = owner.post(
        TASKS_URL,
        {
            "title": "Private",
            "operation_id": "00000000-0000-0000-0000-000000000104",
        },
        format="json",
    ).json()

    attacker, _ = _authenticated_client(settings, "second")
    attacker.put(BOOTSTRAP_URL, {"timezone": "Asia/Tehran"}, format="json")
    attacker_task = attacker.post(
        TASKS_URL,
        {
            "title": "Attacker task",
            "operation_id": "00000000-0000-0000-0000-000000000105",
        },
        format="json",
    ).json()

    assert attacker.get(f"{TASKS_URL}/{private_task['id']}").status_code == 404
    assert (
        attacker.patch(
            f"{TASKS_URL}/{private_task['id']}",
            {"version": 1, "title": "Taken over"},
            format="json",
        ).status_code
        == 404
    )
    assert (
        attacker.delete(
            f"{TASKS_URL}/{private_task['id']}",
            HTTP_IF_MATCH='"1"',
        ).status_code
        == 404
    )
    forged_move = attacker.patch(
        f"{TASKS_URL}/{attacker_task['id']}",
        {
            "version": 1,
            "column_id": owner_workspace["inbox"]["default_column"]["id"],
        },
        format="json",
    )
    assert forged_move.status_code == 404


def test_trashed_task_disappears_from_active_queries_and_can_be_restored(settings):
    client, _ = _authenticated_client(settings)
    client.put(BOOTSTRAP_URL, {"timezone": "Europe/Berlin"}, format="json")
    created = client.post(
        TASKS_URL,
        {
            "title": "Recover me",
            "operation_id": "00000000-0000-0000-0000-000000000106",
        },
        format="json",
    ).json()

    deleted = client.delete(
        f"{TASKS_URL}/{created['id']}",
        HTTP_IF_MATCH='"1"',
    )

    assert deleted.status_code == 204
    assert client.get(f"{TASKS_URL}/{created['id']}").status_code == 404
    trash = client.get(TRASH_TASKS_URL)
    assert trash.status_code == 200
    assert len(trash.json()["results"]) == 1
    trashed = trash.json()["results"][0]
    assert trashed["id"] == created["id"]
    assert trashed["is_trashed"] is True
    assert trashed["trashed_at"] is not None
    assert trashed["version"] == 2

    restored = client.post(
        f"{TASKS_URL}/{created['id']}/restore",
        {"version": trashed["version"]},
        format="json",
    )

    assert restored.status_code == 200
    assert restored.json()["id"] == created["id"]
    assert restored.json()["version"] == 3
    assert restored.json()["column_id"] == created["column_id"]
    assert client.get(f"{TASKS_URL}/{created['id']}").status_code == 200


def test_folder_list_and_column_lifecycle_moves_tasks_without_blind_cascades(settings):
    client, _ = _authenticated_client(settings)
    workspace = client.put(
        BOOTSTRAP_URL,
        {"timezone": "Europe/Berlin"},
        format="json",
    ).json()
    folder = client.post(FOLDERS_URL, {"title": "Projects"}, format="json")
    assert folder.status_code == 201
    custom_list = client.post(
        LISTS_URL,
        {"title": "Launch", "folder_id": folder.json()["id"]},
        format="json",
    )
    assert custom_list.status_code == 201
    columns_url = f"{LISTS_URL}/{custom_list.json()['id']}/columns"
    custom_column = client.post(columns_url, {"title": "Doing"}, format="json")
    assert custom_column.status_code == 201

    created = client.post(
        TASKS_URL,
        {
            "title": "Ship",
            "column_id": custom_column.json()["id"],
            "operation_id": "00000000-0000-0000-0000-000000000107",
        },
        format="json",
    )
    assert created.status_code == 201

    moved_to_default = client.delete(
        f"/api/v1/columns/{custom_column.json()['id']}?items=move_to_default"
    )
    assert moved_to_default.status_code == 204
    after_column_delete = client.get(f"{TASKS_URL}/{created.json()['id']}").json()
    assert after_column_delete["column_id"] == custom_list.json()["default_column"]["id"]
    assert after_column_delete["version"] == 2

    moved_to_inbox = client.delete(f"{LISTS_URL}/{custom_list.json()['id']}?items=move_to_inbox")
    assert moved_to_inbox.status_code == 204
    after_list_delete = client.get(f"{TASKS_URL}/{created.json()['id']}").json()
    assert after_list_delete["column_id"] == workspace["inbox"]["default_column"]["id"]
    assert after_list_delete["version"] == 3

    deleted_folder = client.delete(f"{FOLDERS_URL}/{folder.json()['id']}")
    assert deleted_folder.status_code == 204
    assert client.get(FOLDERS_URL).json()["results"] == []
    assert [row["title"] for row in client.get(LISTS_URL).json()["results"]] == ["Inbox"]


def test_container_deletion_requires_a_choice_and_restore_recovers_the_subtree(settings):
    client, _ = _authenticated_client(settings, "container_trash")
    client.put(BOOTSTRAP_URL, {"timezone": "Europe/Berlin"}, format="json")
    folder = client.post(FOLDERS_URL, {"title": "Projects"}, format="json").json()
    custom_list = client.post(
        LISTS_URL,
        {"title": "Launch", "folder_id": folder["id"]},
        format="json",
    ).json()
    columns_url = f"{LISTS_URL}/{custom_list['id']}/columns"
    custom_column = client.post(columns_url, {"title": "Doing"}, format="json").json()
    task = client.post(
        TASKS_URL,
        {
            "title": "Recover subtree",
            "column_id": custom_column["id"],
            "operation_id": "00000000-0000-0000-0000-000000000108",
        },
        format="json",
    ).json()

    column_blocked = client.delete(f"/api/v1/columns/{custom_column['id']}")
    default_blocked = client.delete(
        f"/api/v1/columns/{custom_list['default_column']['id']}?items=trash"
    )
    list_blocked = client.delete(f"{LISTS_URL}/{custom_list['id']}")
    folder_blocked = client.delete(f"{FOLDERS_URL}/{folder['id']}")

    assert column_blocked.status_code == 409
    assert column_blocked.json()["error"]["code"] == "child_resolution_required"
    assert default_blocked.status_code == 409
    assert default_blocked.json()["error"]["code"] == "immutable_default_column"
    assert list_blocked.status_code == 409
    assert folder_blocked.status_code == 409

    deleted_folder = client.delete(f"{FOLDERS_URL}/{folder['id']}?items=trash")
    assert deleted_folder.status_code == 204
    assert client.get(f"{TASKS_URL}/{task['id']}").status_code == 404
    assert [row["id"] for row in client.get("/api/v1/trash/folders").json()["results"]] == [
        folder["id"]
    ]
    assert client.get("/api/v1/trash/folders").json()["results"][0]["trashed_at"]
    assert [row["id"] for row in client.get("/api/v1/trash/lists").json()["results"]] == [
        custom_list["id"]
    ]

    restored = client.post(f"{FOLDERS_URL}/{folder['id']}/restore", {}, format="json")
    assert restored.status_code == 200
    assert restored.json()["id"] == folder["id"]
    assert client.get(f"{TASKS_URL}/{task['id']}").status_code == 200
    assert client.get(f"{TASKS_URL}/{task['id']}").json()["id"] == task["id"]


def test_lists_can_move_between_folders_and_containers_can_be_reordered(settings):
    client, _ = _authenticated_client(settings, "ordering")
    client.put(BOOTSTRAP_URL, {"timezone": "Europe/Berlin"}, format="json")
    first = client.post(FOLDERS_URL, {"title": "First"}, format="json").json()
    second = client.post(FOLDERS_URL, {"title": "Second"}, format="json").json()
    custom_list = client.post(LISTS_URL, {"title": "Movable"}, format="json").json()
    column = client.post(
        f"{LISTS_URL}/{custom_list['id']}/columns",
        {"title": "Later"},
        format="json",
    ).json()

    moved = client.patch(
        f"{LISTS_URL}/{custom_list['id']}",
        {"folder_id": second["id"], "position": 7},
        format="json",
    )
    reordered_folder = client.patch(
        f"{FOLDERS_URL}/{first['id']}",
        {"position": 4},
        format="json",
    )
    reordered_column = client.patch(
        f"/api/v1/columns/{column['id']}",
        {"position": 3},
        format="json",
    )

    assert moved.status_code == 200
    assert moved.json()["folder_id"] == second["id"]
    assert moved.json()["position"] == 7
    assert reordered_folder.json()["position"] == 4
    assert reordered_column.json()["position"] == 3
