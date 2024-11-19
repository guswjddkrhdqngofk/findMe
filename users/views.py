from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .kakao import KakaoAPI


class KakaoLoginView(APIView):
    def post(self, request):
        access_token = request.data.get("access_token", None)
        if not access_token:
            return Response({"error": "Access token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 카카오 API 호출
            kakao_api = KakaoAPI(access_token)
            kakao_user_info = kakao_api.get_user_info()

            # 카카오에서 받은 사용자 정보
            kakao_oid = kakao_user_info["id"]
            kakao_account = kakao_user_info.get("kakao_account", {})
            email = kakao_account.get("email", f"{kakao_oid}@kakao.com")
            profile = kakao_user_info.get("properties", {})
            profile_image = profile.get("profile_image", "")

            # 사용자 조회 또는 생성
            user, created = User.objects.get_or_create(
                kakao_oid=kakao_oid,
                defaults={
                    "email": email,
                    "profile_image": profile_image,
                },
            )

            if not created:
                # 기존 사용자 정보 업데이트
                user.profile_image = profile_image
                user.save()

            # JWT 토큰 발급
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "profile_image": user.profile_image,
                },
            })

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
