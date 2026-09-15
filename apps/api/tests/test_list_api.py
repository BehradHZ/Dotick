import pytest
from django.contrib.auth import get_user_model
from dotick.identity.sessions import create_auth_session
from dotick.organization.models import Column, Folder, List
from rest_framework.test import APIClient

BOOTSTRAP_URL = "/api/v1/account/bootstrap"
FOLDERS_URL = "/api/v1/folders"
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


def test_list_create_list_get_and_update_follow_the_public_contract():
    user = _user("list-crud@example.test")
    client = _authenticated_client(user)
    inbox = client.put(
        BOOTSTRAP_URL,
        {"timezone": "Europe/Berlin"},
        format="json",
    ).json()["inbox"]
    first_folder = client.post(FOLDERS_URL, {"title": "First"}, format="json").json()
    second_folder = client.post(FOLDERS_URL, {"title": "Second"}, format="json").json()

    first = client.post(
        LISTS_URL,
        {"title": "  Personal  ", "folder_id": first_folder["id"]},
        format="json",
    )
    duplicate = client.post(LISTS_URL, {"title": "Personal"}, format="json")

    assert first.status_code == 201
    assert duplicate.status_code == 201
    assert first.json()["id"] != duplicate.json()["id"]
    assert first.json()["title"] == duplicate.json()["title"] == "Personal"
    assert first.json()["folder_id"] == first_folder["id"]
    assert duplicate.json()["folder_id"] is None
    assert first.json()["position"] == 1
    assert first.json()["is_inbox"] is False
    assert first.json()["is_trashed"] is False
    assert first.json()["trashed_at"] is None
    assert first.json()["default_column"]["is_default"] is True
    assert Column.objects.filter(list_id=first.json()["id"], is_default=True).count() == 1

    listed = client.get(LISTS_URL)
    retrieved = client.get(f"{LISTS_URL}/{first.json()['id']}")
    updated = client.patch(
        f"{LISTS_URL}/{first.json()['id']}",
        {"title": "Projects", "folder_id": second_folder["id"], "position": 9},
        format="json",
    )
    folderless = client.patch(
        f"{LISTS_URL}/{first.json()['id']}",
        {"folder_id": None},
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
    assert folderless.status_code == 200
    assert folderless.json()["folder_id"] is None


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
    assert client.post(LISTS_URL, {"title": "  "}, format="json").status_code == 400
    assert (
        client.post(
            LISTS_URL,
            {"title": "Valid", "owner_user_id": str(owner.id)},
            format="json",
        ).status_code
        == 400
    )
    assert (
        client.post(
            LISTS_URL,
            {"title": "Foreign", "folder_id": str(foreign_folder.id)},
            format="json",
        ).status_code
        == 404
    )
    assert (
        client.post(
            LISTS_URL,
            {"title": "Trashed", "folder_id": str(trashed_folder.id)},
            format="json",
        ).status_code
        == 404
    )

    created = client.post(LISTS_URL, {"title": "Valid"}, format="json").json()
    assert client.patch(f"{LISTS_URL}/{created['id']}", {}, format="json").status_code == 400
    assert (
        client.patch(
            f"{LISTS_URL}/{created['id']}",
            {"position": -1},
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
            {"title": "Taken"},
            format="json",
        ).status_code
        == 404
    )
    assert client.get(f"{LISTS_URL}/{trashed.id}").status_code == 404
    assert client.get(LISTS_URL).json() == {"results": []}
    private.refresh_from_db()
    assert private.title == "Private"


def test_inbox_cannot_be_renamed():
    user = _user("immutable-inbox@example.test")
    client = _authenticated_client(user)
    inbox = client.put(
        BOOTSTRAP_URL,
        {"timezone": "Europe/Berlin"},
        format="json",
    ).json()["inbox"]

    response = client.patch(
        f"{LISTS_URL}/{inbox['id']}",
        {"title": "Renamed"},
        format="json",
    )

    assert response.status_code == 409
    assert response.json()["error"]["code"] == "immutable_inbox"
    assert List.objects.get(pk=inbox["id"]).title == "Inbox"
