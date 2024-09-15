from django.urls import path
from user.views import KakaoConnect

urlpatterns = [path("kakao/connect/", KakaoConnect.as_view(), name="kakao_connect")]
