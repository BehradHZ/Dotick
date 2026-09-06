import base64

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


@pytest.fixture
def signed_in(db):
    def make_client(email="owner@example.test"):
        password = "Only-for-automated-tests-8!"
        user = get_user_model().objects.create_user(email, password)
        client = APIClient()
        token = base64.b64encode(f"{email}:{password}".encode()).decode()
        client.credentials(HTTP_AUTHORIZATION=f"Basic {token}")
        return client, user

    return make_client
