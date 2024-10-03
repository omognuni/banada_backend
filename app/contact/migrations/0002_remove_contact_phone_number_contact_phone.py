# Generated by Django 5.0.4 on 2024-09-22 10:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contact", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="contact",
            name="phone_number",
        ),
        migrations.AddField(
            model_name="contact",
            name="phone",
            field=models.CharField(
                max_length=15,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message="유효한 전화번호 형식이 아닙니다: 010-1234-5678 혹은 +82-10-1234-5678",
                        regex="^(\\+82|0)?1[0-9]{1}-?[0-9]{3,4}-?[0-9]{4}$",
                    )
                ],
            ),
        ),
    ]