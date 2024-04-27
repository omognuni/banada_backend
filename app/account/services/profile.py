from account.models import Profile, ProfileImage
from core.utils import exception
from django.contrib.auth import get_user_model


class ProfileService:

    def __init__(self, user):
        self._user = user

    def _my_profile(self):
        try:
            profile = Profile.objects.get(user=self._user.id)
        except Profile.DoesNotExist:
            raise exception.DoesNotExists
        return profile

    def fetch_my_profile(self):
        return self._my_profile()

    def fetch_profile(self, profile_id):
        try:
            profile = Profile.objects.get(id=profile_id)
        except Profile.DoesNotExist:
            raise exception.DoesNotExists
        return profile

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
