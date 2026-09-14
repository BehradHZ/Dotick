import re
import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.functions import Lower, Trim
from django.utils import timezone

from dotick.identity.validators import normalize_contact_value, validate_iana_timezone

HANDLE_PATTERN = r"^[A-Za-z0-9_]{3,30}$"
handle_validator = RegexValidator(
    regex=HANDLE_PATTERN,
    message="Handle must contain 3 to 30 letters, numbers, or underscores.",
)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def get_by_natural_key(self, email):
        return self.get(email__iexact=email)

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("An email address is required.")

        email = self.normalize_email(email).strip().lower()
        local_part = email.split("@", 1)[0]

        if not extra_fields.get("handle"):
            stem = re.sub(r"[^A-Za-z0-9_]", "_", local_part).strip("_") or "user"
            extra_fields["handle"] = f"{stem[:20]}_{uuid.uuid4().hex[:8]}"

        extra_fields.setdefault("display_name", local_part[:120] or "Dotick User")

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    username = None
    email = models.EmailField(unique=True)
    handle = models.CharField(
        max_length=30,
        unique=True,
        validators=[handle_validator],
    )
    display_name = models.CharField(max_length=120)
    profile_picture_url = models.URLField(
        max_length=2048,
        null=True,
        blank=True,
    )
    email_verified_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def save(self, *args, **kwargs):
        self.email = self.__class__.objects.normalize_email(self.email).strip().lower()
        self.handle = self.handle.strip()
        self.display_name = self.display_name.strip()
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("email"),
                name="identity_user_email_ci_unique",
            ),
            models.CheckConstraint(
                condition=models.Q(email=Trim(Lower("email"))),
                name="identity_user_email_normalized",
            ),
            models.UniqueConstraint(
                Lower("handle"),
                name="identity_user_handle_ci_unique",
            ),
            models.CheckConstraint(
                condition=models.Q(handle__regex=HANDLE_PATTERN),
                name="identity_user_handle_format",
            ),
            models.CheckConstraint(
                condition=~models.Q(display_name=""),
                name="identity_user_display_name_nonempty",
            ),
        ]


class UserPreferences(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="preferences",
    )
    timezone = models.CharField(
        max_length=64,
        validators=[validate_iana_timezone],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        db_table = "user_preferences"


class VerificationChallenge(models.Model):
    class Purpose(models.TextChoices):
        EMAIL_VERIFICATION = "email_verification", "Email verification"
        PASSWORD_RESET = "password_reset", "Password reset"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="verification_challenges",
    )
    purpose = models.CharField(max_length=32, choices=Purpose.choices)
    code_digest = models.CharField(max_length=64)
    expires_at = models.DateTimeField()
    consumed_at = models.DateTimeField(null=True, blank=True)
    failed_attempts = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        db_table = "identity_verification_challenges"
        indexes = [
            models.Index(
                fields=["user", "purpose", "-created_at"],
                name="identity_challenge_lookup",
            )
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(failed_attempts__lte=5),
                name="identity_challenge_attempts_lte_5",
            )
        ]


class AuthSession(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="auth_sessions",
    )
    refresh_jti = models.CharField(max_length=255, unique=True)
    user_agent = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    last_seen_at = models.DateTimeField(default=timezone.now)
    revoked_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "identity_auth_sessions"
        indexes = [
            models.Index(
                fields=["user", "revoked_at", "-last_seen_at"],
                name="identity_session_active",
            )
        ]


class ExternalIdentity(models.Model):
    class Provider(models.TextChoices):
        GOOGLE = "google", "Google"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="external_identities",
    )
    provider = models.CharField(max_length=32, choices=Provider.choices)
    subject = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        db_table = "identity_external_identities"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(provider="google"),
                name="identity_external_provider_google",
            ),
            models.UniqueConstraint(
                fields=["provider", "subject"],
                name="identity_external_subject_unique",
            ),
            models.UniqueConstraint(
                fields=["user", "provider"],
                name="identity_external_user_provider_unique",
            ),
        ]


class PasskeyCredential(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="passkey_credentials",
    )
    credential_id = models.BinaryField(unique=True)
    public_key = models.BinaryField()
    sign_count = models.PositiveBigIntegerField(default=0)
    device_type = models.CharField(max_length=32)
    backed_up = models.BooleanField(default=False)
    transports = models.JSONField(default=list, blank=True)
    name = models.CharField(max_length=120)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    last_used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "identity_passkey_credentials"
        indexes = [
            models.Index(
                fields=["user", "-created_at"],
                name="identity_passkey_user",
            )
        ]


class PasskeyChallenge(models.Model):
    class Purpose(models.TextChoices):
        REGISTRATION = "registration", "Registration"
        AUTHENTICATION = "authentication", "Authentication"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="passkey_challenges",
        null=True,
        blank=True,
    )
    purpose = models.CharField(max_length=32, choices=Purpose.choices)
    challenge = models.BinaryField(unique=True)
    name = models.CharField(max_length=120, blank=True)
    expires_at = models.DateTimeField()
    consumed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        db_table = "identity_passkey_challenges"
        indexes = [
            models.Index(
                fields=["purpose", "expires_at"],
                name="identity_passkey_challenge",
            )
        ]


class AccountContact(models.Model):
    class Kind(models.TextChoices):
        EMAIL = "email", "Email"
        PHONE = "phone", "Phone"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="account_contacts",
    )
    kind = models.CharField(max_length=16, choices=Kind.choices)
    value = models.CharField(max_length=254)
    verified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.value = normalize_contact_value(self.kind, self.value)
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        db_table = "identity_account_contacts"
        indexes = [
            models.Index(
                fields=["user", "kind", "verified_at"],
                name="identity_contact_user",
            )
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(kind__in=["email", "phone"]),
                name="identity_contact_kind_valid",
            ),
            models.UniqueConstraint(
                fields=["kind", "value"],
                condition=models.Q(verified_at__isnull=False),
                name="identity_verified_contact_unique",
            ),
        ]


class ContactVerificationChallenge(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    contact = models.ForeignKey(
        AccountContact,
        on_delete=models.CASCADE,
        related_name="verification_challenges",
    )
    code_digest = models.CharField(max_length=64)
    expires_at = models.DateTimeField()
    consumed_at = models.DateTimeField(null=True, blank=True)
    failed_attempts = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        db_table = "identity_contact_verification_challenges"
        indexes = [
            models.Index(
                fields=["contact", "-created_at"],
                name="identity_contact_challenge",
            )
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(failed_attempts__lte=5),
                name="identity_contact_attempts_lte_5",
            )
        ]
