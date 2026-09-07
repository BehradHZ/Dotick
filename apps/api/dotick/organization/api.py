from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from dotick.organization import application


class BootstrapInput(serializers.Serializer):
    timezone = serializers.CharField(max_length=64)

    def to_internal_value(self, data):
        if isinstance(data, dict) and set(data) - set(self.fields):
            raise serializers.ValidationError({"input": "Unknown fields are not accepted."})
        return super().to_internal_value(data)

    def validate_timezone(self, value):
        try:
            ZoneInfo(value)
        except ZoneInfoNotFoundError as error:
            raise serializers.ValidationError("Use a valid IANA timezone identifier.") from error
        return value


class AccountBootstrap(APIView):
    def put(self, request):
        data = BootstrapInput(data=request.data)
        data.is_valid(raise_exception=True)
        preferences, inbox, default_column = application.bootstrap_account(
            actor_id=request.user.id,
            **data.validated_data,
        )
        return Response(
            {
                "preferences": {"timezone": preferences.timezone},
                "inbox": {
                    "id": inbox.id,
                    "title": inbox.title,
                    "is_inbox": inbox.is_inbox,
                    "default_column": {
                        "id": default_column.id,
                        "is_default": default_column.is_default,
                    },
                },
            }
        )


class ListInput(serializers.Serializer):
    title = serializers.CharField(max_length=240, trim_whitespace=True)
    folder_id = serializers.UUIDField(required=False, allow_null=True)

    def to_internal_value(self, data):
        if isinstance(data, dict) and set(data) - set(self.fields):
            raise serializers.ValidationError({"input": "Unknown fields are not accepted."})
        return super().to_internal_value(data)


class ListRenameInput(serializers.Serializer):
    title = serializers.CharField(max_length=240, trim_whitespace=True, required=False)
    folder_id = serializers.UUIDField(required=False, allow_null=True)
    position = serializers.IntegerField(min_value=0, required=False)

    def to_internal_value(self, data):
        if isinstance(data, dict) and set(data) - set(self.fields):
            raise serializers.ValidationError({"input": "Unknown fields are not accepted."})
        return super().to_internal_value(data)

    def validate(self, attrs):
        if not attrs:
            raise serializers.ValidationError("Provide at least one List change.")
        return attrs


class TitleInput(serializers.Serializer):
    title = serializers.CharField(max_length=240, trim_whitespace=True)

    def to_internal_value(self, data):
        if isinstance(data, dict) and set(data) - set(self.fields):
            raise serializers.ValidationError({"input": "Unknown fields are not accepted."})
        return super().to_internal_value(data)


class ContainerUpdateInput(serializers.Serializer):
    title = serializers.CharField(max_length=240, trim_whitespace=True, required=False)
    position = serializers.IntegerField(min_value=0, required=False)

    def to_internal_value(self, data):
        if isinstance(data, dict) and set(data) - set(self.fields):
            raise serializers.ValidationError({"input": "Unknown fields are not accepted."})
        return super().to_internal_value(data)

    def validate(self, attrs):
        if not attrs:
            raise serializers.ValidationError("Provide at least one container change.")
        return attrs


def _serialize_list(row):
    default_column = next(column for column in row.columns.all() if column.is_default)
    return {
        "id": row.id,
        "title": row.title,
        "folder_id": row.folder_id,
        "is_inbox": row.is_inbox,
        "position": row.position,
        "is_trashed": row.is_trashed,
        "trashed_at": row.trashed_at,
        "default_column": {"id": default_column.id, "is_default": True},
    }


def _serialize_folder(row):
    return {
        "id": row.id,
        "title": row.title,
        "position": row.position,
        "is_trashed": row.is_trashed,
        "trashed_at": row.trashed_at,
    }


def _serialize_column(row):
    return {
        "id": row.id,
        "list_id": row.list_id,
        "title": row.title,
        "position": row.position,
        "is_default": row.is_default,
    }


