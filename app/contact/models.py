from contact.enums import MessageStatus, SNSService
from django.db import models


class Contact(models.Model):
    profile = models.ForeignKey(
        "account.Profile", related_name="contacts", on_delete=models.CASCADE
    )
    phone_number = models.CharField(max_length=20, blank=True)


class SNSInfo(models.Model):
    contact = models.ForeignKey(
        "contact.Contact", related_name="snsinfos", on_delete=models.CASCADE, null=True
    )
    service = models.CharField(max_length=20, choices=SNSService.choices(), blank=True)
    username = models.CharField(max_length=20, blank=True)


class Message(models.Model):
    sender = models.ForeignKey(
        "account.Profile", related_name="messages", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        "account.Profile",
        related_name="received_messages",
        on_delete=models.SET_NULL,
        null=True,
    )
    content = models.TextField(blank=True)
    status = models.CharField(choices=MessageStatus.choices(), max_length=20)

    @property
    def contacts(self):
        return self.sender.contacts.all()