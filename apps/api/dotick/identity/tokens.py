from dataclasses import dataclass
from uuid import UUID

from rest_framework_simplejwt.tokens import RefreshToken


@dataclass(frozen=True)
class TokenPair:
    access: str
    refresh: str
    refresh_jti: str


def issue_token_pair(*, user, session_id: UUID) -> TokenPair:
    refresh = RefreshToken.for_user(user)
    refresh["sid"] = str(session_id)
    access = refresh.access_token

    return TokenPair(
        access=str(access),
        refresh=str(refresh),
        refresh_jti=str(refresh["jti"]),
    )
