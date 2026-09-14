import secrets
from datetime import timedelta
from hmac import compare_digest

from django.db import transaction
from django.utils import timezone
from django.utils.crypto import salted_hmac

from dotick.identity.models import AccountContact, ContactVerificationChallenge

CONTACT_CHALLENGE_TTL = timedelta(minutes=10)
MAX_FAILED_ATTEMPTS = 5


class InvalidContactChallenge(Exception):
    pass


def _code_digest(*, contact, code):
    value = f"{contact.id}:{contact.kind}:{contact.value}:{code}"
    return salted_hmac(
        "dotick.identity.contact-verification-code",
        value,
        algorithm="sha256",
    ).hexdigest()


@transaction.atomic
def issue_contact_challenge(*, contact):
    now = timezone.now()
    locked_contact = AccountContact.objects.select_for_update().get(pk=contact.pk)
    code = f"{secrets.randbelow(1_000_000):06d}"
    ContactVerificationChallenge.objects.filter(
        contact=locked_contact,
        consumed_at__isnull=True,
    ).update(consumed_at=now)
    ContactVerificationChallenge.objects.create(
        contact=locked_contact,
        code_digest=_code_digest(contact=locked_contact, code=code),
        expires_at=now + CONTACT_CHALLENGE_TTL,
        created_at=now,
    )
    return code


@transaction.atomic
def try_consume_contact_challenge(*, contact, code):
    now = timezone.now()
    locked_contact = AccountContact.objects.select_for_update().get(pk=contact.pk)
    try:
        challenge = (
            ContactVerificationChallenge.objects.select_for_update()
            .filter(contact=locked_contact, consumed_at__isnull=True)
            .latest("created_at")
        )
    except ContactVerificationChallenge.DoesNotExist:
        return None

    expected = _code_digest(contact=locked_contact, code=code)
    if challenge.expires_at <= now:
        return None
    if not compare_digest(challenge.code_digest, expected):
        challenge.failed_attempts += 1
        if challenge.failed_attempts >= MAX_FAILED_ATTEMPTS:
            challenge.consumed_at = now
        challenge.save(update_fields=["failed_attempts", "consumed_at"])
        return None

    challenge.consumed_at = now
    challenge.save(update_fields=["consumed_at"])
    return challenge


def consume_contact_challenge(*, contact, code):
    challenge = try_consume_contact_challenge(contact=contact, code=code)
    if challenge is None:
        raise InvalidContactChallenge
    return challenge
