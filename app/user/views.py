import requests
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class CustomKakaoOAuth2Adapter(KakaoOAuth2Adapter):
    def complete_login(self, request, app, token, **kwargs):

        return super().complete_login(request, app, token, **kwargs)
