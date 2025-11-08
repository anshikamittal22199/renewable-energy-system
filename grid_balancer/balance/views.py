from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests, logging

logger = logging.getLogger(__name__)
SOLAR_FORECASTER_URL = "http://solar_forecaster:8000/forecast/"

@api_view(['POST'])
def balance_view(request):
    try:
        data = request.data
        payload = {
            "location": data.get("location"),
            "date": data.get("date"),
            "sun_intensity_factor": data.get("sun_intensity_factor", 5),
            "daylight_hours": data.get("daylight_hours", 10)
        }

        try:
            res = requests.post(SOLAR_FORECASTER_URL, json=payload, timeout=5)
            res.raise_for_status()
            forecast_data = res.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"solar_forecaster unavailable: {e}")
            return Response({"error": "solar_forecaster service unavailable"}, status=503)

        forecast_kwh = forecast_data.get("forecast_kwh", 0)
        decision = "store" if forecast_kwh < 50 else "use" if forecast_kwh < 150 else "sell"

        logger.info(f"Decision for {payload['location']}: {decision} ({forecast_kwh} kWh)")
        return Response({"forecast_kwh": forecast_kwh, "decision": decision}, status=200)

    except Exception as e:
        logger.error(f"Error balancing grid: {e}")
        return Response({"error": str(e)}, status=500)


@api_view(['GET'])
def health_view(_):
    return Response({"status": "grid_balancer healthy"})
