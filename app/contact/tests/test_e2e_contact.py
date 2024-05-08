import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

MESSAGE_URL = reverse("contact:message-list")


@pytest.mark.django_db
def test_send_message(sender, receiver):
    content = "test message"
    data = {"sender_id": sender.id, "receiver_id": receiver.id, "content": content}

    client = APIClient()
    res = client.post(MESSAGE_URL, data)
    print(res.data)

    assert res.status_code == status.HTTP_201_CREATED
