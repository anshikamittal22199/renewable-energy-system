from django.urls import path
from .views import BalanceView, HealthCheckView

urlpatterns = [
    path('balance/', BalanceView.as_view(), name='balance'),
    path('health/', HealthCheckView.as_view(), name='grid_health'),
]
