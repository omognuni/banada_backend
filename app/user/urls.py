from django.urls import path
from user.views import KakaoLogin

urlpatterns = [path("kakao/login/", KakaoLogin.as_view(), name="kakao_connect")]
