from account.models import Profile
from django.contrib.auth import get_user_model


class ProfileService:

    def __init__(self, user):
        self._user = user

    def fetch_my_profile(self):
        profile = Profile.objects.get(user_id=self._user)
        return profile

    def fetch_profile(self, profile_id):
        pass

    def update_my_profile(self, validated_data):
        profile = Profile.objects.get(user_id=self._user)
        for key, value in validated_data.items():
            setattr(profile, key, value)
        profile.save()
        return profile

    def create_my_profile(self, validated_data):
        profile = Profile.objects.create(user_id=self._user, **validated_data)
        return profile

    def delete_my_profile(self):
        profile = Profile.objects.get(user_id=self._user)
        profile.delete()
