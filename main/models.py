from django.db import models


# Create your models here.
class GPSModel(models.Model):
    device_code = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
