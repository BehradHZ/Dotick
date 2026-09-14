import json
import secrets
from datetime import timedelta

from django.conf import settings
from django.db import IntegrityError, transaction
from django.utils import timezone
from webauthn import generate_registration_options, options_to_json, verify_registration_response
from webauthn.helpers.structs import (
    AuthenticatorSelectionCriteria,
    PublicKeyCredentialDescriptor,
    ResidentKeyRequirement,
    UserVerificationRequirement,
)
from webauthn.registration.verify_registration_response import InvalidRegistrationResponse

from dotick.identity.models import PasskeyChallenge, PasskeyCredential

PASSKEY_CHALLENGE_BYTES = 32
PASSKEY_CHALLENGE_TTL = timedelta(minutes=5)


class InvalidPasskeyChallenge(Exception):
    pass


class PasskeyCredentialConflict(Exception):
    pass


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


@transaction.atomic
def finish_passkey_registration(*, user, challenge_id, credential):
    now = timezone.now()
    try:
        challenge = PasskeyChallenge.objects.select_for_update().get(
            id=challenge_id,
            user=user,
            purpose=PasskeyChallenge.Purpose.REGISTRATION,
            consumed_at__isnull=True,
            expires_at__gt=now,
        )
    except PasskeyChallenge.DoesNotExist as error:
        raise InvalidPasskeyChallenge from error

    try:
        verification = verify_registration_response(
            credential=credential,
            expected_challenge=bytes(challenge.challenge),
            expected_rp_id=settings.WEBAUTHN_RP_ID,
            expected_origin=settings.WEBAUTHN_ORIGIN,
            require_user_verification=True,
        )
    except (InvalidRegistrationResponse, KeyError, TypeError, ValueError) as error:
        raise InvalidPasskeyChallenge from error

    transports = credential.get("response", {}).get("transports", [])
    if not isinstance(transports, list) or not all(isinstance(item, str) for item in transports):
        transports = []

    try:
        with transaction.atomic():
            passkey = PasskeyCredential.objects.create(
                user=user,
                credential_id=verification.credential_id,
                public_key=verification.credential_public_key,
                sign_count=verification.sign_count,
                device_type=verification.credential_device_type.value,
                backed_up=verification.credential_backed_up,
                transports=transports,
                name=challenge.name,
            )
    except IntegrityError as error:
        raise PasskeyCredentialConflict from error

    challenge.consumed_at = now
    challenge.save(update_fields=["consumed_at"])
    return passkey
