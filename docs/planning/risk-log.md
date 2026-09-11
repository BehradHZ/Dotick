# Dotick Risk Register

> **Status:** Increment 1 risk treatment reviewed against the actual `test` branch; implementation is in progress
> **Date:** 2026-09-11
> **Scale:** Probability (P) and Impact (I): 1 low — 5 high; Score = P × I

| ID | Risk | P | I | Score | Mitigation / preventive control | Trigger / evidence | Owner stage | Status |
|---|---|---:|---:|---:|---|---|---|---|
| R-001 | scope expansion across future features delays first usable slice | 4 | 4 | 16 | executable I1 schema/API scope guard; no empty future modules/schema | I1 work depends on I2+ implementation | every Increment | Partially mitigated; I1 scope guard active |
| R-002 | conceptual inheritance leaks into fragile ORM/schema coupling | 3 | 4 | 12 | DR-052, explicit composition, architecture inspection | subtype change requires hidden ORM behavior | I0/I1 | Mitigated |
| R-003 | cross-user data leakage from unscoped queries | 3 | 5 | 15 | derive ownership from authenticated actor; owner-scope before lookup; reject client-supplied owner/provenance; scope source and destination in the same write transaction; two-account negative HTTP matrix; ordinary staff endpoints get no bypass | lookup by raw id before owner scope, foreign destination accepted, or writable owner/source metadata | I1 | Treatment defined; I1 runtime evidence pending feature implementation |
| R-004 | multi-auth scope makes I1 too large or splits account identity | 4 | 4 | 16 | one internal User identity and revocable session model; password/Google/Passkey remain credential adapters; provider linking requires proof; no provider-specific User model; provider outage tests and configured-provider smoke | provider flow creates a second internal identity, bypasses central revocation, or changes core User semantics | I1 | Treatment defined; shared User foundation exists, full I1 auth adapters pending |
| R-005 | frontend/backend contract drift | 3 | 4 | 12 | committed `openapi.json`; reject unknown request fields; local-ref and unique-operationId regression checks; route-set conformance once endpoints exist; client consumes the committed contract; contract and implementation change together | serializer/view/client shape changes without matching contract or contract reference breaks | I1+ | Partially mitigated; contract regression guards active, runtime/client conformance pending |
| R-006 | PostgreSQL behavior hidden by SQLite/fakes | 3 | 4 | 12 | PostgreSQL in integration/CI; migration test on clean DB | tests pass locally but constraints fail in deployment | I0+ | Mitigated |
| R-007 | timezone/day-boundary defects corrupt credited dates | 4 | 5 | 20 | persist instants as aware UTC; accept/store IANA timezone names; reject naive instants; explicit DST gap/fold handling; executable 23/24/25-hour day vectors; do not pull I10 day-boundary attribution into I1 | naive datetime, fixed-offset timezone preference, silent DST coercion, or business-day logic appears in I1 | I1/I4/I10 | Partially mitigated; UTC/IANA/DST primitives active, I1 preference validation pending |
| R-008 | historical edits or sync overwrite user data | 3 | 5 | 15 | stable UUIDs, optimistic version/idempotency foundations now; audit I2; sync/history spec I6; backup/restore | lost update or non-reconstructable edit | I1/I2/I6 | Open; I6 compatibility blockers are explicitly tracked |
| R-009 | archive implementation silently becomes active authority | 3 | 3 | 9 | canonical authority rules; new ADRs; archive ignored by Git | design justified only by archive document | all | Mitigated |
| R-010 | optional realtime/queue infrastructure adds premature complexity | 3 | 3 | 9 | add Channels/Redis/worker only in owning Increment | unused service required for local startup | I0-I7 | Mitigated |
| R-011 | dependency/runtime versions drift across machines | 3 | 4 | 12 | committed lockfiles, pinned runtimes/images, clean hosted CI | unpinned `latest` or non-reproducible install | I0 | Mitigated; hosted CI clean lock installs and container builds passed 2026-09-09 |
| R-012 | migrations cause irreversible data loss | 2 | 5 | 10 | additive-first migrations; PostgreSQL schema-drift and fresh-database CI; destructive/opaque operations require explicit safety review; use expand/backfill/contract for destructive changes; production backup/restore rehearsal before destructive rollout | destructive migration without review, fresh DB cannot migrate, upgrade requires downtime/data rewrite, or rollback path is absent | I1+ | Partially mitigated; CI gates active, production upgrade/restore evidence pending |
| R-013 | AI/provider outage breaks core task management | 2 | 5 | 10 | adapter isolation; AI not readiness dependency; failure tests | core endpoint imports/calls provider synchronously | I8+ | Open |
| R-014 | design handoffs or stale references become implicit product decisions | 3 | 4 | 12 | current SRS §7 + Traceability gate + ADR/DR review | code/schema follows an old OPEN claim despite canonical closure | every Increment | Open |
| R-015 | document set drifts after implementation begins | 3 | 4 | 12 | traceability update in DoD; increment review; automated ID checks; implementation-status claims must be verified against the current branch | requirement/test/code lacks trace or tracking document claims implementation absent from the branch | every Increment | Open |
| R-016 | local-hosted install lacks recoverability | 3 | 5 | 15 | persistent volume, backup/restore procedure and rehearsal | no verified restore before release | I0/I11 | Open |

