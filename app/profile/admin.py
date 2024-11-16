from profile.models import AnswerChoice, Profile, ProfileImage, Simulation

from django.contrib import admin


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("nickname", "gender", "age", "created_time", "email")


class AnswerChoiceInline(admin.TabularInline):
    model = AnswerChoice
    extra = 1


class SimulationAdmin(admin.ModelAdmin):
    inlines = [AnswerChoiceInline]


admin.site.register(Profile, ProfileAdmin)
admin.site.register(ProfileImage)
admin.site.register(Simulation, SimulationAdmin)
admin.site.register(AnswerChoice)
