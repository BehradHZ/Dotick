import secrets
import uuid
from datetime import timedelta

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.mail import send_mail
from django.db import IntegrityError, transaction
from django.utils import timezone
from django.utils.crypto import constant_time_compare, salted_hmac
from rest_framework.exceptions import APIException, NotFound, ValidationError
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from dotick.identity.models import (
    AccountContact,
    AuthSession,
    ContactVerificationChallenge,
    ExternalIdentity,
    PasskeyChallenge,
    PasskeyCredential,
    VerificationChallenge,
)
from dotick.identity.providers.google import verify_google_credential
from dotick.identity.providers.passkeys import get_passkey_ceremony

VERIFICATION_TTL = timedelta(minutes=10)
CHALLENGE_COOLDOWN = timedelta(minutes=1)
CHALLENGE_HOURLY_LIMIT = 5
MAX_CODE_ATTEMPTS = 5
PASSKEY_CHALLENGE_TTL = timedelta(minutes=5)
RECENT_AUTH_TTL = timedelta(minutes=10)
UNSET = object()


class InvalidVerificationCode(APIException):
    status_code = 400
    default_detail = "Invalid or expired verification code."
    default_code = "invalid_verification_code"


class InvalidCredentials(APIException):
    status_code = 401
    default_detail = "Invalid credentials."
    default_code = "authentication_failed"


class InvalidRefreshToken(APIException):
    status_code = 401
    default_detail = "Refresh token is invalid or revoked."
    default_code = "token_not_valid"


class AccountLinkRequired(APIException):
    status_code = 409
    default_detail = "Sign in to the existing account before linking Google."
    default_code = "account_link_required"


class ExternalIdentityConflict(APIException):
    status_code = 409
    default_detail = "This Google identity is already linked to another account."
    default_code = "external_identity_conflict"


class RecentAuthenticationRequired(APIException):
    status_code = 403
    default_detail = "Recent authentication is required."
    default_code = "recent_authentication_required"


class InvalidPasskeyChallenge(APIException):
    status_code = 400
    default_detail = "Invalid, expired or consumed Passkey challenge."
    default_code = "invalid_passkey_challenge"


class PasskeyAlreadyRegistered(APIException):
    status_code = 409
    default_detail = "This Passkey is already registered."
    default_code = "passkey_already_registered"


class HandleUnavailable(APIException):
    status_code = 409
    default_detail = "This handle is unavailable."
    default_code = "handle_unavailable"


class ContactUnavailable(APIException):
    status_code = 409
    default_detail = "This contact is already active on another account."
    default_code = "contact_unavailable"


class ContactDeliveryUnavailable(APIException):
    status_code = 503
    default_detail = "Contact verification delivery is unavailable."
    default_code = "contact_delivery_unavailable"


def normalize_email(email):
    return email.strip().lower()


def _digest_code(*, user_id, purpose, code):
    value = f"{user_id}:{purpose}:{code}"
    return salted_hmac("dotick.identity.verification-code", value).hexdigest()


def _issue_challenge(*, user, purpose):
    now = timezone.now()
    recent = VerificationChallenge.objects.filter(user=user, purpose=purpose)
    latest = recent.order_by("-created_at").first()
    if latest is not None and latest.created_at > now - CHALLENGE_COOLDOWN:
        return None
    if recent.filter(created_at__gte=now - timedelta(hours=1)).count() >= CHALLENGE_HOURLY_LIMIT:
        return None
    code = f"{secrets.randbelow(1_000_000):06d}"
    VerificationChallenge.objects.filter(
        user=user,
        purpose=purpose,
        consumed_at__isnull=True,
    ).update(consumed_at=now)
    VerificationChallenge.objects.create(
        user=user,
        purpose=purpose,
        code_digest=_digest_code(user_id=user.id, purpose=purpose, code=code),
        expires_at=now + VERIFICATION_TTL,
    )
    return code


def _send_verification_email(*, user, code):
    send_mail(
        subject="Verify your Dotick email",
        message=f"Your Dotick verification code is {code}. It expires in 10 minutes.",
        from_email=None,
        recipient_list=[user.email],
    )


