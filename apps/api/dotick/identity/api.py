import re
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

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


class GoogleCredentialInput(StrictSerializer):
    credential = serializers.CharField(max_length=8192, trim_whitespace=False, write_only=True)


class PasskeyNameInput(StrictSerializer):
    name = serializers.CharField(max_length=120, trim_whitespace=True)


class PasskeyCeremonyInput(StrictSerializer):
    challenge_id = serializers.UUIDField()
    credential = serializers.JSONField()


class EmptyInput(StrictSerializer):
    pass


class PasskeyOutput(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    device_type = serializers.CharField()
    backed_up = serializers.BooleanField()
    created_at = serializers.DateTimeField()
    last_used_at = serializers.DateTimeField(allow_null=True)


class AccountUpdateInput(StrictSerializer):
    handle = serializers.RegexField(r"^[A-Za-z0-9_]{3,30}$", max_length=30, required=False)
    display_name = serializers.CharField(max_length=120, trim_whitespace=True, required=False)
    profile_picture_url = serializers.URLField(
        max_length=2048,
        required=False,
        allow_null=True,
        allow_blank=True,
    )
    timezone = serializers.CharField(max_length=64, required=False)

    def validate_timezone(self, value):
        try:
            ZoneInfo(value)
        except ZoneInfoNotFoundError as error:
            raise serializers.ValidationError("Use a valid IANA timezone identifier.") from error
        return value

    def validate(self, attrs):
        if not attrs:
            raise serializers.ValidationError("Provide at least one account change.")
        if "timezone" in attrs:
            attrs["timezone_name"] = attrs.pop("timezone")
        return attrs


class PasswordSetInput(StrictSerializer):
    password = serializers.CharField(max_length=128, trim_whitespace=False, write_only=True)
    current_password = serializers.CharField(
        max_length=128,
        trim_whitespace=False,
        write_only=True,
        required=False,
    )


class ContactRequestInput(StrictSerializer):
    kind = serializers.ChoiceField(choices=["email", "phone"])
    value = serializers.CharField(max_length=254, trim_whitespace=True)

    def validate(self, attrs):
        if attrs["kind"] == "email":
            attrs["value"] = serializers.EmailField().run_validation(attrs["value"])
        elif not re.fullmatch(r"\+[1-9]\d{7,14}", attrs["value"]):
            raise serializers.ValidationError({"value": ["Use an E.164 phone number."]})
        return attrs


class ContactVerifyInput(StrictSerializer):
    contact_id = serializers.UUIDField()
    code = serializers.RegexField(r"^\d{6}$", max_length=6)


class ContactOutput(serializers.Serializer):
    id = serializers.UUIDField()
    kind = serializers.CharField()
    value = serializers.CharField(source="normalized_value")
    verified_at = serializers.DateTimeField()


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


class GoogleSignIn(PublicIdentityView):
    def post(self, request):
        data = GoogleCredentialInput(data=request.data)
        data.is_valid(raise_exception=True)
        return Response(
            application.sign_in_with_google(
                credential=data.validated_data["credential"],
                user_agent=request.META.get("HTTP_USER_AGENT", ""),
            )
        )


class Account(APIView):
    def get(self, request):
        return Response(application.account_presentation(user=request.user))

    def patch(self, request):
        data = AccountUpdateInput(data=request.data)
        data.is_valid(raise_exception=True)
        user = application.update_account(
            user_id=request.user.id,
            **data.validated_data,
        )
        return Response(application.account_presentation(user=user))


class Password(APIView):
    def put(self, request):
        data = PasswordSetInput(data=request.data)
        data.is_valid(raise_exception=True)
        application.set_password(
            user=request.user,
            session=request.auth_session,
            **data.validated_data,
        )
        return Response(status=204)


class Contacts(APIView):
    def get(self, request):
        rows = application.list_contacts(user=request.user)
        return Response({"results": ContactOutput(rows, many=True).data})

    def post(self, request):
        data = ContactRequestInput(data=request.data)
        data.is_valid(raise_exception=True)
        row = application.request_contact_verification(
            user=request.user,
            **data.validated_data,
        )
        return Response({"id": row.id, "status": "pending"}, status=202)


class ContactVerify(APIView):
    def post(self, request):
        data = ContactVerifyInput(data=request.data)
        data.is_valid(raise_exception=True)
        application.verify_contact(user=request.user, **data.validated_data)
        return Response(status=204)


class ContactDetail(APIView):
    def delete(self, request, contact_id):
        application.delete_contact(user=request.user, contact_id=contact_id)
        return Response(status=204)


class GoogleLink(APIView):
    def post(self, request):
        data = GoogleCredentialInput(data=request.data)
        data.is_valid(raise_exception=True)
        application.link_google_identity(
            user=request.user,
            session=request.auth_session,
            credential=data.validated_data["credential"],
        )
        return Response(status=204)


class Passkeys(APIView):
    def get(self, request):
        rows = application.list_passkeys(user=request.user)
        return Response({"results": PasskeyOutput(rows, many=True).data})


class PasskeyDetail(APIView):
    def delete(self, request, passkey_id):
        application.delete_passkey(user=request.user, passkey_id=passkey_id)
        return Response(status=204)


class PasskeyRegistrationOptions(APIView):
    def post(self, request):
        data = PasskeyNameInput(data=request.data)
        data.is_valid(raise_exception=True)
        return Response(
            application.begin_passkey_registration(
                user=request.user,
                session=request.auth_session,
                name=data.validated_data["name"],
            )
        )


class PasskeyRegistrationVerify(APIView):
    def post(self, request):
        data = PasskeyCeremonyInput(data=request.data)
        data.is_valid(raise_exception=True)
        row = application.finish_passkey_registration(
            user=request.user,
            **data.validated_data,
        )
        return Response(PasskeyOutput(row).data, status=201)


class PasskeyAuthenticationOptions(PublicIdentityView):
    def post(self, request):
        data = EmptyInput(data=request.data)
        data.is_valid(raise_exception=True)
        return Response(application.begin_passkey_authentication())


class PasskeyAuthenticationVerify(PublicIdentityView):
    def post(self, request):
        data = PasskeyCeremonyInput(data=request.data)
        data.is_valid(raise_exception=True)
        return Response(
            application.finish_passkey_authentication(
                **data.validated_data,
                user_agent=request.META.get("HTTP_USER_AGENT", ""),
            )
        )
