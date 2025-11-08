from django.urls import path
from .views import forecast_view, health_view

urlpatterns = [
    path('forecast/', forecast_view),
    path('health/', health_view),
]