def _send_password_reset_email(*, user, code):
    send_mail(
        subject="Reset your Dotick password",
        message=f"Your Dotick password reset code is {code}. It expires in 10 minutes.",
        from_email=None,
        recipient_list=[user.email],
    )


def register(*, email, password, handle, display_name):
    user_model = get_user_model()
    normalized_email = normalize_email(email)
    code = None
    user = None
    with transaction.atomic():
        existing = (
            user_model.objects.select_for_update().filter(email__iexact=normalized_email).first()
        )
        if existing:
            if existing.email_verified_at is None:
                user = existing
                code = _issue_challenge(
                    user=user,
                    purpose=VerificationChallenge.Purpose.EMAIL_VERIFICATION,
                )
        else:
            try:
                user = user_model.objects.create_user(
                    email=normalized_email,
                    password=password,
                    handle=handle.strip(),
                    display_name=display_name.strip(),
                    is_active=False,
                )
            except IntegrityError as error:
                raise ValidationError({"handle": ["This handle is unavailable."]}) from error
            code = _issue_challenge(
                user=user,
                purpose=VerificationChallenge.Purpose.EMAIL_VERIFICATION,
            )
    if user is not None and code is not None:
        _send_verification_email(user=user, code=code)


def resend_email_verification(*, email):
    user_model = get_user_model()
    user = None
    code = None
    with transaction.atomic():
        user = (
            user_model.objects.select_for_update()
            .filter(
                email__iexact=normalize_email(email),
                email_verified_at__isnull=True,
            )
            .first()
        )
        if user is not None:
            code = _issue_challenge(
                user=user,
                purpose=VerificationChallenge.Purpose.EMAIL_VERIFICATION,
            )
    if user is not None and code is not None:
        _send_verification_email(user=user, code=code)


def verify_email(*, email, code):
    user_model = get_user_model()
    valid = False
    with transaction.atomic():
        try:
            user = user_model.objects.select_for_update().get(email__iexact=normalize_email(email))
            challenge = (
                VerificationChallenge.objects.select_for_update()
                .filter(
                    user=user,
                    purpose=VerificationChallenge.Purpose.EMAIL_VERIFICATION,
                    consumed_at__isnull=True,
                )
                .latest("created_at")
            )
        except user_model.DoesNotExist, VerificationChallenge.DoesNotExist:
            pass
        else:
            now = timezone.now()
            expected = _digest_code(
                user_id=user.id,
                purpose=VerificationChallenge.Purpose.EMAIL_VERIFICATION,
                code=code,
            )
            if (
                challenge.expires_at <= now
                or challenge.failed_attempts >= MAX_CODE_ATTEMPTS
                or not constant_time_compare(challenge.code_digest, expected)
            ):
                challenge.failed_attempts += 1
                if challenge.failed_attempts >= MAX_CODE_ATTEMPTS:
                    challenge.consumed_at = now
                challenge.save(update_fields=["failed_attempts", "consumed_at"])
            else:
                challenge.consumed_at = now
                challenge.save(update_fields=["consumed_at"])
                user.email_verified_at = now
                user.is_active = True
                user.save(update_fields=["email_verified_at", "is_active"])
                valid = True
    if not valid:
        raise InvalidVerificationCode


def request_password_reset(*, email):
    user_model = get_user_model()
    user = None
    code = None
    with transaction.atomic():
        user = (
            user_model.objects.select_for_update()
            .filter(
                email__iexact=normalize_email(email),
                email_verified_at__isnull=False,
                is_active=True,
            )
            .first()
        )
        if user is not None:
            code = _issue_challenge(
                user=user,
                purpose=VerificationChallenge.Purpose.PASSWORD_RESET,
            )
    if user is not None and code is not None:
        _send_password_reset_email(user=user, code=code)


