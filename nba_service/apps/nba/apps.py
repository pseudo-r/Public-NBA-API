"""NBA app configuration."""

from django.apps import AppConfig


class NBAConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.nba"
    verbose_name = "NBA"
