from django.test import TestCase
from rest_framework.test import APIClient
from unittest.mock import patch
import requests

class BalanceTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch('requests.post')
    def test_balance_sell(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"forecast_kwh": 180}
        res = self.client.post("/balance/", {"location": "Delhi", "date": "2025-11-10"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["decision"], "sell")

    @patch('requests.post', side_effect=requests.exceptions.RequestException("Down"))
    def test_forecaster_down(self, mock_post):
        res = self.client.post("/balance/", {"location": "Delhi", "date": "2025-11-10"})
        self.assertEqual(res.status_code, 503)
