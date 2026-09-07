import re
import uuid

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.functions import Lower
from django.utils import timezone


class UserManager(BaseUserManager):
    use_in_migrations = True

    def get_by_natural_key(self, username):
        return self.get(email__iexact=username)

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("An email address is required.")
        local_part = email.strip().split("@", 1)[0]
        if not extra_fields.get("handle"):
            stem = re.sub(r"[^A-Za-z0-9_]", "_", local_part).strip("_") or "user"
            stem = stem[:20]
            extra_fields["handle"] = f"{stem}_{uuid.uuid4().hex[:8]}"
        extra_fields.setdefault("display_name", local_part[:120] or "Dotick User")
        user = self.model(email=email.strip().lower(), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if not extra_fields["is_staff"] or not extra_fields["is_superuser"]:
            raise ValueError("Superusers must have is_staff and is_superuser enabled.")
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(unique=True)
    handle = models.CharField(max_length=30, unique=True)
    display_name = models.CharField(max_length=120)
    profile_picture_url = models.URLField(max_length=2048, null=True, blank=True)
    email_verified_at = models.DateTimeField(null=True, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta:
        db_table = "users"
        constraints = [
            models.UniqueConstraint(Lower("email"), name="users_email_ci_unique"),
            models.UniqueConstraint(Lower("handle"), name="users_handle_ci_unique"),
        ]


class VerificationChallenge(models.Model):
    class Purpose(models.TextChoices):
        EMAIL_VERIFICATION = "email_verification", "Email verification"
        PASSWORD_RESET = "password_reset", "Password reset"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="verification_challenges")
    purpose = models.CharField(max_length=32, choices=Purpose.choices)
    code_digest = models.CharField(max_length=64)
    expires_at = models.DateTimeField()
    consumed_at = models.DateTimeField(null=True, blank=True)
    failed_attempts = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "identity_verification_challenges"
        indexes = [
            models.Index(
                fields=["user", "purpose", "-created_at"],
                name="identity_challenge_lookup",
            )
        ]


class AuthSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auth_sessions")
    refresh_jti = models.CharField(max_length=255, unique=True)
    user_agent = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_seen_at = models.DateTimeField(default=timezone.now)
    revoked_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "identity_auth_sessions"
        indexes = [models.Index(fields=["user", "-last_seen_at"], name="identity_session_user")]


class ExternalIdentity(models.Model):
    class Provider(models.TextChoices):
        GOOGLE = "google", "Google"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="external_identities")
    provider = models.CharField(max_length=32, choices=Provider.choices)
    subject = models.CharField(max_length=255)
    provider_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "identity_external_identities"
        constraints = [
            models.UniqueConstraint(
                fields=["provider", "subject"], name="identity_external_provider_subject_unique"
            ),
            models.UniqueConstraint(
                fields=["user", "provider"], name="identity_external_user_provider_unique"
            ),
        ]


class PasskeyCredential(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="passkeys")
    credential_id = models.CharField(max_length=1024, unique=True)
    public_key = models.BinaryField()
    sign_count = models.PositiveBigIntegerField(default=0)
    device_type = models.CharField(max_length=32, blank=True)
    backed_up = models.BooleanField(default=False)
    transports = models.JSONField(default=list)
    name = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "identity_passkey_credentials"
        indexes = [models.Index(fields=["user", "-created_at"], name="identity_passkey_user")]


class PasskeyChallenge(models.Model):
    class Purpose(models.TextChoices):
        REGISTRATION = "registration", "Registration"
        AUTHENTICATION = "authentication", "Authentication"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="passkey_challenges",
        null=True,
        blank=True,
    )
    purpose = models.CharField(max_length=24, choices=Purpose.choices)
    challenge = models.BinaryField()
    credential_name = models.CharField(max_length=120, blank=True)
    expires_at = models.DateTimeField()
    consumed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "identity_passkey_challenges"
        indexes = [
            models.Index(fields=["purpose", "expires_at"], name="identity_passkey_challenge")
        ]


class AccountContact(models.Model):
    class Kind(models.TextChoices):
        EMAIL = "email", "Email"
        PHONE = "phone", "Phone"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contacts")
    kind = models.CharField(max_length=16, choices=Kind.choices)
    value = models.CharField(max_length=254)
    normalized_value = models.CharField(max_length=254)
    verified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "identity_account_contacts"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "kind", "normalized_value"],
                name="identity_contact_user_value_unique",
            ),
            models.UniqueConstraint(
                fields=["kind", "normalized_value"],
                condition=models.Q(verified_at__isnull=False),
                name="identity_contact_verified_value_unique",
            ),
        ]


class ContactVerificationChallenge(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contact = models.ForeignKey(
        AccountContact,
        on_delete=models.CASCADE,
        related_name="verification_challenges",
    )
    code_digest = models.CharField(max_length=64)
    expires_at = models.DateTimeField()
    consumed_at = models.DateTimeField(null=True, blank=True)
    failed_attempts = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "identity_contact_verification_challenges"
        indexes = [
            models.Index(fields=["contact", "-created_at"], name="identity_contact_challenge")
        ]
