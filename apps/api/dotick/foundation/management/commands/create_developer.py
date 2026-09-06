import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.management.base import BaseCommand, CommandError


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
        else:
            user = get_user_model()(email=email)
            user.full_clean(exclude=["password"])
            validate_password(password, user)
            get_user_model().objects.create_user(email, password)
        self.stdout.write(self.style.SUCCESS(f"Developer account ready: {email}"))
