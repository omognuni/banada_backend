from allauth.socialaccount.models import SocialAccount, SocialLogin
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


class CustomKakaoOAuth2Adapter(KakaoOAuth2Adapter):
    def complete_login(self, request, app, token, response):
        # 로그인 정보 처리
        login = super().complete_login(request, app, token, response)
        user = login.user

        # 해당 소셜 계정이 이미 있는지 확인
        social_account_exists = SocialAccount.objects.filter(
            provider="kakao", user=user
        ).exists()

        # JWT 토큰 발급
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # 쿠키에 access_token 설정
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,  # JavaScript에서 접근 불가
            secure=True,  # HTTPS에서만 전송 (개발 환경에 따라 조정)
            samesite="Lax",  # CSRF 보호를 위한 SameSite 설정
        )

        # 쿠키에 refresh_token 설정
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="Lax",
        )

        if social_account_exists:
            # 사용자가 존재하는 경우, 홈 페이지로 리디렉션
            return HttpResponseRedirect("/")
        else:
            # 사용자가 존재하지 않는 경우, 사용자 ID를 JSON으로 반환
            return Response(
                status=status.HTTP_200_OK,
                data={"user": user.id, "username": user.username},
            )
