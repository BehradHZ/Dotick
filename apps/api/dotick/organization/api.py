from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from dotick.identity.validators import validate_iana_timezone
from dotick.organization import application


class BootstrapInput(serializers.Serializer):
    timezone = serializers.CharField(
        max_length=64,
        validators=[validate_iana_timezone],
    )

    def to_internal_value(self, data):
        if isinstance(data, dict) and set(data) - set(self.fields):
            raise serializers.ValidationError({"input": "Unknown fields are not accepted."})
        return super().to_internal_value(data)


class AccountBootstrap(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = BootstrapInput(data=request.data)
        serializer.is_valid(raise_exception=True)
        preferences, inbox, default_column = application.bootstrap_account(
            actor_id=request.user.id,
            **serializer.validated_data,
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


class StrictInput(serializers.Serializer):
    def to_internal_value(self, data):
        if isinstance(data, dict) and set(data) - set(self.fields):
            raise serializers.ValidationError({"input": "Unknown fields are not accepted."})
        return super().to_internal_value(data)


class FolderCreateInput(StrictInput):
    title = serializers.CharField(max_length=240, trim_whitespace=True)


class FolderUpdateInput(StrictInput):
    title = serializers.CharField(
        max_length=240,
        trim_whitespace=True,
        required=False,
    )
    position = serializers.IntegerField(min_value=0, required=False)

    def validate(self, attrs):
        if not attrs:
            raise serializers.ValidationError("Provide at least one Folder change.")
        return attrs


def _serialize_folder(row):
    return {
        "id": row.id,
        "title": row.title,
        "position": row.position,
        "is_trashed": row.is_trashed,
        "trashed_at": row.trashed_at,
    }


class Folders(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rows = application.list_folders(actor_id=request.user.id)
        return Response({"results": [_serialize_folder(row) for row in rows]})

    def post(self, request):
        serializer = FolderCreateInput(data=request.data)
        serializer.is_valid(raise_exception=True)
        row = application.create_folder(
            owner=request.user,
            **serializer.validated_data,
        )
        return Response(_serialize_folder(row), status=201)


class FolderDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, folder_id):
        row = application.get_folder(actor_id=request.user.id, folder_id=folder_id)
        return Response(_serialize_folder(row))

    def patch(self, request, folder_id):
        serializer = FolderUpdateInput(data=request.data)
        serializer.is_valid(raise_exception=True)
        row = application.update_folder(
            actor_id=request.user.id,
            folder_id=folder_id,
            **serializer.validated_data,
        )
        return Response(_serialize_folder(row))
