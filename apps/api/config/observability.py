import json
import logging
import time
import uuid
from datetime import UTC, datetime

from django.conf import settings
from django.http import JsonResponse

logger = logging.getLogger("dotick.http")


class JsonFormatter(logging.Formatter):
    """Explicit allowlist: no arbitrary message, exception, body, or credentials."""

    def format(self, record):
        return json.dumps(
            {
                "timestamp": datetime.fromtimestamp(record.created, UTC).isoformat(),
                "level": record.levelname,
                "service": "dotick-api",
                "event": getattr(record, "event", "application_log"),
                **{
                    key: getattr(record, key)
                    for key in ("request_id", "route", "status", "duration_ms")
                    if hasattr(record, key)
                },
            }
        )


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.request_id = str(uuid.uuid4())
        started = time.perf_counter()
        try:
            size = int(request.META.get("CONTENT_LENGTH") or 0)
        except ValueError:
            size = settings.DATA_UPLOAD_MAX_MEMORY_SIZE + 1
        if size > settings.DATA_UPLOAD_MAX_MEMORY_SIZE:
            response = JsonResponse({"error": {"code": "payload_too_large"}}, status=413)
        else:
            response = self.get_response(request)
        response["X-Request-ID"] = request.request_id
        response["Cache-Control"] = "no-store"
        match = request.resolver_match
        logger.info(
            "http_request",
            extra={
                "event": "http_request",
                "request_id": request.request_id,
                "route": str(match.route) if match else "unmatched",
                "status": response.status_code,
                "duration_ms": round((time.perf_counter() - started) * 1000, 2),
            },
        )
        return response
