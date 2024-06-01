import random

from account.models import Profile, ProfileAnswer, ProfileImage
from core.utils import exception
from django.contrib.auth import get_user_model


class ProfileService:

    def __init__(self, user=None):
        self._user = user

    def _my_profile(self):
        try:
            profile = Profile.objects.get(user=self._user.id)
        except Profile.DoesNotExist:
            raise exception.DoesNotExists
        return profile

    def fetch_profiles(self):
        profiles = Profile.objects.all()
        return profiles

    def fetch_my_profile(self):
        return self._my_profile()

    def fetch_profile(self, profile_id):
        try:
            profile = Profile.objects.get(id=profile_id)
            message_type = profile.has_match(self._my_profile())

        except Profile.DoesNotExist:
            raise exception.DoesNotExists
        return profile, message_type

    def fetch_random_profiles(self):
        DEFAULT_RANDOM_COUNT = 4

        my_profile = self._my_profile()
        max_id = Profile.objects.last().id
        sample_ids = set()
        for _ in range(DEFAULT_RANDOM_COUNT):
            sample_ids.add(random.randint(1, max_id))

        profiles = Profile.objects.filter(id__in=sample_ids).exclude(
            id=my_profile.id, gender=my_profile.gender
        )[:DEFAULT_RANDOM_COUNT]

        return profiles

    def update_my_profile(self, validated_data):
        images = validated_data.pop("images", [])
        profile = self._my_profile()
        for key, value in validated_data.items():
            setattr(profile, key, value)
        profile.save()

        for i, image in enumerate(images):
            ProfileImage.objects.create(profile=profile, image=image)

        return profile

    def create_my_profile(self, validated_data):
        images = validated_data.pop("images", [])

        profile = Profile.objects.create(user=self._user, **validated_data)

        for i, image in enumerate(images):
            ProfileImage.objects.create(profile=profile, image=image)

        return profile

    def delete_my_profile(self):
        profile = self._my_profile()
        profile.delete()

    def create_answer(self, validated_data):
        profile = self._my_profile()
        ProfileAnswer.objects.create(profile=profile, **validated_data)

    def update_answer(self, answer_id, validated_data):
        try:
            answer = ProfileAnswer.objects.get(id=answer_id)
        except ProfileAnswer.DoesNotExist:
            raise exception.DoesNotExists

        for key, value in validated_data.items():
            setattr(answer, key, value)
        answer.save()
        return answer
