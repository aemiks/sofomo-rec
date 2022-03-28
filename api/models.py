from django.db import models
from django.conf import settings


class GeolocationData(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="geolocation")
    ip = models.CharField(max_length=50)
    continent_code = models.CharField(max_length=3)
    continent_name = models.CharField(max_length=50)
    country_code = models.CharField(max_length=3)
    country_name = models.CharField(max_length=50)
    region_code = models.CharField(max_length=3)
    region_name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip = models.CharField(max_length=10)
    latitude = models.FloatField(max_length=50, null=True, blank=True)
    longitude = models.FloatField(max_length=50, null=True, blank=True)

    # is_own parameter to distinguish between foreign queries and your own
    is_own = models.BooleanField(default=False)

    def __str__(self):
        return self.ip
