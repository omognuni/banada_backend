from contact.models import Message
from account.models import Profile

class MessageService:

    def __init__(self, user):
        self._user = Profile.objects.get(user=user)

    def fetch_received_messages(self):
        messages = Message.objects.filter(receiver=self._user)

        return messages

    def fetch_sent_messages(self):
        messages = Message.objects.filter(sender=self._user)

        return messages

    def send_message(self, validated_data):
        message = Message.objects.create(**validated_data)
        return message
