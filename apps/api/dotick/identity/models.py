import re
import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.functions import Lower

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
