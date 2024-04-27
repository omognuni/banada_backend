import tempfile

import pytest
from account.models import Profile
from django.contrib.auth import get_user_model
from PIL import Image


@pytest.fixture
def user(username="test", password="testpass"):
    return get_user_model().objects.create_user(username=username, password=password)


@pytest.fixture
def profile(user):
    return Profile.objects.create(user=user)


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
