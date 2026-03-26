"""Celery application configuration for nba_service."""

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("nba_service")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
