from profile.models import Profile, ProfileImage

from contact.enums import MessageTypeChoices
from contact.models import Contact, Message, MessageType, SNSInfo
from rest_framework import serializers


class SNSInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = SNSInfo
        fields = ("id", "service", "username")


class ContactSerializer(serializers.ModelSerializer):
    snsinfos = SNSInfoSerializer(many=True)

    class Meta:
        model = Contact
        fields = ("id", "phone", "snsinfos")

    def create(self, validated_data):
        snsinfos_data = validated_data.pop("snsinfos")
        user = self.context["request"].user
        profile = Profile.objects.get(user=user)

        contact = Contact.objects.create(**validated_data, profile=profile)
        for snsinfo_data in snsinfos_data:
            SNSInfo.objects.create(contact=contact, **snsinfo_data)
        return contact

    def update(self, instance, validated_data):
        snsinfos_data = validated_data.pop("snsinfos")
        instance.phone = validated_data.get("phone", instance.phone)
        instance.save()

        instance.snsinfos.all().delete()
        for snsinfo_data in snsinfos_data:
            SNSInfo.objects.create(contact=instance, **snsinfo_data)

        return instance


class MessageTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessageType
        fields = ("id", "name", "cost")


class MessageProfileImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProfileImage
        fields = ("id", "image")


class MessageProfileSerializer(serializers.ModelSerializer):
    images = MessageProfileImageSerializer(read_only=True, many=True)

    class Meta:
        model = Profile
        fields = ("id", "nickname", "age", "images")


class ReceivedMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.nickname", read_only=True)
    receiver_name = serializers.CharField(source="receiver.nickname", read_only=True)
    contacts = ContactSerializer(source="sender.contacts", read_only=True, many=True)
    message_type = MessageTypeSerializer(read_only=True)
    is_match = serializers.BooleanField(read_only=True)

    class Meta:
        model = Message
        fields = (
            "id",
            "sender_name",
            "receiver_name",
            "contacts",
            "content",
            "status",
            "message_type",
            "is_match",
        )


class SentMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.nickname", read_only=True)
    receiver_name = serializers.CharField(source="receiver.nickname", read_only=True)
    contacts = ContactSerializer(source="receiver.contacts", read_only=True, many=True)
    message_type = MessageTypeSerializer(read_only=True)
    is_match = serializers.BooleanField(read_only=True)

    class Meta:
        model = Message
        fields = (
            "id",
            "sender_name",
            "receiver_name",
            "contacts",
            "content",
            "status",
            "message_type",
            "is_match",
        )


class MessagePostSerializer(serializers.Serializer):
    sender_id = serializers.IntegerField()
    receiver_id = serializers.IntegerField()
    message_type_id = serializers.IntegerField(required=False)
    content = serializers.CharField()


class MessagePatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = (
            "content",
            "status",
        )
