import uuid

from django.db import transaction

from dotick.identity.models import AuthSession
from dotick.identity.tokens import issue_token_pair


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
