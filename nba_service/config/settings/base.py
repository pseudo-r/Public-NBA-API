"""Base settings for nba_service project."""

import os
from pathlib import Path
from typing import Any

import environ
import structlog

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Initialize django-environ
env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
    CORS_ALLOWED_ORIGINS=(list, []),
)

# Read .env file if it exists
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY", default="django-insecure-nba-change-me-in-production")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS: list[str] = env.list("ALLOWED_HOSTS", default=[])


# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "django_filters",
    "corsheaders",
    "drf_spectacular",
]

LOCAL_APPS = [
    "apps.core",
    "apps.nba",
    "apps.ingest",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.core.middleware.RequestIDMiddleware",
    "apps.core.middleware.StructuredLoggingMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
DATABASES = {
    "default": env.db("DATABASE_URL", default="sqlite:///db.sqlite3"),
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Static files
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Django REST Framework
REST_FRAMEWORK: dict[str, Any] = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 25,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "EXCEPTION_HANDLER": "apps.core.exceptions.custom_exception_handler",
}


# DRF Spectacular (OpenAPI/Swagger)
SPECTACULAR_SETTINGS = {
    "TITLE": "NBA Stats Service API",
    "DESCRIPTION": (
        "Production-ready REST API for NBA Stats data — "
        "ingests from stats.nba.com and exposes structured endpoints for "
        "games, players, teams, standings, and season statistics."
    ),
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
    "SCHEMA_PATH_PREFIX": "/api/v1/",
    "TAGS": [
        {"name": "Teams", "description": "NBA team data"},
        {"name": "Players", "description": "NBA player data"},
        {"name": "Games", "description": "Game / scoreboard data"},
        {"name": "Standings", "description": "League standings"},
        {"name": "Player Stats", "description": "Player season statistics"},
        {"name": "Team Stats", "description": "Team season statistics"},
        {"name": "Game Logs", "description": "Player game logs"},
        {"name": "Ingest", "description": "Data ingestion trigger endpoints"},
        {"name": "Health", "description": "Health check"},
    ],
}


# CORS settings
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])
CORS_ALLOW_ALL_ORIGINS = env.bool("CORS_ALLOW_ALL_ORIGINS", default=False)


# Cache settings
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}


# Celery settings
CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="redis://localhost:6379/0")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND", default="redis://localhost:6379/0")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes
CELERY_BEAT_SCHEDULE = {
    # Scoreboard — every 30 minutes during season hours
    "refresh-nba-scoreboard-30min": {
        "task": "apps.ingest.tasks.refresh_scoreboard_today_task",
        "schedule": 1800.0,  # Every 30 minutes
    },
    # Standings — refreshed daily
    "refresh-nba-standings-daily": {
        "task": "apps.ingest.tasks.refresh_standings_task",
        "schedule": 86400.0,
        "args": ("2024-25", "Regular Season"),
    },
    # League player stats — refreshed daily (Base, PerGame)
    "refresh-nba-player-stats-daily": {
        "task": "apps.ingest.tasks.refresh_player_stats_task",
        "schedule": 86400.0,
        "args": ("2024-25", "Regular Season", "Base", "PerGame"),
    },
    # League team stats — refreshed daily (Advanced, PerGame)
    "refresh-nba-team-stats-daily": {
        "task": "apps.ingest.tasks.refresh_team_stats_task",
        "schedule": 86400.0,
        "args": ("2024-25", "Regular Season", "Advanced", "PerGame"),
    },
    # Players and teams roster — weekly
    "refresh-nba-players-weekly": {
        "task": "apps.ingest.tasks.refresh_players_task",
        "schedule": 86400.0 * 7,
        "args": ("2024-25",),
    },
    "refresh-nba-teams-weekly": {
        "task": "apps.ingest.tasks.refresh_teams_task",
        "schedule": 86400.0 * 7,
    },
}


# NBA Stats API Client settings
NBA_CLIENT: dict[str, Any] = {
    "BASE_URL": env("NBA_STATS_BASE_URL", default="https://stats.nba.com/stats"),
    "REFERER": env("NBA_STATS_REFERER", default="https://www.nba.com/"),
    "ORIGIN": env("NBA_STATS_ORIGIN", default="https://www.nba.com"),
    "ORIGIN_HEADER": env("NBA_STATS_ORIGIN_HEADER", default="stats"),
    "TOKEN_HEADER": env("NBA_STATS_TOKEN_HEADER", default="true"),
    "TIMEOUT": env.float("NBA_TIMEOUT", default=30.0),
    "MAX_RETRIES": env.int("NBA_MAX_RETRIES", default=3),
    "RETRY_BACKOFF": env.float("NBA_RETRY_BACKOFF", default=2.0),
    "USER_AGENT": env(
        "NBA_USER_AGENT",
        default=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        ),
    ),
}


# Structured logging configuration
LOGGING_LEVEL = env("LOGGING_LEVEL", default="INFO")

timestamper = structlog.processors.TimeStamper(fmt="iso")

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        timestamper,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
            "foreign_pre_chain": [
                structlog.contextvars.merge_contextvars,
                structlog.stdlib.add_log_level,
                structlog.stdlib.add_logger_name,
                timestamper,
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
            ],
        },
        "console": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.dev.ConsoleRenderer(),
            "foreign_pre_chain": [
                structlog.contextvars.merge_contextvars,
                structlog.stdlib.add_log_level,
                structlog.stdlib.add_logger_name,
                timestamper,
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
            ],
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
        "json": {
            "class": "logging.StreamHandler",
            "formatter": "json",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": LOGGING_LEVEL,
    },
    "loggers": {
        "django": {"handlers": ["console"], "level": LOGGING_LEVEL, "propagate": False},
        "apps": {"handlers": ["console"], "level": LOGGING_LEVEL, "propagate": False},
        "clients": {"handlers": ["console"], "level": LOGGING_LEVEL, "propagate": False},
        "celery": {"handlers": ["console"], "level": LOGGING_LEVEL, "propagate": False},
    },
}
