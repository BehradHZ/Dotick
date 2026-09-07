import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone

from dotick.organization.models import Column


class Item(models.Model):
    class Kind(models.TextChoices):
        TASK = "task", "Task"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    kind = models.CharField(max_length=16, choices=Kind.choices)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_items",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_items",
    )
    column = models.ForeignKey(Column, on_delete=models.PROTECT, related_name="items")
    title = models.CharField(max_length=240)
    creation_operation_id = models.UUIDField()
    creation_intent_digest = models.CharField(max_length=64)
    is_trashed = models.BooleanField(default=False)
    trashed_at = models.DateTimeField(null=True, blank=True)
    trash_origin_column_id = models.UUIDField(null=True, blank=True)
    version = models.PositiveBigIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "items"
        indexes = [
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
        ]
        constraints = [
            models.CheckConstraint(condition=~models.Q(title=""), name="item_title_nonempty"),
            models.CheckConstraint(
                condition=models.Q(version__gte=1), name="item_version_positive"
            ),
            models.CheckConstraint(condition=models.Q(kind="task"), name="item_kind_i1_task"),
            models.CheckConstraint(
                condition=models.Q(is_trashed=False, trashed_at__isnull=True)
                | models.Q(is_trashed=True, trashed_at__isnull=False),
                name="item_trash_state_consistent",
            ),
            models.UniqueConstraint(
                fields=["owner", "creation_operation_id"],
                name="item_owner_creation_operation",
            ),
        ]


class ItemSource(models.Model):
    class Platform(models.TextChoices):
        MANUAL = "manual", "Manual"

    item = models.OneToOneField(
        Item,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="source",
    )
    platform = models.CharField(max_length=32, choices=Platform.choices)
    external_account_id = models.CharField(max_length=255, null=True, blank=True)
    external_id = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "item_sources"


def trash_item(row):
    row.is_trashed = True
    row.trashed_at = timezone.now()
    row.trash_origin_column_id = row.column_id
    row.version += 1
    row.save(
        update_fields=[
            "is_trashed",
            "trashed_at",
            "trash_origin_column_id",
            "version",
            "updated_at",
        ]
    )
