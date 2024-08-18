from datetime import datetime, timedelta

from contact.enums import MessageStatus, MessageTypeChoices, SNSService
from core.models import SoftDeletedModel, TimeStampModel
from django.core.validators import RegexValidator
from django.db import models


class Contact(SoftDeletedModel, TimeStampModel):
    profile = models.ForeignKey(
        "profile.Profile", related_name="contacts", on_delete=models.CASCADE
    )
    phone = models.CharField(
        max_length=15,
        null=True,
        validators=[
            RegexValidator(
                regex=r"^(\+82|0)?1[0-9]{1}-?[0-9]{3,4}-?[0-9]{4}$",
                message="유효한 전화번호 형식이 아닙니다: 010-1234-5678 혹은 +82-10-1234-5678",
            )
        ],
    )


class SNSInfo(SoftDeletedModel, TimeStampModel):
    contact = models.ForeignKey(
        "contact.Contact", related_name="snsinfos", on_delete=models.CASCADE, null=True
    )
    service = models.CharField(max_length=200, choices=SNSService.choices(), blank=True)
    username = models.CharField(max_length=200, blank=True)


class Message(SoftDeletedModel, TimeStampModel):
    sender = models.ForeignKey(
        "profile.Profile", related_name="messages", on_delete=models.SET_NULL, null=True
    )
    receiver = models.ForeignKey(
        "profile.Profile",
        related_name="received_messages",
        on_delete=models.SET_NULL,
        null=True,
    )
    message_type = models.ForeignKey(
        "contact.MessageType", on_delete=models.SET_NULL, null=True
    )
    content = models.TextField(blank=True)
    status = models.CharField(
        choices=MessageStatus.choices(), max_length=200, default=MessageStatus.WAIT
    )

    @property
    def contacts(self):
        return self.receiver.contacts.all()

    @property
    def is_match(self):
        if Message.objects.filter(
            receiver=self.sender,
            sender=self.receiver,
            message_type=self.message_type,
            status=MessageStatus.WAIT,
        ).exists():
            return True
        return False

    @property
    def expire(self):
        WEEK = 7
        if (self.created_time - datetime.now()).days >= WEEK:
            self.status = MessageStatus.EXPIRED
            self.save()


class MessageType(models.Model):
    name = models.CharField(
        choices=MessageTypeChoices.choices(), max_length=200, blank=True
    )
    cost = models.IntegerField(blank=True, default=0)
