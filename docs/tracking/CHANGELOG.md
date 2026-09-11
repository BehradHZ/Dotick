# Changelog

تمام تغییرات مهم و قابل‌مشاهدهٔ پروژه باید در این فایل ثبت شوند.

## Unreleased — Increment 1 backend (2026-09-08)

- Added verified email registration, resend throttling and password reset using single-use ten-minute codes.
- Added five-minute access tokens, rotating 30-day refresh tokens, active-session listing and specific/current/all-session revocation.
- Added unique handles and display names, append-only identity migrations, a validated OpenAPI contract and dedicated production JWT signing key.
- Added Google-only sign-in and explicit account linking, optional WebAuthn Passkeys, independent password fallback, account/profile/timezone presentation and separately verified secondary contacts.
- Added atomic account bootstrap, exactly one Inbox/default Column, personal Folder/List/Column CRUD and ordering, explicit recoverable container deletion, and owner-scoped Trash/restore.
- Added explicit Item/Task composition, stable UUID identity, manual provenance, Task create/read/edit/move/status/Trash/restore, optimistic versions and idempotent creation.
- Expanded the validated OpenAPI 3.1 contract to every published Increment 1 backend route and added PostgreSQL behavior tests for concurrency, isolation, conflicts and recovery.
- Product client integration, configured email/Google/WebAuthn/phone delivery smoke and release publication remain pending; the locally verified backend is not the whole Increment 1 release.

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
