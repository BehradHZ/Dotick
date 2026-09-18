import pytest
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import F
from django.http import Http404
from rest_framework.exceptions import ValidationError

from config.errors import api_exception_handler
from dotick.organization.concurrency import (
    OrganizationVersionConflict,
    increment_locked_version,
    lock_owned_versioned_resource,
    validate_expected_version,
)
from dotick.organization.models import Column, Folder, List

pytestmark = pytest.mark.django_db(transaction=True)


def _user(email):
    return get_user_model().objects.create_user(
        email=email,
        password="Only-for-automated-tests-8!",
    )


def test_version_conflict_has_stable_http_409_surface():
    owner = _user("version-conflict@example.test")
    folder = Folder.objects.create(owner=owner, title="Work")

    response = api_exception_handler(OrganizationVersionConflict(folder), {})

    assert response.status_code == 409
    assert response.data["error"]["code"] == "version_conflict"
    assert response.data["error"]["details"]["current"] == {
        "id": str(folder.id),
        "version": 1,
    }


@pytest.mark.parametrize("value", [0, -1, True, None, "1"])
def test_expected_version_validator_rejects_non_positive_or_non_integer_values(value):
    with pytest.raises(ValidationError):
        validate_expected_version(value)


def test_expected_version_validator_accepts_positive_integer():
    assert validate_expected_version(1) == 1
    assert validate_expected_version(7) == 7


def test_version_comparison_requires_an_active_transaction():
    owner = _user("transaction-required@example.test")
    folder = Folder.objects.create(owner=owner, title="Work")

    with pytest.raises(RuntimeError, match="requires an active transaction"):
        lock_owned_versioned_resource(
            model=Folder,
            actor_id=owner.id,
            resource_id=folder.id,
            expected_version=1,
        )


def test_locked_update_increments_server_version_atomically():
    owner = _user("atomic-version@example.test")
    folder = Folder.objects.create(owner=owner, title="Work")

    with transaction.atomic():
        row = lock_owned_versioned_resource(
            model=Folder,
            actor_id=owner.id,
            resource_id=folder.id,
            expected_version=1,
        )
        row = increment_locked_version(
            row=row,
            actor_id=owner.id,
            expected_version=1,
            updates={"title": "Renamed"},
        )

    assert row.title == "Renamed"
    assert row.version == 2


def test_stale_version_is_rejected_without_overwriting_current_state():
    owner = _user("stale-version@example.test")
    folder = Folder.objects.create(owner=owner, title="Current")
    Folder.objects.filter(pk=folder.pk).update(version=2)

    with transaction.atomic(), pytest.raises(OrganizationVersionConflict):
        lock_owned_versioned_resource(
            model=Folder,
            actor_id=owner.id,
            resource_id=folder.id,
            expected_version=1,
        )

    folder.refresh_from_db()
    assert folder.title == "Current"
    assert folder.version == 2


def test_owner_scope_is_applied_before_mutation():
    owner = _user("resource-owner@example.test")
    other = _user("other-actor@example.test")
    folder = Folder.objects.create(owner=owner, title="Private")

    with transaction.atomic(), pytest.raises(Http404):
        lock_owned_versioned_resource(
            model=Folder,
            actor_id=other.id,
            resource_id=folder.id,
            expected_version=1,
        )

    folder.refresh_from_db()
    assert folder.title == "Private"
    assert folder.version == 1


def test_column_owner_scope_flows_through_its_list():
    owner = _user("column-owner@example.test")
    other = _user("column-other@example.test")
    row = List.objects.create(owner=owner, title="Private List")
    column = Column.objects.create(list=row, title="Private Column")

    with transaction.atomic(), pytest.raises(Http404):
        lock_owned_versioned_resource(
            model=Column,
            actor_id=other.id,
            resource_id=column.id,
            expected_version=1,
        )


def test_client_version_cannot_be_written_as_server_state():
    owner = _user("server-version@example.test")
    folder = Folder.objects.create(owner=owner, title="Work")

    with transaction.atomic():
        row = lock_owned_versioned_resource(
            model=Folder,
            actor_id=owner.id,
            resource_id=folder.id,
            expected_version=1,
        )
        with pytest.raises(ValueError, match="server-owned"):
            increment_locked_version(
                row=row,
                actor_id=owner.id,
                expected_version=1,
                updates={"title": "Rejected", "version": 99},
            )

    folder.refresh_from_db()
    assert folder.title == "Work"
    assert folder.version == 1


def test_compare_and_swap_guard_rejects_changed_database_version():
    owner = _user("cas-version@example.test")
    folder = Folder.objects.create(owner=owner, title="Original")

    with transaction.atomic():
        row = lock_owned_versioned_resource(
            model=Folder,
            actor_id=owner.id,
            resource_id=folder.id,
            expected_version=1,
        )
        Folder.objects.filter(pk=folder.pk).update(
            title="Competing state",
            version=F("version") + 1,
        )
        with pytest.raises(OrganizationVersionConflict):
            increment_locked_version(
                row=row,
                actor_id=owner.id,
                expected_version=1,
                updates={"title": "Stale overwrite"},
            )

    folder.refresh_from_db()
    assert folder.title == "Competing state"
    assert folder.version == 2
