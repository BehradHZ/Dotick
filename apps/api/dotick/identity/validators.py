import re
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from django.core.exceptions import ValidationError
from django.core.validators import validate_email

E164_PATTERN = re.compile(r"^\+[1-9][0-9]{1,14}$")


def validate_iana_timezone(value):
    try:
        ZoneInfo(value)
    except (TypeError, ValueError, ZoneInfoNotFoundError) as error:
        raise ValidationError(
            "Enter a valid IANA timezone identifier.",
            code="invalid_timezone",
        ) from error


def normalize_contact_value(kind, value):
    normalized = value.strip()
    if kind == "email":
        normalized = normalized.lower()
        validate_email(normalized)
    elif kind == "phone":
        if not E164_PATTERN.fullmatch(normalized):
            raise ValidationError(
                "Enter a valid E.164 phone number.",
                code="invalid_phone",
            )
    else:
        raise ValidationError("Unknown contact kind.", code="invalid_contact_kind")
    return normalized
