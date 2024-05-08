import pytest
from account.models import Profile
from contact.models import Contact
from django.contrib.auth import get_user_model


@pytest.fixture
def sender(nickname="sender"):
    username = "sender"
    password = "testpass"
    user = get_user_model().objects.create(username=username, password=password)

    profile_data = {"user": user, "nickname": nickname}

    profile = Profile.objects.create(**profile_data)
    Contact.objects.create(profile=profile, phone_number="010-0000-1234")
    return profile


@pytest.fixture
def receiver(nickname="receiver"):
    username = "receiver"
    password = "testpass"
    user = get_user_model().objects.create(username=username, password=password)

    profile_data = {"user": user, "nickname": nickname}

    profile = Profile.objects.create(**profile_data)
    Contact.objects.create(profile=profile, phone_number="010-1000-1234")
    return profile
