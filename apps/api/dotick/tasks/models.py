from django.db import models

from dotick.items.models import Item


class Task(models.Model):
    class Status(models.TextChoices):
        TODO = "todo", "Todo"
        OVERDUE = "overdue", "Overdue"
        MISSED = "missed", "Missed"
        DONE = "done", "Done"
        WONT_DO = "wont_do", "Won't do"
        SKIPPED = "skipped", "Skipped"

    class Priority(models.TextChoices):
        URGENT_IMPORTANT = "urgent_important", "Urgent and important"
        IMPORTANT = "important", "Important"
        URGENT = "urgent", "Urgent"
        NONE = "none", "None"

    item = models.OneToOneField(
        Item,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="task",
    )
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.TODO)
    priority = models.CharField(
        max_length=24,
        choices=Priority.choices,
        default=Priority.NONE,
    )
    due_at = models.DateTimeField(null=True, blank=True)
    end_at = models.DateTimeField(null=True, blank=True)
    is_all_day = models.BooleanField(default=False)
    deadline_at = models.DateTimeField(null=True, blank=True)
    grace_period_days = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "tasks"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(
                    status__in=[
                        "todo",
                        "overdue",
                        "missed",
                        "done",
                        "wont_do",
                        "skipped",
                    ]
                ),
                name="task_status_valid",
            ),
            models.CheckConstraint(
                condition=models.Q(
                    priority__in=["urgent_important", "important", "urgent", "none"]
                ),
                name="task_priority_valid",
            ),
            models.CheckConstraint(
                condition=models.Q(end_at__isnull=True)
                | models.Q(due_at__isnull=False, end_at__gte=models.F("due_at")),
                name="task_end_after_due",
            ),
            models.CheckConstraint(
                condition=models.Q(deadline_at__isnull=True)
                | models.Q(due_at__isnull=True)
                | models.Q(deadline_at__gte=models.F("due_at")),
                name="task_deadline_after_due",
            ),
            models.CheckConstraint(
                condition=models.Q(deadline_at__isnull=True)
                | models.Q(end_at__isnull=True)
                | models.Q(deadline_at__gte=models.F("end_at")),
                name="task_deadline_after_end",
            ),
            models.CheckConstraint(
                condition=models.Q(is_all_day=False) | models.Q(due_at__isnull=False),
                name="task_all_day_has_due",
            ),
            models.CheckConstraint(
                condition=models.Q(deadline_at__isnull=False) | models.Q(grace_period_days=0),
                name="task_grace_requires_deadline",
            ),
        ]
