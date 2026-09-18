import uuid
from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from dotick.identity.sessions import create_auth_session
from dotick.organization import idempotency
from dotick.organization.application import create_list
from dotick.organization.models import Column, OrganizationCreateOperation
from rest_framework.test import APIClient

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


def _columns_url(list_id):
    return f"/api/v1/lists/{list_id}/columns"


def test_column_create_requires_client_operation_id():
    user = _user("column-operation-required@example.test")
    row, _ = create_list(owner=user, title="Project")

    response = _client(user).post(_columns_url(row.id), {"title": "Doing"}, format="json")

    assert response.status_code == 400
    assert Column.objects.filter(list=row, is_default=False).count() == 0


def test_identical_column_retry_returns_existing_column():
    user = _user("column-operation-retry@example.test")
    row, default_column = create_list(owner=user, title="Project")
    client = _client(user)
    operation_id = uuid.uuid4()
    payload = {"title": "  Doing  ", "operation_id": str(operation_id)}

    first = client.post(_columns_url(row.id), payload, format="json")
    retry = client.post(
        _columns_url(row.id),
        {**payload, "title": "Doing"},
        format="json",
    )

    assert first.status_code == 201
    assert retry.status_code == 200
    assert retry.json() == first.json()
    assert first.json()["is_default"] is False
    assert first.json()["position"] == 1
    assert Column.objects.filter(list=row, is_default=True).get().id == default_column.id
    assert Column.objects.filter(list=row, is_default=False).count() == 1

    operation = OrganizationCreateOperation.objects.get(
        owner=user,
        resource_type=OrganizationCreateOperation.ResourceType.COLUMN,
        operation_id=operation_id,
    )
    assert operation.intent_digest == idempotency._column_creation_intent_digest(
        list_id=row.id,
        title="Doing",
    )
    assert str(operation.resource_id) == first.json()["id"]


def test_column_operation_reuse_with_different_title_returns_conflict():
    user = _user("column-operation-title-conflict@example.test")
    row, _ = create_list(owner=user, title="Project")
    client = _client(user)
    operation_id = uuid.uuid4()

    created = client.post(
        _columns_url(row.id),
        {"title": "Doing", "operation_id": str(operation_id)},
        format="json",
    )
    conflict = client.post(
        _columns_url(row.id),
        {"title": "Done", "operation_id": str(operation_id)},
        format="json",
    )

    assert created.status_code == 201
    assert conflict.status_code == 409
    assert conflict.json()["error"]["code"] == "idempotency_conflict"
    assert Column.objects.filter(list=row, is_default=False).count() == 1


def test_column_operation_reuse_with_different_list_returns_conflict():
    user = _user("column-operation-list-conflict@example.test")
    first_list, _ = create_list(owner=user, title="First")
    second_list, _ = create_list(owner=user, title="Second")
    client = _client(user)
    operation_id = uuid.uuid4()

    created = client.post(
        _columns_url(first_list.id),
        {"title": "Doing", "operation_id": str(operation_id)},
        format="json",
    )
    conflict = client.post(
        _columns_url(second_list.id),
        {"title": "Doing", "operation_id": str(operation_id)},
        format="json",
    )

    assert created.status_code == 201
    assert conflict.status_code == 409
    assert conflict.json()["error"]["code"] == "idempotency_conflict"
    assert Column.objects.filter(list=first_list, is_default=False).count() == 1
    assert Column.objects.filter(list=second_list, is_default=False).count() == 0


def test_column_creation_preserves_list_owner_scope():
    owner = _user("column-operation-owner@example.test")
    other = _user("column-operation-other@example.test")
    foreign_list, _ = create_list(owner=other, title="Foreign")
    operation_id = uuid.uuid4()

    response = _client(owner).post(
        _columns_url(foreign_list.id),
        {"title": "Rejected", "operation_id": str(operation_id)},
        format="json",
    )

    assert response.status_code == 404
    assert Column.objects.filter(list=foreign_list, is_default=False).count() == 0
    assert not OrganizationCreateOperation.objects.filter(
        owner=owner,
        resource_type=OrganizationCreateOperation.ResourceType.COLUMN,
        operation_id=operation_id,
    ).exists()


def test_same_column_operation_id_is_independent_across_owners():
    first_user = _user("column-operation-owner-a@example.test")
    second_user = _user("column-operation-owner-b@example.test")
    first_list, _ = create_list(owner=first_user, title="First")
    second_list, _ = create_list(owner=second_user, title="Second")
    operation_id = uuid.uuid4()

    first = _client(first_user).post(
        _columns_url(first_list.id),
        {"title": "Doing", "operation_id": str(operation_id)},
        format="json",
    )
    second = _client(second_user).post(
        _columns_url(second_list.id),
        {"title": "Doing", "operation_id": str(operation_id)},
        format="json",
    )

    assert first.status_code == 201
    assert second.status_code == 201
    assert first.json()["id"] != second.json()["id"]
    assert OrganizationCreateOperation.objects.filter(
        resource_type=OrganizationCreateOperation.ResourceType.COLUMN,
        operation_id=operation_id,
    ).count() == 2


def test_column_and_operation_are_atomic():
    user = _user("column-operation-atomic@example.test")
    row, default_column = create_list(owner=user, title="Project")

    with patch.object(
        OrganizationCreateOperation.objects,
        "create",
        side_effect=RuntimeError("operation write failed"),
    ):
        with pytest.raises(RuntimeError, match="operation write failed"):
            idempotency.create_column(
                actor_id=user.id,
                list_id=row.id,
                title="Doing",
                operation_id=uuid.uuid4(),
            )

    assert Column.objects.filter(list=row).count() == 1
    assert Column.objects.get(list=row).id == default_column.id
    assert OrganizationCreateOperation.objects.filter(owner=user).count() == 0


def test_column_integrity_race_resolves_to_concurrent_existing_result():
    user = _user("column-operation-race@example.test")
    row, default_column = create_list(owner=user, title="Project")
    operation_id = uuid.uuid4()
    existing_column = Column.objects.create(
        list=row,
        title="Doing",
        position=1,
        is_default=False,
    )
    existing_operation = OrganizationCreateOperation.objects.create(
        owner=user,
        resource_type=OrganizationCreateOperation.ResourceType.COLUMN,
        operation_id=operation_id,
        intent_digest=idempotency._column_creation_intent_digest(
            list_id=row.id,
            title="Doing",
        ),
        resource_id=existing_column.id,
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
        column, created = idempotency.create_column(
            actor_id=user.id,
            list_id=row.id,
            title="Doing",
            operation_id=operation_id,
        )

    assert created is False
    assert column.id == existing_column.id
    assert Column.objects.filter(list=row, is_default=False).count() == 1
    assert Column.objects.filter(list=row, is_default=True).get().id == default_column.id
