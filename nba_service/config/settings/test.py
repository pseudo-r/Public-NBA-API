"""Test settings — uses SQLite in-memory for fast test runs."""

import os as _os

import environ as _environ

from config.settings.base import *  # noqa: E402, F401, F403

DEBUG = True
ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Use synchronous task execution in tests
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# Disable structlog for cleaner test output
LOGGING = {}

# Speed up password hashing in tests
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Opt into a separate test database explicitly; never use production DATABASE_URL.


if _os.environ.get("TEST_DATABASE_URL"):
    DATABASES = {"default": _environ.Env.db_url_config(_os.environ["TEST_DATABASE_URL"])}
MIDDLEWARE = [m for m in MIDDLEWARE if m != "whitenoise.middleware.WhiteNoiseMiddleware"]  # noqa: F405
INGEST_REQUIRE_STAFF = False
