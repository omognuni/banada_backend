import tempfile
from profile.models import AnswerChoice, Profile, ProfileAnswer, Simulation

import pytest
from django.contrib.auth import get_user_model
from PIL import Image
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(username="test", password="testpass"):
    return get_user_model().objects.create_user(username=username, password=password)


@pytest.fixture
def profile(user):
    return Profile.objects.create(user=user, nickname="testprofile")


@pytest.fixture
def images():
    images = []
    for _ in range(5):
        image_file = tempfile.NamedTemporaryFile(suffix=".jpg")
        img = Image.new("RGB", (10, 10))
        img.save(image_file, format="JPEG")
        image_file.seek(0)
        images.append(image_file)
    return images


@pytest.fixture
def another_user():
    User = get_user_model()
    return User.objects.create_user(username="anotheruser", password="anotherpass")


@pytest.fixture
def another_profile(another_user):
    return Profile.objects.create(user=another_user, nickname="anotherprofile")


@pytest.fixture
def simulation():
    return Simulation.objects.create(
        category="relationship", question="What is your favorite color?"
    )


@pytest.fixture
def answer_choice(simulation):
    return AnswerChoice.objects.create(simulation=simulation, index=1, content="Blue")


@pytest.fixture
def profile_answer(profile, simulation, answer_choice):
    return ProfileAnswer.objects.create(
        profile=profile, simulation=simulation, answer_choice=answer_choice
    )
