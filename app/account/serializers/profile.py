from account.models import Profile, ProfileImage
from rest_framework import serializers


class ProfileImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProfileImage
        fields = ("id", "image")
        read_only_fields = ("id",)


class ProfileSerializer(serializers.ModelSerializer):
    images = ProfileImageSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "nickname",
            "height",
            "job",
            "residence",
            "religion",
            "is_smoke",
            "drinking_frequency",
            "images",
        )
        read_only_fields = ("id", "user")


class ProfilePostSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )

    class Meta:
        model = Profile
        fields = (
            "nickname",
            "height",
            "job",
            "residence",
            "religion",
            "is_smoke",
            "drinking_frequency",
            "images",
        )
