from django.urls import path
from .views import balance_view, health_view

urlpatterns = [
    path('balance/', balance_view),
    path('health/', health_view),
]
