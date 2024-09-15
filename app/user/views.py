import requests
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class KakaoLogin(SocialLoginView):
    adaptor_class = KakaoOAuth2Adapter


class SocialCallbackView(APIView):
    def get(self, request, *args, **kwargs):
        # 클라이언트로부터 소셜 제공자의 액세스 토큰을 쿼리 매개변수로 받습니다.
        code = request.query_params.get("code")
        state = request.query_params.get("state")
        access_token = request.COOKIES.get("refresh_token") or request.COOKIES.get(
            "access"
        )

        url = reverse("kakao_login")
        data = {"code": code, "state": state, "access_token": access_token}
        response = requests.post(url, data=data)
        return response
