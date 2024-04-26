from account.models import Profile
from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):

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
            "image",
        )
        read_only_fields = ("id", "user")
