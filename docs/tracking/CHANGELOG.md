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

## Increment 0 foundation candidate (2026-09-06)

- Added locked Django/PostgreSQL and Expo web workspaces, migrations, isolated authenticated checkpoint workbench and responsive prototype-derived styling.
- Added owner-isolation, input-validation, safe-logging and UTC/DST/calendar checks; CI, local containers and reproducible setup.
- Verified a fresh Git clone with 33 API tests, 8 client tests and 2 desktop/mobile persistence tests, plus lint, types, migrations and web build.
- Prepared I1 readiness with canonical Inbox, authentication, deletion and sync/history constraints.

See [foundation review](increment-0-foundation-review.md) and [v0.1.0 candidate](../../releases/v0.1.0.md). Hosted CI and release publication remain pending.

برای هر نسخه یا release، تاریخ، قابلیت‌های افزوده، تغییرات رفتاری، رفع اشکال‌ها، تغییرات امنیتی، موارد deprecated و breaking changeها درج شود. تغییر صرفاً ویراستاری اسناد لازم نیست در این فایل ثبت شود.
