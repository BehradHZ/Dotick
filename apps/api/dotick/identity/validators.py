from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from django.core.exceptions import ValidationError


def validate_iana_timezone(value):
    try:
        ZoneInfo(value)
    except (TypeError, ValueError, ZoneInfoNotFoundError) as error:
        raise ValidationError(
            "Enter a valid IANA timezone identifier.",
            code="invalid_timezone",
        ) from error
