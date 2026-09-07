import uuid

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("identity", "0003_auth_session")]

    operations = [
        migrations.CreateModel(
            name="ExternalIdentity",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False
                    ),
                ),
                ("provider", models.CharField(choices=[("google", "Google")], max_length=32)),
                ("subject", models.CharField(max_length=255)),
                ("provider_email", models.EmailField(max_length=254)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("last_used_at", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="external_identities",
                        to="identity.user",
                    ),
                ),
            ],
            options={"db_table": "identity_external_identities"},
        ),
        migrations.AddConstraint(
            model_name="externalidentity",
            constraint=models.UniqueConstraint(
                fields=("provider", "subject"), name="identity_external_provider_subject_unique"
            ),
        ),
        migrations.AddConstraint(
            model_name="externalidentity",
            constraint=models.UniqueConstraint(
                fields=("user", "provider"), name="identity_external_user_provider_unique"
            ),
        ),
    ]
