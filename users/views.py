import os

from django.contrib.auth import login
from django.core.exceptions import ImproperlyConfigured
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView

from .models import User
from .serializers import UserSerializer
from rest_framework import viewsets, status
from django.conf import settings
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from json.decoder import JSONDecodeError
from rest_framework.response import Response
from dj_rest_auth.registration.views import SocialLoginView
import requests
from allauth.socialaccount.models import SocialAccount
from rest_framework.permissions import AllowAny
from allauth.account.adapter import get_adapter


def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = 'Set the {} environment variable'.format(var_name)
        raise ImproperlyConfigured(error_msg)


class KakaoLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        kakao_token = request.data.get("access_token", None)
        if not kakao_token:
            return Response({"error": "Access token is required."}, status=400)

        user_info_url = "https://kapi.kakao.com/v2/user/me"
        headers = {"Authorization": f"Bearer {kakao_token}"}

        response = requests.get(user_info_url, headers=headers)
        user_info = response.json()

        if "id" not in user_info:
            return Response({"error": "Invalid Kakao token."}, status=400)

        kakao_oid = user_info["id"]
        kakao_email = user_info.get("kakao_account", {}).get("email")
        profile_image = (
            user_info.get("kakao_account", {})
            .get("profile", {})
            .get("thumbnail_image_url", "")
        )

        if not kakao_email:
            kakao_email = f"kakao_{kakao_oid}@example.com"

        user, created = User.objects.get_or_create(
            kakao_oid=kakao_oid,
            defaults={
                "email": kakao_email,
                "profile_image": profile_image,
                "is_active": True,
            },
        )

        if created:
            user.set_password(User.objects.make_random_password())
            user.save()

        login(request, user)

        # 직렬화된 사용자 데이터 반환
        user_data = UserSerializer(user).data
        return Response(
            {
                "message": "Login successful",
                "user": user_data,
            },
            status=200,
        )


class KakaoLoginRedirectView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """
        카카오 로그인 인증 코드 처리 및 토큰 발급
        """
        code = request.GET.get("code")
        if not code:
            raise ValidationError({"error": "Authorization code is missing."})

        REST_API_KEY = get_env_variable("REST_API_KEY")  # 환경 변수 또는 설정에서 가져오기
        REDIRECT_URI = "http://127.0.0.1:8000/kakaoLoginLogicRedirect"
        token_url = (
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code"
            f"&client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&code={code}"
        )
        response = requests.post(token_url)
        token_data = response.json()

        if "access_token" not in token_data:
            return Response({"error": "Failed to retrieve access token"}, status=400)

        # Save the token to the session (or database)
        request.session["access_token"] = token_data["access_token"]
        request.session.modified = True

        return Response({"message": "Login successful", "access_token": token_data["access_token"]}, status=200)


class KakaoLogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        카카오 로그아웃 처리
        """
        access_token = request.session.get("access_token")
        if not access_token:
            return Response({"error": "User is not logged in."}, status=400)

        logout_url = "https://kapi.kakao.com/v1/user/logout"
        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.post(logout_url, headers=headers)
        result = response.json()

        if result.get("id"):
            del request.session["access_token"]
            request.session.modified = True
            return Response({"message": "Logout successful."}, status=200)
        return Response({"error": "Logout failed."}, status=400)
