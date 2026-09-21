from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="status",
            field=models.CharField(
                choices=[("todo", "Todo"), ("done", "Done"), ("wont_do", "Won't do")],
                default="todo",
                max_length=16,
            ),
        ),
        migrations.AddConstraint(
            model_name="task",
            constraint=models.CheckConstraint(
                condition=models.Q(("status__in", ["todo", "done", "wont_do"])),
                name="task_status_valid",
            ),
        ),
    ]
