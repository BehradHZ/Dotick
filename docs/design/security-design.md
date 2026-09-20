# Dotick Security Design

> **Status:** Increment 1 security baseline implemented and hosted-CI verified; deployment-specific provider/edge smoke remains open
> **Reconciled:** 2026-09-20

This document describes security controls implemented for the current I0/I1 boundary. It does not pull later authorization, offline-sync or collaboration behavior into Increment 1.

## 1. Identity and credentials

- The internal User has a stable UUID identity independent of login method.
- Passwords use Django password machinery with Argon2 as the primary hasher.
- Email verification and password-reset codes are short-lived, single-use challenge material and are not stored as reusable plaintext credentials.
- Access tokens are short-lived; refresh/session state is database-backed and revocable.
- Google and Passkey credentials resolve to the same internal User/session model rather than creating provider-specific ownership identities.
- Google linking requires explicit authenticated proof; provider assertion alone cannot silently merge accounts.
- Passkey enrollment and sensitive verification paths enforce recent authentication and WebAuthn user-verification requirements where applicable.
- Secondary contacts remain pending until code verification; pending contacts are excluded from active/discovery flows. Phone contacts are validated in E.164 form.
- Production JWT signing configuration is separate from the ordinary Django secret and must be explicitly supplied.

## 2. Authorization and ownership

- Private product resources are queried from the authenticated account scope; code must not fetch a private object by raw ID and authorize afterward.
- Owner, creator and provenance/source fields are derived or constrained server-side; client-supplied metadata cannot grant ownership.
- Task moves validate source and destination ownership inside the write transaction.
- Cross-account reads/writes/moves/deletes/restores are covered by negative HTTP tests.
- Ordinary staff status does not provide a product-endpoint authorization bypass.
- Group/effective-permission expansion belongs to Increment 7 and is intentionally not represented by a premature I1 abstraction.

## 3. Network and origin controls

Local loopback development may use HTTP. Non-local/production-like configuration is fail-closed:

- `DJANGO_ALLOWED_HOSTS` must be an explicit non-wildcard allowlist outside local/test.
- `DJANGO_CSRF_TRUSTED_ORIGINS` and `DJANGO_CORS_ORIGINS` must be explicitly configured outside local/test.
- production trusted origins, CORS origins and WebAuthn origin must use HTTPS;
- secure redirect, secure session/CSRF cookies, HSTS and trusted proxy HTTPS-header handling are enabled for non-local configuration;
- CORS never uses `*`, does not enable cross-origin credentials, and permits the `If-Match` header required by versioned Task mutations only for trusted origins.

The production Django deployment check and dedicated security/CORS tests exercise these invariants.

## 4. API request boundary

All versioned product API write methods (`POST`, `PUT`, `PATCH`, `DELETE`) share a transport boundary before view dispatch:

- request bodies are limited to 16 KiB;
- non-empty bodies must use `application/json`;
- malformed `Content-Length`, malformed JSON and body-size mismatches are rejected;
- unsupported media, malformed input and oversized bodies use stable error codes/envelopes;
- serializers reject unknown input fields.

Operational endpoints such as `/health` remain outside the product JSON-body boundary.

## 5. Error and information disclosure

Public errors use the stable envelope:

```json
{"error":{"code":"...","details":{}}}
```

Error codes are contract-level identifiers. Validation/parser/authentication/authorization failures are normalized so framework-specific internals are not exposed as the public API contract. Private-object absence and unauthorized foreign-object lookup use the owner-scoped surface rather than leaking existence through a separate fetch-then-authorize path.

## 6. Logging and secrets

Structured request logging uses an allowlist of fields such as timestamp, level, service, event, request ID, method, normalized route, status and duration. Normal request logs do not include Authorization headers, cookies, passwords, tokens, request bodies, provider assertions, secret keys, DSNs, environment objects or free-form exception messages.

Each request receives a server correlation/request ID. API responses are configured to avoid accidental caching of sensitive product responses where the current boundary requires it.

