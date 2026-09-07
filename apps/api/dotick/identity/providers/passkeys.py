import base64
import json

from django.conf import settings
from rest_framework.exceptions import APIException


class PasskeyConfigurationUnavailable(APIException):
    status_code = 503
    default_detail = "Passkey configuration is unavailable."
    default_code = "passkey_configuration_unavailable"


class InvalidPasskeyCredential(APIException):
    status_code = 400
    default_detail = "Invalid Passkey credential."
    default_code = "invalid_passkey_credential"


def _b64url(value):
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode("ascii")


class WebAuthnCeremony:
    def _configuration(self):
        origins = [origin.strip() for origin in settings.WEBAUTHN_ORIGINS if origin.strip()]
        if not settings.WEBAUTHN_RP_ID or not origins:
            raise PasskeyConfigurationUnavailable
        return origins

    def registration_options(self, *, user, challenge):
        from webauthn import generate_registration_options, options_to_json
        from webauthn.helpers.structs import (
            AuthenticatorSelectionCriteria,
            ResidentKeyRequirement,
            UserVerificationRequirement,
        )

        self._configuration()
        options = generate_registration_options(
            rp_id=settings.WEBAUTHN_RP_ID,
            rp_name=settings.WEBAUTHN_RP_NAME,
            user_id=user.id.bytes,
            user_name=user.email,
            user_display_name=user.display_name,
            challenge=challenge,
            authenticator_selection=AuthenticatorSelectionCriteria(
                resident_key=ResidentKeyRequirement.REQUIRED,
                require_resident_key=True,
                user_verification=UserVerificationRequirement.REQUIRED,
            ),
        )
        return json.loads(options_to_json(options))

    def verify_registration(self, *, credential, challenge):
        from webauthn import verify_registration_response
        from webauthn.helpers.exceptions import WebAuthnException

        origins = self._configuration()
        try:
            verified = verify_registration_response(
                credential=credential,
                expected_challenge=challenge,
                expected_rp_id=settings.WEBAUTHN_RP_ID,
                expected_origin=origins,
                require_user_verification=True,
            )
        except (WebAuthnException, ValueError, TypeError) as error:
            raise InvalidPasskeyCredential from error
        return {
            "credential_id": _b64url(verified.credential_id),
            "public_key": verified.credential_public_key,
            "sign_count": verified.sign_count,
            "device_type": verified.credential_device_type.value,
            "backed_up": verified.credential_backed_up,
        }

    def authentication_options(self, *, challenge):
        from webauthn import generate_authentication_options, options_to_json
        from webauthn.helpers.structs import UserVerificationRequirement

        self._configuration()
        options = generate_authentication_options(
            rp_id=settings.WEBAUTHN_RP_ID,
            challenge=challenge,
            user_verification=UserVerificationRequirement.REQUIRED,
        )
        return json.loads(options_to_json(options))

    def verify_authentication(self, *, credential, challenge, stored_credential):
        from webauthn import verify_authentication_response
        from webauthn.helpers.exceptions import WebAuthnException

        origins = self._configuration()
        try:
            verified = verify_authentication_response(
                credential=credential,
                expected_challenge=challenge,
                expected_rp_id=settings.WEBAUTHN_RP_ID,
                expected_origin=origins,
                credential_public_key=bytes(stored_credential.public_key),
                credential_current_sign_count=stored_credential.sign_count,
                require_user_verification=True,
            )
        except (WebAuthnException, ValueError, TypeError) as error:
            raise InvalidPasskeyCredential from error
        return {"new_sign_count": verified.new_sign_count}


def get_passkey_ceremony():
    configured = getattr(settings, "WEBAUTHN_CEREMONY", None)
    return configured or WebAuthnCeremony()
