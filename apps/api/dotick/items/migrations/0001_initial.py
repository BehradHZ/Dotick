import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("organization", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Item",
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
                ("kind", models.CharField(choices=[("task", "Task")], max_length=16)),
                ("title", models.CharField(max_length=240)),
                ("creation_operation_id", models.UUIDField()),
                ("creation_intent_digest", models.CharField(max_length=64)),
                ("is_trashed", models.BooleanField(default=False)),
                ("trashed_at", models.DateTimeField(blank=True, null=True)),
                ("trash_origin_column_id", models.UUIDField(blank=True, null=True)),
                ("version", models.PositiveBigIntegerField(default=1)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "column",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="items",
                        to="organization.column",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="created_items",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="owned_items",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "items",
                "indexes": [
                    models.Index(
                        fields=["owner", "is_trashed", "-updated_at"],
                        name="item_owner_active_updated",
                    ),
                    models.Index(
                        fields=["column", "is_trashed", "-updated_at"],
                        name="item_column_active_updated",
                    ),
                    models.Index(
                        fields=["owner", "kind", "is_trashed"],
                        name="item_owner_kind_active",
                    ),
                ],
                "constraints": [
                    models.CheckConstraint(
                        condition=models.Q(("title", ""), _negated=True),
                        name="item_title_nonempty",
                    ),
                    models.CheckConstraint(
                        condition=models.Q(("version__gte", 1)),
                        name="item_version_positive",
                    ),
                    models.CheckConstraint(
                        condition=models.Q(("kind", "task")),
                        name="item_kind_i1_task",
                    ),
                    models.CheckConstraint(
                        condition=models.Q(
                            models.Q(("is_trashed", False), ("trashed_at__isnull", True)),
                            models.Q(("is_trashed", True), ("trashed_at__isnull", False)),
                            _connector="OR",
                        ),
                        name="item_trash_state_consistent",
                    ),
                    models.UniqueConstraint(
                        fields=("owner", "creation_operation_id"),
                        name="item_owner_creation_operation",
                    ),
                ],
            },
        ),
        migrations.CreateModel(
            name="ItemSource",
            fields=[
                (
                    "item",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name="source",
                        serialize=False,
                        to="items.item",
                    ),
                ),
                (
                    "platform",
                    models.CharField(choices=[("manual", "Manual")], max_length=32),
                ),
                ("external_account_id", models.CharField(blank=True, max_length=255, null=True)),
                ("external_id", models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={"db_table": "item_sources"},
        ),
    ]