def reset_password(*, email, code, password):
    user_model = get_user_model()
    valid = False
    with transaction.atomic():
        try:
            user = user_model.objects.select_for_update().get(
                email__iexact=normalize_email(email),
                email_verified_at__isnull=False,
                is_active=True,
            )
            challenge = (
                VerificationChallenge.objects.select_for_update()
                .filter(
                    user=user,
                    purpose=VerificationChallenge.Purpose.PASSWORD_RESET,
                    consumed_at__isnull=True,
                )
                .latest("created_at")
            )
        except user_model.DoesNotExist, VerificationChallenge.DoesNotExist:
            pass
        else:
            now = timezone.now()
            expected = _digest_code(
                user_id=user.id,
                purpose=VerificationChallenge.Purpose.PASSWORD_RESET,
                code=code,
            )
            if (
                challenge.expires_at <= now
                or challenge.failed_attempts >= MAX_CODE_ATTEMPTS
                or not constant_time_compare(challenge.code_digest, expected)
            ):
                challenge.failed_attempts += 1
                if challenge.failed_attempts >= MAX_CODE_ATTEMPTS:
                    challenge.consumed_at = now
                challenge.save(update_fields=["failed_attempts", "consumed_at"])
            else:
                try:
                    validate_password(password, user=user)
                except DjangoValidationError as error:
                    raise ValidationError({"password": error.messages}) from error
                challenge.consumed_at = now
                challenge.save(update_fields=["consumed_at"])
                user.set_password(password)
                user.save(update_fields=["password"])
                AuthSession.objects.filter(user=user, revoked_at__isnull=True).update(
                    revoked_at=now
                )
                valid = True
    if not valid:
        raise InvalidVerificationCode


def _tokens_for_session(*, user, session):
    refresh = RefreshToken.for_user(user)
    refresh["sid"] = str(session.id)
    session.refresh_jti = refresh["jti"]
    session.last_seen_at = timezone.now()
    session.save(update_fields=["refresh_jti", "last_seen_at"])
    return {"access": str(refresh.access_token), "refresh": str(refresh)}


def _public_user(user):
    return {
        "email": user.email,
        "handle": user.handle,
        "display_name": user.display_name,
    }


def create_token_pair_for_user(*, user, user_agent=""):
    session = AuthSession.objects.create(
        user=user,
        refresh_jti=f"pending-{uuid.uuid4()}",
        user_agent=user_agent[:200],
    )
    return {**_tokens_for_session(user=user, session=session), "user": _public_user(user)}


def ensure_recent_authentication(session):
    if session.created_at <= timezone.now() - RECENT_AUTH_TTL:
        raise RecentAuthenticationRequired


def account_presentation(*, user):
    try:
        account_timezone = user.preferences.timezone
    except AttributeError:
        account_timezone = None
    return {
        "id": user.id,
        "email": user.email,
        "handle": user.handle,
        "display_name": user.display_name,
        "profile_picture_url": user.profile_picture_url,
        "timezone": account_timezone,
        "authentication_methods": {
            "password": user.has_usable_password(),
            "google": ExternalIdentity.objects.filter(
                user=user, provider=ExternalIdentity.Provider.GOOGLE
            ).exists(),
            "passkey": PasskeyCredential.objects.filter(user=user).exists(),
        },
    }


@transaction.atomic
def update_account(
    *,
    user_id,
    handle=UNSET,
    display_name=UNSET,
    profile_picture_url=UNSET,
    timezone_name=UNSET,
):
    from dotick.organization.models import UserPreferences

    user = get_user_model().objects.select_for_update().get(id=user_id)
    changed_fields = []
    if handle is not UNSET:
        user.handle = handle.strip()
        changed_fields.append("handle")
    if display_name is not UNSET:
        user.display_name = display_name.strip()
        changed_fields.append("display_name")
    if profile_picture_url is not UNSET:
        user.profile_picture_url = profile_picture_url or None
        changed_fields.append("profile_picture_url")
    if changed_fields:
        try:
            with transaction.atomic():
                user.save(update_fields=changed_fields)
        except IntegrityError as error:
            raise HandleUnavailable from error
    if timezone_name is not UNSET:
        UserPreferences.objects.update_or_create(
            user=user,
            defaults={"timezone": timezone_name},
        )
    return get_user_model().objects.get(id=user.id)


