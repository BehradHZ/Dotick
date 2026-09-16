# Changelog

تمام تغییرات مهم و قابل‌مشاهدهٔ پروژه باید در این فایل ثبت شوند.

## Unreleased — Increment 1 (reconciled 2026-09-16)

- Added verified email registration, resend throttling and password reset using single-use ten-minute codes.
- Added five-minute access tokens, rotating 30-day refresh tokens, active-session listing and specific/current/all-session revocation.
- Added unique mutable handles, display names, profile-picture references, IANA timezone preferences and dedicated production JWT signing-key configuration.
- Added Google-only sign-in and explicit account linking, optional WebAuthn Passkeys, independent password fallback, recent-auth/user-verification protections and separately verified secondary contacts. Pending contacts remain inactive and undiscoverable; phone contacts use E.164 validation.
- Added atomic and concurrently idempotent account bootstrap, exactly one Inbox/default Column, personal Folder/List/Column CRUD and ordering, recoverable container deletion/restore, child-resolution rules and query indexes for I1 navigation paths.
- Added explicit Item/Task/Source composition, stable UUID identity, manual provenance, unscheduled Task create/read/edit/move/status/Trash/restore, optimistic versions, owner-isolated destinations and idempotent creation.
- Integrated the Expo product client with the I1 API for registration/verification/reset, sign-in/bootstrap, Inbox/List navigation, Task creation/edit/status/move/Trash/restore, Persian/English titles, web Google/Passkey surfaces and LAN API discovery. Tokens intentionally remain session-memory only.
- Expanded the validated OpenAPI 3.1 contract to the exact published Increment 1 route set. Contract tests validate the document, lock the reviewed canonical hash and fail when Django routes and documented paths diverge.
- Hardened the API with stable error codes/envelopes, unknown-field rejection, JSON-only versioned request boundaries, a 16 KiB body limit, malformed request rejection and explicit CORS support for `If-Match` without wildcard origins or cross-origin credentials.
- Hardened production-like settings with explicit host/CSRF/CORS allowlists, HTTPS-only non-local origins, secure redirect/cookie/HSTS/proxy settings and safe request-correlation logging.
- Declared identity-sensitive operations with OpenAPI `x-edge-rate-limit-policy: identity-ceremony`; actual threshold/enforcement remains a deployment-edge responsibility and release configuration concern.
- Enforced append-only Django migration history in CI: existing numbered migrations may not be modified, deleted or renamed; schema changes require new migrations. Fresh-database and schema-drift checks remain active.
- Hosted CI run `35057831342` completed successfully against audited implementation HEAD `7302ca3b18a79af35058828102bb62e845a56645`, covering locked installs, static checks, traceability, migrations, backend/Golden Time tests, production checks, frontend tests, web export, desktop/mobile E2E, dependency audits, secret scan, non-root container builds and persistence smoke.
- Configured real email delivery, Google credentials, real WebAuthn browser/authenticator smoke, phone delivery-adapter smoke and formal Increment 1 release/publication remain open. Hosted CI and local product-client integration are no longer open engineering gates.

See [the complete post-reset implementation audit](development-commit-audit.md) for the 148-commit reconciliation boundary and documentation-impact rules.

## Increment 0 foundation — closed (2026-09-09)

- Reconciled branch `test` with the exact verified Codex Increment 0 snapshot while preserving the newer backend hardening already implemented on `test`.
- Restored the real responsive Walking Skeleton client, developer-only in-memory sign-in, sign-out cleanup, Checkpoint create/list/refresh, loading/error/retry states, and draft preservation.
- Restored executable UTC/timezone/DST/all-day Golden Time tests and Gregorian/Jalali client vectors from the shared catalog.
- Added Vitest/Testing Library component/network tests and Playwright desktop/mobile persistence E2E coverage.
- Added non-root API/web Docker images and PostgreSQL + API + web Compose topology.
- Added hosted GitHub Actions gates for locked installs, Ruff, ESLint, Prettier, TypeScript, migration/schema drift, clean PostgreSQL, backend/frontend/time tests, web export, E2E, dependency audits, secret scan, Django deployment checks, container builds, smoke, and API-restart persistence.
- Hosted CI run `34330581198` completed successfully against implementation commit `88aa5986a5673224a3d4ea78fca164f742e9d83e`: 30 Django tests, 14 backend Golden Time tests, 8 client tests, and 2 desktop/mobile E2E tests passed.
- Python dependency audit reported no known vulnerabilities; npm has no high/critical findings and retains 10 reviewed moderate Expo/native-tooling transitive findings as accepted technical debt.
- Increment 0 self-review and intentional technical debt were recorded in [the foundation review](increment-0-foundation-review.md), and the [v0.1.0 foundation record](../../releases/v0.1.0.md) was created.
- Increment 0 is formally closed. No public Git tag, GitHub Release, or production deployment is claimed by this closure.

برای هر نسخه یا release، تاریخ، قابلیت‌های افزوده، تغییرات رفتاری، رفع اشکال‌ها، تغییرات امنیتی، موارد deprecated و breaking changeها درج شود. تغییر صرفاً ویراستاری اسناد لازم نیست در این فایل ثبت شود.
