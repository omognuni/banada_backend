import os
from json.decoder import JSONDecodeError

import requests
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


class KakaoLogin(SocialLoginView):
    adapter_class = KakaoOAuth2Adapter
    callback_url = "https://banada.duckdns.org/auth/login/"
    client_class = OAuth2Client


BASE_URL = "https://banada.duckdns.org/"

KAKAO_CALLBACK_URI = "https://banada.duckdns.org/auth/login"  # 프론트 로그인 URI 입력


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

    """
    Email Request
    """
    profile_request = requests.post(
        "https://kapi.kakao.com/v2/user/me",
        headers={
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
            "Authorization": f"Bearer {access_token}",
        },
    )
    profile_json = profile_request.json()
    kakao_account = profile_json.get("kakao_account")

    """
    kakao_account에서 이메일 외에
    카카오톡 프로필 이미지, 배경 이미지 url 가져올 수 있음
    print(kakao_account) 참고
    """
    email = kakao_account.get("email")

    """
    Signup or Signin Request
    """
    try:
        user = get_user_model().objects.get(email=email)
        # 기존에 가입된 유저의 Provider가 kakao가 아니면 에러 발생, 맞으면 로그인
        # 다른 SNS로 가입된 유저
        social_user = SocialAccount.objects.get(user=user)
        if social_user is None:
            return JsonResponse(
                {"err_msg": "email exists but not social user"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if social_user.provider != "kakao":
            return JsonResponse(
                {"err_msg": "no matching social type"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # 기존에 kakao로 가입된 유저
        data = {"access": access_token, "code": code}
        accept = requests.post(f"{BASE_URL}api/v1/kakao/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({"err_msg": "failed to signin"}, status=accept_status)
        accept_json = accept.json()
        # refresh_token을 headers 문자열에서 추출함
        refresh_token = accept.headers["Set-Cookie"]
        refresh_token = refresh_token.replace("=", ";").replace(",", ";").split(";")
        token_index = refresh_token.index(" refresh")
        cookie_max_age = 3600 * 24 * 14  # 14 days
        refresh_token = refresh_token[token_index + 1]
        accept_json.pop("user", None)
        response_cookie = JsonResponse(accept_json)
        response_cookie.set_cookie(
            "refresh",
            refresh_token,
            max_age=cookie_max_age,
            httponly=True,
            samesite="Lax",
        )
        return response_cookie

    except get_user_model().DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        data = {"access": access_token, "code": code}
        accept = requests.post(f"{BASE_URL}api/v1/kakao/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({"err_msg": "failed to signup"}, status=accept_status)
        # user의 pk, email, first name, last name과 Access Token, Refresh token 가져옴

        accept_json = accept.json()
        # refresh_token을 headers 문자열에서 추출함
        refresh_token = accept.headers["Set-Cookie"]
        refresh_token = refresh_token.replace("=", ";").replace(",", ";").split(";")
        token_index = refresh_token.index("refresh")
        refresh_token = refresh_token[token_index + 1]

        accept_json.pop("user", None)
        response_cookie = JsonResponse(accept_json)
        response_cookie.set_cookie(
            "refresh",
            refresh_token,
            max_age=cookie_max_age,
            httponly=True,
            samesite="Lax",
        )
        return response_cookie