@transaction.atomic
def set_password(*, user, session, password, current_password=None):
    ensure_recent_authentication(session)
    if user.has_usable_password() and not user.check_password(current_password or ""):
        raise InvalidCredentials
    try:
        validate_password(password, user=user)
    except DjangoValidationError as error:
        raise ValidationError({"password": error.messages}) from error
    user.set_password(password)
    user.save(update_fields=["password"])
    AuthSession.objects.filter(user=user, revoked_at__isnull=True).exclude(id=session.id).update(
        revoked_at=timezone.now()
    )


def _contact_code_digest(*, contact_id, code):
    return salted_hmac(
        "dotick.identity.contact-verification-code",
        f"{contact_id}:{code}",
    ).hexdigest()


def _deliver_contact_code(*, kind, value, code):
    from django.conf import settings

    deliverer = getattr(settings, "CONTACT_CODE_DELIVERER", None)
    if callable(deliverer):
        deliverer(kind=kind, value=value, code=code)
        return
    if kind == AccountContact.Kind.EMAIL:
        send_mail(
            subject="Verify your Dotick contact",
            message=f"Your Dotick contact verification code is {code}. It expires in 10 minutes.",
            from_email=None,
            recipient_list=[value],
        )
        return
    raise ContactDeliveryUnavailable


def request_contact_verification(*, user, kind, value):
    normalized = value.strip().lower() if kind == AccountContact.Kind.EMAIL else value.strip()
    if (
        kind == AccountContact.Kind.EMAIL
        and get_user_model().objects.filter(email__iexact=normalized).exists()
    ):
        raise ContactUnavailable
    with transaction.atomic():
        contact, _ = AccountContact.objects.get_or_create(
            user=user,
            kind=kind,
            normalized_value=normalized,
            defaults={"value": normalized},
        )
        if contact.verified_at is not None:
            return contact
        code = f"{secrets.randbelow(1_000_000):06d}"
        now = timezone.now()
        ContactVerificationChallenge.objects.filter(
            contact=contact,
            consumed_at__isnull=True,
        ).update(consumed_at=now)
        ContactVerificationChallenge.objects.create(
            contact=contact,
            code_digest=_contact_code_digest(contact_id=contact.id, code=code),
            expires_at=now + VERIFICATION_TTL,
        )
    _deliver_contact_code(kind=contact.kind, value=contact.value, code=code)
    return contact


def verify_contact(*, user, contact_id, code):
    valid = False
    conflict = False
    with transaction.atomic():
        try:
            contact = AccountContact.objects.select_for_update().get(
                id=contact_id,
                user=user,
                verified_at__isnull=True,
            )
            challenge = (
                ContactVerificationChallenge.objects.select_for_update()
                .filter(contact=contact, consumed_at__isnull=True)
                .latest("created_at")
            )
        except AccountContact.DoesNotExist, ContactVerificationChallenge.DoesNotExist:
            pass
        else:
            now = timezone.now()
            expected = _contact_code_digest(contact_id=contact.id, code=code)
            if (
                challenge.expires_at <= now
                or challenge.failed_attempts >= MAX_CODE_ATTEMPTS
                or not constant_time_compare(challenge.code_digest, expected)
            ):
                challenge.failed_attempts += 1
                if challenge.failed_attempts >= MAX_CODE_ATTEMPTS:
                    challenge.consumed_at = now
                challenge.save(update_fields=["failed_attempts", "consumed_at"])
            elif (
                AccountContact.objects.filter(
                    kind=contact.kind,
                    normalized_value=contact.normalized_value,
                    verified_at__isnull=False,
                )
                .exclude(user=user)
                .exists()
            ):
                conflict = True
            else:
                try:
                    with transaction.atomic():
                        contact.verified_at = now
                        contact.save(update_fields=["verified_at"])
                except IntegrityError:
                    conflict = True
                else:
                    challenge.consumed_at = now
                    challenge.save(update_fields=["consumed_at"])
                    valid = True
    if conflict:
        raise ContactUnavailable
    if not valid:
        raise InvalidVerificationCode


