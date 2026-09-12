import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import identify_hasher
from django.core.exceptions import FieldDoesNotExist, ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.utils import timezone

from dotick.identity.models import UserPreferences


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

    def test_direct_save_normalizes_email_to_lowercase(self):
        user = get_user_model()(
            email="  Direct@Example.TEST  ",
            handle="direct_user",
            display_name="Direct User",
        )

        user.save()

        self.assertEqual(user.email, "direct@example.test")

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
            handle="first_case_user",
            display_name="First Case User",
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                user_model.objects.create(
                    email="casesensitive@example.test",
                    handle="second_case_user",
                    display_name="Second Case User",
                )

    def test_account_fields_preserve_uuid_identity_and_lifecycle(self):
        user = get_user_model().objects.create_user(
            email="account@example.test",
            password="Strong-Test-Password-123!",
            handle="Account_User",
            display_name="Account User",
            profile_picture_url="https://example.test/profile.png",
            is_active=False,
        )

        account_id = user.id
        verified_at = timezone.now()
        user.email_verified_at = verified_at
        user.is_active = True
        user.save(update_fields=["email_verified_at", "is_active"])
        user.refresh_from_db()

        self.assertEqual(user.id, account_id)
        self.assertEqual(user.handle, "Account_User")
        self.assertEqual(user.display_name, "Account User")
        self.assertEqual(user.profile_picture_url, "https://example.test/profile.png")
        self.assertEqual(user.email_verified_at, verified_at)
        self.assertTrue(user.is_active)

    def test_handle_is_case_insensitively_unique(self):
        user_model = get_user_model()
        user_model.objects.create_user(
            email="first-handle@example.test",
            handle="Shared_Handle",
            display_name="First User",
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                user_model.objects.create_user(
                    email="second-handle@example.test",
                    handle="shared_handle",
                    display_name="Second User",
                )

    def test_handle_validator_enforces_public_format(self):
        user = get_user_model()(
            email="invalid-handle@example.test",
            handle="no-hyphens",
            display_name="Invalid Handle",
        )

        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_framework_created_user_gets_required_identity_fields(self):
        user = get_user_model().objects.create_user(
            email="generated.identity@example.test",
        )

        self.assertRegex(user.handle, r"^[A-Za-z0-9_]{3,30}$")
        self.assertEqual(user.display_name, "generated.identity")

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


class UserPreferencesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            email="preferences@example.test",
            password="Strong-Test-Password-123!",
        )

    def test_preferences_use_account_uuid_and_store_iana_timezone(self):
        preferences = UserPreferences.objects.create(
            user=self.user,
            timezone="Europe/Berlin",
        )

        self.assertEqual(preferences.pk, self.user.id)
        self.assertEqual(preferences.timezone, "Europe/Berlin")

    def test_preferences_reject_unknown_timezone(self):
        with self.assertRaisesMessage(
            ValidationError,
            "Enter a valid IANA timezone identifier.",
        ):
            UserPreferences.objects.create(
                user=self.user,
                timezone="Mars/Olympus_Mons",
            )

        self.assertFalse(UserPreferences.objects.filter(user=self.user).exists())

    def test_preferences_do_not_include_day_boundary_behavior(self):
        field_names = {field.name for field in UserPreferences._meta.get_fields()}

        self.assertNotIn("day_boundary_offset_minutes", field_names)
