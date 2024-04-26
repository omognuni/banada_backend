import pytest
from account.models import Profile
from django.contrib.auth import get_user_model


@pytest.fixture
def user(username="test", password="testpass"):
    return get_user_model().objects.create_user(username=username, password=password)


@pytest.fixture
def profile(user):
    return Profile.objects.create(user=user)
