# Generated by Django 5.0.4 on 2024-07-04 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0009_alter_profile_drinking_frequency_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="phone",
            field=models.CharField(max_length=200, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="nickname",
            field=models.CharField(max_length=200, null=True, unique=True),
        ),
    ]
