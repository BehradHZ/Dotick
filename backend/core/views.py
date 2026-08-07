from django.db import DatabaseError, connection
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def health_check(request):
    """
    Stage 1 smoke-test endpoint.

    Proves the full path (browser -> Django -> PostgreSQL -> response)
    works, per ROADMAP.md §6 Stage 1. Runs a trivial query against the
    database so "status": "ok" reflects a real, live DB connection
    rather than a hardcoded value. If the database is unreachable, this
    surfaces as a 500 rather than a false "ok".
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except DatabaseError:
        return Response({"status": "error"}, status=500)

    return Response({"status": "ok"})
