# Dotick Risk Register

> **Status:** Increment 0 implementation / Increment 1 readiness
> **Date:** 2026-09-06
> **Scale:** Probability (P) and Impact (I): 1 low — 5 high; Score = P × I

| ID | Risk | P | I | Score | Mitigation / preventive control | Trigger / evidence | Owner stage | Status |
|---|---|---:|---:|---:|---|---|---|---|
| R-001 | scope expansion across future features delays first usable slice | 4 | 4 | 16 | enforce Increment gates; no empty future modules/schema | I1 work depends on I2+ implementation | every Increment | Open |
| R-002 | conceptual inheritance leaks into fragile ORM/schema coupling | 3 | 4 | 12 | DR-052, explicit composition, architecture inspection | subtype change requires hidden ORM behavior | I0/I1 | Mitigated |
| R-003 | cross-user data leakage from unscoped queries | 3 | 5 | 15 | owner-scoped repository/service patterns and negative tests | lookup by raw id before scope | I1 | Open |
| R-004 | multi-auth scope makes I1 too large | 4 | 4 | 16 | verified email/JWT slice now isolated; add Google/Passkey through explicit linking adapters | provider work changes internal User identity | I1 | Partially mitigated |
| R-005 | frontend/backend contract drift | 3 | 4 | 12 | validated `openapi.json`; contract tests; generated types only from committed contract | serializer/client models edited independently | I1+ | Partially mitigated |
| R-006 | PostgreSQL behavior hidden by SQLite/fakes | 3 | 4 | 12 | PostgreSQL in integration/CI; migration test on clean DB | tests pass locally but constraints fail in deployment | I0+ | Mitigated |
| R-007 | timezone/day-boundary defects corrupt credited dates | 4 | 5 | 20 | UTC instants, IANA timezone, controllable clock, DST test matrix | naive datetime enters persistence/domain | I1/I4/I10 | Open |
| R-008 | historical edits or sync overwrite user data | 3 | 5 | 15 | version metadata now; audit I2; sync spec I6; backup/restore | lost update or non-reconstructable edit | I1/I2/I6 | Open |
| R-009 | archive implementation silently becomes active authority | 3 | 3 | 9 | canonical authority rules; new ADRs; archive ignored by Git | design justified only by archive document | all | Mitigated |
| R-010 | optional realtime/queue infrastructure adds premature complexity | 3 | 3 | 9 | add Channels/Redis/worker only in owning Increment | unused service required for local startup | I0-I7 | Mitigated |
| R-011 | dependency/runtime versions drift across machines | 3 | 4 | 12 | committed lockfiles, pinned runtimes/images, clean-clone CI | unpinned `latest` or non-reproducible install | I0 | Locally mitigated by locked container builds; hosted CI pending |
| R-012 | migrations cause irreversible data loss | 2 | 5 | 10 | migration tests, backup before risky change, restore rehearsal | destructive migration without staged rollout | I1+ | Open |
| R-013 | AI/provider outage breaks core task management | 2 | 5 | 10 | adapter isolation; AI not readiness dependency; failure tests | core endpoint imports/calls provider synchronously | I8+ | Open |
| R-014 | design handoffs or stale references become implicit product decisions | 3 | 4 | 12 | current SRS §7 + Traceability gate + ADR/DR review | code/schema follows an old OPEN claim despite canonical closure | every Increment | Open |
| R-015 | document set drifts after implementation begins | 3 | 4 | 12 | traceability update in DoD; increment review; automated ID checks | requirement/test/code lacks trace | every Increment | Open |
| R-016 | local-hosted install lacks recoverability | 3 | 5 | 15 | persistent volume, backup/restore procedure and rehearsal | no verified restore before release | I0/I11 | Open |

# Review rule

I1 treatment is recorded in [the readiness baseline](../tracking/increment-1-readiness.md): R-001/R-004 use small vertical slices while retaining full I1 auth scope; R-003 requires negative ownership tests; R-005/R-008 require version/idempotency contracts and I6 compatibility review; R-007 validates IANA timezone/UTC boundaries. Remaining risks retain their owning increments.

- score 15+ باید در Scope & Readiness Increment مالک treatment صریح داشته باشد.
- risk بسته حذف نمی‌شود؛ status و evidence تغییر می‌کند.
- risk جدید با ID پایدار اضافه می‌شود.
- risk پذیرفته‌شده باید rationale و review date داشته باشد.
