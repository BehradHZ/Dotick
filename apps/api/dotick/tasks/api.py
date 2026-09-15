from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from dotick.tasks import application


class StrictInput(serializers.Serializer):
    def to_internal_value(self, data):
        if isinstance(data, dict) and set(data) - set(self.fields):
            raise serializers.ValidationError({"input": "Unknown fields are not accepted."})
        return super().to_internal_value(data)


class TaskCreateInput(StrictInput):
    title = serializers.CharField(max_length=240, trim_whitespace=True)
    operation_id = serializers.UUIDField()
    column_id = serializers.UUIDField(required=False, allow_null=True)


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

    def post(self, request):
        serializer = TaskCreateInput(data=request.data)
        serializer.is_valid(raise_exception=True)
        item, created = application.create_task(
            actor_id=request.user.id,
            **serializer.validated_data,
        )
        return Response(TaskOutput(item).data, status=201 if created else 200)
