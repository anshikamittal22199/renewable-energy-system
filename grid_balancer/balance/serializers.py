from rest_framework import serializers

class BalanceRequestSerializer(serializers.Serializer):
    location = serializers.CharField(max_length=100)
    date = serializers.DateField()
    sun_intensity_factor = serializers.FloatField()
    daylight_hours = serializers.FloatField()