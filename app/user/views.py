import logging
import os
from profile.models import Profile

import requests
from allauth.socialaccount.adapter import get_adapter
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

logger = logging.getLogger("django")


class KakaoLogin(SocialLoginView):
    adapter_class = KakaoOAuth2Adapter
    callback_url = "https://banada.duckdns.org/auth/login/"
    client_class = OAuth2Client


BASE_URL = "https://banada.duckdns.org/"

KAKAO_CALLBACK_URI = "https://banada.duckdns.org/api/v1/kakao/callback/"


@api_view(["GET"])
@permission_classes([AllowAny])
def kakao_callback(request):
    secret_key = os.environ.get("KAKAO_SECRET")
    client_id = os.environ.get("KAKAO_CLIENT_ID")
    code = request.GET.get("code")
    redirect_uri = KAKAO_CALLBACK_URI

    """
    Access Token Request
    """
    headers = {"Content-type": "application/x-www-form-urlencoded;charset=utf-8"}
    params = {
        "grant_type": "authorization_code",
        "client_secret": secret_key,
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "code": code,
    }
    token_req = requests.get(
        f"https://kauth.kakao.com/oauth/token", params=params, headers=headers
    )
    token_req_json = token_req.json()
    access_token = token_req_json.get("access_token")

    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    profile_json = profile_request.json()
    try:
        uid = profile_json.get("id")
        kakao_account = profile_json.get("kakao_account")
        profile = kakao_account.get("profile")
        nickname = profile.get("nickname")
    except (TypeError, AttributeError, KeyError):
        return JsonResponse(
            {"msg": "profile 접근 권한 동의가 필요합니다."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    """
    Signup or Signin Request
    """
    try:
        social_user = SocialAccount.objects.get(uid=uid, provider="kakao")
        user = social_user.user
        if social_user is None:
            return JsonResponse(
                {"err_msg": "email exists but not social user"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if social_user.provider != "kakao":
            return JsonResponse(
                {"msg": "no matching social type"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    except SocialAccount.DoesNotExist:
        user = get_user_model().objects.create(username=nickname)
        user.set_unusable_password()
        social_user = SocialAccount.objects.create(user=user, uid=uid, provider="kakao")
    except Exception as e:
        return JsonResponse({"msg": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

    if not user.profiles.exists():
        profile = Profile.objects.create(user=user)
    else:
        profile = Profile.objects.get(user=user)

    # JWT 생성
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    # 응답에 Set-Cookie 헤더 추가
    response = JsonResponse(
        {
            "user_id": user.id,
            "profile_id": profile.id,
            "access": access_token,
            "refresh": refresh_token,
        }
    )

    # 설정된 JWT를 쿠키에 추가
    cookie_max_age = 3600 * 24 * 14  # 14 days

    response.delete_cookie("sessionid")
    response.set_cookie(
        "refresh",
        refresh_token,
        max_age=cookie_max_age,
        httponly=True,
        samesite="Lax",
    )
    response.set_cookie(
        "access",
        access_token,
        max_age=settings.SIMPLE_JWT.get("ACCESS_TOKEN_LIFETIME"),
        httponly=True,
        samesite="Lax",
    )

    return response
