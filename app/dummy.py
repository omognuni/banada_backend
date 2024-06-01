import os

import django
from account.enums import CategoryChoices, GenderChoices
from account.models import (
    AnswerChoice,
    Profile,
    ProfileAnswer,
    ProfileImage,
    Simulation,
)
from contact.enums import MessageStatus, MessageTypeChoices, SNSService
from contact.models import Contact, Message, MessageType, SNSInfo
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
try:
    django.setup()
except ImproperlyConfigured:
    raise ImproperlyConfigured(
        "Django settings are not configured properly. Please check the DJANGO_SETTINGS_MODULE environment variable."
    )

fake = Faker()


# 유저 생성
def create_user():
    User = get_user_model()
    user = User.objects.create_user(
        username=fake.user_name(), email=fake.email(), password="testpass"
    )
    return user


# 프로필 생성
def create_profile(user):
    profile = Profile.objects.create(
        user=user,
        nickname=fake.first_name(),
        gender=fake.random_element(elements=GenderChoices.values),
        age=fake.random_int(min=18, max=99),
        height=fake.random_int(min=150, max=200),
        job=fake.job(),
        residence=fake.address(),
        religion=fake.random_element(elements=["Christianity", "Islam", "None"]),
        is_smoke=fake.boolean(),
        drinking_frequency=fake.random_element(
            elements=["None", "Occasionally", "Frequently"]
        ),
    )
    return profile


# 프로필 이미지 생성
def create_profile_image(profile):
    profile_image = ProfileImage.objects.create(
        profile=profile, image=fake.image_url(), is_main=fake.boolean()
    )
    return profile_image


# 시뮬레이션 및 답변 생성
def create_simulation_and_answers():
    simulation = Simulation.objects.create(
        category=fake.random_element(elements=CategoryChoices.values),
        question=fake.sentence(),
    )
    for i in range(4):
        AnswerChoice.objects.create(
            simulation=simulation, index=i, content=fake.sentence()
        )
    return simulation


# 프로필 답변 생성
def create_profile_answer(profile, simulation, answer_choice):
    profile_answer = ProfileAnswer.objects.create(
        profile=profile, simulation=simulation, answer_choice=answer_choice
    )
    return profile_answer


# 연락처 및 SNS 정보 생성
def create_contact_and_sns(profile):
    contact = Contact.objects.create(profile=profile, phone_number=fake.phone_number())
    sns_info = SNSInfo.objects.create(
        contact=contact,
        service=fake.random_element(elements=SNSService.values),
        username=fake.user_name(),
    )
    return contact, sns_info


# 메시지 타입 생성
def create_message_type():
    message_type = MessageType.objects.create(
        name=fake.random_element(elements=MessageTypeChoices.values),
        cost=fake.random_int(min=1, max=10),
    )
    return message_type


# 메시지 생성
def create_message(sender, receiver, message_type):
    message = Message.objects.create(
        sender=sender,
        receiver=receiver,
        message_type=message_type,
        content=fake.text(),
        status=fake.random_element(elements=MessageStatus.values),
    )
    return message


def create_dummy_data():
    for _ in range(10):
        user = create_user()
        profile = create_profile(user)
        create_profile_image(profile)

        simulation = create_simulation_and_answers()
        answer_choice = AnswerChoice.objects.filter(simulation=simulation).first()
        create_profile_answer(profile, simulation, answer_choice)

        contact, sns_info = create_contact_and_sns(profile)
        message_type = create_message_type()

        receiver_profile = Profile.objects.order_by("?").first()
        create_message(profile, receiver_profile, message_type)


if __name__ == "__main__":
    create_dummy_data()
