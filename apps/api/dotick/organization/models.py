import uuid

from django.conf import settings
from django.db import models


class Folder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="folders",
        db_column="owner_user_id",
    )
    title = models.CharField(max_length=240)
    position = models.PositiveIntegerField(default=0)
    is_trashed = models.BooleanField(default=False)
    trashed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "folders"
        indexes = [models.Index(fields=["owner", "position"], name="folder_owner_position")]
        constraints = [
            models.CheckConstraint(condition=~models.Q(title=""), name="folder_title_nonempty"),
            models.CheckConstraint(
                condition=models.Q(is_trashed=False, trashed_at__isnull=True)
                | models.Q(is_trashed=True, trashed_at__isnull=False),
                name="folder_trash_state_consistent",
            ),
        ]


class List(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="lists",
        db_column="owner_user_id",
    )
    folder = models.ForeignKey(
        Folder,
        on_delete=models.PROTECT,
        related_name="lists",
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=240)
    position = models.PositiveIntegerField(default=0)
    is_inbox = models.BooleanField(default=False)
    is_trashed = models.BooleanField(default=False)
    trashed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "lists"
        indexes = [
            models.Index(
                fields=["owner", "folder", "position"],
                name="list_owner_folder_position",
            ),
            models.Index(fields=["folder", "position"], name="list_folder_position"),
        ]
        constraints = [
            models.CheckConstraint(condition=~models.Q(title=""), name="list_title_nonempty"),
            models.CheckConstraint(
                condition=models.Q(is_trashed=False, trashed_at__isnull=True)
                | models.Q(is_trashed=True, trashed_at__isnull=False),
                name="list_trash_state_consistent",
            ),
            models.UniqueConstraint(
                fields=["owner"],
                condition=models.Q(is_inbox=True),
                name="list_one_inbox_per_owner",
            ),
        ]


class Column(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name="columns")
    title = models.CharField(max_length=240)
    position = models.PositiveIntegerField(default=0)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "columns"
        indexes = [models.Index(fields=["list", "position"], name="column_list_position")]
        constraints = [
            models.CheckConstraint(condition=~models.Q(title=""), name="column_title_nonempty"),
            models.UniqueConstraint(
                fields=["list"],
                condition=models.Q(is_default=True),
                name="column_one_default_per_list",
            ),
        ]
