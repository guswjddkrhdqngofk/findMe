from django.urls import path
from .views import GPSModelViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register('gps-models', GPSModelViewSet, basename='gps-models')


urlpatterns = router.urls + [

]
