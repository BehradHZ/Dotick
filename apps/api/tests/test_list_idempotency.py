import uuid
from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from dotick.identity.sessions import create_auth_session
from dotick.organization import idempotency
from dotick.organization.application import create_list
from dotick.organization.models import Column, Folder, List, OrganizationCreateOperation
from rest_framework.test import APIClient

LISTS_URL = "/api/v1/lists"
pytestmark = pytest.mark.django_db


def _user(email):
    return get_user_model().objects.create_user(
        email=email,
        password="Only-for-automated-tests-8!",
    )


def _client(user):
    _, pair = create_auth_session(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {pair.access}")
    return client


def test_list_create_requires_client_operation_id():
    user = _user("list-operation-required@example.test")

    response = _client(user).post(LISTS_URL, {"title": "Work"}, format="json")

    assert response.status_code == 400
    assert List.objects.filter(owner=user).count() == 0


def test_identical_list_retry_returns_same_list_and_default_column():
    user = _user("list-operation-retry@example.test")
    client = _client(user)
    folder = Folder.objects.create(owner=user, title="Projects")
    operation_id = uuid.uuid4()
    payload = {
        "title": "  Work  ",
        "folder_id": str(folder.id),
        "position": 7,
        "operation_id": str(operation_id),
    }

    first = client.post(LISTS_URL, payload, format="json")
    retry = client.post(
        LISTS_URL,
        {**payload, "title": "Work"},
        format="json",
    )

    assert first.status_code == 201
    assert retry.status_code == 200
    assert retry.json() == first.json()
    assert first.json()["folder_id"] == str(folder.id)
    assert first.json()["position"] == 7
    assert first.json()["default_column"]["id"] == retry.json()["default_column"]["id"]
    assert List.objects.filter(owner=user).count() == 1
    assert Column.objects.filter(list_id=first.json()["id"], is_default=True).count() == 1

    operation = OrganizationCreateOperation.objects.get(
        owner=user,
        resource_type=OrganizationCreateOperation.ResourceType.LIST,
        operation_id=operation_id,
    )
    assert operation.intent_digest == idempotency._list_creation_intent_digest(
        title="Work",
        folder_id=folder.id,
        position=7,
    )
    assert str(operation.resource_id) == first.json()["id"]


def test_list_operation_reuse_with_different_intent_returns_conflict():
    user = _user("list-operation-conflict@example.test")
    client = _client(user)
    first_folder = Folder.objects.create(owner=user, title="First")
    second_folder = Folder.objects.create(owner=user, title="Second")
    operation_id = uuid.uuid4()
    original = {
        "title": "Work",
        "folder_id": str(first_folder.id),
        "position": 4,
        "operation_id": str(operation_id),
    }

    created = client.post(LISTS_URL, original, format="json")
    changed_title = client.post(
        LISTS_URL,
        {**original, "title": "Personal"},
        format="json",
    )
    changed_folder = client.post(
        LISTS_URL,
        {**original, "folder_id": str(second_folder.id)},
        format="json",
    )
    changed_position = client.post(
        LISTS_URL,
        {**original, "position": 5},
        format="json",
    )

    assert created.status_code == 201
    for conflict in (changed_title, changed_folder, changed_position):
        assert conflict.status_code == 409
        assert conflict.json()["error"]["code"] == "idempotency_conflict"
    assert List.objects.filter(owner=user).count() == 1


def test_implicit_and_explicit_list_position_are_different_intents():
    user = _user("list-position-intent@example.test")
    client = _client(user)
    operation_id = uuid.uuid4()

    first = client.post(
        LISTS_URL,
        {"title": "Work", "operation_id": str(operation_id)},
        format="json",
    )
    conflict = client.post(
        LISTS_URL,
        {"title": "Work", "position": 0, "operation_id": str(operation_id)},
        format="json",
    )

    assert first.status_code == 201
    assert conflict.status_code == 409
    assert conflict.json()["error"]["code"] == "idempotency_conflict"


def test_list_creation_preserves_folder_owner_scope():
    owner = _user("list-operation-owner@example.test")
    other = _user("list-operation-other@example.test")
    foreign_folder = Folder.objects.create(owner=other, title="Foreign")
    operation_id = uuid.uuid4()

    response = _client(owner).post(
        LISTS_URL,
        {
            "title": "Rejected",
            "folder_id": str(foreign_folder.id),
            "operation_id": str(operation_id),
        },
        format="json",
    )

    assert response.status_code == 404
    assert List.objects.filter(owner=owner).count() == 0
    assert not OrganizationCreateOperation.objects.filter(
        owner=owner,
        resource_type=OrganizationCreateOperation.ResourceType.LIST,
        operation_id=operation_id,
    ).exists()


def test_same_list_operation_id_is_independent_across_owners():
    first_user = _user("list-operation-owner-a@example.test")
    second_user = _user("list-operation-owner-b@example.test")
    operation_id = uuid.uuid4()

    first = _client(first_user).post(
        LISTS_URL,
        {"title": "First", "operation_id": str(operation_id)},
        format="json",
    )
    second = _client(second_user).post(
        LISTS_URL,
        {"title": "Second", "operation_id": str(operation_id)},
        format="json",
    )

    assert first.status_code == 201
    assert second.status_code == 201
    assert first.json()["id"] != second.json()["id"]
    assert OrganizationCreateOperation.objects.filter(
        resource_type=OrganizationCreateOperation.ResourceType.LIST,
        operation_id=operation_id,
    ).count() == 2


def test_list_default_column_and_operation_are_atomic():
    user = _user("list-operation-atomic@example.test")

    with patch.object(
        OrganizationCreateOperation.objects,
        "create",
        side_effect=RuntimeError("operation write failed"),
    ):
        with pytest.raises(RuntimeError, match="operation write failed"):
            idempotency.create_list(
                actor_id=user.id,
                title="Atomic",
                operation_id=uuid.uuid4(),
            )

    assert List.objects.filter(owner=user).count() == 0
    assert Column.objects.filter(list__owner=user).count() == 0
    assert OrganizationCreateOperation.objects.filter(owner=user).count() == 0


def test_list_integrity_race_resolves_to_concurrent_existing_result():
    user = _user("list-operation-race@example.test")
    operation_id = uuid.uuid4()
    existing_list, existing_default = create_list(owner=user, title="Work")
    existing_operation = OrganizationCreateOperation.objects.create(
        owner=user,
        resource_type=OrganizationCreateOperation.ResourceType.LIST,
        operation_id=operation_id,
        intent_digest=idempotency._list_creation_intent_digest(
            title="Work",
            folder_id=None,
        ),
        resource_id=existing_list.id,
    )

    with (
        patch.object(
            idempotency,
            "_get_create_operation",
            side_effect=[None, existing_operation],
        ),
        patch.object(
            OrganizationCreateOperation.objects,
            "create",
            side_effect=IntegrityError("duplicate operation"),
        ),
    ):
        row, default_column, created = idempotency.create_list(
            actor_id=user.id,
            title="Work",
            operation_id=operation_id,
        )

    assert created is False
    assert row.id == existing_list.id
    assert default_column.id == existing_default.id
    assert List.objects.filter(owner=user).count() == 1
    assert Column.objects.filter(list__owner=user).count() == 1
