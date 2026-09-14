from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import APIException, PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from dotick.identity import application
from dotick.identity.models import AuthSession, PasskeyCredential
from dotick.identity.passkeys import (
    InvalidPasskeyChallenge,
    PasskeyCredentialConflict,
    begin_passkey_authentication,
    begin_passkey_registration,
    finish_passkey_authentication,
    finish_passkey_registration,
)
from dotick.identity.sessions import (
    RecentAuthenticationRequired,
    require_recent_authentication,
    revoke_all_sessions,
    revoke_session,
)


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


class PasswordResetConfirmInput(VerifyEmailInput):
    password = serializers.CharField(
        max_length=128,
        trim_whitespace=False,
        write_only=True,
    )

    def validate(self, attrs):
        candidate = get_user_model()(email=attrs["email"])
        try:
            validate_password(attrs["password"], user=candidate)
        except DjangoValidationError as error:
            raise serializers.ValidationError({"password": error.messages}) from error
        return attrs


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


class PasswordSetInput(StrictSerializer):
    password = serializers.CharField(
        max_length=128,
        trim_whitespace=False,
        write_only=True,
    )
    current_password = serializers.CharField(
        max_length=128,
        trim_whitespace=False,
        write_only=True,
        required=False,
    )

    def validate(self, attrs):
        try:
            validate_password(attrs["password"], user=self.context["request"].user)
        except DjangoValidationError as error:
            raise serializers.ValidationError({"password": error.messages}) from error
        return attrs


class GoogleCredentialInput(StrictSerializer):
    credential = serializers.CharField(
        max_length=8192,
        trim_whitespace=False,
        write_only=True,
    )


class PasskeyNameInput(StrictSerializer):
    name = serializers.CharField(max_length=120, trim_whitespace=True)


class EmptyInput(StrictSerializer):
    pass


class PasskeyCeremonyInput(StrictSerializer):
    challenge_id = serializers.UUIDField()
    credential = serializers.DictField()


class PasskeyOutput(serializers.ModelSerializer):
    class Meta:
        model = PasskeyCredential
        fields = ["id", "name", "device_type", "backed_up", "created_at", "last_used_at"]


class InvalidPasskeyCeremony(APIException):
    status_code = 400
    default_detail = "Passkey ceremony is invalid or expired."
    default_code = "invalid_passkey_ceremony"


class PasskeyConflict(APIException):
    status_code = 409
    default_detail = "Passkey credential already exists."
    default_code = "passkey_conflict"


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


class ConfirmPasswordReset(PublicIdentityView):
    def post(self, request):
        serializer = PasswordResetConfirmInput(data=request.data)
        serializer.is_valid(raise_exception=True)
        application.confirm_password_reset(**serializer.validated_data)
        return Response(status=204)


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


class SetPassword(AuthenticatedIdentityView):
    def put(self, request):
        serializer = PasswordSetInput(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        application.set_password(
            user=request.user,
            session=request.auth_session,
            password=serializer.validated_data["password"],
            current_password=serializer.validated_data.get("current_password"),
        )
        return Response(status=204)


class GoogleSignIn(PublicIdentityView):
    def post(self, request):
        serializer = GoogleCredentialInput(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token_pair, fallback_recommended = application.sign_in_with_google(
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
                "fallback_recommended": fallback_recommended,
            }
        )


class LinkGoogleIdentity(AuthenticatedIdentityView):
    def post(self, request):
        serializer = GoogleCredentialInput(data=request.data)
        serializer.is_valid(raise_exception=True)
        application.link_google_identity(
            user=request.user,
            session=request.auth_session,
            **serializer.validated_data,
        )
        return Response(status=204)


class BeginPasskeyRegistration(AuthenticatedIdentityView):
    def post(self, request):
        serializer = PasskeyNameInput(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            require_recent_authentication(session=request.auth_session)
        except RecentAuthenticationRequired as error:
            raise PermissionDenied(
                "Recent authentication is required.",
                code="recent_auth_required",
            ) from error
        challenge, public_key = begin_passkey_registration(
            user=request.user,
            **serializer.validated_data,
        )
        return Response(
            {
                "challenge_id": challenge.id,
                "public_key": public_key,
            }
        )


class FinishPasskeyRegistration(AuthenticatedIdentityView):
    def post(self, request):
        serializer = PasskeyCeremonyInput(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            passkey = finish_passkey_registration(
                user=request.user,
                **serializer.validated_data,
            )
        except InvalidPasskeyChallenge as error:
            raise InvalidPasskeyCeremony from error
        except PasskeyCredentialConflict as error:
            raise PasskeyConflict from error
        return Response(PasskeyOutput(passkey).data, status=201)


class BeginPasskeyAuthentication(PublicIdentityView):
    def post(self, request):
        serializer = EmptyInput(data=request.data)
        serializer.is_valid(raise_exception=True)
        challenge, public_key = begin_passkey_authentication()
        return Response(
            {
                "challenge_id": challenge.id,
                "public_key": public_key,
            }
        )


class FinishPasskeyAuthentication(PublicIdentityView):
    def post(self, request):
        serializer = PasskeyCeremonyInput(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user, token_pair = finish_passkey_authentication(
                **serializer.validated_data,
                user_agent=request.META.get("HTTP_USER_AGENT", ""),
            )
        except InvalidPasskeyChallenge as error:
            raise InvalidPasskeyCeremony from error
        return Response(
            {
                "access": token_pair.access,
                "refresh": token_pair.refresh,
                "user": {
                    "email": user.email,
                    "handle": user.handle,
                    "display_name": user.display_name,
                },
                "fallback_recommended": False,
            }
        )


class Passkeys(AuthenticatedIdentityView):
    def get(self, request):
        passkeys = PasskeyCredential.objects.filter(user=request.user).order_by("-created_at")
        return Response({"results": PasskeyOutput(passkeys, many=True).data})


class RevokeOwnedSession(AuthenticatedIdentityView):
    def delete(self, request, session_id):
        session = get_object_or_404(
            AuthSession,
            id=session_id,
            user=request.user,
        )
        revoke_session(session=session)
        return Response(status=204)
