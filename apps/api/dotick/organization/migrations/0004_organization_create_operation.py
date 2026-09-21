import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("organization", "0003_folder_list_column_version"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="OrganizationCreateOperation",
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
                    "resource_type",
                    models.CharField(
                        choices=[
                            ("folder", "Folder"),
                            ("list", "List"),
                            ("column", "Column"),
                        ],
                        editable=False,
                        max_length=16,
                    ),
                ),
                ("operation_id", models.UUIDField(editable=False)),
                ("intent_digest", models.CharField(editable=False, max_length=64)),
                ("resource_id", models.UUIDField(editable=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "owner",
                    models.ForeignKey(
                        db_column="owner_user_id",
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="organization_create_operations",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "organization_create_operations",
                "indexes": [
                    models.Index(
                        fields=["owner", "resource_type", "resource_id"],
                        name="orgop_result_lookup",
                    )
                ],
                "constraints": [
                    models.UniqueConstraint(
                        fields=("owner", "resource_type", "operation_id"),
                        name="orgop_owner_type_operation_uq",
                    ),
                    models.CheckConstraint(
                        condition=models.Q(
                            ("resource_type__in", ["folder", "list", "column"])
                        ),
                        name="orgop_resource_type_valid",
                    ),
                    models.CheckConstraint(
                        condition=models.Q(("intent_digest", ""), _negated=True),
                        name="orgop_intent_digest_nonempty",
                    ),
                ],
            },
        ),
    ]
