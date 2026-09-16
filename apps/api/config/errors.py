from django.http import JsonResponse
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler

STATUS_ERROR_CODES = {
    400: "bad_request",
    401: "not_authenticated",
    403: "permission_denied",
    404: "not_found",
    405: "method_not_allowed",
    406: "not_acceptable",
    415: "unsupported_media_type",
    429: "throttled",
}


def _error_payload(code, details):
    return {
        "error": {
            "code": code,
            "details": details,
        }
    }


def _get_error_code(error, status_code):
    if isinstance(error, ValidationError):
        return "validation_error"

    if hasattr(error, "get_codes"):
        codes = error.get_codes()

        if isinstance(codes, str):
            return codes

    return STATUS_ERROR_CODES.get(status_code, "api_error")


def api_exception_handler(error, context):
    response = exception_handler(error, context)

    if response is None:
        return Response(
            _error_payload("internal_error", {}),
            status=500,
        )

    details = response.data
    if hasattr(error, "current"):
        details = {
            "message": response.data["detail"],
            "current": error.current,
        }

    response.data = _error_payload(
        _get_error_code(error, response.status_code),
        details,
    )

    return response


def bad_request(request, exception):
    return JsonResponse(
        _error_payload("bad_request", {}),
        status=400,
    )


def not_found(request, exception):
    return JsonResponse(
        _error_payload("not_found", {}),
        status=404,
    )


def server_error(request):
    return JsonResponse(
        _error_payload("internal_error", {}),
        status=500,
    )
