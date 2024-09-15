from allauth.socialaccount.models import SocialToken
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class KakaoLoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        access_token = request.data.get("access_token")

        if access_token:
            # KakaoOAuth2Adapter를 사용하여 토큰 검증 및 사용자 정보 가져오기
            adapter = KakaoOAuth2Adapter()
            client = OAuth2Client(
                request, client_id=adapter.get_provider().get_app(request).client_id
            )
            token = SocialToken(token=access_token)

            # 사용자가 존재하는지 확인하고, 없으면 생성
            login = adapter.complete_login(
                request, app=adapter.get_provider().get_app(request), token=token
            )
            login.token = token
            login.user.save()

            # 여기서 추가적으로 user 정보나 다른 응답 데이터를 구성할 수 있습니다.
            return Response({"access_token": access_token, "user": login.user.id})
        else:
            return Response({"error": "Access token not provided"}, status=400)
