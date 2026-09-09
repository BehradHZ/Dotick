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
            {
                "error": {
                    "code": "internal_error",
                }
            },
            status=500,
        )

    response.data = {
        "error": {
            "code": _get_error_code(error, response.status_code),
            "details": response.data,
        }
    }

    return response


def bad_request(request, exception):
    return JsonResponse(
        {
            "error": {
                "code": "bad_request",
            }
        },
        status=400,
    )


def not_found(request, exception):
    return JsonResponse(
        {
            "error": {
                "code": "not_found",
            }
        },
        status=404,
    )


def server_error(request):
    return JsonResponse(
        {
            "error": {
                "code": "internal_error",
            }
        },
        status=500,
    )
