# Generated for Dotick Increment 1 email identity.

import re
import uuid

import django.db.models.deletion
from django.db import migrations, models
from django.db.models.functions import Lower


def populate_identity_names(apps, schema_editor):
    user_model = apps.get_model("identity", "User")
    for user in user_model.objects.all().iterator():
        local_part = user.email.split("@", 1)[0]
        stem = re.sub(r"[^A-Za-z0-9_]", "_", local_part).strip("_") or "user"
        user.handle = f"{stem[:20]}_{str(user.id).replace('-', '')[:8]}"
        user.display_name = local_part[:120] or "Dotick User"
        user.save(update_fields=["handle", "display_name"])


class Migration(migrations.Migration):
    dependencies = [("identity", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="user",
            name="display_name",
            field=models.CharField(max_length=120, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="email_verified_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="handle",
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.CreateModel(
            name="VerificationChallenge",
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
                (
                    "purpose",
                    models.CharField(
                        choices=[
                            ("email_verification", "Email verification"),
                            ("password_reset", "Password reset"),
                        ],
                        max_length=32,
                    ),
                ),
                ("code_digest", models.CharField(max_length=64)),
                ("expires_at", models.DateTimeField()),
                ("consumed_at", models.DateTimeField(blank=True, null=True)),
                ("failed_attempts", models.PositiveSmallIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="verification_challenges",
                        to="identity.user",
                    ),
                ),
            ],
            options={
                "db_table": "identity_verification_challenges",
                "indexes": [
                    models.Index(
                        fields=["user", "purpose", "-created_at"],
                        name="identity_challenge_lookup",
                    )
                ],
            },
        ),
        migrations.RunPython(populate_identity_names, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="user",
            name="display_name",
            field=models.CharField(max_length=120),
        ),
        migrations.AlterField(
            model_name="user",
            name="handle",
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.AddConstraint(
            model_name="user",
            constraint=models.UniqueConstraint(Lower("handle"), name="users_handle_ci_unique"),
        ),
    ]
