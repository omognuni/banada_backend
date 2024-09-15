from allauth.socialaccount.providers.oauth2.views import OAuth2CallbackView
from django.urls import path
from user.views import KakaoLogin

urlpatterns = [path("auth/kakao/", KakaoLogin.as_view(), name="kakao_auth")]
