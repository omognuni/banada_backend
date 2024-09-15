from allauth.socialaccount.providers.oauth2.views import OAuth2CallbackView
from django.urls import path
from user.views import CustomKakaoOAuth2Adapter

urlpatterns = [
    path(
        "kakao/login/callback/",
        OAuth2CallbackView.adapter_view(CustomKakaoOAuth2Adapter),
        name="kakao_callback",
    )
]
