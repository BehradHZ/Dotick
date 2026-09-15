from django.db import models

from dotick.items.models import Item


class Task(models.Model):
    class Status(models.TextChoices):
        TODO = "todo", "Todo"
        DONE = "done", "Done"
        WONT_DO = "wont_do", "Won't do"

    item = models.OneToOneField(
        Item,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="task",
    )
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.TODO)

    class Meta:
        db_table = "tasks"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(status__in=["todo", "done", "wont_do"]),
                name="task_status_valid",
            )
        ]
