from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("organization", "0002_list_folder_position"),
    ]

    operations = [
        migrations.AddField(
            model_name="folder",
            name="version",
            field=models.PositiveBigIntegerField(default=1),
        ),
        migrations.AddField(
            model_name="list",
            name="version",
            field=models.PositiveBigIntegerField(default=1),
        ),
        migrations.AddField(
            model_name="column",
            name="version",
            field=models.PositiveBigIntegerField(default=1),
        ),
        migrations.AddConstraint(
            model_name="folder",
            constraint=models.CheckConstraint(
                condition=models.Q(version__gte=1),
                name="folder_version_positive",
            ),
        ),
        migrations.AddConstraint(
            model_name="list",
            constraint=models.CheckConstraint(
                condition=models.Q(version__gte=1),
                name="list_version_positive",
            ),
        ),
        migrations.AddConstraint(
            model_name="column",
            constraint=models.CheckConstraint(
                condition=models.Q(version__gte=1),
                name="column_version_positive",
            ),
        ),
    ]
