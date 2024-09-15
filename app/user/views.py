from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from django.contrib.auth import login as auth_login
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils.http import urlencode
from rest_framework_simplejwt.tokens import RefreshToken


class CustomKakaoOAuth2Adapter(KakaoOAuth2Adapter):
    def complete_login(self, request, app, token, **kwargs):
        try:
            # 로그인 정보 처리
            login = super().complete_login(request, app, token, **kwargs)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

        user = login.user

        # 만약 사용자 인스턴스가 저장되지 않았다면, 먼저 저장합니다.
        if not user.pk:
            user.save()

        # 사용자를 Django의 세션에 로그인 시킵니다.
        auth_login(request, user)

        # 이제 dj-rest-auth의 로그인 엔드포인트를 호출합니다.
        # 자동으로 JWT 토큰을 발급하고 이를 쿠키에 저장하도록 처리할 수 있습니다.

        # 이 예제에서는 JWT 토큰을 발급한 후 /dashboard로 리디렉션합니다.
        # 필요한 경우 이 부분을 수정하여 다른 페이지로 리디렉션하거나 JSON 응답을 반환할 수 있습니다.

        # 리다이렉트 URL 설정 (로그인 후 리다이렉트할 경로)
        redirect_url = reverse("dashboard")  # 예: 사용자가 로그인 후 대시보드로 이동

        # Optional: 추가적인 URL 파라미터 설정 (필요할 경우)
        query_string = urlencode({"next": redirect_url})

        # 실제 리다이렉션을 수행할 URL
        url = f"{reverse('rest_login')}?{query_string}"

        return HttpResponseRedirect(url)
