from django.urls import path
from user.views import KakaoLogin, SocialCallbackView

urlpatterns = [
    path(
        "kakao/login/callback/",
        SocialCallbackView.as_view(),
        name="kakao_callback",
    ),
    path("kakao/", KakaoLogin.as_view(), name="kakao_login"),
]
