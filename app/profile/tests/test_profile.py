from profile.models import Profile, ProfileAnswer, ProfileImage

import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_list_profiles(api_client, user, profile):
    api_client.force_authenticate(user=user)

    url = reverse("profile:profile-list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data[0]["nickname"] == "testprofile"


@pytest.mark.django_db
def test_retrieve_profile(api_client, user, profile, another_profile):
    api_client.force_authenticate(user=user)

    url = reverse("profile:profile-detail", args=[another_profile.id])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["nickname"] == "anotherprofile"


@pytest.mark.django_db
def test_create_profile(api_client, user):
    api_client.force_authenticate(user=user)

    data = {
        "nickname": "newprofile",
        "height": 180,
        "job": "developer",
        "residence": "Seoul",
        "religion": "None",
        "is_smoke": False,
        "drinking_frequency": "Often",
    }

    url = reverse("profile:profile-list")
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["nickname"] == "newprofile"
    assert Profile.objects.filter(nickname="newprofile").exists()


@pytest.mark.django_db
def test_partial_update_profile(api_client, user, profile):
    api_client.force_authenticate(user=user)

    data = {"nickname": "updatedprofile"}

    url = reverse("profile:profile-detail", args=[profile.id])
    response = api_client.patch(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["nickname"] == "updatedprofile"


@pytest.mark.django_db
def test_delete_profile(api_client, user, profile):
    api_client.force_authenticate(user=user)

    url = reverse("profile:profile-detail", args=[profile.id])
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Profile.objects.filter(id=profile.id).exists()


@pytest.mark.django_db
def test_today_profiles(api_client, user, profile):
    api_client.force_authenticate(user=user)

    url = reverse("profile:profile-today")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_create_profile_answer(api_client, user, profile, simulation, answer_choice):
    api_client.force_authenticate(user=user)

    data = {"simulation_id": simulation.id, "answer_choice_id": answer_choice.id}

    url = reverse("profile:profile-answer")
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert ProfileAnswer.objects.filter(profile=profile, simulation=simulation).exists()


@pytest.mark.django_db
def test_update_profile_answer(api_client, user, profile_answer, answer_choice):
    api_client.force_authenticate(user=user)

    data = {"answer_choice_id": answer_choice.id}

    url = reverse("profile:profile-update-answer", args=[profile_answer.id])
    response = api_client.patch(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["answer"] == "Blue"
