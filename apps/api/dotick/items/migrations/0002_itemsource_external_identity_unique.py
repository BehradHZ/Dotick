from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("items", "0001_initial"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="itemsource",
            constraint=models.UniqueConstraint(
                condition=models.Q(
                    external_account_id__isnull=False,
                    external_id__isnull=False,
                ),
                fields=("platform", "external_account_id", "external_id"),
                name="item_source_complete_external_unique",
            ),
        ),
    ]
