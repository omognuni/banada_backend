from contact.models import Message


class MessageService:

    def __init__(self, user):
        self._user = user

    def fetch_received_messages(self):
        messages = Message.objects.filter(reciever=self._user)

        return messages

    def fetch_sent_messages(self):
        messages = Message.objects.filter(sender=self._user)

        return messages

    def send_message(self, validated_data):
        message = Message.objects.create(**validated_data)
        return message
