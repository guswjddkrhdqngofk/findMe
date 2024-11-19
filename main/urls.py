from django.db import router
from django.urls import path
from .views import GPSModelViewSet

router.register('gps-models', GPSModelViewSet, basename='gps-models')


urlpatterns = router.urls + [

]
