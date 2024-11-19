from rest_framework import serializers
from .models import GPSModel


class GPSModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPSModel
        fields = '__all__'


class GPSModelCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPSModel
        fields = ('device_code',)
