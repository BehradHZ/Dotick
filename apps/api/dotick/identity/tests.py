import uuid
from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import identify_hasher
from django.core.exceptions import FieldDoesNotExist, ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.utils import timezone

from dotick.identity.challenges import (
    CHALLENGE_TTL,
    ChallengeIssuanceBlocked,
    InvalidChallenge,
    consume_challenge,
    issue_challenge,
)
from dotick.identity.models import (
    AuthSession,
    ExternalIdentity,
    UserPreferences,
    VerificationChallenge,
)


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

    def test_database_rejects_email_that_bypasses_normalization(self):
        user = get_user_model().objects.create_user(
            email="normalized@example.test",
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                get_user_model().objects.filter(pk=user.pk).update(
                    email=" Not-Normalized@Example.TEST "
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
        self.assertIsNone(user.profile_picture_url)

    def test_display_name_is_not_unique(self):
        get_user_model().objects.create_user(
            email="first-name@example.test",
            handle="first_name_user",
            display_name="Shared Name",
        )
        get_user_model().objects.create_user(
            email="second-name@example.test",
            handle="second_name_user",
            display_name="Shared Name",
        )

        self.assertEqual(
            get_user_model().objects.filter(display_name="Shared Name").count(),
            2,
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


class AuthSessionTests(TestCase):
    def test_session_has_uuid_identity_and_belongs_to_user(self):
        user = get_user_model().objects.create_user(
            email="session@example.test",
            password="Strong-Test-Password-123!",
        )

        session = AuthSession.objects.create(
            user=user,
            refresh_jti=uuid.uuid4().hex,
            user_agent="Dotick test client",
        )

        self.assertIsInstance(session.pk, uuid.UUID)
        self.assertEqual(session.user, user)
        self.assertEqual(list(user.auth_sessions.all()), [session])
        self.assertIsNone(session.revoked_at)


class ExternalIdentityTests(TestCase):
    def test_external_identity_belongs_to_internal_user(self):
        user = get_user_model().objects.create_user(
            email="external@example.test",
            password=None,
        )

        identity = ExternalIdentity.objects.create(
            user=user,
            provider=ExternalIdentity.Provider.GOOGLE,
            subject="google-subject-123",
        )

        self.assertIsInstance(identity.pk, uuid.UUID)
        self.assertEqual(identity.user, user)
        self.assertEqual(list(user.external_identities.all()), [identity])


class VerificationChallengeTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            email="challenge@example.test",
            password="Strong-Test-Password-123!",
        )

    def test_code_is_six_digits_and_only_hmac_digest_is_persisted(self):
        issued_at = timezone.now()

        with (
            patch(
                "dotick.identity.challenges.timezone.now",
                return_value=issued_at,
            ),
            patch(
                "dotick.identity.challenges.secrets.randbelow",
                return_value=42,
            ) as secure_random,
        ):
            code = issue_challenge(
                user=self.user,
                purpose=VerificationChallenge.Purpose.EMAIL_VERIFICATION,
            )

        challenge = VerificationChallenge.objects.get()
        secure_random.assert_called_once_with(1_000_000)
        self.assertEqual(code, "000042")
        self.assertNotEqual(challenge.code_digest, code)
        self.assertEqual(len(challenge.code_digest), 64)
        self.assertNotIn(code, str(challenge.__dict__))
        self.assertEqual(challenge.expires_at, issued_at + CHALLENGE_TTL)

    def test_challenge_is_single_use(self):
        code = issue_challenge(
            user=self.user,
            purpose=VerificationChallenge.Purpose.EMAIL_VERIFICATION,
        )

        consume_challenge(
            user=self.user,
            purpose=VerificationChallenge.Purpose.EMAIL_VERIFICATION,
            code=code,
        )

        with self.assertRaises(InvalidChallenge):
            consume_challenge(
                user=self.user,
                purpose=VerificationChallenge.Purpose.EMAIL_VERIFICATION,
                code=code,
            )

    def test_expired_challenge_is_rejected(self):
        issued_at = timezone.now()

        with patch("dotick.identity.challenges.timezone.now", return_value=issued_at):
            code = issue_challenge(
                user=self.user,
                purpose=VerificationChallenge.Purpose.EMAIL_VERIFICATION,
            )

        with (
            patch(
                "dotick.identity.challenges.timezone.now",
                return_value=issued_at + CHALLENGE_TTL,
            ),
            self.assertRaises(InvalidChallenge),
        ):
            consume_challenge(
                user=self.user,
                purpose=VerificationChallenge.Purpose.EMAIL_VERIFICATION,
                code=code,
            )

    def test_new_challenge_consumes_previous_challenge_for_same_purpose(self):
        first_code = issue_challenge(
            user=self.user,
            purpose=VerificationChallenge.Purpose.EMAIL_VERIFICATION,
        )
        first = VerificationChallenge.objects.get()
        VerificationChallenge.objects.filter(pk=first.pk).update(
            created_at=timezone.now() - timedelta(minutes=2)
        )

        second_code = issue_challenge(
            user=self.user,
            purpose=VerificationChallenge.Purpose.EMAIL_VERIFICATION,
        )
        first.refresh_from_db()

        self.assertIsNotNone(first.consumed_at)
        with self.assertRaises(InvalidChallenge):
            consume_challenge(
                user=self.user,
                purpose=VerificationChallenge.Purpose.EMAIL_VERIFICATION,
                code=first_code,
            )
        consume_challenge(
            user=self.user,
            purpose=VerificationChallenge.Purpose.EMAIL_VERIFICATION,
            code=second_code,
        )

    def test_fifth_failed_attempt_consumes_challenge(self):
        code = issue_challenge(
            user=self.user,
            purpose=VerificationChallenge.Purpose.PASSWORD_RESET,
        )
        wrong_code = "000000" if code != "000000" else "111111"

        for _ in range(5):
            with self.assertRaises(InvalidChallenge):
                consume_challenge(
                    user=self.user,
                    purpose=VerificationChallenge.Purpose.PASSWORD_RESET,
                    code=wrong_code,
                )

        challenge = VerificationChallenge.objects.get()
        self.assertEqual(challenge.failed_attempts, 5)
        self.assertIsNotNone(challenge.consumed_at)
        with self.assertRaises(InvalidChallenge):
            consume_challenge(
                user=self.user,
                purpose=VerificationChallenge.Purpose.PASSWORD_RESET,
                code=code,
            )

    def test_issuance_has_sixty_second_cooldown(self):
        issue_challenge(
            user=self.user,
            purpose=VerificationChallenge.Purpose.EMAIL_VERIFICATION,
        )

        with self.assertRaises(ChallengeIssuanceBlocked):
            issue_challenge(
                user=self.user,
                purpose=VerificationChallenge.Purpose.EMAIL_VERIFICATION,
            )

        self.assertEqual(VerificationChallenge.objects.count(), 1)

    def test_issuance_is_limited_to_five_per_hour(self):
        now = timezone.now()
        for minutes_ago in (2, 4, 6, 8, 10):
            VerificationChallenge.objects.create(
                user=self.user,
                purpose=VerificationChallenge.Purpose.EMAIL_VERIFICATION,
                code_digest="a" * 64,
                expires_at=now + timedelta(minutes=10),
                consumed_at=now,
                created_at=now - timedelta(minutes=minutes_ago),
            )

        with self.assertRaises(ChallengeIssuanceBlocked):
            issue_challenge(
                user=self.user,
                purpose=VerificationChallenge.Purpose.EMAIL_VERIFICATION,
            )

        self.assertEqual(VerificationChallenge.objects.count(), 5)

    def test_limits_and_invalidation_are_scoped_by_purpose(self):
        email_code = issue_challenge(
            user=self.user,
            purpose=VerificationChallenge.Purpose.EMAIL_VERIFICATION,
        )
        reset_code = issue_challenge(
            user=self.user,
            purpose=VerificationChallenge.Purpose.PASSWORD_RESET,
        )

        consume_challenge(
            user=self.user,
            purpose=VerificationChallenge.Purpose.EMAIL_VERIFICATION,
            code=email_code,
        )
        consume_challenge(
            user=self.user,
            purpose=VerificationChallenge.Purpose.PASSWORD_RESET,
            code=reset_code,
        )
