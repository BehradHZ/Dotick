from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from dotick.identity import application


class StrictSerializer(serializers.Serializer):
    def to_internal_value(self, data):
        if isinstance(data, dict) and set(data) - set(self.fields):
            raise serializers.ValidationError({"input": "Unknown fields are not accepted."})
        return super().to_internal_value(data)


class RegisterInput(StrictSerializer):
    email = serializers.EmailField(max_length=254)
    password = serializers.CharField(max_length=128, trim_whitespace=False, write_only=True)
    handle = serializers.RegexField(r"^[A-Za-z0-9_]{3,30}$", max_length=30)
    display_name = serializers.CharField(max_length=120, trim_whitespace=True)

    def validate(self, attrs):
        candidate = get_user_model()(
            email=attrs["email"],
            handle=attrs["handle"],
            display_name=attrs["display_name"],
        )
        validate_password(attrs["password"], user=candidate)
        return attrs


class VerifyEmailInput(StrictSerializer):
    email = serializers.EmailField(max_length=254)
    code = serializers.RegexField(r"^\d{6}$", max_length=6)


class TokenInput(StrictSerializer):
    email = serializers.EmailField(max_length=254)
    password = serializers.CharField(max_length=128, trim_whitespace=False, write_only=True)


class RefreshInput(StrictSerializer):
    refresh = serializers.CharField(max_length=4096, trim_whitespace=False, write_only=True)


class EmailInput(StrictSerializer):
    email = serializers.EmailField(max_length=254)


class PasswordResetConfirmInput(VerifyEmailInput):
    password = serializers.CharField(max_length=128, trim_whitespace=False, write_only=True)


class SessionOutput(serializers.Serializer):
    id = serializers.UUIDField()
    user_agent = serializers.CharField()
    created_at = serializers.DateTimeField()
    last_seen_at = serializers.DateTimeField()
    current = serializers.BooleanField()


class PublicIdentityView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]


class Register(PublicIdentityView):
    def post(self, request):
        data = RegisterInput(data=request.data)
        data.is_valid(raise_exception=True)
        application.register(**data.validated_data)
        return Response({"status": "accepted"}, status=202)


class VerifyEmail(PublicIdentityView):
    def post(self, request):
        data = VerifyEmailInput(data=request.data)
        data.is_valid(raise_exception=True)
        application.verify_email(**data.validated_data)
        return Response(status=204)


class Token(PublicIdentityView):
    def post(self, request):
        data = TokenInput(data=request.data)
        data.is_valid(raise_exception=True)
        return Response(
            application.create_token_pair(
                **data.validated_data,
                user_agent=request.META.get("HTTP_USER_AGENT", ""),
            )
        )


class Refresh(PublicIdentityView):
    def post(self, request):
        data = RefreshInput(data=request.data)
        data.is_valid(raise_exception=True)
        return Response(
            application.rotate_refresh_token(encoded_token=data.validated_data["refresh"])
        )


class Sessions(APIView):
    def get(self, request):
        rows = application.list_sessions(
            user_id=request.user.id,
            current_session_id=request.auth_session.id,
        )
        return Response({"results": SessionOutput(rows, many=True).data})

    def delete(self, request):
        application.revoke_all_sessions(user_id=request.user.id)
        return Response(status=204)


class SessionDetail(APIView):
    def delete(self, request, session_id):
        application.revoke_session(user_id=request.user.id, session_id=session_id)
        return Response(status=204)


class Logout(APIView):
    def post(self, request):
        application.revoke_session(
            user_id=request.user.id,
            session_id=request.auth_session.id,
        )
        return Response(status=204)


class PasswordResetRequest(PublicIdentityView):
    def post(self, request):
        data = EmailInput(data=request.data)
        data.is_valid(raise_exception=True)
        application.request_password_reset(**data.validated_data)
        return Response({"status": "accepted"}, status=202)


class PasswordResetConfirm(PublicIdentityView):
    def post(self, request):
        data = PasswordResetConfirmInput(data=request.data)
        data.is_valid(raise_exception=True)
        application.reset_password(**data.validated_data)
        return Response(status=204)


class ResendEmailVerification(PublicIdentityView):
    def post(self, request):
        data = EmailInput(data=request.data)
        data.is_valid(raise_exception=True)
        application.resend_email_verification(**data.validated_data)
        return Response({"status": "accepted"}, status=202)
