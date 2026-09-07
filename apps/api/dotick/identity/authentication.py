from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication

from dotick.identity.models import AuthSession


class SessionJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        result = super().authenticate(request)
        if result is None:
            return None
        user, token = result
        session_id = token.get("sid")
        try:
            session = AuthSession.objects.get(
                id=session_id,
                user=user,
                revoked_at__isnull=True,
            )
        except (AuthSession.DoesNotExist, ValueError, TypeError) as error:
            raise AuthenticationFailed("Session is no longer active.") from error
        AuthSession.objects.filter(id=session.id).update(last_seen_at=timezone.now())
        request.auth_session = session
        return user, token
