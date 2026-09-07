import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APIClient

from apps.api.tests.test_organization_api import _authenticated_client

pytestmark = pytest.mark.django_db
GOOGLE_URL = "/api/v1/auth/google"
GOOGLE_LINK_URL = "/api/v1/auth/google/link"
TOKEN_URL = "/api/v1/auth/token"
PASSWORD_URL = "/api/v1/auth/password"
ACCOUNT_URL = "/api/v1/account"
CONTACTS_URL = "/api/v1/account/contacts"
CONTACT_VERIFY_URL = "/api/v1/account/contacts/verify"
PASSKEYS_URL = "/api/v1/auth/passkeys"
PASSKEY_REGISTRATION_OPTIONS_URL = "/api/v1/auth/passkeys/registration/options"
PASSKEY_REGISTRATION_VERIFY_URL = "/api/v1/auth/passkeys/registration/verify"
PASSKEY_AUTHENTICATION_OPTIONS_URL = "/api/v1/auth/passkeys/authentication/options"
PASSKEY_AUTHENTICATION_VERIFY_URL = "/api/v1/auth/passkeys/authentication/verify"


class FakePasskeyCeremony:
    def registration_options(self, *, user, challenge):
        return {"challenge": "registration-challenge", "rp": {"name": "Dotick"}}

    def verify_registration(self, *, credential, challenge):
        assert credential["id"] == "credential-one"
        return {
            "credential_id": "credential-one",
            "public_key": b"public-key-one",
            "sign_count": 0,
            "device_type": "single_device",
            "backed_up": False,
        }

    def authentication_options(self, *, challenge):
        return {"challenge": "authentication-challenge"}

    def verify_authentication(self, *, credential, challenge, stored_credential):
        assert stored_credential.credential_id == "credential-one"
        return {"new_sign_count": 1}


def test_google_only_account_signs_in_without_mandatory_fallback(settings):
    settings.GOOGLE_ID_TOKEN_VERIFIER = lambda credential: {
        "subject": "google-subject-1",
        "email": "google-only@example.test",
        "email_verified": True,
        "display_name": "Google Only",
    }
    anonymous = APIClient()

    signed_in = anonymous.post(GOOGLE_URL, {"credential": "valid-google-token"}, format="json")

    assert signed_in.status_code == 200
    assert set(signed_in.json()) == {"access", "refresh", "user", "fallback_recommended"}
    assert signed_in.json()["user"]["email"] == "google-only@example.test"
    assert signed_in.json()["fallback_recommended"] is True
    assert (
        anonymous.post(
            TOKEN_URL,
            {"email": "google-only@example.test", "password": "not-a-password"},
            format="json",
        ).status_code
        == 401
    )


def test_google_only_account_can_add_password_fallback(settings):
    settings.GOOGLE_ID_TOKEN_VERIFIER = lambda credential: {
        "subject": "google-subject-fallback",
        "email": "fallback@example.test",
        "email_verified": True,
        "display_name": "Fallback User",
    }
    anonymous = APIClient()
    google_tokens = anonymous.post(
        GOOGLE_URL,
        {"credential": "valid-google-token"},
        format="json",
    ).json()
    account = APIClient()
    account.credentials(HTTP_AUTHORIZATION=f"Bearer {google_tokens['access']}")

    added = account.put(
        PASSWORD_URL,
        {"password": "Independent-fallback-password-8!"},
        format="json",
    )
    settings.GOOGLE_ID_TOKEN_VERIFIER = lambda credential: (_ for _ in ()).throw(
        RuntimeError("provider unavailable")
    )
    password_sign_in = anonymous.post(
        TOKEN_URL,
        {
            "email": "fallback@example.test",
            "password": "Independent-fallback-password-8!",
        },
        format="json",
    )

    assert added.status_code == 204
    assert password_sign_in.status_code == 200


