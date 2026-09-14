import secrets
from datetime import timedelta

from django.utils import timezone

from dotick.identity.models import PasskeyChallenge

PASSKEY_CHALLENGE_BYTES = 32
PASSKEY_CHALLENGE_TTL = timedelta(minutes=5)


def issue_passkey_challenge(*, purpose, user=None, name=""):
    now = timezone.now()
    return PasskeyChallenge.objects.create(
        user=user,
        purpose=purpose,
        challenge=secrets.token_bytes(PASSKEY_CHALLENGE_BYTES),
        name=name,
        expires_at=now + PASSKEY_CHALLENGE_TTL,
        created_at=now,
    )
