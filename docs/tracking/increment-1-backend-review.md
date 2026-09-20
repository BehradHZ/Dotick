# Increment 1 backend review

> **Reconciled:** 2026-09-20
>
> **Implementation baseline before this documentation commit:** `4485c63`
>
> **Result:** Repository backend slice implemented; not an Increment 1 release.

## Implemented boundary

- **Identity:** custom UUID account, verified email/password registration and recovery, rotating/revocable JWT sessions, Google identity, Passkeys, password fallback and verified secondary contacts.
- **Account:** unique mutable handle, display name, profile-picture reference, IANA timezone and authentication-method reporting.
- **Organization:** concurrent-idempotent bootstrap, one Inbox per account, one default Column per List, optional Folder, owner-scoped Folder/List/Column CRUD and ordering, version conflicts, retry-safe creation and recoverable deletion.
- **Task:** Item/Task/Source composition, manual provenance, unscheduled Basic Task create/read/edit/move/status/Trash/restore, optimistic versions and idempotent creation.
- **Contract:** validated OpenAPI 3.1 route equality, global bearer security with explicit public exceptions, stable errors, JSON/request-size boundaries and identity-ceremony edge classification.
- **Configuration:** environment-driven external email/SMS adapters, Google client IDs, WebAuthn RP settings and machine-readable edge-rate-limit policy thresholds.

## Current executable evidence

The repository contains ordinary tests for:

- identity/account/provider behavior and disclosure-safe failures;
- owner isolation, concurrency, stale versions and idempotent replay/conflict behavior;
- OpenAPI validity, reviewed hash, exact route equality and authentication/rate-limit metadata;
- append-only migrations, schema drift and clean PostgreSQL reconstruction;
- production host/origin/HTTPS, Google, WebAuthn, delivery-adapter and edge-policy configuration.

The former strict compatibility gaps for OpenAPI bearer security and Folder/List/Column version/idempotency are resolved; their tests are no longer expected failures.

Historical pass counts and hosted run `35057831342` remain evidence only for their recorded historical SHA. CI targeting now includes `increment`; an exact final-candidate hosted result is still pending.

## Deliberate limits and pending evidence

- Email and SMS have configurable delivery boundaries, not proven target-environment delivery.
- Google tests validate configuration and provider-boundary behavior, not a real Google account/browser flow.
- WebAuthn tests validate relying-party configuration and ceremony boundaries, not a real authenticator.
- The `identity-ceremony` threshold contract is defined for proxy/CDN enforcement; Django intentionally has no process-local substitute, and deployed enforcement remains unverified.
- Event, Routine, scheduling, collaboration, full Sync/History/Undo and permanent Trash purge are later-Increment work.
- Formal I1 release publication remains pending.

See [Increment 1 readiness](increment-1-readiness.md) for closure gates, [formal Increment 1 review](increment-1-review.md) for the release-candidate decision and [Increment 1 client review](increment-1-client-review.md) for current UI scope.
