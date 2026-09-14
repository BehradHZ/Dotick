import uuid
from datetime import timedelta

from django.db import transaction
from django.utils import timezone
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from dotick.identity.models import AuthSession
from dotick.identity.tokens import issue_token_pair


class InvalidSessionToken(Exception):
    pass


class RecentAuthenticationRequired(Exception):
    pass


RECENT_AUTHENTICATION_WINDOW = timedelta(minutes=10)


@transaction.atomic
def create_auth_session(*, user, user_agent=""):
    session_id = uuid.uuid4()
    token_pair = issue_token_pair(user=user, session_id=session_id)
    session = AuthSession.objects.create(
        id=session_id,
        user=user,
        refresh_jti=token_pair.refresh_jti,
        user_agent=user_agent[:200],
    )
    return session, token_pair


@transaction.atomic
def rotate_refresh_token(*, encoded_refresh):
    try:
        submitted = RefreshToken(encoded_refresh)
        session_id = uuid.UUID(str(submitted["sid"]))
        user_id = uuid.UUID(str(submitted["user_id"]))
        submitted_jti = str(submitted["jti"])
    except (KeyError, TokenError, TypeError, ValueError) as error:
        raise InvalidSessionToken from error

    try:
        session = (
            AuthSession.objects.select_for_update()
            .select_related("user")
            .get(
                id=session_id,
                user_id=user_id,
                revoked_at__isnull=True,
                user__is_active=True,
                user__email_verified_at__isnull=False,
            )
        )
    except AuthSession.DoesNotExist as error:
        raise InvalidSessionToken from error

    if session.refresh_jti != submitted_jti:
        raise InvalidSessionToken

    token_pair = issue_token_pair(user=session.user, session_id=session.id)
    session.refresh_jti = token_pair.refresh_jti
    session.last_seen_at = timezone.now()
    session.save(update_fields=["refresh_jti", "last_seen_at"])
    return token_pair


def revoke_session(*, session):
    if session.revoked_at is None:
        session.revoked_at = timezone.now()
        session.save(update_fields=["revoked_at"])


def revoke_all_sessions(*, user):
    return AuthSession.objects.filter(
        user=user,
        revoked_at__isnull=True,
    ).update(revoked_at=timezone.now())


def require_recent_authentication(*, session):
    if session.created_at < timezone.now() - RECENT_AUTHENTICATION_WINDOW:
        raise RecentAuthenticationRequired
