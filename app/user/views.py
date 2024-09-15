from allauth.socialaccount.models import SocialAccount, SocialLogin
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


class CustomKakaoOAuth2Adapter(KakaoOAuth2Adapter):
    def complete_login(self, request, app, token, **kwargs):
        # 로그인 정보 처리
        # login = super().complete_login(request, app, token, **kwargs)
        try:
            # 로그인 정보 처리
            login = super().complete_login(request, app, token, **kwargs)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

        user = login.user

        # 만약 사용자 인스턴스가 저장되지 않았다면, 먼저 저장합니다.
        if not user.pk:
            user.save()

        # 해당 소셜 계정이 이미 있는지 확인
        social_account_exists = SocialAccount.objects.filter(
            provider="kakao", user=user
        ).exists()

        # JWT 토큰 발급
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # 응답 객체 생성
        response = Response(
            {"access_token": access_token, "refresh_token": refresh_token}
        )
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="Lax",
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="Lax",
        )

        if social_account_exists:
            response["Location"] = "/"
            response.status_code = 302
            return response
        else:
            return Response({"user_id": user.id})
