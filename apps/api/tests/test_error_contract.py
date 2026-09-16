from config.errors import _get_error_code
from rest_framework.exceptions import (
    APIException,
    AuthenticationFailed,
    NotAuthenticated,
    NotFound,
    ValidationError,
)


class Conflict(APIException):
    status_code = 409


class ProviderUnavailable(APIException):
    status_code = 503


def test_generic_error_classes_have_stable_codes():
    assert _get_error_code(ValidationError(), 400) == "validation_error"
    assert _get_error_code(NotAuthenticated(), 401) == "not_authenticated"
    assert _get_error_code(AuthenticationFailed(), 401) == "authentication_failed"
    assert _get_error_code(NotFound(), 404) == "not_found"
    assert _get_error_code(Conflict(), 409) == "conflict"
    assert _get_error_code(ProviderUnavailable(), 503) == "provider_unavailable"
