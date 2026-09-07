import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("identity", "0004_external_identity")]

    operations = [
        migrations.CreateModel(
            name="PasskeyCredential",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False
                    ),
                ),
                ("credential_id", models.CharField(max_length=1024, unique=True)),
                ("public_key", models.BinaryField()),
                ("sign_count", models.PositiveBigIntegerField(default=0)),
                ("device_type", models.CharField(blank=True, max_length=32)),
                ("backed_up", models.BooleanField(default=False)),
                ("transports", models.JSONField(default=list)),
                ("name", models.CharField(max_length=120)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("last_used_at", models.DateTimeField(blank=True, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="passkeys",
                        to="identity.user",
                    ),
                ),
            ],
            options={
                "db_table": "identity_passkey_credentials",
                "indexes": [
                    models.Index(fields=["user", "-created_at"], name="identity_passkey_user")
                ],
            },
        ),
        migrations.CreateModel(
            name="PasskeyChallenge",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False
                    ),
                ),
                (
                    "purpose",
                    models.CharField(
                        choices=[
                            ("registration", "Registration"),
                            ("authentication", "Authentication"),
                        ],
                        max_length=24,
                    ),
                ),
                ("challenge", models.BinaryField()),
                ("credential_name", models.CharField(blank=True, max_length=120)),
                ("expires_at", models.DateTimeField()),
                ("consumed_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="passkey_challenges",
                        to="identity.user",
                    ),
                ),
            ],
            options={
                "db_table": "identity_passkey_challenges",
                "indexes": [
                    models.Index(
                        fields=["purpose", "expires_at"], name="identity_passkey_challenge"
                    )
                ],
            },
        ),
    ]
