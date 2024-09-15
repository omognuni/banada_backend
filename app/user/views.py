from allauth.socialaccount.helpers import complete_social_login
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from django.http import HttpResponse
from django.urls import reverse
from django.utils.http import urlencode
from rest_framework_simplejwt.tokens import RefreshToken


class CustomKakaoOAuth2Adapter(KakaoOAuth2Adapter):
    def complete_login(self, request, app, token, **kwargs):
        return super().complete_login(request, app, token, **kwargs)
