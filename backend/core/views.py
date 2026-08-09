from django.db import DatabaseError, connection
from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from core.models import Event, Routine, Task
from core.serializers import EventSerializer, RoutineSerializer, TaskSerializer


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


class TaskViewSet(viewsets.ModelViewSet):
    """
    Stage 2 CRUD for Task (§6), plus the Postpone / Postpone All actions
    (§4.7) as the API surface the frontend's postpone buttons call.
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @action(detail=True, methods=["post"])
    def postpone(self, request, pk=None):
        task = self.get_object()
        task.postpone(action="postpone_single")
        return Response(self.get_serializer(task).data)

    @action(detail=False, methods=["post"])
    def postpone_all(self, request):
        count = Task.objects.postpone_all()
        return Response({"postponed_count": count})


class EventViewSet(viewsets.ModelViewSet):
    """Stage 2 CRUD for Event (§6, §4.5)."""

    queryset = Event.objects.all()
    serializer_class = EventSerializer


class RoutineViewSet(viewsets.ModelViewSet):
    """Stage 2 CRUD for Routine (§6, §4.6) — manually-created single
    occurrences; automatic generation from a recurrence rule is Stage 3."""

    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer
