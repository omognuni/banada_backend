from profile.enums import CategoryChoices, GenderChoices
from profile.models import (
    AnswerChoice,
    Profile,
    ProfileAnswer,
    ProfileImage,
    Simulation,
)

import django
from contact.enums import MessageStatus, MessageTypeChoices, SNSService
from contact.models import Contact, Message, MessageType, SNSInfo
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand
from faker import Faker

fake = Faker()


class Command(BaseCommand):
    def create_message(self, sender, receiver):
        message = Message.objects.create(
            sender=sender,
            receiver=receiver,
            message_type=MessageType.objects.order_by("?").first(),
            content=fake.text(),
            status=fake.random_element(
                elements=[MessageStatus.EXPIRED, MessageStatus.REFUSED]
            ),
        )
        return message

    def handle(self, *args, **options):
        users = get_user_model().objects.all()

        for user in users:
            profile = Profile.objects.filter(user=user).first()

            for _ in range(100):
                receiver = Profile.objects.order_by("?").first()
                self.create_message(sender=profile, receiver=receiver)
                self.create_message(sender=receiver, receiver=profile)
