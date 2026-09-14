import json
import secrets
from datetime import timedelta

from django.conf import settings
from django.db import IntegrityError, transaction
from django.utils import timezone
from webauthn import (
    generate_authentication_options,
    generate_registration_options,
    options_to_json,
    verify_authentication_response,
    verify_registration_response,
)
from webauthn.authentication.verify_authentication_response import (
    InvalidAuthenticationResponse,
    InvalidSignature,
)
from webauthn.helpers import parse_authentication_credential_json
from webauthn.helpers.exceptions import InvalidJSONStructure
from webauthn.helpers.structs import (
    AuthenticatorSelectionCriteria,
    PublicKeyCredentialDescriptor,
    ResidentKeyRequirement,
    UserVerificationRequirement,
)
from webauthn.registration.verify_registration_response import InvalidRegistrationResponse

from dotick.identity.models import PasskeyChallenge, PasskeyCredential
from dotick.identity.sessions import create_auth_session

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


def begin_passkey_authentication():
    challenge = issue_passkey_challenge(
        purpose=PasskeyChallenge.Purpose.AUTHENTICATION,
    )
    options = generate_authentication_options(
        rp_id=settings.WEBAUTHN_RP_ID,
        challenge=bytes(challenge.challenge),
        allow_credentials=None,
        user_verification=UserVerificationRequirement.REQUIRED,
    )
    return challenge, json.loads(options_to_json(options))


@transaction.atomic
def finish_passkey_authentication(*, challenge_id, credential, user_agent=""):
    now = timezone.now()
    try:
        challenge = PasskeyChallenge.objects.select_for_update().get(
            id=challenge_id,
            purpose=PasskeyChallenge.Purpose.AUTHENTICATION,
            consumed_at__isnull=True,
            expires_at__gt=now,
        )
        parsed_credential = parse_authentication_credential_json(credential)
        passkey = (
            PasskeyCredential.objects.select_for_update()
            .select_related("user")
            .get(
                credential_id=parsed_credential.raw_id,
                user__is_active=True,
            )
        )
    except (
        InvalidAuthenticationResponse,
        InvalidJSONStructure,
        PasskeyChallenge.DoesNotExist,
        PasskeyCredential.DoesNotExist,
        KeyError,
        TypeError,
        ValueError,
    ) as error:
        raise InvalidPasskeyChallenge from error

    user_handle = parsed_credential.response.user_handle
    if user_handle is None or user_handle != passkey.user_id.bytes:
        raise InvalidPasskeyChallenge

    try:
        verification = verify_authentication_response(
            credential=parsed_credential,
            expected_challenge=bytes(challenge.challenge),
            expected_rp_id=settings.WEBAUTHN_RP_ID,
            expected_origin=settings.WEBAUTHN_ORIGIN,
            credential_public_key=bytes(passkey.public_key),
            credential_current_sign_count=passkey.sign_count,
            require_user_verification=True,
        )
    except (InvalidAuthenticationResponse, InvalidSignature, TypeError, ValueError) as error:
        raise InvalidPasskeyChallenge from error

    if verification.credential_id != bytes(passkey.credential_id):
        raise InvalidPasskeyChallenge

    passkey.sign_count = verification.new_sign_count
    passkey.device_type = verification.credential_device_type.value
    passkey.backed_up = verification.credential_backed_up
    passkey.last_used_at = now
    passkey.save(
        update_fields=["sign_count", "device_type", "backed_up", "last_used_at"]
    )
    challenge.consumed_at = now
    challenge.save(update_fields=["consumed_at"])
    _, token_pair = create_auth_session(user=passkey.user, user_agent=user_agent)
    return passkey.user, token_pair
