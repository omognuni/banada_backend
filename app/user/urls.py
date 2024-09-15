from django.urls import path
from user.views import KakaoLogin

urlpatterns = [
    # path(
    #     "kakao/login/callback/",
    #     SocialCallbackView.as_view(),
    #     name="kakao_callback",
    # ),
    path("kakao/login/", KakaoLogin.as_view(), name="kakao_login"),
]
