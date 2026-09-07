import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("identity", "0006_account_profile_picture")]

    operations = [
        migrations.CreateModel(
            name="AccountContact",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False
                    ),
                ),
                (
                    "kind",
                    models.CharField(
                        choices=[("email", "Email"), ("phone", "Phone")], max_length=16
                    ),
                ),
                ("value", models.CharField(max_length=254)),
                ("normalized_value", models.CharField(max_length=254)),
                ("verified_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="contacts",
                        to="identity.user",
                    ),
                ),
            ],
            options={"db_table": "identity_account_contacts"},
        ),
        migrations.CreateModel(
            name="ContactVerificationChallenge",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False
                    ),
                ),
                ("code_digest", models.CharField(max_length=64)),
                ("expires_at", models.DateTimeField()),
                ("consumed_at", models.DateTimeField(blank=True, null=True)),
                ("failed_attempts", models.PositiveSmallIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "contact",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="verification_challenges",
                        to="identity.accountcontact",
                    ),
                ),
            ],
            options={
                "db_table": "identity_contact_verification_challenges",
                "indexes": [
                    models.Index(
                        fields=["contact", "-created_at"], name="identity_contact_challenge"
                    )
                ],
            },
        ),
        migrations.AddConstraint(
            model_name="accountcontact",
            constraint=models.UniqueConstraint(
                fields=("user", "kind", "normalized_value"),
                name="identity_contact_user_value_unique",
            ),
        ),
        migrations.AddConstraint(
            model_name="accountcontact",
            constraint=models.UniqueConstraint(
                condition=models.Q(("verified_at__isnull", False)),
                fields=("kind", "normalized_value"),
                name="identity_contact_verified_value_unique",
            ),
        ),
    ]