def list_contacts(*, user):
    return AccountContact.objects.filter(user=user, verified_at__isnull=False).order_by(
        "kind", "created_at"
    )


def delete_contact(*, user, contact_id):
    deleted, _ = AccountContact.objects.filter(id=contact_id, user=user).delete()
    if not deleted:
        raise NotFound("Contact not found.")


@transaction.atomic
def create_token_pair(*, email, password, user_agent=""):
    user = authenticate(username=normalize_email(email), password=password)
    if user is None or user.email_verified_at is None:
        raise InvalidCredentials
    return create_token_pair_for_user(user=user, user_agent=user_agent)


@transaction.atomic
def sign_in_with_google(*, credential, user_agent=""):
    claims = verify_google_credential(credential)
    now = timezone.now()
    identity = (
        ExternalIdentity.objects.select_for_update()
        .select_related("user")
        .filter(provider=ExternalIdentity.Provider.GOOGLE, subject=claims["subject"])
        .first()
    )
    if identity is not None:
        if not identity.user.is_active:
            raise InvalidCredentials
        identity.provider_email = claims["email"]
        identity.last_used_at = now
        identity.save(update_fields=["provider_email", "last_used_at"])
        user = identity.user
    else:
        user_model = get_user_model()
        if user_model.objects.filter(email__iexact=claims["email"]).exists():
            raise AccountLinkRequired
        try:
            with transaction.atomic():
                user = user_model.objects.create_user(
                    email=claims["email"],
                    password=None,
                    display_name=claims["display_name"],
                    email_verified_at=now,
                    is_active=True,
                )
                ExternalIdentity.objects.create(
                    user=user,
                    provider=ExternalIdentity.Provider.GOOGLE,
                    subject=claims["subject"],
                    provider_email=claims["email"],
                    last_used_at=now,
                )
        except IntegrityError as error:
            identity = (
                ExternalIdentity.objects.select_related("user")
                .filter(
                    provider=ExternalIdentity.Provider.GOOGLE,
                    subject=claims["subject"],
                )
                .first()
            )
            if identity is not None:
                user = identity.user
            elif user_model.objects.filter(email__iexact=claims["email"]).exists():
                raise AccountLinkRequired from error
            else:
                raise ExternalIdentityConflict from error
    return {
        **create_token_pair_for_user(user=user, user_agent=user_agent),
        "fallback_recommended": not user.has_usable_password(),
    }


@transaction.atomic
def link_google_identity(*, user, session, credential):
    ensure_recent_authentication(session)
    claims = verify_google_credential(credential)
    if normalize_email(claims["email"]) != normalize_email(user.email):
        raise ValidationError({"credential": ["Google email must match the account email."]})
    identity = (
        ExternalIdentity.objects.select_for_update()
        .filter(provider=ExternalIdentity.Provider.GOOGLE, subject=claims["subject"])
        .first()
    )
    if identity is not None and identity.user_id != user.id:
        raise ExternalIdentityConflict
    if identity is None:
        try:
            ExternalIdentity.objects.create(
                user=user,
                provider=ExternalIdentity.Provider.GOOGLE,
                subject=claims["subject"],
                provider_email=claims["email"],
            )
        except IntegrityError as error:
            raise ExternalIdentityConflict from error


def _passkey_output(row):
    return {
        "id": row.id,
        "name": row.name,
        "device_type": row.device_type,
        "backed_up": row.backed_up,
        "created_at": row.created_at,
        "last_used_at": row.last_used_at,
    }