class Folders(APIView):
    def get(self, request):
        return Response(
            {
                "results": [
                    _serialize_folder(row)
                    for row in application.list_folders(actor_id=request.user.id)
                ]
            }
        )

    def post(self, request):
        data = TitleInput(data=request.data)
        data.is_valid(raise_exception=True)
        row = application.create_folder(actor_id=request.user.id, **data.validated_data)
        return Response(_serialize_folder(row), status=201)


class FolderDetail(APIView):
    def get(self, request, folder_id):
        row = application.get_folder(actor_id=request.user.id, folder_id=folder_id)
        return Response(_serialize_folder(row))

    def patch(self, request, folder_id):
        data = ContainerUpdateInput(data=request.data)
        data.is_valid(raise_exception=True)
        row = application.update_folder(
            actor_id=request.user.id,
            folder_id=folder_id,
            **data.validated_data,
        )
        return Response(_serialize_folder(row))

    def delete(self, request, folder_id):
        application.delete_folder(
            actor_id=request.user.id,
            folder_id=folder_id,
            item_resolution=request.query_params.get("items"),
        )
        return Response(status=204)


class Lists(APIView):
    def get(self, request):
        return Response(
            {
                "results": [
                    _serialize_list(row) for row in application.list_lists(actor_id=request.user.id)
                ]
            }
        )

    def post(self, request):
        data = ListInput(data=request.data)
        data.is_valid(raise_exception=True)
        row = application.create_list(actor_id=request.user.id, **data.validated_data)
        return Response(_serialize_list(row), status=201)


class ListDetail(APIView):
    def get(self, request, list_id):
        row = application.get_list(actor_id=request.user.id, list_id=list_id)
        return Response(_serialize_list(row))

    def patch(self, request, list_id):
        data = ListRenameInput(data=request.data)
        data.is_valid(raise_exception=True)
        row = application.update_list(
            actor_id=request.user.id,
            list_id=list_id,
            **data.validated_data,
        )
        return Response(_serialize_list(row))

    def delete(self, request, list_id):
        application.delete_list(
            actor_id=request.user.id,
            list_id=list_id,
            item_resolution=request.query_params.get("items"),
        )
        return Response(status=204)


class Columns(APIView):
    def get(self, request, list_id):
        rows = application.list_columns(actor_id=request.user.id, list_id=list_id)
        return Response({"results": [_serialize_column(row) for row in rows]})

    def post(self, request, list_id):
        data = TitleInput(data=request.data)
        data.is_valid(raise_exception=True)
        row = application.create_column(
            actor_id=request.user.id,
            list_id=list_id,
            **data.validated_data,
        )
        return Response(_serialize_column(row), status=201)


class ColumnDetail(APIView):
    def get(self, request, column_id):
        row = application.get_column(actor_id=request.user.id, column_id=column_id)
        return Response(_serialize_column(row))

    def patch(self, request, column_id):
        data = ContainerUpdateInput(data=request.data)
        data.is_valid(raise_exception=True)
        row = application.update_column(
            actor_id=request.user.id,
            column_id=column_id,
            **data.validated_data,
        )
        return Response(_serialize_column(row))

    def delete(self, request, column_id):
        application.delete_column(
            actor_id=request.user.id,
            column_id=column_id,
            item_resolution=request.query_params.get("items"),
        )
        return Response(status=204)


class TrashLists(APIView):
    def get(self, request):
        rows = application.list_trashed_lists(actor_id=request.user.id)
        return Response({"results": [_serialize_list(row) for row in rows]})


class ListRestore(APIView):
    def post(self, request, list_id):
        if request.data:
            raise serializers.ValidationError({"input": "Unknown fields are not accepted."})
        row = application.restore_list(actor_id=request.user.id, list_id=list_id)
        return Response(_serialize_list(row))


class TrashFolders(APIView):
    def get(self, request):
        rows = application.list_trashed_folders(actor_id=request.user.id)
        return Response({"results": [_serialize_folder(row) for row in rows]})


class FolderRestore(APIView):
    def post(self, request, folder_id):
        if request.data:
            raise serializers.ValidationError({"input": "Unknown fields are not accepted."})
        row = application.restore_folder(actor_id=request.user.id, folder_id=folder_id)
        return Response(_serialize_folder(row))
