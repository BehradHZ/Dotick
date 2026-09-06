from django.http import JsonResponse
from rest_framework.views import exception_handler


def api_exception_handler(error, context):
    response = exception_handler(error, context)
    if response is not None:
        response.data = {"error": {"code": str(response.status_code), "details": response.data}}
    return response


def bad_request(request, exception):
    return JsonResponse({"error": {"code": "bad_request"}}, status=400)


def not_found(request, exception):
    return JsonResponse({"error": {"code": "not_found"}}, status=404)


def server_error(request):
    return JsonResponse({"error": {"code": "internal_error"}}, status=500)
