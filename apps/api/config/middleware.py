import uuid

from django.conf import settings
from django.core.exceptions import RequestDataTooBig
from django.http import JsonResponse, UnreadablePostError

from config.errors import _error_payload

_BODY_METHODS = {"POST", "PUT", "PATCH", "DELETE"}


class JsonRequestBoundaryMiddleware:
    """Enforce the JSON transport boundary for versioned product APIs."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/api/v1/") and request.method in _BODY_METHODS:
            rejection = self._validate(request)
            if rejection is not None:
                return rejection

        return self.get_response(request)

    def _validate(self, request):
        maximum = settings.API_MAX_JSON_BODY_BYTES
        content_length = request.META.get("CONTENT_LENGTH")

        if content_length:
            try:
                declared_length = int(content_length)
            except TypeError, ValueError:
                return self._malformed_length()

            if declared_length < 0:
                return self._malformed_length()
            if declared_length > maximum:
                return self._payload_too_large()

        try:
            body = request.body
        except RequestDataTooBig, UnreadablePostError:
            return self._payload_too_large()

        if len(body) > maximum:
            return self._payload_too_large()

        if body:
            media_type = request.content_type.split(";", 1)[0].strip().lower()
            if media_type != "application/json":
                return JsonResponse(
                    _error_payload(
                        "unsupported_media_type",
                        {"detail": "Use application/json for API request bodies."},
                    ),
                    status=415,
                )

        return None

    @staticmethod
    def _malformed_length():
        return JsonResponse(
            _error_payload("bad_request", {"detail": "Malformed Content-Length header."}),
            status=400,
        )

    @staticmethod
    def _payload_too_large():
        return JsonResponse(
            _error_payload(
                "payload_too_large",
                {"detail": "Request body exceeds the 16 KiB limit."},
            ),
            status=413,
        )


class RequestIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.request_id = str(uuid.uuid4())

        response = self.get_response(request)

        response["X-Request-ID"] = request.request_id
        response["Cache-Control"] = "no-store"

        return response
