from allauth.socialaccount.providers.oauth2.views import OAuth2CallbackView
from django.urls import path
from user.views import KakaoLogin, kakao_callback

urlpatterns = [
    path("kakao/login/finish/", KakaoLogin.as_view(), name="kakao_auth"),
    path("kakao/callback/", kakao_callback, name="kakao_callback"),
]
