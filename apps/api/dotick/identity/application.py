from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import IntegrityError, transaction
from django.utils import timezone
from rest_framework.exceptions import APIException, ValidationError

from dotick.identity.challenges import (
    ChallengeIssuanceBlocked,
    issue_challenge,
    try_consume_challenge,
)
from dotick.identity.models import VerificationChallenge


class InvalidVerificationCode(APIException):
    status_code = 400
    default_detail = "Invalid or expired verification code."
    default_code = "invalid_verification_code"


def normalize_email(email):
    return get_user_model().objects.normalize_email(email).strip().lower()


def _send_verification_email(*, user, code):
    send_mail(
        subject="Verify your Dotick email",
        message=f"Your Dotick verification code is {code}. It expires in 10 minutes.",
        from_email=None,
        recipient_list=[user.email],
    )


def _issue_email_verification(user):
    try:
        return issue_challenge(
            user=user,
            purpose=VerificationChallenge.Purpose.EMAIL_VERIFICATION,
        )
    except ChallengeIssuanceBlocked:
        return None


def register_account(*, email, password, handle, display_name):
    user_model = get_user_model()
    normalized_email = normalize_email(email)
    normalized_handle = handle.strip()
    normalized_display_name = display_name.strip()
    recipient = None
    code = None

    with transaction.atomic():
        existing = (
            user_model.objects.select_for_update().filter(email__iexact=normalized_email).first()
        )

        if existing is not None:
            if existing.email_verified_at is None:
                recipient = existing
                code = _issue_email_verification(existing)
        else:
            if user_model.objects.filter(handle__iexact=normalized_handle).exists():
                raise ValidationError({"handle": ["This handle is unavailable."]})

            try:
                with transaction.atomic():
                    recipient = user_model.objects.create_user(
                        email=normalized_email,
                        password=password,
                        handle=normalized_handle,
                        display_name=normalized_display_name,
                        is_active=False,
                    )
            except IntegrityError as error:
                if user_model.objects.filter(email__iexact=normalized_email).exists():
                    recipient = None
                elif user_model.objects.filter(handle__iexact=normalized_handle).exists():
                    raise ValidationError({"handle": ["This handle is unavailable."]}) from error
                else:
                    raise
            else:
                code = _issue_email_verification(recipient)

    if recipient is not None and code is not None:
        _send_verification_email(user=recipient, code=code)


def resend_email_verification(*, email):
    user_model = get_user_model()
    recipient = None
    code = None

    with transaction.atomic():
        recipient = (
            user_model.objects.select_for_update()
            .filter(
                email__iexact=normalize_email(email),
                email_verified_at__isnull=True,
            )
            .first()
        )
        if recipient is not None:
            code = _issue_email_verification(recipient)

    if recipient is not None and code is not None:
        _send_verification_email(user=recipient, code=code)


def verify_email(*, email, code):
    user_model = get_user_model()
    verified = False

    with transaction.atomic():
        user = (
            user_model.objects.select_for_update()
            .filter(email__iexact=normalize_email(email))
            .first()
        )

        if user is not None:
            challenge = try_consume_challenge(
                user=user,
                purpose=VerificationChallenge.Purpose.EMAIL_VERIFICATION,
                code=code,
            )
            if challenge is not None:
                user.email_verified_at = timezone.now()
                user.is_active = True
                user.save(update_fields=["email_verified_at", "is_active"])
                verified = True

    if not verified:
        raise InvalidVerificationCode
