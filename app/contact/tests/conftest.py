from profile.models import Profile

import pytest
from contact.models import Contact
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


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


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    User = get_user_model()
    return User.objects.create_user(username="testuser", password="testpass")


@pytest.fixture
def profile(user):
    return Profile.objects.create(user=user, nickname="testprofile")


@pytest.fixture
def another_profile():
    User = get_user_model()
    another_user = User.objects.create_user(
        username="anotheruser", password="anotherpass"
    )
    return Profile.objects.create(user=another_user, nickname="anotherprofile")
