import random
import string

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import User
from django.utils.text import slugify


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)

        # 기존에 username이 존재하는지 확인
        if not user.username:
            user.username = self.generate_unique_username(sociallogin)

        return user

    def generate_unique_username(self, sociallogin):
        base_username = slugify(sociallogin.account.extra_data.get("name", "user"))

        # 만약 base_username이 비어있거나 중복된다면 임의의 값을 생성
        while not base_username or User.objects.filter(username=base_username).exists():
            base_username = base_username + "".join(
                random.choices(string.ascii_lowercase + string.digits, k=5)
            )

        return base_username
