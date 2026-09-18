import uuid
from concurrent.futures import ThreadPoolExecutor

import pytest
from django.contrib.auth import get_user_model
from django.db import close_old_connections
from dotick.identity.sessions import create_auth_session
from dotick.organization import application, idempotency
from dotick.organization.models import Column, Folder, List, OrganizationCreateOperation
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db(transaction=True)


def _user(email):
    return get_user_model().objects.create_user(
        email=email,
        password="Only-for-automated-tests-8!",
    )


def _run_concurrently(call):
    def run():
        close_old_connections()
        try:
            return call()
        finally:
            close_old_connections()

    with ThreadPoolExecutor(max_workers=2) as pool:
        return [future.result(timeout=10) for future in [pool.submit(run), pool.submit(run)]]


def _post(*, access_token, url, payload):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return client.post(url, payload, format="json")


def _folder_api_case(owner):
    return "/api/v1/folders", {"title": "Work"}, Folder.objects.filter(owner=owner)


def _list_api_case(owner):
    return "/api/v1/lists", {"title": "Work"}, List.objects.filter(owner=owner)


def _column_api_case(owner):
    parent, _ = application.create_list(owner=owner, title="Project")
    return (
        f"/api/v1/lists/{parent.id}/columns",
        {"title": "Doing"},
        Column.objects.filter(list=parent, is_default=False),
    )


def test_two_identical_folder_creates_leave_one_resource_and_operation():
    owner = _user("folder-create-race@example.test")
    operation_id = uuid.uuid4()

    results = _run_concurrently(
        lambda: application.create_folder_idempotent(
            actor_id=owner.id,
            title="Work",
            operation_id=operation_id,
        )
    )

    assert {row.id for row, _ in results} == {results[0][0].id}
    assert sorted(created for _, created in results) == [False, True]
    assert Folder.objects.filter(owner=owner).count() == 1
    assert OrganizationCreateOperation.objects.filter(
        owner=owner,
        resource_type=OrganizationCreateOperation.ResourceType.FOLDER,
        operation_id=operation_id,
    ).count() == 1


def test_two_identical_list_creates_leave_one_resource_default_column_and_operation():
    owner = _user("list-create-race@example.test")
    operation_id = uuid.uuid4()

    results = _run_concurrently(
        lambda: idempotency.create_list(
            actor_id=owner.id,
            title="Work",
            operation_id=operation_id,
        )
    )

    assert {row.id for row, _, _ in results} == {results[0][0].id}
    assert {column.id for _, column, _ in results} == {results[0][1].id}
    assert sorted(created for _, _, created in results) == [False, True]
    assert List.objects.filter(owner=owner).count() == 1
    assert Column.objects.filter(list__owner=owner, is_default=True).count() == 1
    assert OrganizationCreateOperation.objects.filter(
        owner=owner,
        resource_type=OrganizationCreateOperation.ResourceType.LIST,
        operation_id=operation_id,
    ).count() == 1


def test_two_identical_column_creates_leave_one_resource_and_operation():
    owner = _user("column-create-race@example.test")
    parent, _ = application.create_list(owner=owner, title="Project")
    operation_id = uuid.uuid4()

    results = _run_concurrently(
        lambda: idempotency.create_column(
            actor_id=owner.id,
            list_id=parent.id,
            title="Doing",
            operation_id=operation_id,
        )
    )

    assert {row.id for row, _ in results} == {results[0][0].id}
    assert sorted(created for _, created in results) == [False, True]
    assert Column.objects.filter(list=parent, is_default=False).count() == 1
    assert OrganizationCreateOperation.objects.filter(
        owner=owner,
        resource_type=OrganizationCreateOperation.ResourceType.COLUMN,
        operation_id=operation_id,
    ).count() == 1


@pytest.mark.parametrize(
    "case_factory",
    [_folder_api_case, _list_api_case, _column_api_case],
    ids=["folder", "list", "column"],
)
def test_concurrent_identical_api_retry_returns_created_and_replayed_result(case_factory):
    owner = _user(f"concurrent-api-{case_factory.__name__}@example.test")
    _, pair = create_auth_session(user=owner)
    url, intent, resources = case_factory(owner)
    operation_id = uuid.uuid4()
    payload = {**intent, "operation_id": str(operation_id)}

    responses = _run_concurrently(
        lambda: _post(
            access_token=pair.access,
            url=url,
            payload=payload,
        )
    )

    assert sorted(response.status_code for response in responses) == [200, 201]
    assert responses[0].json() == responses[1].json()
    assert resources.count() == 1
    assert OrganizationCreateOperation.objects.filter(
        owner=owner,
        operation_id=operation_id,
    ).count() == 1
