from contact.models import Contact, Message, SNSInfo
from rest_framework import serializers


class SNSInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = SNSInfo
        fields = ("id", "service", "username")


class ContactSerializer(serializers.ModelSerializer):
    snsinfos = SNSInfoSerializer(read_only=True, many=True)

    class Meta:
        model = Contact
        fields = ("id", "phone_number", "snsinfos")


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.nickname", read_only=True)
    receiver_name = serializers.CharField(source="receiver.nickname", read_only=True)
    contacts = ContactSerializer(read_only=True, many=True)

    class Meta:
        model = Message
        fields = ("id", "sender_name", "receiver_name", "contacts", "content", "status")


class MessagePostSerializer(serializers.Serializer):
    sender_id = serializers.IntegerField()
    receiver_id = serializers.IntegerField()
    content = serializers.CharField()
