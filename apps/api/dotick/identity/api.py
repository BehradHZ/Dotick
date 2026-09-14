from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from dotick.identity import application
from dotick.identity.models import AuthSession
from dotick.identity.sessions import revoke_all_sessions, revoke_session


class StrictSerializer(serializers.Serializer):
    def to_internal_value(self, data):
        if isinstance(data, dict) and set(data) - set(self.fields):
            raise serializers.ValidationError({"input": "Unknown fields are not accepted."})
        return super().to_internal_value(data)


class RegisterInput(StrictSerializer):
    email = serializers.EmailField(max_length=254)
    password = serializers.CharField(
        max_length=128,
        trim_whitespace=False,
        write_only=True,
    )
    handle = serializers.RegexField(
        r"^[A-Za-z0-9_]{3,30}$",
        max_length=30,
    )
    display_name = serializers.CharField(
        max_length=120,
        trim_whitespace=True,
    )

    def validate(self, attrs):
        candidate = get_user_model()(
            email=attrs["email"],
            handle=attrs["handle"],
            display_name=attrs["display_name"],
        )
        try:
            validate_password(attrs["password"], user=candidate)
        except DjangoValidationError as error:
            raise serializers.ValidationError({"password": error.messages}) from error
        return attrs


class EmailInput(StrictSerializer):
    email = serializers.EmailField(max_length=254)


class VerifyEmailInput(EmailInput):
    code = serializers.RegexField(r"^[0-9]{6}$", max_length=6)


class TokenInput(EmailInput):
    password = serializers.CharField(
        max_length=128,
        trim_whitespace=False,
        write_only=True,
    )


class RefreshInput(StrictSerializer):
    refresh = serializers.CharField(
        max_length=4096,
        trim_whitespace=False,
        write_only=True,
    )


class AuthSessionOutput(serializers.ModelSerializer):
    current = serializers.SerializerMethodField()

    class Meta:
        model = AuthSession
        fields = ["id", "user_agent", "created_at", "last_seen_at", "current"]

    def get_current(self, session):
        return session.id == self.context["current_session_id"]


class PublicIdentityView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]


class AuthenticatedIdentityView(APIView):
    permission_classes = [IsAuthenticated]


class Register(PublicIdentityView):
    def post(self, request):
        serializer = RegisterInput(data=request.data)
        serializer.is_valid(raise_exception=True)
        application.register_account(**serializer.validated_data)
        return Response({"status": "accepted"}, status=202)


class ResendEmailVerification(PublicIdentityView):
    def post(self, request):
        serializer = EmailInput(data=request.data)
        serializer.is_valid(raise_exception=True)
        application.resend_email_verification(**serializer.validated_data)
        return Response({"status": "accepted"}, status=202)


class VerifyEmail(PublicIdentityView):
    def post(self, request):
        serializer = VerifyEmailInput(data=request.data)
        serializer.is_valid(raise_exception=True)
        application.verify_email(**serializer.validated_data)
        return Response(status=204)


class RequestPasswordReset(PublicIdentityView):
    def post(self, request):
        serializer = EmailInput(data=request.data)
        serializer.is_valid(raise_exception=True)
        application.request_password_reset(**serializer.validated_data)
        return Response({"status": "accepted"}, status=202)


class CreateTokenPair(PublicIdentityView):
    def post(self, request):
        serializer = TokenInput(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token_pair = application.login_with_password(
            **serializer.validated_data,
            user_agent=request.META.get("HTTP_USER_AGENT", ""),
        )
        return Response(
            {
                "access": token_pair.access,
                "refresh": token_pair.refresh,
                "user": {
                    "email": user.email,
                    "handle": user.handle,
                    "display_name": user.display_name,
                },
            }
        )


class RotateRefreshToken(PublicIdentityView):
    def post(self, request):
        serializer = RefreshInput(data=request.data)
        serializer.is_valid(raise_exception=True)
        token_pair = application.refresh_session(**serializer.validated_data)
        return Response(
            {
                "access": token_pair.access,
                "refresh": token_pair.refresh,
            }
        )


class LogoutCurrentSession(AuthenticatedIdentityView):
    def post(self, request):
        revoke_session(session=request.auth_session)
        return Response(status=204)


class ActiveSessions(AuthenticatedIdentityView):
    def get(self, request):
        sessions = AuthSession.objects.filter(
            user=request.user,
            revoked_at__isnull=True,
        ).order_by("-last_seen_at", "-created_at")
        serializer = AuthSessionOutput(
            sessions,
            many=True,
            context={"current_session_id": request.auth_session.id},
        )
        return Response({"results": serializer.data})

    def delete(self, request):
        revoke_all_sessions(user=request.user)
        return Response(status=204)


class RevokeOwnedSession(AuthenticatedIdentityView):
    def delete(self, request, session_id):
        session = get_object_or_404(
            AuthSession,
            id=session_id,
            user=request.user,
        )
        revoke_session(session=session)
        return Response(status=204)
