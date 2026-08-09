"""
Stage 2 — DRF serializers (ROADMAP.md §6 Stage 2: "CRUD endpoints for
Task, Event, and Routine").

Each serializer exposes the model's stored fields plus its computed
status (effective_status for Task, status for Event/Routine) as a
read-only field, so API consumers get the full six/three/four-state
picture (§4.3, §4.5, §4.6) without recomputing it client-side.
"""

from rest_framework import serializers

from core.models import Event, Routine, Task


class TaskSerializer(serializers.ModelSerializer):
    effective_status = serializers.CharField(read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "user_status",
            "due_date",
            "deadline",
            "deadline_enabled",
            "grace_period",
            "effective_status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class EventSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "start_time",
            "end_time",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class RoutineSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Routine
        fields = [
            "id",
            "title",
            "description",
            "user_status",
            "period_end",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
