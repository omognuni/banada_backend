from profile.models import Profile

from django import forms
from django.contrib import admin
from django.db import models


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("nickname", "gender", "age", "created_time", "email")
