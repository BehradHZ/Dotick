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
