from django.contrib.auth import authenticate, get_user_model
from django.core.mail import send_mail
from django.db import IntegrityError, models, transaction
from django.utils import timezone
from rest_framework.exceptions import APIException, PermissionDenied, ValidationError

from dotick.identity.challenges import (
    ChallengeIssuanceBlocked,
    issue_challenge,
    try_consume_challenge,
)
from dotick.identity.google_identity import (
    GoogleProviderUnavailable,
    InvalidGoogleCredential,
    verify_google_id_credential,
)
from dotick.identity.models import ExternalIdentity, VerificationChallenge
from dotick.identity.sessions import InvalidSessionToken as SessionTokenError
from dotick.identity.sessions import (
    RecentAuthenticationRequired,
    create_auth_session,
    require_recent_authentication,
    revoke_all_sessions,
    revoke_other_sessions,
    rotate_refresh_token,
)


class InvalidVerificationCode(APIException):
    status_code = 400
    default_detail = "Invalid or expired verification code."
    default_code = "invalid_verification_code"


class InvalidCredentials(APIException):
    status_code = 401
    default_detail = "Invalid credentials."
    default_code = "invalid_credentials"


class InvalidSessionToken(APIException):
    status_code = 401
    default_detail = "Token or session is invalid."
    default_code = "token_not_valid"


class InvalidExternalAuthentication(APIException):
    status_code = 401
    default_detail = "External credential is invalid."
    default_code = "invalid_external_credential"


class AccountLinkRequired(APIException):
    status_code = 409
    default_detail = "Authenticate to the existing account before linking Google."
    default_code = "account_link_required"


class ExternalProviderUnavailable(APIException):
    status_code = 503
    default_detail = "External authentication provider is unavailable."
    default_code = "provider_unavailable"


class ExternalIdentityConflict(APIException):
    status_code = 409
    default_detail = "External identity is already linked."
    default_code = "external_identity_conflict"


def normalize_email(email):
    return get_user_model().objects.normalize_email(email).strip().lower()


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


def request_password_reset(*, email):
    user_model = get_user_model()
    recipient = None
    code = None

    with transaction.atomic():
        recipient = (
            user_model.objects.select_for_update()
            .filter(
                email__iexact=normalize_email(email),
                email_verified_at__isnull=False,
                is_active=True,
            )
            .first()
        )
        if recipient is not None:
            try:
                code = issue_challenge(
                    user=recipient,
                    purpose=VerificationChallenge.Purpose.PASSWORD_RESET,
                )
            except ChallengeIssuanceBlocked:
                code = None

    if recipient is not None and code is not None:
        _send_password_reset_email(user=recipient, code=code)


def confirm_password_reset(*, email, code, password):
    user_model = get_user_model()
    changed = False

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
            challenge = try_consume_challenge(
                user=user,
                purpose=VerificationChallenge.Purpose.PASSWORD_RESET,
                code=code,
            )
            if challenge is not None:
                user.set_password(password)
                user.save(update_fields=["password"])
                revoke_all_sessions(user=user)
                changed = True

    if not changed:
        raise InvalidVerificationCode


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


def login_with_password(*, email, password, user_agent=""):
    user = authenticate(
        email=normalize_email(email),
        password=password,
    )
    if user is None or not user.is_active or user.email_verified_at is None:
        raise InvalidCredentials

    _, token_pair = create_auth_session(
        user=user,
        user_agent=user_agent,
    )
    return user, token_pair


def refresh_session(*, refresh):
    try:
        return rotate_refresh_token(encoded_refresh=refresh)
    except SessionTokenError as error:
        raise InvalidSessionToken from error


@transaction.atomic
def set_password(*, user, session, password, current_password=None):
    try:
        require_recent_authentication(session=session)
    except RecentAuthenticationRequired as error:
        raise PermissionDenied(
            "Recent authentication is required.",
            code="recent_auth_required",
        ) from error

    locked_user = get_user_model().objects.select_for_update().get(pk=user.pk)
    if locked_user.has_usable_password():
        if not current_password:
            raise ValidationError({"current_password": ["Current password is required."]})
        if not locked_user.check_password(current_password):
            raise ValidationError({"current_password": ["Current password is invalid."]})

    locked_user.set_password(password)
    locked_user.save(update_fields=["password"])
    revoke_other_sessions(user=locked_user, current_session=session)


def _fallback_recommended(user):
    return not user.has_usable_password() and not user.passkey_credentials.exists()


def _verify_google_credential(credential):
    try:
        return verify_google_id_credential(credential)
    except InvalidGoogleCredential as error:
        raise InvalidExternalAuthentication from error
    except GoogleProviderUnavailable as error:
        raise ExternalProviderUnavailable from error


def sign_in_with_google(*, credential, user_agent=""):
    claims = _verify_google_credential(credential)
    user_model = get_user_model()

    with transaction.atomic():
        identity = (
            ExternalIdentity.objects.select_for_update()
            .select_related("user")
            .filter(
                provider=ExternalIdentity.Provider.GOOGLE,
                subject=claims.subject,
            )
            .first()
        )
        if identity is not None:
            user = identity.user
        else:
            if user_model.objects.filter(email__iexact=claims.email).exists():
                raise AccountLinkRequired

            try:
                with transaction.atomic():
                    user = user_model.objects.create_user(
                        email=claims.email,
                        password=None,
                        display_name=claims.display_name[:120],
                        profile_picture_url=(claims.picture_url or "")[:2048] or None,
                        email_verified_at=timezone.now(),
                        is_active=True,
                    )
                    ExternalIdentity.objects.create(
                        user=user,
                        provider=ExternalIdentity.Provider.GOOGLE,
                        subject=claims.subject,
                    )
            except IntegrityError:
                identity = (
                    ExternalIdentity.objects.select_related("user")
                    .filter(
                        provider=ExternalIdentity.Provider.GOOGLE,
                        subject=claims.subject,
                    )
                    .first()
                )
                if identity is None:
                    raise AccountLinkRequired from None
                user = identity.user

        if not user.is_active:
            raise InvalidExternalAuthentication

        _, token_pair = create_auth_session(user=user, user_agent=user_agent)

    return user, token_pair, _fallback_recommended(user)


def link_google_identity(*, user, session, credential):
    try:
        require_recent_authentication(session=session)
    except RecentAuthenticationRequired as error:
        raise PermissionDenied(
            "Recent authentication is required.",
            code="recent_auth_required",
        ) from error

    claims = _verify_google_credential(credential)
    with transaction.atomic():
        locked_user = get_user_model().objects.select_for_update().get(pk=user.pk)
        existing = (
            ExternalIdentity.objects.select_for_update()
            .filter(provider=ExternalIdentity.Provider.GOOGLE)
            .filter(models.Q(subject=claims.subject) | models.Q(user=locked_user))
            .first()
        )
        if existing is not None:
            if existing.user_id == locked_user.id and existing.subject == claims.subject:
                return
            raise ExternalIdentityConflict

        try:
            with transaction.atomic():
                ExternalIdentity.objects.create(
                    user=locked_user,
                    provider=ExternalIdentity.Provider.GOOGLE,
                    subject=claims.subject,
                )
        except IntegrityError as error:
            raise ExternalIdentityConflict from error
