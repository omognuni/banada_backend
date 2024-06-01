# Generated by Django 5.0.4 on 2024-05-26 00:38

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0005_alter_simulation_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="age",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="created_time",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="profile",
            name="gender",
            field=models.CharField(
                blank=True,
                choices=[("남성", "male"), ("여성", "female")],
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="is_deleted",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="profile",
            name="updated_time",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="profileimage",
            name="created_time",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="profileimage",
            name="is_deleted",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="profileimage",
            name="is_main",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="profileimage",
            name="updated_time",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="simulation",
            name="created_time",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="simulation",
            name="is_deleted",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="simulation",
            name="updated_time",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.CreateModel(
            name="AnswerChoice",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("index", models.IntegerField(blank=True, null=True, unique=True)),
                ("content", models.CharField(blank=True, max_length=200)),
                (
                    "simulation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="answer_choices",
                        to="account.simulation",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProfileAnswer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_deleted", models.BooleanField(default=False)),
                ("created_time", models.DateTimeField(auto_now_add=True)),
                ("updated_time", models.DateTimeField(auto_now=True)),
                (
                    "answer_choice",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="account.answerchoice",
                    ),
                ),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="answers",
                        to="account.profile",
                    ),
                ),
                (
                    "simulation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="account.simulation",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.DeleteModel(
            name="Answer",
        ),
    ]