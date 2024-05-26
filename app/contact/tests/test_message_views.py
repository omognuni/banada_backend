import pytest
from contact.enums import MessageStatus
from contact.models import Message
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_received_messages(api_client, user, profile, another_profile):
    api_client.force_authenticate(user=user)
    Message.objects.create(sender=another_profile, receiver=profile, content="Hello")

    url = reverse("contact:message-received")  # Define this URL pattern in your urls.py
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["content"] == "Hello"


@pytest.mark.django_db
def test_sent_messages(api_client, user, profile, another_profile):
    api_client.force_authenticate(user=user)
    Message.objects.create(sender=profile, receiver=another_profile, content="Hello")

    url = reverse("contact:message-sent")  # Define this URL pattern in your urls.py
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["content"] == "Hello"


@pytest.mark.django_db
def test_create_message(api_client, user, profile, another_profile):
    api_client.force_authenticate(user=user)
    data = {
        "sender_id": profile.id,
        "receiver_id": another_profile.id,
        "content": "Hello",
    }

    url = reverse("contact:message-list")  # Define this URL pattern in your urls.py
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["content"] == "Hello"
    assert Message.objects.filter(sender=profile, receiver=another_profile).exists()


@pytest.mark.django_db
def test_partial_update_message(api_client, user, profile, another_profile):
    api_client.force_authenticate(user=user)
    message = Message.objects.create(
        sender=profile, receiver=another_profile, content="Hello"
    )

    data = {"content": "Updated content", "status": MessageStatus.ACCEPTED}

    url = reverse(
        "contact:message-detail", args=[message.id]
    )  # Define this URL pattern in your urls.py
    response = api_client.patch(url, data)
    print(response.data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["content"] == "Updated content"
    assert response.data["status"] == MessageStatus.ACCEPTED


@pytest.mark.django_db
def test_past_match(api_client, user, profile, another_profile):
    api_client.force_authenticate(user=user)

    url = reverse(
        "contact:message-past-match"
    )  # Define this URL pattern in your urls.py
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    # Additional assertions based on the expected data format
