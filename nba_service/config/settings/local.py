"""Local development settings."""

from config.settings.base import *  # noqa: F401, F403

DEBUG = True
ALLOWED_HOSTS = ["*"]
CORS_ALLOW_ALL_ORIGINS = True

# Use console email backend in dev
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
