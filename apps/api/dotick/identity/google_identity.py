from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.request import Request as UrlRequest
from urllib.request import urlopen

from django.conf import settings
from google.auth import exceptions as google_exceptions
from google.auth import transport as google_transport
from google.oauth2 import id_token


class InvalidGoogleCredential(Exception):
    pass


class GoogleProviderUnavailable(Exception):
    pass


class _StandardLibraryResponse(google_transport.Response):
    def __init__(self, *, status, headers, data):
        self._status = status
        self._headers = headers
        self._data = data

    @property
    def status(self):
        return self._status

    @property
    def headers(self):
        return self._headers

    @property
    def data(self):
        return self._data


class _StandardLibraryRequest(google_transport.Request):
    def __call__(self, url, method="GET", body=None, headers=None, timeout=None, **kwargs):
        del kwargs
        request = UrlRequest(
            url=url,
            data=body,
            headers=dict(headers or {}),
            method=method,
        )

        try:
            if timeout is None:
                response = urlopen(request)
            else:
                response = urlopen(request, timeout=timeout)
            with response:
                return _StandardLibraryResponse(
                    status=response.status,
                    headers=response.headers,
                    data=response.read(),
                )
        except HTTPError as error:
            return _StandardLibraryResponse(
                status=error.code,
                headers=error.headers,
                data=error.read(),
            )
        except (OSError, TimeoutError, URLError) as error:
            raise google_exceptions.TransportError(error) from error


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
            _StandardLibraryRequest(),
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
