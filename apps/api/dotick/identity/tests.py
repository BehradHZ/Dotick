import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import identify_hasher
from django.core.exceptions import FieldDoesNotExist
from django.db import IntegrityError, transaction
from django.test import TestCase


class CustomUserTests(TestCase):
    def test_identity_user_is_the_configured_custom_user(self):
        user_model = get_user_model()

        self.assertEqual(user_model._meta.label, "identity.User")
        self.assertEqual(user_model.USERNAME_FIELD, "email")

        with self.assertRaises(FieldDoesNotExist):
            user_model._meta.get_field("username")

    def test_create_user_normalizes_email_to_lowercase(self):
        user = get_user_model().objects.create_user(
            email="Developer@Example.TEST",
            password="Strong-Test-Password-123!",
        )

        self.assertEqual(user.email, "developer@example.test")

    def test_user_primary_key_is_uuid(self):
        user = get_user_model().objects.create_user(
            email="uuid@example.test",
            password="Strong-Test-Password-123!",
        )

        self.assertIsInstance(user.pk, uuid.UUID)

    def test_email_uniqueness_is_case_insensitive(self):
        user_model = get_user_model()

        user_model.objects.create(
            email="CaseSensitive@Example.TEST",
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                user_model.objects.create(
                    email="casesensitive@example.test",
                )

    def test_password_is_hashed_with_argon2(self):
        password = "Strong-Test-Password-123!"

        user = get_user_model().objects.create_user(
            email="argon2@example.test",
            password=password,
        )

        self.assertEqual(identify_hasher(user.password).algorithm, "argon2")
        self.assertTrue(user.check_password(password))

    def test_natural_key_email_lookup_is_case_insensitive(self):
        user = get_user_model().objects.create_user(
            email="lookup@example.test",
            password="Strong-Test-Password-123!",
        )

        found = get_user_model().objects.get_by_natural_key("LOOKUP@EXAMPLE.TEST")

        self.assertEqual(found, user)
