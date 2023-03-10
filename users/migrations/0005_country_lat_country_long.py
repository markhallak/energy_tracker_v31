# Generated by Django 4.1.3 on 2023-01-13 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_alter_user_profile_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="country",
            name="lat",
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="country",
            name="long",
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
