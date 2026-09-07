# Dotick Authentication Design

> **Status:** Increment 1 email/password baseline; Google and Passkey adapters pending
> **Date:** 2026-09-07
> **Decision sources:** System Definition §6.13; DR-048, DR-061, DR-128; SRS-AUTH-001..013

## 1. Scope

This design defines the shared Account identity, verified email/password flow and revocable JWT session boundary. It also fixes the account-linking rules that later Google and Passkey adapters must follow. Provider-specific implementation remains in Increment 1 delivery order 4.

The public API contract is [`openapi.json`](openapi.json). The I0 HTTP Basic workbench remains isolated behind its local/test-only guard and is not a product authentication method.

## 2. Account identity

- Internal Account identity is the existing UUID `User.id`; authentication methods never replace it.
- Every Account has a case-insensitively unique mutable `handle`, a nonunique `display_name`, and an optional profile picture added with the later presentation slice.
- Product registration accepts handles matching `[A-Za-z0-9_]{3,30}`. Framework-created developer accounts receive a generated collision-resistant handle so the database invariant remains true.
- Email is normalized to trimmed lowercase and remains case-insensitively unique.
- A registration email may exist as a pending credential candidate, but the Account stays inactive and `email_verified_at` stays null until verification succeeds. Pending email must not authenticate or participate in contact discovery.

## 3. Password and email verification

- Django's password validation and hashing APIs own password processing. Argon2 is the preferred hasher; plaintext is never persisted or logged.
- Verification and reset codes are six decimal digits generated with Python's cryptographic `secrets` API.
- Only a keyed HMAC digest bound to User UUID, challenge purpose and code is stored. The code is sent through Django's email adapter and never returned by the API.
- A challenge expires after 10 minutes, is single-use, and is invalidated when a newer challenge for the same Account and purpose is issued.
- Five failed attempts consume a challenge. Issuance has a 60-second cooldown and a maximum of five issued challenges per Account and purpose per hour.
- Registration, resend and password-reset request return the same `202 {"status":"accepted"}` result when an email is unknown, already registered, or currently rate-limited. Public deployment must add network/IP abuse controls at the edge; Account-level database limits do not replace them.
- Password reset requires a verified active email. Success changes the password through Django and revokes every active session.
- Automated tests use Django's in-memory email backend. A real delivery-provider smoke test remains an Increment 1 release gate; delivery transport never owns challenge validity.

## 4. JWT sessions

- `djangorestframework-simplejwt` 5.5.1 and PyJWT 2.13.0 provide JWT encoding and validation. Dotick does not implement signing primitives.
- Access tokens expire after 5 minutes. Refresh tokens expire after 30 days.
- Production uses a dedicated `DJANGO_JWT_SIGNING_KEY` of at least 50 characters. Local/test may fall back to the Django secret for developer convenience. Keys and tokens never enter source or ordinary logs.
- Each login creates an `AuthSession` UUID. Both access and refresh tokens carry its `sid`; the server stores only the current refresh-token `jti` for that session.
- Every refresh rotates both tokens under a row lock and replaces the stored `jti`. Reusing an older refresh token fails.
- Every authenticated API request verifies that `sid` belongs to the token User and has not been revoked. Revoking a session therefore rejects its existing access and refresh tokens immediately rather than waiting for expiry.
- Users can list active sessions, revoke one owned session, revoke the current session, or revoke all sessions. Session lookup is always scoped by current User UUID.

## 5. Browser boundary, CORS and CSRF

- Tokens use the `Authorization: Bearer` header. The initial PWA adapter may retain them in memory; browser `localStorage` is not the default or an approved persistence choice.
- Refresh tokens are returned only in JSON over TLS. Platform clients must use an approved secure-storage adapter before persistent token storage is added.
- Current bearer-header requests do not use ambient cookies, so cookie CSRF does not apply to these endpoints. If a later PWA design moves refresh credentials into cookies, it must enable `Secure`, `HttpOnly`, appropriate `SameSite`, CSRF tokens and credentialed CORS together, then update this contract.
- CORS remains an explicit origin allowlist. Production HTTPS and reverse-proxy controls remain mandatory.

## 6. Google and Passkey linking rules

- A signed-in User may link a Google identity only after a state/PKCE-protected provider flow and recent Account authentication. Provider subject is the stable external key; email alone is not an external identity key.
- A signed-out Google flow resolves an already-linked provider subject. If none exists and the provider asserts a verified unused email, it may create a new Account. If that email already belongs to another Account, Dotick does not silently link it; the User must authenticate to the existing Account and complete an explicit link flow.
- Passkeys are independent credentials bound to Dotick's WebAuthn relying party and the internal User UUID. Enrollment requires an authenticated/recently authenticated Account or a controlled registration ceremony.
- Google-only Accounts remain valid without a password or Passkey, but the UI must recommend an independent fallback. Provider outage does not revoke otherwise valid Dotick sessions.
- Provider identities and Passkey credentials will use separate tables and adapters. Their migrations are not created before those flows have executable acceptance tests.

## 7. Failure and verification rules

- Public errors use the stable envelope `{"error":{"code":...,"details":...}}`.
- Invalid credentials, unknown Accounts and inactive/unverified Accounts share the same authentication failure.
- Invalid, expired, consumed and locked verification codes share the same verification failure.
- Tests observe behavior through the HTTP API and PostgreSQL. Email is replaced only at its external adapter boundary.
- I1-AC-01 and I1-AC-02 are partially implemented by `apps/api/tests/test_identity_api.py`; configured provider delivery, Google and Passkey remain open.
