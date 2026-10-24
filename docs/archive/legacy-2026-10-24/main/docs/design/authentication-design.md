# Dotick Authentication Design

> **Status:** Increment 1 backend and sign-in client implemented locally; configured provider smoke pending
> **Date:** 2026-09-08
> **Decision sources:** System Definition §6.13; DR-048, DR-061, DR-128, DR-140; SRS-AUTH-001..015

## 1. Scope

This design defines the shared Account identity, verified contacts, email/password, Google, Passkey and revocable JWT session boundaries. These adapters and their PostgreSQL persistence are implemented behind the public Increment 1 API. Real deployment credentials, provider callbacks/browser ceremonies and delivery smoke remain release evidence rather than automated-provider simulations.

The public API contract is [`openapi.json`](openapi.json). The Expo client implements password sign-in, registration/email verification, password recovery, Google credential handoff on configured web builds and browser Passkey sign-in. The I0 HTTP Basic workbench remains isolated behind its local/test-only guard and is not a product authentication method.

## 2. Account identity

- Internal Account identity is the existing UUID `User.id`; authentication methods never replace it.
- Every Account has a case-insensitively unique mutable `handle`, a nonunique `display_name`, an optional profile-picture URL and one shared IANA timezone preference.
- Product registration accepts handles matching `[A-Za-z0-9_]{3,30}`. Framework-created developer accounts receive a generated collision-resistant handle so the database invariant remains true.
- Email is normalized to trimmed lowercase and remains case-insensitively unique.
- A registration email may exist as a pending credential candidate, but the Account stays inactive and `email_verified_at` stays null until verification succeeds. Pending email must not authenticate or participate in contact discovery.
- Secondary email/phone contacts live separately from the primary login email. E.164 is required for phone input. Only verified contacts appear in the active-contact API; pending values and challenges cannot be used for discovery.

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

- The client obtains a Google ID credential through the provider's protected flow; the API validates signature, audience, expiry and verified email with `google-auth` 2.57.1. A signed-in User may link it only after recent Account authentication. Provider subject is the stable external key; email alone is not an external identity key.
- A signed-out Google flow resolves an already-linked provider subject. If none exists and the provider asserts a verified unused email, it may create a new Account. If that email already belongs to another Account, Dotick does not silently link it; the User must authenticate to the existing Account and complete an explicit link flow.
- Passkeys use `webauthn` 3.0.0 and are independent discoverable credentials bound to the configured Dotick RP, allowed origin and internal User UUID. User verification is required. Registration requires a session created within ten minutes. Registration/authentication challenges are 32 random bytes, expire after five minutes and become unusable after successful verification.
- Google-only Accounts remain valid without a password or Passkey, but the UI must recommend an independent fallback. Provider outage does not revoke otherwise valid Dotick sessions.
- Provider identities, Passkey credentials/challenges and contact credentials use separate tables/adapters around the same User UUID. Credential public keys and counters are persisted; private-key material never reaches Dotick.
- A Google-only Account can add a validated password through recent authenticated session or enroll a Passkey. Existing password changes require the current password and revoke other sessions. The response explicitly indicates whether an independent fallback is still recommended.

## 7. Failure and verification rules

- Public errors use the stable envelope `{"error":{"code":...,"details":...}}`.
- Invalid credentials, unknown Accounts and inactive/unverified Accounts share the same authentication failure.
- Invalid, expired, consumed and locked verification codes share the same verification failure.
- Tests observe behavior through the HTTP API and PostgreSQL. Google assertion verification, WebAuthn ceremony verification and delivery are replaced only at external adapter boundaries; one test also executes the real WebAuthn option generator.
- `apps/api/tests/test_identity_api.py` covers email/password/session failures. `test_federated_identity_api.py` covers Google-only/linking/takeover prevention, independent fallback, Passkey enrollment/sign-in/challenge lifecycle, account presentation and verified contacts.
- Public ceremony endpoints require deployment edge rate limiting in addition to the database challenge lifecycle. Real email/phone delivery, Google credentials and browser-authenticator smoke remain pending because they need deployment-specific services/devices.