def test_existing_email_requires_authenticated_explicit_google_link(settings):
    owner, credentials = _authenticated_client(settings, "google_link")
    settings.GOOGLE_ID_TOKEN_VERIFIER = lambda credential: {
        "subject": "google-subject-2",
        "email": credentials["email"],
        "email_verified": True,
        "display_name": "Linked User",
    }
    anonymous = APIClient()

    refused = anonymous.post(GOOGLE_URL, {"credential": "valid-google-token"}, format="json")
    linked = owner.post(
        GOOGLE_LINK_URL,
        {"credential": "valid-google-token"},
        format="json",
    )
    signed_in = anonymous.post(GOOGLE_URL, {"credential": "valid-google-token"}, format="json")

    assert refused.status_code == 409
    assert refused.json()["error"]["code"] == "account_link_required"
    assert linked.status_code == 204
    assert signed_in.status_code == 200
    assert signed_in.json()["user"]["handle"] == "workspace_google_link"


def test_google_link_rejects_a_different_verified_email(settings):
    owner, _ = _authenticated_client(settings, "google_takeover")
    settings.GOOGLE_ID_TOKEN_VERIFIER = lambda credential: {
        "subject": "attacker-subject",
        "email": "attacker@example.test",
        "email_verified": True,
        "display_name": "Attacker",
    }

    refused = owner.post(
        GOOGLE_LINK_URL,
        {"credential": "valid-google-token"},
        format="json",
    )

    assert refused.status_code == 400
    assert get_user_model().objects.get(email__iexact="workspace-google_takeover@example.test")
    assert owner.get(ACCOUNT_URL).status_code == 200


def test_passkey_enrollment_and_passwordless_sign_in(settings):
    owner, credentials = _authenticated_client(settings, "passkey")
    settings.WEBAUTHN_CEREMONY = FakePasskeyCeremony()

    options = owner.post(
        PASSKEY_REGISTRATION_OPTIONS_URL,
        {"name": "Laptop"},
        format="json",
    )
    enrolled = owner.post(
        PASSKEY_REGISTRATION_VERIFY_URL,
        {
            "challenge_id": options.json()["challenge_id"],
            "credential": {"id": "credential-one", "response": {}},
        },
        format="json",
    )
    listed = owner.get(PASSKEYS_URL)

    anonymous = APIClient()
    auth_options = anonymous.post(PASSKEY_AUTHENTICATION_OPTIONS_URL, {}, format="json")
    signed_in = anonymous.post(
        PASSKEY_AUTHENTICATION_VERIFY_URL,
        {
            "challenge_id": auth_options.json()["challenge_id"],
            "credential": {"id": "credential-one", "response": {}},
        },
        format="json",
    )

    assert options.status_code == 200
    assert options.json()["public_key"]["challenge"] == "registration-challenge"
    assert enrolled.status_code == 201
    assert enrolled.json()["name"] == "Laptop"
    assert listed.status_code == 200
    assert listed.json()["results"][0]["id"] == enrolled.json()["id"]
    assert signed_in.status_code == 200
    assert signed_in.json()["user"]["email"] == credentials["email"]
    assert signed_in.json()["fallback_recommended"] is False


def test_passkey_challenge_is_scoped_expires_and_is_single_use(settings):
    owner, _ = _authenticated_client(settings, "passkey_replay")
    settings.WEBAUTHN_CEREMONY = FakePasskeyCeremony()
    options = owner.post(
        PASSKEY_REGISTRATION_OPTIONS_URL,
        {"name": "Security key"},
        format="json",
    )
    payload = {
        "challenge_id": options.json()["challenge_id"],
        "credential": {"id": "credential-one", "response": {}},
    }

    first = owner.post(PASSKEY_REGISTRATION_VERIFY_URL, payload, format="json")
    replay = owner.post(PASSKEY_REGISTRATION_VERIFY_URL, payload, format="json")
    other, _ = _authenticated_client(settings, "passkey_other")
    foreign = other.post(PASSKEY_REGISTRATION_VERIFY_URL, payload, format="json")

    expired_options = owner.post(
        PASSKEY_REGISTRATION_OPTIONS_URL,
        {"name": "Expired"},
        format="json",
    )
    from dotick.identity.models import PasskeyChallenge

    PasskeyChallenge.objects.filter(id=expired_options.json()["challenge_id"]).update(
        expires_at=timezone.now()
    )
    expired = owner.post(
        PASSKEY_REGISTRATION_VERIFY_URL,
        {
            "challenge_id": expired_options.json()["challenge_id"],
            "credential": {"id": "credential-two", "response": {}},
        },
        format="json",
    )

    assert first.status_code == 201
    assert replay.status_code == 400
    assert foreign.status_code == 400
    assert expired.status_code == 400
    assert replay.json()["error"]["code"] == "invalid_passkey_challenge"


