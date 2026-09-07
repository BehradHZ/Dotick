from django.http import JsonResponse
from rest_framework.views import exception_handler


def api_exception_handler(error, context):
    response = exception_handler(error, context)
    if response is not None:
        codes = error.get_codes() if hasattr(error, "get_codes") else None
        code = codes if isinstance(codes, str) else "validation_error"
        response.data = {"error": {"code": code, "details": response.data}}
    return response


def bad_request(request, exception):
    return JsonResponse({"error": {"code": "bad_request"}}, status=400)


def not_found(request, exception):
    return JsonResponse({"error": {"code": "not_found"}}, status=404)


def server_error(request):
    return JsonResponse({"error": {"code": "internal_error"}}, status=500)
