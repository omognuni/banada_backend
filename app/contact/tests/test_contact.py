import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

MESSAGE_URL = reverse("contact:message-list")


@pytest.mark.django_db
def test_send_message(api_client, user, profile, sender, receiver):
    content = "test message"
    data = {"sender_id": sender.id, "receiver_id": receiver.id, "content": content}

    api_client = APIClient()
    api_client.force_authenticate(user=user)
    response = api_client.post(MESSAGE_URL, data)

    assert response.status_code == status.HTTP_201_CREATED
