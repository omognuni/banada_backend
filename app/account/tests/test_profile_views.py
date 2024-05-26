import pytest
from account.models import Profile, ProfileAnswer, ProfileImage
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_list_profiles(api_client, user, profile):
    api_client.force_authenticate(user=user)

    url = reverse("account:profile-list")  # Define this URL pattern in your urls.py
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["nickname"] == "testprofile"


@pytest.mark.django_db
def test_retrieve_profile(api_client, user, profile, another_profile):
    api_client.force_authenticate(user=user)

    url = reverse(
        "account:profile-detail", args=[another_profile.id]
    )  # Define this URL pattern in your urls.py
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

    url = reverse("account:profile-list")  # Define this URL pattern in your urls.py
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["nickname"] == "newprofile"
    assert Profile.objects.filter(nickname="newprofile").exists()


@pytest.mark.django_db
def test_partial_update_profile(api_client, user, profile):
    api_client.force_authenticate(user=user)

    data = {"nickname": "updatedprofile"}

    url = reverse(
        "account:profile-detail", args=[profile.id]
    )  # Define this URL pattern in your urls.py
    response = api_client.patch(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["nickname"] == "updatedprofile"


@pytest.mark.django_db
def test_delete_profile(api_client, user, profile):
    api_client.force_authenticate(user=user)

    url = reverse(
        "account:profile-detail", args=[profile.id]
    )  # Define this URL pattern in your urls.py
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Profile.objects.filter(id=profile.id).exists()


@pytest.mark.django_db
def test_today_profiles(api_client, user, profile):
    api_client.force_authenticate(user=user)

    url = reverse("account:profile-today")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    # Additional assertions based on the expected data format


@pytest.mark.django_db
def test_create_profile_answer(api_client, user, profile, simulation, answer_choice):
    api_client.force_authenticate(user=user)

    data = {"simulation_id": simulation.id, "answer_choice_id": answer_choice.id}

    url = reverse("account:profile-answer")  # Define this URL pattern in your urls.py
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert ProfileAnswer.objects.filter(profile=profile, simulation=simulation).exists()


@pytest.mark.django_db
def test_update_profile_answer(api_client, user, profile_answer, answer_choice):
    api_client.force_authenticate(user=user)

    data = {"answer_choice_id": answer_choice.id}

    url = reverse(
        "account:profile-update-answer", args=[profile_answer.id]
    )  # Define this URL pattern in your urls.py
    response = api_client.patch(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["answer"] == "Blue"
