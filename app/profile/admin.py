from profile.models import Profile

from django.contrib import admin


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("nickname", "gender", "age", "created_time", "email")
