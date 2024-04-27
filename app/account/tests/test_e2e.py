import pytest
from account.models import Profile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

PROFILE_URL = reverse("account:profile-list")


@pytest.mark.django_db
def test_get_my_profile(user, profile):

    client = APIClient()
    client.force_authenticate(user)

    res = client.get(PROFILE_URL)

    assert res.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_create_my_profile(user, profile, images):
    client = APIClient()
    client.force_authenticate(user)

    data = {
        "nickname": "testnick",
        "height": 180,
        "job": "학생",
        "residence": "광명",
        "religion": "무교",
        "is_smoke": False,
        "drinking_frequency": 2,
        "images": images,
    }

    res = client.post(PROFILE_URL, data=data)
    print(res.data)
    assert res.status_code == status.HTTP_201_CREATED
