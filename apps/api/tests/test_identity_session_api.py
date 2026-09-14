from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

pytestmark = pytest.mark.django_db


def test_jwt_access_and_refresh_lifetimes():
    user = get_user_model().objects.create_user(
        email="token-lifetime@example.test",
        password="Long-unique-password-for-tests-8!",
    )

    refresh = RefreshToken.for_user(user)
    access = refresh.access_token

    assert refresh["exp"] - refresh["iat"] == int(timedelta(days=30).total_seconds())
    assert access["exp"] - access["iat"] == int(timedelta(minutes=5).total_seconds())
