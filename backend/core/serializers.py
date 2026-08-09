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

    def validate(self, attrs):
        """
        `due_date <= deadline` is implied by the domain model (§4.3's
        status ladder only makes sense in that order) but was never
        enforced — TESTING_PLAN.md §3.7 calls for rejecting the
        opposite case explicitly.

        Only checked while `deadline_enabled` is true: when it's off,
        the stored `deadline` value is inert by design (§4.3's note —
        preserved for later re-enabling, not an active constraint), so
        comparing against it here would incorrectly block updates to a
        task's `due_date` while its old deadline sits disabled.

        Falls back to each field's current value on a partial
        (PATCH) update, since either field may be omitted from attrs.
        """
        instance = self.instance
        deadline_enabled = attrs.get(
            "deadline_enabled",
            getattr(instance, "deadline_enabled", False),
        )
        if not deadline_enabled:
            return attrs

        due_date = attrs.get("due_date", getattr(instance, "due_date", None))
        deadline = attrs.get("deadline", getattr(instance, "deadline", None))

        if due_date is not None and deadline is not None and due_date > deadline:
            raise serializers.ValidationError(
                {"due_date": "due_date must not be after deadline."}
            )

        return attrs


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