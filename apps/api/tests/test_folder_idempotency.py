import hashlib
import json
import uuid
from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from dotick.identity.sessions import create_auth_session
from dotick.organization import application
from dotick.organization.models import Folder, OrganizationCreateOperation
from rest_framework.test import APIClient

FOLDERS_URL = "/api/v1/folders"
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


def test_folder_create_requires_client_operation_id():
    user = _user("folder-operation-required@example.test")
    response = _client(user).post(FOLDERS_URL, {"title": "Work"}, format="json")

    assert response.status_code == 400
    assert Folder.objects.filter(owner=user).count() == 0


def test_same_operation_and_normalized_intent_returns_existing_folder():
    user = _user("folder-operation-retry@example.test")
    client = _client(user)
    operation_id = uuid.uuid4()

    first = client.post(
        FOLDERS_URL,
        {"title": "  Work  ", "operation_id": str(operation_id)},
        format="json",
    )
    retry = client.post(
        FOLDERS_URL,
        {"title": "Work", "operation_id": str(operation_id)},
        format="json",
    )

    assert first.status_code == 201
    assert retry.status_code == 200
    assert retry.json() == first.json()
    assert Folder.objects.filter(owner=user).count() == 1
    operation = OrganizationCreateOperation.objects.get(
        owner=user,
        resource_type=OrganizationCreateOperation.ResourceType.FOLDER,
        operation_id=operation_id,
    )
    expected_digest = hashlib.sha256(
        json.dumps(
            {"title": "Work"},
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode()
    ).hexdigest()
    assert operation.intent_digest == expected_digest
    assert str(operation.resource_id) == first.json()["id"]


def test_same_operation_with_different_intent_returns_stable_conflict():
    user = _user("folder-operation-conflict@example.test")
    client = _client(user)
    operation_id = uuid.uuid4()

    first = client.post(
        FOLDERS_URL,
        {"title": "Work", "operation_id": str(operation_id)},
        format="json",
    )
    conflict = client.post(
        FOLDERS_URL,
        {"title": "Personal", "operation_id": str(operation_id)},
        format="json",
    )

    assert first.status_code == 201
    assert conflict.status_code == 409
    assert conflict.json()["error"]["code"] == "idempotency_conflict"
    assert Folder.objects.filter(owner=user).count() == 1
    assert Folder.objects.get(owner=user).title == "Work"


def test_same_operation_id_is_owner_scoped_for_folder_creation():
    first_user = _user("folder-operation-owner-a@example.test")
    second_user = _user("folder-operation-owner-b@example.test")
    operation_id = uuid.uuid4()

    first = _client(first_user).post(
        FOLDERS_URL,
        {"title": "First", "operation_id": str(operation_id)},
        format="json",
    )
    second = _client(second_user).post(
        FOLDERS_URL,
        {"title": "Second", "operation_id": str(operation_id)},
        format="json",
    )

    assert first.status_code == 201
    assert second.status_code == 201
    assert first.json()["id"] != second.json()["id"]
    assert OrganizationCreateOperation.objects.filter(operation_id=operation_id).count() == 2


def test_folder_and_operation_record_are_atomic():
    user = _user("folder-operation-atomic@example.test")

    with patch.object(
        OrganizationCreateOperation.objects,
        "create",
        side_effect=RuntimeError("operation write failed"),
    ):
        with pytest.raises(RuntimeError, match="operation write failed"):
            application.create_folder_idempotent(
                actor_id=user.id,
                title="Atomic",
                operation_id=uuid.uuid4(),
            )

    assert Folder.objects.filter(owner=user).count() == 0
    assert OrganizationCreateOperation.objects.filter(owner=user).count() == 0


def test_integrity_race_resolves_to_the_concurrent_existing_folder():
    user = _user("folder-operation-race@example.test")
    operation_id = uuid.uuid4()
    existing_folder = Folder.objects.create(owner=user, title="Work", position=0)
    existing_operation = OrganizationCreateOperation.objects.create(
        owner=user,
        resource_type=OrganizationCreateOperation.ResourceType.FOLDER,
        operation_id=operation_id,
        intent_digest=application._folder_creation_intent_digest(title="Work"),
        resource_id=existing_folder.id,
    )

    with (
        patch.object(
            application,
            "_get_folder_creation_operation",
            side_effect=[None, existing_operation],
        ),
        patch.object(
            OrganizationCreateOperation.objects,
            "create",
            side_effect=IntegrityError("concurrent duplicate"),
        ),
    ):
        row, created = application.create_folder_idempotent(
            actor_id=user.id,
            title="Work",
            operation_id=operation_id,
        )

    assert created is False
    assert row.id == existing_folder.id
    assert Folder.objects.filter(owner=user).count() == 1
