# Increment 1 client review

> **Reconciled:** 2026-09-20
>
> **Implementation baseline before this documentation commit:** `4485c63`
>
> **Result:** Usable I1 web/Android product client present; not an Increment 1 release.

## Implemented product surface

- Expo configuration targets web and Android.
- Signed-out flows provide registration, email verification/resend, password reset/confirmation and password sign-in.
- Configured web builds provide Google ID credential and browser Passkey sign-in; missing provider configuration preserves password fallback.
- First authentication bootstraps timezone preferences, Inbox and default Column.
- Workspace UI provides Inbox/List navigation, List creation and Basic Task creation, title/status changes, movement between loaded Columns, Trash and restore.
- Session access/refresh credentials remain in memory. Sign-out removes private workspace state, drafts and response cache before completing server revocation.
- Network failures preserve drafts; version/conflict paths refresh authoritative resources rather than silently overwriting them.
- Local-network API address discovery remains available for Android development.

## Current executable evidence

- Component/network tests cover signed-out identity flows, Google/Passkey availability, session rotation/privacy, API response validation, workspace/list/task behavior, bilingual input, draft retention, conflicts and recovery.
- Playwright desktop/mobile projects exercise the real client-to-Django-to-PostgreSQL I1 path: sign-in, bootstrap, List/Task creation, status mutation, Trash/restore, reload persistence and sign-out.
- Additional E2E scenarios cover failed-save draft retention and cross-account resource/operation isolation.
- The retained I0 Checkpoint browser/API regression is separate compatibility coverage and is not counted as I1 product acceptance.

Historical test counts and hosted runs are not restated as current-HEAD results. CI targeting now includes `increment`; an exact final-candidate hosted result is still pending.

## Deliberate limits

- Folder management and full custom-Column management are not complete product UI surfaces, although backend APIs and client API bindings exist.
- Passkey enrollment, Google linking, profile/contact/session management and delivery configuration remain API-first boundaries.
- Provider-specific native Google/Passkey behavior is not claimed.
- Tokens intentionally remain session-memory only; durable secure credential storage needs a later security-reviewed client slice.
- Permanent deletion, purge execution, scheduling, Event/Routine, comments, collaboration and full Offline/Sync/History remain outside I1.

## Pending release evidence

This client review was completed before formal closure. Increment 1 later closed at `v0.2.0`; optional delivery and live Google/WebAuthn, edge and production-device smoke remain assigned to Increment 11.

See [Increment 1 readiness](increment-1-readiness.md) for the complete closure rule and [formal Increment 1 review](increment-1-review.md) for the release-candidate status.