Secret material belongs in environment configuration or secret storage, never Expo public variables, repository files or test fixtures. `EXPO_PUBLIC_*` values are bundled into the client and are never secret. Google OAuth client IDs are public identifiers; this credential flow does not require a browser-visible Google secret. SMTP passwords, SMS-provider credentials, Django/JWT signing keys and any future provider secrets remain server-only.

## 7. External identity and delivery boundaries

Automated tests replace external provider/delivery boundaries deterministically. This is implementation evidence, not release evidence for a configured real provider.

- Email delivery is selected through Django's environment-driven backend/SMTP settings. Invalid port, credential pairing and simultaneous TLS/SSL configuration are rejected. Missing or failed contact delivery has a stable unavailable response and does not verify the contact.
- SMS delivery is selected by a server-side adapter import path. The default unavailable adapter keeps phone contacts pending; provider credentials are owned by the deployment adapter.
- Google uses matching public client IDs on server and client. Missing server configuration returns provider unavailable before token verification; missing client configuration hides the Google action.
- WebAuthn RP ID, display name and origin are environment-driven. Production-like startup rejects blank/invalid RP settings, insecure non-local origins and origins outside the RP ID domain; localhost HTTP remains available for development.

Formal I1 closure still requires target-environment smoke for:

- real email delivery;
- configured Google OAuth client/redirect path;
- WebAuthn with the target RP ID/origins and a real browser/authenticator;
- phone verification delivery adapter.

Provider failure must remain isolated from core manual Task management.

The authoritative variable-by-variable setup is in [Development environment](../development/environment-setup.md). Operational verification and secret-handling guidance is in [Security operations](../operations/security-operations.md).

## 8. Rate limiting and abuse controls

The OpenAPI contract classifies sensitive identity ceremonies with:

```text
x-edge-rate-limit-policy: identity-ceremony
```

The classified operations include registration, verification/resend, password-reset, Passkey authentication ceremonies and contact verification flows. The exact operation set is machine-readable in [`identity-rate-limit-policy.json`](../operations/identity-rate-limit-policy.json) and is checked against OpenAPI.

The initial deployment baseline applies both limits collectively per verified client IP: 10 requests per 60 seconds and 100 requests per 3,600 seconds. Deployment tooling reads the corresponding `DOTICK_EDGE_IDENTITY_CEREMONY_*` variables. Client IP must come from the trusted proxy/CDN connection metadata, not an untrusted forwarded header supplied by the caller. A rejected request returns `429` and a `Retry-After` header without disclosing account state.

This is an explicit handoff to the deployment edge. Per-process counters would diverge across workers and are not an acceptable substitute. Target-environment enforcement and threshold smoke tests remain required before formal I1 release.

## 9. Database and migration safety

- PostgreSQL is the integration/system-of-record database; security/integrity behavior is not accepted from SQLite-only tests.
- Database constraints enforce critical cardinality/integrity rules such as one Inbox per owner and one default Column per List.
- Fresh-database migration and schema-drift checks run in CI.
- Historical numbered migrations are append-only. CI rejects modification, deletion or rename of an existing migration; schema evolution must add a new migration.
- Destructive production evolution still requires explicit backup/restore and upgrade-path review.

## 10. Dependency and supply-chain controls

Hosted CI performs locked Python/Node installs, Python dependency audit, npm audit at the documented threshold, secret scanning, static checks and non-root container builds. CI workflow actions are version-pinned rather than floating on unreviewed `latest` references.

## 11. Verification status

Hosted run `35057831342` succeeded against audited implementation HEAD `7302ca3b18a79af35058828102bb62e845a56645` before the documentation reconciliation. The run exercised production settings, API/security/request-boundary tests, dependency/secret checks, containers and persistence alongside the rest of the I1 suite.

Remaining security evidence is deployment-specific provider/delivery/edge smoke, not missing core I1 API implementation.

See [API Contracts](api-contracts.md), [Authentication Design](authentication-design.md), [Increment 1 readiness](../tracking/increment-1-readiness.md), and [the full development commit audit](../tracking/development-commit-audit.md).
