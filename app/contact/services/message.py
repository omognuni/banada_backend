from profile.models import Profile

from contact.enums import MessageStatus
from contact.models import Message
from django.db.models import Q


class MessageService:

    def __init__(self, user):
        self._user = Profile.objects.get(user=user)

    def _messages(self):
        messages = Message.objects.select_related(
            "sender", "receiver", "message_type"
        ).all()
        return messages

    def fetch_received_messages(self):
        messages = (
            Message.objects.select_related("sender", "message_type")
            .prefetch_related("contacts")
            .filter(receiver=self._user)
        )

        return messages

    def fetch_sent_messages(self):
        messages = (
            Message.objects.select_related("receiver", "message_type")
            .prefetch_related("contacts")
            .filter(sender=self._user)
        )

        return messages

    def send_message(self, validated_data):
        message = Message.objects.create(**validated_data)
        return message

    def update_message(self, pk, validated_data):
        message = Message.objects.filter(id=pk)
        message.update(**validated_data)
        return message.first()

    def past_match(self):
        # 내가 메시지를 보냈을때 거절(만료) 당한 경우
        # 상대가 메세지를 보냈는데 만료된 경우
        # 단방향 호감 표시한 경우
        profile_ids = (
            Message.objects.filter(Q(sender=self._user) | Q(receiver=self._user))
            .filter(Q(status=MessageStatus.EXPIRED) | Q(status=MessageStatus.REFUSED))
            .values_list("receiver", flat=True)
            .distinct()
        )
        profiles = Profile.objects.filter(id__in=profile_ids)
        # messages = self.fetch_sent_messages()
        # profiles = (
        #     messages.filter(
        #         Q(status=MessageStatus.EXPIRED) | Q(status=MessageStatus.REFUSED)
        #     )
        #     .values("receiver")
        #     .distinct()
        # )
        return profiles
