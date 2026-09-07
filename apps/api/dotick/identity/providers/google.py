from django.conf import settings
from google.auth.exceptions import TransportError
from rest_framework.exceptions import APIException, AuthenticationFailed


class GoogleProviderUnavailable(APIException):
    status_code = 503
    default_detail = "Google identity verification is temporarily unavailable."
    default_code = "identity_provider_unavailable"


def _official_verifier(credential):
    if not settings.GOOGLE_OAUTH_CLIENT_ID:
        raise GoogleProviderUnavailable
    try:
        from google.auth.transport.requests import Request
        from google.oauth2 import id_token

        return id_token.verify_oauth2_token(
            credential,
            Request(),
            settings.GOOGLE_OAUTH_CLIENT_ID,
        )
    except ValueError as error:
        raise AuthenticationFailed("Invalid Google credential.") from error
    except (OSError, TimeoutError, TransportError) as error:
        raise GoogleProviderUnavailable from error


def verify_google_credential(credential):
    verifier = getattr(settings, "GOOGLE_ID_TOKEN_VERIFIER", None)
    raw = verifier(credential) if callable(verifier) else _official_verifier(credential)
    subject = raw.get("subject") or raw.get("sub")
    email = str(raw.get("email", "")).strip().lower()
    verified = raw.get("email_verified") is True
    if not subject or not email or not verified:
        raise AuthenticationFailed("Invalid Google credential.")
    display_name = str(raw.get("display_name") or raw.get("name") or email.split("@", 1)[0])
    return {
        "subject": str(subject),
        "email": email,
        "display_name": display_name[:120],
    }
