from django.urls import path
from .views import KakaoLoginView, KakaoLogoutView, KakaoLoginRedirectView

urlpatterns = [
    path("kakao/login/", KakaoLoginView.as_view(), name="kakao_login"),
    path("kakao/logout/", KakaoLogoutView.as_view(), name="kakao_logout"),
    path("kakao/redirect/", KakaoLoginRedirectView.as_view(), name="kakao_redirect"),
]