from django.contrib.auth import get_user_model
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer as DefaultRegisterSerializer

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'kakao_oid', 'position', 'profile_image', 'is_staff', 'is_active', 'created_at']
        read_only_fields = ['id', 'is_staff', 'is_active', 'created_at']


class KakaoTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    code = serializers.CharField()


class UserInfoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "position", "profile_image")


class GetUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "position", "profile_image")
