"""Core middleware: request ID injection and structured access logging."""

import uuid
from typing import Callable

import structlog
from django.http import HttpRequest, HttpResponse

logger = structlog.get_logger(__name__)


class RequestIDMiddleware:
    """Attach a unique request ID to every incoming request."""

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        request_id = str(uuid.uuid4())
        request.META["HTTP_X_REQUEST_ID"] = request_id
        structlog.contextvars.bind_contextvars(request_id=request_id)
        response = self.get_response(request)
        response["X-Request-ID"] = request_id
        structlog.contextvars.unbind_contextvars("request_id")
        return response


class StructuredLoggingMiddleware:
    """Log every request/response with structured logging."""

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)
        logger.info(
            "http_request",
            method=request.method,
            path=request.path,
            status_code=response.status_code,
            content_length=len(response.content) if hasattr(response, "content") else None,
        )
        return response
