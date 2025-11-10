from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Forecast
from .serializers import ForecastSerializer
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

@api_view(['POST'])
def forecast_view(request):
    try:
        data = request.data
        location = data.get("location")
        date_str = data.get("date")
        sun_intensity_factor = float(data.get("sun_intensity_factor", 0))
        daylight_hours = float(data.get("daylight_hours", 0))
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except Exception:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)

        # Simple simulation
        some_base_value = 50
        forecast_kwh = some_base_value + (sun_intensity_factor * daylight_hours)
        forecast = Forecast.objects.create(
            location=location,
            date=date,
            sun_intensity_factor=sun_intensity_factor,
            daylight_hours=daylight_hours,
            forecast_kwh=forecast_kwh,
        )

        return Response(ForecastSerializer(forecast).data, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        logger.error(f"Error generating forecast: {e}")
        return Response({"error": str(e)}, status=500)


@api_view(['GET'])
def health_view(request):
    return Response({"status": "solar_forecaster healthy"})
