from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction

from dotick.identity.models import ExternalIdentity, UserPreferences


class AccountHandleConflict(Exception):
    pass


def enabled_authentication_methods(user):
    return {
        "password": user.has_usable_password(),
        "google": user.external_identities.filter(
            provider=ExternalIdentity.Provider.GOOGLE,
        ).exists(),
        "passkey": user.passkey_credentials.exists(),
    }


@transaction.atomic
def update_account(*, user, changes):
    locked_user = get_user_model().objects.select_for_update().get(pk=user.pk)
    user_fields = {
        field: value
        for field, value in changes.items()
        if field in {"handle", "display_name", "profile_picture_url"}
    }

    handle = user_fields.get("handle")
    if handle is not None and (
        get_user_model()
        .objects.filter(handle__iexact=handle)
        .exclude(pk=locked_user.pk)
        .exists()
    ):
        raise AccountHandleConflict

    for field, value in user_fields.items():
        setattr(locked_user, field, value)

    if user_fields:
        try:
            locked_user.save(update_fields=list(user_fields))
        except IntegrityError as error:
            raise AccountHandleConflict from error

    if "timezone" in changes:
        UserPreferences.objects.update_or_create(
            user=locked_user,
            defaults={"timezone": changes["timezone"]},
        )

    return locked_user
