from profile.models import AnswerChoice, Profile, ProfileImage, Simulation

from django.contrib import admin


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("nickname", "gender", "age", "created_time", "email")


admin.site.register(Profile, ProfileAdmin)
admin.site.register(ProfileImage)
admin.site.register(Simulation)
admin.site.register(AnswerChoice)
