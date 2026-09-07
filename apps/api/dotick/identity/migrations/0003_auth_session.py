# Generated for Dotick Increment 1 revocable JWT sessions.

import uuid

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("identity", "0002_identity_email_verification")]

    operations = [
        migrations.CreateModel(
            name="AuthSession",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("refresh_jti", models.CharField(max_length=255, unique=True)),
                ("user_agent", models.CharField(blank=True, max_length=200)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("last_seen_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("revoked_at", models.DateTimeField(blank=True, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="auth_sessions",
                        to="identity.user",
                    ),
                ),
            ],
            options={
                "db_table": "identity_auth_sessions",
                "indexes": [
                    models.Index(
                        fields=["user", "-last_seen_at"],
                        name="identity_session_user",
                    )
                ],
            },
        )
    ]
