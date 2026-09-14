import json
import secrets
from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from webauthn import generate_registration_options, options_to_json
from webauthn.helpers.structs import (
    AuthenticatorSelectionCriteria,
    PublicKeyCredentialDescriptor,
    ResidentKeyRequirement,
    UserVerificationRequirement,
)

from dotick.identity.models import PasskeyChallenge, PasskeyCredential

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


def begin_passkey_registration(*, user, name):
    challenge = issue_passkey_challenge(
        user=user,
        purpose=PasskeyChallenge.Purpose.REGISTRATION,
        name=name,
    )
    excluded = [
        PublicKeyCredentialDescriptor(id=bytes(credential_id))
        for credential_id in PasskeyCredential.objects.filter(user=user).values_list(
            "credential_id",
            flat=True,
        )
    ]
    options = generate_registration_options(
        rp_id=settings.WEBAUTHN_RP_ID,
        rp_name=settings.WEBAUTHN_RP_NAME,
        user_name=user.email,
        user_id=user.id.bytes,
        user_display_name=user.display_name,
        challenge=bytes(challenge.challenge),
        authenticator_selection=AuthenticatorSelectionCriteria(
            resident_key=ResidentKeyRequirement.REQUIRED,
            require_resident_key=True,
            user_verification=UserVerificationRequirement.REQUIRED,
        ),
        exclude_credentials=excluded,
    )
    return challenge, json.loads(options_to_json(options))
