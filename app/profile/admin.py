from profile.models import Profile

from django.contrib import admin


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("nickname", "gender", "age", "created_time", "email")


admin.site.register(Profile, ProfileAdmin)
