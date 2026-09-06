import uuid

import pytest
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db
URL = "/api/v1/foundation/checkpoints"


def test_checkpoint_survives_a_new_request_and_has_stable_identity(signed_in):
    client, user = signed_in()
    response = client.post(URL, {"text": "  First persisted checkpoint  "}, format="json")
    assert response.status_code == 201
    created = response.json()
    assert uuid.UUID(created["id"])
    assert created["text"] == "First persisted checkpoint"
    assert created["created_at"].endswith("Z")
    assert set(created) == {"id", "text", "created_at"}
    assert client.get(f"{URL}/{created['id']}").json() == created
    assert client.get(URL).json() == {"results": [created]}


def test_private_checkpoint_requires_credentials():
    client = APIClient()
    assert client.get(URL).status_code == 401
    assert client.post(URL, {"text": "Anonymous"}, format="json").status_code == 401


def test_another_user_including_staff_cannot_list_or_retrieve_a_checkpoint(signed_in):
    owner, _ = signed_in()
    other, staff = signed_in("other@example.test")
    staff.is_staff = True
    staff.is_superuser = True
    staff.save()
    record = owner.post(URL, {"text": "Private text"}, format="json").json()
    assert other.get(URL).json() == {"results": []}
    assert other.get(f"{URL}/{record['id']}").status_code == 404


@pytest.mark.parametrize("payload", [{}, {"text": "  "}, {"text": "x" * 241}, {"text": None}])
def test_invalid_checkpoint_does_not_create_a_record(signed_in, payload):
    client, _ = signed_in()
    assert client.post(URL, payload, format="json").status_code == 400
    assert client.get(URL).json() == {"results": []}


def test_forged_ownership_fields_are_rejected(signed_in):
    client, _ = signed_in()
    response = client.post(URL, {"text": "Hello", "owner_id": str(uuid.uuid4())}, format="json")
    assert response.status_code == 400
    assert client.get(URL).json() == {"results": []}


def test_workbench_is_unavailable_when_disabled(signed_in, settings):
    client, _ = signed_in()
    settings.FOUNDATION_ENABLED = False
    assert client.get(URL).status_code == 404


def test_inactive_account_cannot_read_its_data(signed_in):
    client, user = signed_in()
    user.is_active = False
    user.save()
    assert client.get(URL).status_code == 401
