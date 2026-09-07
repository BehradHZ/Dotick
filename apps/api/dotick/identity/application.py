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

from dotick.identity.models import AuthSession, VerificationChallenge

VERIFICATION_TTL = timedelta(minutes=10)
CHALLENGE_COOLDOWN = timedelta(minutes=1)
CHALLENGE_HOURLY_LIMIT = 5
MAX_CODE_ATTEMPTS = 5


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


@transaction.atomic
def create_token_pair(*, email, password, user_agent=""):
    user = authenticate(username=normalize_email(email), password=password)
    if user is None or user.email_verified_at is None:
        raise InvalidCredentials
    session = AuthSession.objects.create(
        user=user,
        refresh_jti=f"pending-{uuid.uuid4()}",
        user_agent=user_agent[:200],
    )
    return {
        **_tokens_for_session(user=user, session=session),
        "user": {
            "email": user.email,
            "handle": user.handle,
            "display_name": user.display_name,
        },
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
