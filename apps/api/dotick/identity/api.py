from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
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


class PublicIdentityView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]


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
