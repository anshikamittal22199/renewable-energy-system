from django.db import models

class Forecast(models.Model):
    location = models.CharField(max_length=100)
    date = models.DateField()
    sun_intensity_factor = models.FloatField()
    daylight_hours = models.FloatField()
    forecast_kwh = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
