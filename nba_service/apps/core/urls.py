"""Core URL configuration — health check."""

from django.urls import path

from apps.core.views import HealthCheckView

urlpatterns = [
    path("", HealthCheckView.as_view(), name="health-check"),
]
