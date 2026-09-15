import re

from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from dotick.tasks import application
from dotick.tasks.models import Task


class StrictInput(serializers.Serializer):
    def to_internal_value(self, data):
        if isinstance(data, dict) and set(data) - set(self.fields):
            raise serializers.ValidationError({"input": "Unknown fields are not accepted."})
        return super().to_internal_value(data)


class TaskCreateInput(StrictInput):
    title = serializers.CharField(max_length=240, trim_whitespace=True)
    operation_id = serializers.UUIDField()
    column_id = serializers.UUIDField(required=False, allow_null=True)


class TaskUpdateInput(StrictInput):
    version = serializers.IntegerField(min_value=1)
    title = serializers.CharField(max_length=240, trim_whitespace=True, required=False)
    status = serializers.ChoiceField(choices=Task.Status.values, required=False)
    column_id = serializers.UUIDField(required=False)

    def validate(self, attrs):
        if set(attrs) == {"version"}:
            raise serializers.ValidationError("Provide at least one Task change.")
        return attrs


class ItemSourceOutput(serializers.Serializer):
    platform = serializers.CharField()
    external_account_id = serializers.CharField(allow_null=True)
    external_id = serializers.CharField(allow_null=True)


class TaskOutput(serializers.Serializer):
    id = serializers.UUIDField()
    title = serializers.CharField()
    status = serializers.CharField(source="task.status")
    version = serializers.IntegerField()
    column_id = serializers.UUIDField()
    owner_user_id = serializers.UUIDField(source="owner_id")
    created_by_user_id = serializers.UUIDField(source="created_by_id")
    source = ItemSourceOutput()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class Tasks(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rows = application.list_tasks(actor_id=request.user.id)
        return Response({"results": TaskOutput(rows, many=True).data})

    def post(self, request):
        serializer = TaskCreateInput(data=request.data)
        serializer.is_valid(raise_exception=True)
        item, created = application.create_task(
            actor_id=request.user.id,
            **serializer.validated_data,
        )
        return Response(TaskOutput(item).data, status=201 if created else 200)


class TaskDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, task_id):
        item = application.get_task(actor_id=request.user.id, task_id=task_id)
        return Response(TaskOutput(item).data)

    def patch(self, request, task_id):
        serializer = TaskUpdateInput(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = application.update_task(
            actor_id=request.user.id,
            task_id=task_id,
            **serializer.validated_data,
        )
        return Response(TaskOutput(item).data)

    def delete(self, request, task_id):
        value = request.headers.get("If-Match", "").strip()
        if re.fullmatch(r'(?:[1-9][0-9]*|"[1-9][0-9]*")', value) is None:
            raise serializers.ValidationError(
                {"if_match": ["Use the current positive integer version."]}
            )
        application.delete_task(
            actor_id=request.user.id,
            task_id=task_id,
            version=int(value.strip('"')),
        )
        return Response(status=204)
