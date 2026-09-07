import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [("items", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "item",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name="task",
                        serialize=False,
                        to="items.item",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("todo", "Todo"), ("done", "Done"), ("wont_do", "Won't do")],
                        default="todo",
                        max_length=16,
                    ),
                ),
            ],
            options={
                "db_table": "tasks",
                "constraints": [
                    models.CheckConstraint(
                        condition=models.Q(("status__in", ["todo", "done", "wont_do"])),
                        name="task_status_valid",
                    )
                ],
            },
        )
    ]
