from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import IntegrityError, transaction
from django.utils import timezone

from dotick.identity.contact_challenges import (
    issue_contact_challenge,
    try_consume_contact_challenge,
)
from dotick.identity.models import AccountContact
from dotick.identity.validators import normalize_contact_value


class ContactConflict(Exception):
    pass


class ContactDeliveryUnavailable(Exception):
    pass


class InvalidContactVerification(Exception):
    pass


def _deliver_contact_code(*, contact, code):
    if contact.kind == AccountContact.Kind.EMAIL:
        delivered = send_mail(
            subject="Verify your Dotick contact",
            message=f"Your Dotick contact verification code is {code}. It expires in 10 minutes.",
            from_email=None,
            recipient_list=[contact.value],
        )
        if delivered != 1:
            raise ContactDeliveryUnavailable
        return

    # A deployment-specific SMS adapter is intentionally required for phone delivery.
    raise ContactDeliveryUnavailable


def request_contact_verification(*, user, kind, value):
    normalized_value = normalize_contact_value(kind, value)

    with transaction.atomic():
        if (
            AccountContact.objects.select_for_update()
            .active()
            .filter(kind=kind, value=normalized_value)
            .exists()
        ):
            raise ContactConflict

        contact = (
            AccountContact.objects.select_for_update()
            .filter(
                user=user,
                kind=kind,
                value=normalized_value,
                verified_at__isnull=True,
            )
            .order_by("created_at")
            .first()
        )
        if contact is None:
            contact = AccountContact.objects.create(
                user=user,
                kind=kind,
                value=normalized_value,
            )
        code = issue_contact_challenge(contact=contact)

    _deliver_contact_code(contact=contact, code=code)
    return contact


def verify_contact(*, user, contact_id, code):
    contact = AccountContact.objects.filter(
        id=contact_id,
        user=user,
        verified_at__isnull=True,
    ).first()
    if contact is None:
        raise InvalidContactVerification

    challenge = try_consume_contact_challenge(contact=contact, code=code)
    if challenge is None:
        raise InvalidContactVerification

    try:
        with transaction.atomic():
            locked_contact = AccountContact.objects.select_for_update().get(
                id=contact.id,
                user=user,
                verified_at__isnull=True,
            )
            locked_contact.verified_at = timezone.now()
            locked_contact.save(update_fields=["verified_at", "updated_at"])
    except (AccountContact.DoesNotExist, IntegrityError, ValidationError) as error:
        raise ContactConflict from error

    return locked_contact
