# Generated by Django 4.1.3 on 2022-12-16 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_alter_user_options_user_date_joined_user_first_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="profile_image",
            field=models.FilePathField(
                default=None, null=True, path="/assets/img/profile"
            ),
        ),
    ]
