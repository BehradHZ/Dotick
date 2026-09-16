from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("organization", "0001_initial"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="list",
            index=models.Index(fields=["folder", "position"], name="list_folder_position"),
        ),
    ]
