from django.db import models

from dotick.items.models import Item


class Task(models.Model):
    item = models.OneToOneField(
        Item,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="task",
    )

    class Meta:
        db_table = "tasks"
