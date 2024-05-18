from contact.enums import MessageStatus, MessageTypeChoices, SNSService
from core.models import SoftDeletedModel, TimeStampModel
from django.db import models


class Contact(SoftDeletedModel, TimeStampModel):
    profile = models.ForeignKey(
        "account.Profile", related_name="contacts", on_delete=models.CASCADE
    )
    phone_number = models.CharField(max_length=20, blank=True)


class SNSInfo(SoftDeletedModel, TimeStampModel):
    contact = models.ForeignKey(
        "contact.Contact", related_name="snsinfos", on_delete=models.CASCADE, null=True
    )
    service = models.CharField(max_length=20, choices=SNSService.choices(), blank=True)
    username = models.CharField(max_length=20, blank=True)


class Message(SoftDeletedModel, TimeStampModel):
    sender = models.ForeignKey(
        "account.Profile", related_name="messages", on_delete=models.SET_NULL, null=True
    )
    receiver = models.ForeignKey(
        "account.Profile",
        related_name="received_messages",
        on_delete=models.SET_NULL,
        null=True,
    )
    message_type = models.ForeignKey(
        "contact.MessageType", on_delete=models.SET_NULL, null=True
    )
    content = models.TextField(blank=True)
    status = models.CharField(
        choices=MessageStatus.choices(), max_length=20, default=MessageStatus.WAIT
    )

    @property
    def contacts(self):
        return self.sender.contacts.all()


class MessageType(models.Model):
    name = models.CharField(
        choices=MessageTypeChoices.choices(), max_length=20, blank=True
    )
    cost = models.IntegerField(blank=True, default=0)
