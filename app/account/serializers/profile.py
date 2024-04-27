from account.models import Profile, ProfileImage, Answer
from rest_framework import serializers


class ProfileAnswerSerializer(serializers.ModelSerializer):
    question = serializers.CharField()
    
    class Meta:
        model = Answer
        fields = ("id", "question", "answer")
        read_only_fields = ("id",)


class ProfileImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProfileImage
        fields = ("id", "image")
        read_only_fields = ("id",)


class ProfileSerializer(serializers.ModelSerializer):
    images = ProfileImageSerializer(many=True, read_only=True)
    answers = ProfileAnswerSerializer(many=True, read_only=True)

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
        
class ProfileAnswerPostSerializer(serializers.Serializer):
    simulation_id = serializers.IntegerField()
    answer = serializers.CharField()
    
    
class ProfileAnswerPatchSerializer(serializers.Serializer):
    answer = serializers.CharField()