@transaction.atomic
def begin_passkey_registration(*, user, session, name):
    ensure_recent_authentication(session)
    raw_challenge = secrets.token_bytes(32)
    row = PasskeyChallenge.objects.create(
        user=user,
        purpose=PasskeyChallenge.Purpose.REGISTRATION,
        challenge=raw_challenge,
        credential_name=name.strip(),
        expires_at=timezone.now() + PASSKEY_CHALLENGE_TTL,
    )
    options = get_passkey_ceremony().registration_options(
        user=user,
        challenge=raw_challenge,
    )
    return {"challenge_id": row.id, "public_key": options}


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
    challenge.consumed_at = now
    challenge.save(update_fields=["consumed_at"])
    verified = get_passkey_ceremony().verify_registration(
        credential=credential,
        challenge=bytes(challenge.challenge),
    )
    try:
        row = PasskeyCredential.objects.create(
            user=user,
            credential_id=verified["credential_id"],
            public_key=verified["public_key"],
            sign_count=verified["sign_count"],
            device_type=verified["device_type"],
            backed_up=verified["backed_up"],
            transports=credential.get("response", {}).get("transports", []),
            name=challenge.credential_name,
        )
    except IntegrityError as error:
        raise PasskeyAlreadyRegistered from error
    return _passkey_output(row)


def list_passkeys(*, user):
    return [_passkey_output(row) for row in PasskeyCredential.objects.filter(user=user)]


def delete_passkey(*, user, passkey_id):
    deleted, _ = PasskeyCredential.objects.filter(id=passkey_id, user=user).delete()
    if not deleted:
        raise NotFound("Passkey not found.")


def begin_passkey_authentication():
    raw_challenge = secrets.token_bytes(32)
    row = PasskeyChallenge.objects.create(
        purpose=PasskeyChallenge.Purpose.AUTHENTICATION,
        challenge=raw_challenge,
        expires_at=timezone.now() + PASSKEY_CHALLENGE_TTL,
    )
    options = get_passkey_ceremony().authentication_options(challenge=raw_challenge)
    return {"challenge_id": row.id, "public_key": options}


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
    except PasskeyChallenge.DoesNotExist as error:
        raise InvalidPasskeyChallenge from error
    challenge.consumed_at = now
    challenge.save(update_fields=["consumed_at"])
    credential_id = str(credential.get("id", ""))
    try:
        stored = (
            PasskeyCredential.objects.select_for_update()
            .select_related("user")
            .get(
                credential_id=credential_id,
                user__is_active=True,
            )
        )
    except PasskeyCredential.DoesNotExist as error:
        raise InvalidCredentials from error
    verified = get_passkey_ceremony().verify_authentication(
        credential=credential,
        challenge=bytes(challenge.challenge),
        stored_credential=stored,
    )
    stored.sign_count = verified["new_sign_count"]
    stored.last_used_at = now
    stored.save(update_fields=["sign_count", "last_used_at"])
    return {
        **create_token_pair_for_user(user=stored.user, user_agent=user_agent),
        "fallback_recommended": False,
    }


@transaction.atomic
def rotate_refresh_token(*, encoded_token):
    try:
        token = RefreshToken(encoded_token)
        session = AuthSession.objects.select_for_update().get(
            id=token.get("sid"),
            user_id=token.get("user_id"),
            revoked_at__isnull=True,
        )
    except (TokenError, AuthSession.DoesNotExist, ValueError, TypeError) as error:
        raise InvalidRefreshToken from error
    if session.refresh_jti != token.get("jti") or not session.user.is_active:
        raise InvalidRefreshToken
    return _tokens_for_session(user=session.user, session=session)


def list_sessions(*, user_id, current_session_id):
    rows = AuthSession.objects.filter(user_id=user_id, revoked_at__isnull=True).order_by(
        "-last_seen_at"
    )
    return [
        {
            "id": row.id,
            "user_agent": row.user_agent,
            "created_at": row.created_at,
            "last_seen_at": row.last_seen_at,
            "current": row.id == current_session_id,
        }
        for row in rows
    ]


def revoke_session(*, user_id, session_id):
    updated = AuthSession.objects.filter(
        id=session_id,
        user_id=user_id,
        revoked_at__isnull=True,
    ).update(revoked_at=timezone.now())
    if not updated:
        raise NotFound("Session not found.")


def revoke_all_sessions(*, user_id):
    AuthSession.objects.filter(user_id=user_id, revoked_at__isnull=True).update(
        revoked_at=timezone.now()
    )
