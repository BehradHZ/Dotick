import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="Folder",
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
                ("title", models.CharField(max_length=240)),
                ("position", models.PositiveIntegerField(default=0)),
                ("is_trashed", models.BooleanField(default=False)),
                ("trashed_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="folders",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "folders",
                "indexes": [
                    models.Index(fields=["owner", "position"], name="folder_owner_position")
                ],
                "constraints": [
                    models.CheckConstraint(
                        condition=models.Q(("title", ""), _negated=True),
                        name="folder_title_nonempty",
                    ),
                    models.CheckConstraint(
                        condition=models.Q(
                            models.Q(("is_trashed", False), ("trashed_at__isnull", True)),
                            models.Q(("is_trashed", True), ("trashed_at__isnull", False)),
                            _connector="OR",
                        ),
                        name="folder_trash_state_consistent",
                    ),
                ],
            },
        ),
        migrations.CreateModel(
            name="UserPreferences",
            fields=[
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name="preferences",
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("timezone", models.CharField(max_length=64)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"db_table": "user_preferences"},
        ),
        migrations.CreateModel(
            name="List",
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
                ("title", models.CharField(max_length=240)),
                ("position", models.PositiveIntegerField(default=0)),
                ("is_inbox", models.BooleanField(default=False)),
                ("is_trashed", models.BooleanField(default=False)),
                ("trashed_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "folder",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="lists",
                        to="organization.folder",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lists",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "lists",
                "indexes": [models.Index(fields=["owner", "position"], name="list_owner_position")],
                "constraints": [
                    models.CheckConstraint(
                        condition=models.Q(("title", ""), _negated=True),
                        name="list_title_nonempty",
                    ),
                    models.CheckConstraint(
                        condition=models.Q(
                            models.Q(("is_trashed", False), ("trashed_at__isnull", True)),
                            models.Q(("is_trashed", True), ("trashed_at__isnull", False)),
                            _connector="OR",
                        ),
                        name="list_trash_state_consistent",
                    ),
                    models.UniqueConstraint(
                        condition=models.Q(("is_inbox", True)),
                        fields=("owner",),
                        name="list_one_inbox_per_owner",
                    ),
                ],
            },
        ),
        migrations.CreateModel(
            name="Column",
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
                ("title", models.CharField(max_length=240)),
                ("position", models.PositiveIntegerField(default=0)),
                ("is_default", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "list",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="columns",
                        to="organization.list",
                    ),
                ),
            ],
            options={
                "db_table": "columns",
                "indexes": [models.Index(fields=["list", "position"], name="column_list_position")],
                "constraints": [
                    models.CheckConstraint(
                        condition=models.Q(("title", ""), _negated=True),
                        name="column_title_nonempty",
                    ),
                    models.UniqueConstraint(
                        condition=models.Q(("is_default", True)),
                        fields=("list",),
                        name="column_one_default_per_list",
                    ),
                ],
            },
        ),
    ]
