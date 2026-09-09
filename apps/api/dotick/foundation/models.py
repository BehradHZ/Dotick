import uuid

from django.conf import settings
from django.db import models


class Checkpoint(models.Model):
    """Disposable Increment 0 verification resource outside the Item domain."""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    text = models.CharField(max_length=240)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "foundation_checkpoints"
        ordering = ["-created_at", "-id"]
        indexes = [
            models.Index(fields=["owner", "-created_at", "-id"]),
        ]
        constraints = [
            models.CheckConstraint(
                condition=~models.Q(text=""),
                name="checkpoint_text_nonempty",
            ),
        ]
