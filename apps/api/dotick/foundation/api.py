from django.conf import settings
from django.http import Http404
from rest_framework import serializers
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from dotick.foundation import application


class CheckpointInput(serializers.Serializer):
    text = serializers.CharField(max_length=240, trim_whitespace=True)

    def to_internal_value(self, data):
        if isinstance(data, dict) and set(data) - set(self.fields):
            raise serializers.ValidationError({"input": "Unknown fields are not accepted."})

        return super().to_internal_value(data)


class CheckpointOutput(serializers.Serializer):
    id = serializers.UUIDField()
    text = serializers.CharField()
    created_at = serializers.DateTimeField()


class FoundationView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def initial(self, request, *args, **kwargs):
        if not settings.FOUNDATION_ENABLED:
            raise Http404
        return super().initial(request, *args, **kwargs)


class CheckpointList(FoundationView):
    def get(self, request):
        rows = application.list_checkpoints(actor_id=request.user.id)
        return Response({"results": CheckpointOutput(rows, many=True).data})

    def post(self, request):
        serializer = CheckpointInput(data=request.data)
        serializer.is_valid(raise_exception=True)

        row = application.create_checkpoint(
            actor_id=request.user.id,
            **serializer.validated_data,
        )

        return Response(
            CheckpointOutput(row).data,
            status=201,
        )


class CheckpointDetail(FoundationView):
    def get(self, request, checkpoint_id):
        row = application.get_checkpoint(
            actor_id=request.user.id,
            checkpoint_id=checkpoint_id,
        )
        return Response(CheckpointOutput(row).data)
