import secrets
from datetime import timedelta
from hmac import compare_digest

from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from django.utils.crypto import salted_hmac

from dotick.identity.models import VerificationChallenge

CODE_UPPER_BOUND = 1_000_000
CHALLENGE_TTL = timedelta(minutes=10)
ISSUANCE_COOLDOWN = timedelta(seconds=60)
HOURLY_ISSUANCE_LIMIT = 5
MAX_FAILED_ATTEMPTS = 5


class ChallengeIssuanceBlocked(Exception):
    pass


class InvalidChallenge(Exception):
    pass


def _code_digest(*, user_id, purpose, code):
    value = f"{user_id}:{purpose}:{code}"
    return salted_hmac(
        "dotick.identity.verification-code",
        value,
        algorithm="sha256",
    ).hexdigest()


def _validate_purpose(purpose):
    if purpose not in VerificationChallenge.Purpose.values:
        raise ValueError("Unknown verification challenge purpose.")


@transaction.atomic
def issue_challenge(*, user, purpose):
    _validate_purpose(purpose)
    now = timezone.now()
    locked_user = get_user_model().objects.select_for_update().get(pk=user.pk)
    issued = VerificationChallenge.objects.filter(user=locked_user, purpose=purpose)

    if issued.filter(created_at__gt=now - ISSUANCE_COOLDOWN).exists():
        raise ChallengeIssuanceBlocked

    if issued.filter(created_at__gte=now - timedelta(hours=1)).count() >= HOURLY_ISSUANCE_LIMIT:
        raise ChallengeIssuanceBlocked

    code = f"{secrets.randbelow(CODE_UPPER_BOUND):06d}"

    issued.filter(consumed_at__isnull=True).update(consumed_at=now)
    VerificationChallenge.objects.create(
        user=locked_user,
        purpose=purpose,
        code_digest=_code_digest(
            user_id=locked_user.id,
            purpose=purpose,
            code=code,
        ),
        expires_at=now + CHALLENGE_TTL,
        created_at=now,
    )

    return code


def consume_challenge(*, user, purpose, code):
    _validate_purpose(purpose)
    now = timezone.now()
    consumed_challenge = None
    invalid = False

    with transaction.atomic():
        locked_user = get_user_model().objects.select_for_update().get(pk=user.pk)

        try:
            challenge = (
                VerificationChallenge.objects.select_for_update()
                .filter(
                    user=locked_user,
                    purpose=purpose,
                    consumed_at__isnull=True,
                )
                .latest("created_at")
            )
        except VerificationChallenge.DoesNotExist:
            invalid = True
        else:
            expected_digest = _code_digest(
                user_id=locked_user.id,
                purpose=purpose,
                code=code,
            )

            if challenge.expires_at <= now:
                invalid = True
            elif not compare_digest(challenge.code_digest, expected_digest):
                challenge.failed_attempts += 1
                if challenge.failed_attempts >= MAX_FAILED_ATTEMPTS:
                    challenge.consumed_at = now
                challenge.save(update_fields=["failed_attempts", "consumed_at"])
                invalid = True
            else:
                challenge.consumed_at = now
                challenge.save(update_fields=["consumed_at"])
                consumed_challenge = challenge

    if invalid:
        raise InvalidChallenge

    return consumed_challenge
