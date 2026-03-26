"""Custom exception handling for nba_service."""

from typing import Any

import structlog
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = structlog.get_logger(__name__)


class IngestionError(Exception):
    """Raised when a data ingestion operation fails."""


def custom_exception_handler(exc: Exception, context: dict[str, Any]) -> Response | None:
    """Custom DRF exception handler with structured logging."""
    response = exception_handler(exc, context)

    if response is not None:
        logger.warning(
            "api_error",
            status_code=response.status_code,
            detail=response.data,
            view=context.get("view").__class__.__name__ if context.get("view") else None,
        )
        # Wrap in consistent structure
        response.data = {
            "error": response.data,
            "status_code": response.status_code,
        }
    else:
        # Unhandled exception
        logger.exception("unhandled_api_exception", exc_type=type(exc).__name__)
        response = Response(
            {"error": "Internal server error", "status_code": 500},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return response
