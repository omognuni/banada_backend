from allauth.socialaccount.providers.instagram.views import InstagramOAuth2Adapter
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView


class KakaoConnect(SocialLoginView):
    adapter_class = KakaoOAuth2Adapter
    callback_url = "https://banada.duckdns.org/accounts/kakao/login/callback/"
    client_class = OAuth2Client
