import uuid

from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication

from dotick.identity.models import AuthSession


class SessionJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        authenticated = super().authenticate(request)
        if authenticated is None:
            return None

        user, validated_token = authenticated
        try:
            session_id = uuid.UUID(str(validated_token["sid"]))
        except (KeyError, TypeError, ValueError) as error:
            raise AuthenticationFailed(
                "Token or session is invalid.",
                code="token_not_valid",
            ) from error

        try:
            session = AuthSession.objects.get(
                id=session_id,
                user=user,
                revoked_at__isnull=True,
            )
        except AuthSession.DoesNotExist as error:
            raise AuthenticationFailed(
                "Token or session is invalid.",
                code="token_not_valid",
            ) from error

        now = timezone.now()
        updated = AuthSession.objects.filter(
            pk=session.pk,
            revoked_at__isnull=True,
        ).update(last_seen_at=now)
        if updated != 1:
            raise AuthenticationFailed(
                "Token or session is invalid.",
                code="token_not_valid",
            )
        session.last_seen_at = now
        request.auth_session = session
        return user, validated_token
