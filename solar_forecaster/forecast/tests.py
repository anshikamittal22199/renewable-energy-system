from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

class ForecastTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_valid_forecast(self):
        data = {"location": "Delhi", "date": "2025-11-10", "sun_intensity_factor": 12, "daylight_hours": 8}
        res = self.client.post("/forecast/", data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn("forecast_kwh", res.data)

    def test_invalid_date(self):
        data = {"location": "Delhi", "date": "not-a-date", "sun_intensity_factor": 12, "daylight_hours": 8}
        res = self.client.post("/forecast/", data, format='json')
        self.assertEqual(res.status_code, 400)
