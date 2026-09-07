from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("identity", "0005_passkeys")]

    operations = [
        migrations.AddField(
            model_name="user",
            name="profile_picture_url",
            field=models.URLField(blank=True, max_length=2048, null=True),
        )
    ]
