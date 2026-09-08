import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone


class Command(BaseCommand):
    help = "Create a local foundation account using DOTICK_DEVELOPMENT_PASSWORD."

    def add_arguments(self, parser):
        parser.add_argument("--email", default="developer@example.test")

    def handle(self, *args, **options):
        if not settings.FOUNDATION_ENABLED or not settings.IS_LOCAL:
            raise CommandError("Developer provisioning requires the local/test workbench.")
        password = os.getenv("DOTICK_DEVELOPMENT_PASSWORD")
        if not password:
            raise CommandError("Set DOTICK_DEVELOPMENT_PASSWORD in your private environment.")
        email = options["email"].strip().lower()
        existing = get_user_model().objects.filter(email__iexact=email).first()
        if existing:
            if not existing.check_password(password):
                raise CommandError("Account exists with another password; no credentials changed.")
            user = existing
        else:
            user = get_user_model()(
                email=email,
                handle="local_developer",
                display_name="Local Developer",
            )
            user.full_clean(exclude=["password"])
            validate_password(password, user)
            user = get_user_model().objects.create_user(
                email,
                password,
                handle="local_developer",
                display_name="Local Developer",
            )
        changed_fields = []
        if user.email_verified_at is None:
            user.email_verified_at = timezone.now()
            changed_fields.append("email_verified_at")
        if not user.is_active:
            user.is_active = True
            changed_fields.append("is_active")
        if changed_fields:
            user.save(update_fields=changed_fields)
        self.stdout.write(self.style.SUCCESS(f"Developer account ready: {email}"))
