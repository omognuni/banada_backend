from allauth.socialaccount.providers.oauth2.views import OAuth2CallbackView
from django.urls import path
from user.views import SocialCallbackView

urlpatterns = [
    path(
        "kakao/login/callback/",
        SocialCallbackView.as_view(),
        name="kakao_callback",
    )
]
