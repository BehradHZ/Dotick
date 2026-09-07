from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from dotick.tasks import application


class TaskCreateInput(serializers.Serializer):
    title = serializers.CharField(max_length=240, trim_whitespace=True)
    operation_id = serializers.UUIDField()
    column_id = serializers.UUIDField(required=False, allow_null=True)

    def to_internal_value(self, data):
        if isinstance(data, dict) and set(data) - set(self.fields):
            raise serializers.ValidationError({"input": "Unknown fields are not accepted."})
        return super().to_internal_value(data)


class TaskUpdateInput(serializers.Serializer):
    version = serializers.IntegerField(min_value=1)
    title = serializers.CharField(max_length=240, trim_whitespace=True, required=False)
    status = serializers.ChoiceField(choices=["todo", "done", "wont_do"], required=False)
    column_id = serializers.UUIDField(required=False)

    def to_internal_value(self, data):
        if isinstance(data, dict) and set(data) - set(self.fields):
            raise serializers.ValidationError({"input": "Unknown fields are not accepted."})
        return super().to_internal_value(data)

    def validate(self, attrs):
        if set(attrs) == {"version"}:
            raise serializers.ValidationError("Provide at least one task change.")
        return attrs


class VersionInput(serializers.Serializer):
    version = serializers.IntegerField(min_value=1)

    def to_internal_value(self, data):
        if isinstance(data, dict) and set(data) - set(self.fields):
            raise serializers.ValidationError({"input": "Unknown fields are not accepted."})
        return super().to_internal_value(data)


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


class TrashedTaskOutput(TaskOutput):
    is_trashed = serializers.BooleanField()
    trashed_at = serializers.DateTimeField()


class TaskList(APIView):
    def get(self, request):
        raw_column_id = request.query_params.get("column_id")
        column_id = None
        if raw_column_id is not None:
            field = serializers.UUIDField()
            column_id = field.run_validation(raw_column_id)
        rows = application.list_tasks(actor_id=request.user.id, column_id=column_id)
        return Response({"results": TaskOutput(rows, many=True).data})

    def post(self, request):
        data = TaskCreateInput(data=request.data)
        data.is_valid(raise_exception=True)
        item, created = application.create_task(actor_id=request.user.id, **data.validated_data)
        return Response(TaskOutput(item).data, status=201 if created else 200)


class TaskDetail(APIView):
    def get(self, request, task_id):
        item = application.get_task(actor_id=request.user.id, task_id=task_id)
        return Response(TaskOutput(item).data)

    def patch(self, request, task_id):
        data = TaskUpdateInput(data=request.data)
        data.is_valid(raise_exception=True)
        item = application.update_task(
            actor_id=request.user.id,
            task_id=task_id,
            **data.validated_data,
        )
        return Response(TaskOutput(item).data)

    def delete(self, request, task_id):
        value = request.headers.get("If-Match", "")
        try:
            version = int(value.strip('"'))
        except ValueError as error:
            raise ValidationError(
                {"if_match": ["Use the current positive integer version."]}
            ) from error
        if version < 1:
            raise ValidationError({"if_match": ["Use the current positive integer version."]})
        application.delete_task(actor_id=request.user.id, task_id=task_id, version=version)
        return Response(status=204)


class TrashTasks(APIView):
    def get(self, request):
        rows = application.list_trashed_tasks(actor_id=request.user.id)
        return Response({"results": TrashedTaskOutput(rows, many=True).data})


class TaskRestore(APIView):
    def post(self, request, task_id):
        data = VersionInput(data=request.data)
        data.is_valid(raise_exception=True)
        item = application.restore_task(
            actor_id=request.user.id,
            task_id=task_id,
            **data.validated_data,
        )
        return Response(TaskOutput(item).data)
