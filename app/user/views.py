from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class KakaoLogin(SocialLoginView):
    adaptor_class = KakaoOAuth2Adapter


class SocialCallbackView(APIView):
    def get(self, request, *args, **kwargs):
        # 클라이언트로부터 소셜 제공자의 액세스 토큰을 쿼리 매개변수로 받습니다.
        code = request.query_params.get("code")
        access_token = request.COOKIES.get("refresh_token") or request.COOKIES.get(
            "access"
        )

        query_params = request.GET.copy()
        query_params["access_token"] = access_token

        # 새로운 QueryDict를 사용하여 request._request.GET을 덮어씁니다.
        request._request.GET = query_params

        # KakaoLogin 같은 SocialLoginView를 호출하여 사용자 로그인 및 JWT 발급
        view = KakaoLogin.as_view()
        response = view(
            request._request
        )  # `_request`를 사용하여 원본 WSGIRequest를 전달

        return response
