import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create the local developer account for the Increment 0 walking skeleton."

    def add_arguments(self, parser):
        parser.add_argument(
            "--email",
            default="developer@example.test",
        )

    def handle(self, *args, **options):
        environment = os.getenv("DOTICK_ENV", "local")

        if not settings.FOUNDATION_ENABLED or environment not in {"local", "test"}:
            raise CommandError(
                "Developer provisioning is available only for the local/test foundation workbench."
            )

        password = os.getenv("DOTICK_DEVELOPMENT_PASSWORD")
        if not password:
            raise CommandError("Set DOTICK_DEVELOPMENT_PASSWORD in your private environment.")

        email = options["email"].strip().lower()
        User = get_user_model()

        existing = User.objects.filter(email__iexact=email).first()

        if existing:
            if not existing.check_password(password):
                raise CommandError(
                    "Developer account already exists with a different password; no changes made."
                )

            self.stdout.write(self.style.SUCCESS(f"Developer account ready: {email}"))
            return

        candidate = User(email=email)
        validate_password(password, candidate)

        User.objects.create_user(
            email=email,
            password=password,
        )

        self.stdout.write(self.style.SUCCESS(f"Developer account created: {email}"))