def test_real_webauthn_adapter_generates_browser_options(settings):
    owner, _ = _authenticated_client(settings, "real_webauthn")

    generated = owner.post(
        PASSKEY_REGISTRATION_OPTIONS_URL,
        {"name": "Browser"},
        format="json",
    )

    assert generated.status_code == 200
    assert generated.json()["public_key"]["rp"]["id"] == "localhost"
    assert generated.json()["public_key"]["user"]["name"].endswith("@example.test")
    assert generated.json()["public_key"]["challenge"]
    assert generated.json()["public_key"]["authenticatorSelection"] == {
        "requireResidentKey": True,
        "residentKey": "required",
        "userVerification": "required",
    }


def test_secondary_contacts_are_inactive_until_code_verification(settings):
    owner, _ = _authenticated_client(settings, "contacts")
    delivered = []
    settings.CONTACT_CODE_DELIVERER = lambda **message: delivered.append(message)

    pending_email = owner.post(
        CONTACTS_URL,
        {"kind": "email", "value": "Second@Example.test"},
        format="json",
    )
    before_verification = owner.get(CONTACTS_URL)
    email_code = delivered[-1]["code"]
    verified_email = owner.post(
        CONTACT_VERIFY_URL,
        {"contact_id": pending_email.json()["id"], "code": email_code},
        format="json",
    )

    pending_phone = owner.post(
        CONTACTS_URL,
        {"kind": "phone", "value": "+4915112345678"},
        format="json",
    )
    phone_code = delivered[-1]["code"]
    verified_phone = owner.post(
        CONTACT_VERIFY_URL,
        {"contact_id": pending_phone.json()["id"], "code": phone_code},
        format="json",
    )
    active = owner.get(CONTACTS_URL)

    assert pending_email.status_code == 202
    assert before_verification.status_code == 200
    assert before_verification.json()["results"] == []
    assert verified_email.status_code == 204
    assert pending_phone.status_code == 202
    assert verified_phone.status_code == 204
    assert {(row["kind"], row["value"]) for row in active.json()["results"]} == {
        ("email", "second@example.test"),
        ("phone", "+4915112345678"),
    }


def test_verified_contact_cannot_be_claimed_by_another_account(settings):
    first, _ = _authenticated_client(settings, "contact_first")
    second, _ = _authenticated_client(settings, "contact_second")
    delivered = []
    settings.CONTACT_CODE_DELIVERER = lambda **message: delivered.append(message)

    first_pending = first.post(
        CONTACTS_URL,
        {"kind": "email", "value": "shared-contact@example.test"},
        format="json",
    )
    assert (
        first.post(
            CONTACT_VERIFY_URL,
            {"contact_id": first_pending.json()["id"], "code": delivered[-1]["code"]},
            format="json",
        ).status_code
        == 204
    )

    second_pending = second.post(
        CONTACTS_URL,
        {"kind": "email", "value": "SHARED-contact@example.test"},
        format="json",
    )
    conflict = second.post(
        CONTACT_VERIFY_URL,
        {"contact_id": second_pending.json()["id"], "code": delivered[-1]["code"]},
        format="json",
    )

    assert conflict.status_code == 409
    assert conflict.json()["error"]["code"] == "contact_unavailable"