# Increment 1 risk treatment — 2026-09-11

This review defines controls for I1 without claiming that the not-yet-implemented I1 organization,
Task, or multi-auth endpoints already provide them. A risk moves to **Mitigated** only when the
listed verification evidence exists on the current branch and in CI.

| Risk | Required I1 implementation rule | Verification / release gate |
|---|---|---|
| R-004 Multi-auth complexity | Password, Google and Passkey authenticate to the same stable internal User. Provider credentials stay outside core User identity. Session issuance/revocation is central and provider-independent. Linking a provider requires authenticated proof and cannot silently merge accounts. | Contract test proves common User identity; password/Google/Passkey integration tests resolve the intended User; revoked sessions fail; configured Google and WebAuthn smoke before release. |
| R-003 Cross-user leakage | Never lookup a private object by raw ID and authorize afterward. Start from the authenticated actor's scope, derive owner/creator server-side, reject forged owner/source fields, and validate both source and destination ownership inside write transactions. Foreign private resources return the same not-found surface as absent resources. | Two real users exercise list/read/create/edit/move/delete/restore and foreign destination IDs. Include inactive/revoked session cases and an ordinary staff account to prove there is no endpoint bypass. |
| R-005 Contract drift | `docs/design/openapi.json` is the committed I1 API design handoff. Request schemas reject unknown fields. Local `$ref`s must resolve and operation IDs remain unique/stable. Endpoint implementation and client models cannot change independently of the contract. | OpenAPI regression tests on every commit; route-set/runtime conformance test as I1 endpoints are added; client integration against the committed contract; CI fails on unmatched contract changes. |
| R-007 Timezone handling | Persist instants as timezone-aware UTC. Store user timezone as an IANA zone name, not a numeric offset. Reject timezone-free instants. DST gaps are invalid and overlaps require explicit fold choice. I1 must not implement I10 Dotick-Day attribution or `day_boundary_offset_minutes` behavior. | Existing golden time vectors remain green, including ambiguous/nonexistent wall times and 23/25-hour days. Add timezone-preference API validation tests when preferences are implemented. |
| R-012 Migration safety | Prefer additive schema changes. Fresh PostgreSQL must migrate from zero and model state must match migrations. Rename/remove/delete/raw-SQL operations require explicit migration safety review. Destructive evolution uses expand → backfill → contract instead of a one-step rewrite. | CI retains `makemigrations --check`, PostgreSQL `migrate`, `showmigrations`, migration checks and fresh-database reconstruction. Before a destructive production migration, verify backup/restore and an upgrade from the previous release snapshot. |

# Review rule

I1 treatment is recorded here and in
[the readiness baseline](../tracking/increment-1-readiness.md). R-001/R-004 use small vertical
slices while retaining full I1 auth scope; R-003 requires negative ownership tests; R-005/R-008
require version/idempotency and contract guards; R-007 validates IANA timezone/UTC boundaries;
R-012 requires PostgreSQL migration safety gates. Remaining risks retain their owning increments.

- score 15+ باید در Scope & Readiness Increment مالک treatment صریح داشته باشد.
- risk بسته حذف نمی‌شود؛ status و evidence تغییر می‌کند.
- risk جدید با ID پایدار اضافه می‌شود.
- risk پذیرفته‌شده باید rationale و review date داشته باشد.
