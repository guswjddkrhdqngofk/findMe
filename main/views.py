from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from .models import GPSModel
from .serializers import GPSModelSerializer, GPSModelCreateSerializer


class GPSModelViewSet(viewsets.ModelViewSet):
    queryset = GPSModel.objects.all()
    permission_classes = []
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = []
    ordering_fields = []
    search_fields = []

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GPSModelSerializer
        return GPSModelCreateSerializer

