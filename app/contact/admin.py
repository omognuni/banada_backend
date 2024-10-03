from contact.models import Message
from django.contrib import admin


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass
