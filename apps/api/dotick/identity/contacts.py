import smtplib

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import IntegrityError, transaction
from django.utils import timezone

from dotick.identity.contact_challenges import (
    issue_contact_challenge,
    try_consume_contact_challenge,
)
from dotick.identity.models import AccountContact
from dotick.identity.sms import SmsDeliveryUnavailable, get_sms_delivery_adapter
from dotick.identity.validators import normalize_contact_value


class ContactConflict(Exception):
    pass


class ContactDeliveryUnavailable(Exception):
    pass


class InvalidContactVerification(Exception):
    pass


def _email_delivery_is_configured():
    if settings.EMAIL_BACKEND != "django.core.mail.backends.smtp.EmailBackend":
        return True
    return bool(settings.EMAIL_HOST and settings.DEFAULT_FROM_EMAIL)


def _deliver_contact_code(*, contact, code):
    if contact.kind == AccountContact.Kind.EMAIL:
        if not _email_delivery_is_configured():
            raise ContactDeliveryUnavailable
        try:
            delivered = send_mail(
                subject="Verify your Dotick contact",
                message=(
                    f"Your Dotick contact verification code is {code}. It expires in 10 minutes."
                ),
                from_email=None,
                recipient_list=[contact.value],
            )
        except (OSError, smtplib.SMTPException) as error:
            raise ContactDeliveryUnavailable from error
        if delivered != 1:
            raise ContactDeliveryUnavailable
        return

    try:
        get_sms_delivery_adapter().send_verification_code(
            phone_number=contact.value,
            code=code,
        )
    except SmsDeliveryUnavailable as error:
        raise ContactDeliveryUnavailable from error


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
