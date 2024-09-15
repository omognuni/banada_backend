from django.urls import path
from user.views import SocialCallbackView

urlpatterns = [
    path(
        "kakao/login/callback/",
        SocialCallbackView.as_view(),
        name="kakao_callback",
    )
]
