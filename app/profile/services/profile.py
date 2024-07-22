import random
from profile.models import Profile, ProfileAnswer, ProfileImage

from contact.enums import MessageStatus
from core.utils import exception


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

        profiles = Profile.objects.exclude(id=my_profile.id).exclude(
            gender=my_profile.gender
        )

        MAX_RANDOM_COUNT = max(len(profiles), DEFAULT_RANDOM_COUNT)

        profiles = profiles.order_by("?")[:MAX_RANDOM_COUNT]
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

    def validate(self, validated_data):
        profile_id = validated_data.get("profile_id")
        nickname = validated_data.get("nickname")

        if profile_id:
            try:
                profile = Profile.objects.get(id=profile_id)
            except:
                raise exception.DoesNotExists
        else:
            profile = self._my_profile()

        if nickname and Profile.objects.filter(nickname=nickname).exists():
            raise exception.AlreadyExists
        elif profile.phone is None:
            raise exception.PhoneNotExists

    def match_answer(self, profile_id):
        my_answers = ProfileAnswer.objects.filter(profile=self._my_profile())
        other_answers = ProfileAnswer.objects.filter(profile_id=profile_id)

        results = []

        for my_answer in my_answers:
            other_answer = other_answers.filter(simulation=my_answer.simulation)
            if other_answer.exists():
                other_answer = other_answer.first()
                if other_answer.answer_choice == my_answer.answer_choice:
                    results.append(
                        {
                            "question": other_answer.question,
                            "answer": other_answer.answer,
                            "is_matched": True,
                        }
                    )
                else:
                    results.append(
                        {
                            "question": other_answer.question,
                            "answer": other_answer.answer,
                            "is_matched": False,
                        }
                    )
            else:
                continue

        return results
