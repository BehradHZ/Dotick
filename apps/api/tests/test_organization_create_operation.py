import uuid

import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction

from dotick.organization.models import OrganizationCreateOperation

pytestmark = pytest.mark.django_db


def _user(email):
    return get_user_model().objects.create_user(
        email=email,
        password="Only-for-automated-tests-8!",
    )


def _operation(*, owner, operation_id=None, resource_type=None, digest="a" * 64):
    return OrganizationCreateOperation.objects.create(
        owner=owner,
        resource_type=resource_type or OrganizationCreateOperation.ResourceType.FOLDER,
        operation_id=operation_id or uuid.uuid4(),
        intent_digest=digest,
        resource_id=uuid.uuid4(),
    )


def test_create_operation_persists_owner_scope_intent_and_result_identity():
    owner = _user("operation-owner@example.test")
    operation_id = uuid.uuid4()
    resource_id = uuid.uuid4()

    row = OrganizationCreateOperation.objects.create(
        owner=owner,
        resource_type=OrganizationCreateOperation.ResourceType.FOLDER,
        operation_id=operation_id,
        intent_digest="b" * 64,
        resource_id=resource_id,
    )

    assert row.owner_id == owner.id
    assert row.resource_type == "folder"
    assert row.operation_id == operation_id
    assert row.intent_digest == "b" * 64
    assert row.resource_id == resource_id


def test_same_owner_resource_and_operation_id_cannot_be_reused_with_different_intent():
    owner = _user("operation-conflict@example.test")
    operation_id = uuid.uuid4()
    _operation(owner=owner, operation_id=operation_id, digest="a" * 64)

    with pytest.raises(IntegrityError), transaction.atomic():
        _operation(owner=owner, operation_id=operation_id, digest="b" * 64)


def test_same_operation_id_is_independent_across_owners_and_resource_types():
    first_owner = _user("operation-first@example.test")
    second_owner = _user("operation-second@example.test")
    operation_id = uuid.uuid4()

    first = _operation(owner=first_owner, operation_id=operation_id)
    second = _operation(owner=second_owner, operation_id=operation_id)
    third = _operation(
        owner=first_owner,
        operation_id=operation_id,
        resource_type=OrganizationCreateOperation.ResourceType.LIST,
    )

    assert first.operation_id == second.operation_id == third.operation_id
    assert OrganizationCreateOperation.objects.count() == 3


def test_create_operation_record_is_append_only_after_creation():
    owner = _user("operation-immutable@example.test")
    row = _operation(owner=owner)
    row.intent_digest = "c" * 64

    with pytest.raises(ValueError, match="immutable"):
        row.save()

    row.refresh_from_db()
    assert row.intent_digest == "a" * 64


def test_create_operation_model_declares_lookup_index_and_database_constraints():
    index_names = {index.name for index in OrganizationCreateOperation._meta.indexes}
    constraint_names = {
        constraint.name for constraint in OrganizationCreateOperation._meta.constraints
    }

    assert "orgop_result_lookup" in index_names
    assert {
        "orgop_owner_type_operation_uq",
        "orgop_resource_type_valid",
        "orgop_intent_digest_nonempty",
    } <= constraint_names
