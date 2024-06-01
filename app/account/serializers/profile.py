from account.models import Profile, ProfileAnswer, ProfileImage
from rest_framework import serializers


class ProfileAnswerSerializer(serializers.ModelSerializer):
    question = serializers.CharField()
    answer = serializers.CharField()

    class Meta:
        model = ProfileAnswer
        fields = ("id", "question", "answer")
        read_only_fields = ("id",)


class ProfileImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProfileImage
        fields = ("id", "image")
        read_only_fields = ("id",)


class ProfileListSerializer(serializers.ModelSerializer):
    main_image = serializers.ImageField()

    class Meta:
        model = Profile
        fields = ("id", "nickname", "age", "height", "main_image")


class ProfileDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
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
            "answers",
            "images",
        )
        read_only_fields = ("id", "user")


class ProfilePostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )

    class Meta:
        model = Profile
        fields = (
            "id",
            "nickname",
            "height",
            "job",
            "residence",
            "religion",
            "is_smoke",
            "drinking_frequency",
            "images",
        )
        read_only_fields = ("id",)


class ProfileAnswerPostSerializer(serializers.Serializer):
    simulation_id = serializers.IntegerField()
    answer_choice_id = serializers.IntegerField()


class ProfileAnswerPatchSerializer(serializers.Serializer):
    answer_choice_id = serializers.CharField()
