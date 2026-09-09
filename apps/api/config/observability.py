import json
import logging
import time
from datetime import UTC, datetime

logger = logging.getLogger("dotick.http")

LOG_FIELD_ALLOWLIST = (
    "timestamp",
    "level",
    "service",
    "event",
    "request_id",
    "method",
    "route",
    "status",
    "duration_ms",
)


class JsonFormatter(logging.Formatter):
    """Emit only explicitly approved structured log fields."""

    def format(self, record):
        candidates = {
            "timestamp": datetime.fromtimestamp(
                record.created,
                UTC,
            ).isoformat(),
            "level": record.levelname,
            "service": "dotick-api",
            "event": getattr(record, "event", "application_log"),
        }

        for field in ("request_id", "method", "route", "status", "duration_ms"):
            if hasattr(record, field):
                candidates[field] = getattr(record, field)

        payload = {field: candidates[field] for field in LOG_FIELD_ALLOWLIST if field in candidates}

        return json.dumps(payload)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        started = time.perf_counter()

        response = self.get_response(request)

        match = getattr(request, "resolver_match", None)

        logger.info(
            "http_request",
            extra={
                "event": "http_request",
                "request_id": request.request_id,
                "method": request.method,
                "route": str(match.route) if match else "unmatched",
                "status": response.status_code,
                "duration_ms": round(
                    (time.perf_counter() - started) * 1000,
                    2,
                ),
            },
        )

        return response
