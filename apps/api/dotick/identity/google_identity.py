from dataclasses import dataclass

from django.conf import settings
from google.auth import exceptions as google_exceptions
from google.auth.transport.requests import Request
from google.oauth2 import id_token


class InvalidGoogleCredential(Exception):
    pass


class GoogleProviderUnavailable(Exception):
    pass


@dataclass(frozen=True)
class GoogleIdentityClaims:
    subject: str
    email: str
    display_name: str
    picture_url: str | None


def verify_google_id_credential(credential):
    if not settings.GOOGLE_OAUTH_CLIENT_ID:
        raise GoogleProviderUnavailable

    try:
        claims = id_token.verify_oauth2_token(
            credential,
            Request(),
            audience=settings.GOOGLE_OAUTH_CLIENT_ID,
        )
    except google_exceptions.TransportError as error:
        raise GoogleProviderUnavailable from error
    except (google_exceptions.GoogleAuthError, KeyError, TypeError, ValueError) as error:
        raise InvalidGoogleCredential from error

    subject = claims.get("sub")
    email = claims.get("email")
    if not isinstance(subject, str) or not subject:
        raise InvalidGoogleCredential
    if not isinstance(email, str) or not email:
        raise InvalidGoogleCredential
    if claims.get("email_verified") is not True:
        raise InvalidGoogleCredential

    name = claims.get("name")
    picture = claims.get("picture")
    return GoogleIdentityClaims(
        subject=subject,
        email=email.strip().lower(),
        display_name=(
            name.strip() if isinstance(name, str) and name.strip() else email.split("@", 1)[0]
        ),
        picture_url=picture if isinstance(picture, str) and picture else None,
    )
