# Generated by Django 5.0.4 on 2024-10-03 07:08

import profile.enums

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profile", "0002_remove_profile_phone"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="profile",
            options={"verbose_name": "회원", "verbose_name_plural": "회원 목록"},
        ),
        migrations.AddField(
            model_name="profile",
            name="email",
            field=models.EmailField(max_length=255, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="recommdender",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="profile.profile",
                verbose_name="추천인",
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="status",
            field=models.CharField(
                choices=[
                    ("활성화", "ACTIVE"),
                    ("영구 정지", "BANNED"),
                    ("일시 정지", "TEMP_BANNED"),
                ],
                default=profile.enums.ProfileStatus["ACTIVE"],
                max_length=100,
                verbose_name="계정 상태",
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="age",
            field=models.IntegerField(blank=True, null=True, verbose_name="나이(만)"),
        ),
        migrations.AlterField(
            model_name="profile",
            name="drinking_frequency",
            field=models.CharField(
                blank=True, max_length=200, verbose_name="음주 빈도"
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="gender",
            field=models.CharField(
                blank=True,
                choices=[("남성", "male"), ("여성", "female")],
                max_length=200,
                verbose_name="성별",
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="height",
            field=models.IntegerField(blank=True, null=True, verbose_name="키"),
        ),
        migrations.AlterField(
            model_name="profile",
            name="is_smoke",
            field=models.BooleanField(
                blank=True, default=False, verbose_name="흡연 여부"
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="job",
            field=models.CharField(blank=True, max_length=200, verbose_name="직업"),
        ),
        migrations.AlterField(
            model_name="profile",
            name="nickname",
            field=models.CharField(
                max_length=200, null=True, unique=True, verbose_name="닉네임"
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="religion",
            field=models.CharField(blank=True, max_length=200, verbose_name="종교"),
        ),
        migrations.AlterField(
            model_name="profile",
            name="residence",
            field=models.CharField(blank=True, max_length=200, verbose_name="주소"),
        ),
    ]
