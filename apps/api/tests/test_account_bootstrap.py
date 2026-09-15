from concurrent.futures import ThreadPoolExecutor

import pytest
from django.contrib.auth import get_user_model
from django.db import close_old_connections
from dotick.identity.models import UserPreferences
from dotick.identity.sessions import create_auth_session
from dotick.organization.models import Column, List
from rest_framework.test import APIClient

BOOTSTRAP_URL = "/api/v1/account/bootstrap"
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


def test_bootstrap_creates_preferences_inbox_and_default_column():
    user = _user("bootstrap@example.test")

    response = _authenticated_client(user).put(
        BOOTSTRAP_URL,
        {"timezone": "Europe/London"},
        format="json",
    )

    assert response.status_code == 200
    preferences = UserPreferences.objects.get(user=user)
    inbox = List.objects.get(owner=user, is_inbox=True)
    default_column = Column.objects.get(list=inbox, is_default=True)
    assert preferences.timezone == "Europe/London"
    assert inbox.title == "Inbox"
    assert inbox.folder is None
    assert inbox.is_trashed is False
    assert inbox.columns.count() == 1
    assert response.json() == {
        "preferences": {"timezone": "Europe/London"},
        "inbox": {
            "id": str(inbox.id),
            "title": "Inbox",
            "is_inbox": True,
            "default_column": {
                "id": str(default_column.id),
                "is_default": True,
            },
        },
    }
    assert "not_sectioned" not in response.content.decode()


def test_repeated_bootstrap_is_idempotent():
    user = _user("repeated-bootstrap@example.test")
    client = _authenticated_client(user)

    first = client.put(BOOTSTRAP_URL, {"timezone": "Europe/London"}, format="json")
    repeated = client.put(BOOTSTRAP_URL, {"timezone": "Europe/London"}, format="json")

    assert first.status_code == 200
    assert repeated.status_code == 200
    assert repeated.json() == first.json()
    assert UserPreferences.objects.filter(user=user).count() == 1
    assert List.objects.filter(owner=user, is_inbox=True).count() == 1
    assert (
        Column.objects.filter(list__owner=user, list__is_inbox=True, is_default=True).count() == 1
    )


def test_bootstrap_does_not_overwrite_existing_preferences():
    user = _user("existing-preferences@example.test")
    UserPreferences.objects.create(user=user, timezone="Asia/Tehran")

    response = _authenticated_client(user).put(
        BOOTSTRAP_URL,
        {"timezone": "Europe/London"},
        format="json",
    )

    assert response.status_code == 200
    assert response.json()["preferences"] == {"timezone": "Asia/Tehran"}
    assert UserPreferences.objects.get(user=user).timezone == "Asia/Tehran"


def test_bootstrap_requires_authentication_and_valid_timezone():
    assert (
        APIClient().put(
            BOOTSTRAP_URL,
            {"timezone": "Europe/London"},
            format="json",
        ).status_code
        == 401
    )

    user = _user("invalid-bootstrap@example.test")
    response = _authenticated_client(user).put(
        BOOTSTRAP_URL,
        {"timezone": "Mars/Olympus_Mons"},
        format="json",
    )

    assert response.status_code == 400
    assert not UserPreferences.objects.filter(user=user).exists()
    assert not List.objects.filter(owner=user, is_inbox=True).exists()


@pytest.mark.django_db(transaction=True)
def test_concurrent_bootstrap_keeps_exactly_one_inbox_and_default_column():
    user = _user("concurrent-bootstrap@example.test")
    tokens = [create_auth_session(user=user)[1].access for _ in range(2)]

    def bootstrap(access):
        close_old_connections()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        response = client.put(
            BOOTSTRAP_URL,
            {"timezone": "Europe/London"},
            format="json",
        )
        result = response.status_code, response.json()
        close_old_connections()
        return result

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(bootstrap, tokens))

    assert [status for status, _ in results] == [200, 200]
    assert results[0][1] == results[1][1]
    assert UserPreferences.objects.filter(user=user).count() == 1
    assert List.objects.filter(owner=user, is_inbox=True).count() == 1
    assert (
        Column.objects.filter(list__owner=user, list__is_inbox=True, is_default=True).count() == 1
    )
