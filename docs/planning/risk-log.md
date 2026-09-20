# Dotick Risk Register

> **Status:** Increment 1 risk treatment reconciled against the implemented `increment` branch and hosted CI
> **Date:** 2026-09-20
> **Scale:** Probability (P) and Impact (I): 1 low — 5 high; Score = P × I

| ID | Risk | P | I | Score | Mitigation / preventive control | Trigger / evidence | Owner stage | Status |
|---|---|---:|---:|---:|---|---|---|---|
| R-001 | scope expansion across future features delays first usable slice | 4 | 4 | 16 | executable I1 scope tests; no Event/Routine/collaboration/sync-history future schema in I1 | I1 depends on I2+ implementation | every Increment | **Mitigated for I1**; guard remains continuous |
| R-002 | conceptual inheritance leaks into fragile ORM/schema coupling | 3 | 4 | 12 | DR-052 explicit Item/Task/Source composition | subtype change requires hidden ORM behavior | I0/I1 | **Mitigated** |
| R-003 | cross-user data leakage from unscoped queries | 3 | 5 | 15 | derive ownership from authenticated actor; owner-scope before lookup; reject forged owner/source; validate source/destination in write transaction; two-account negative HTTP matrix; no staff bypass | foreign resource/destination accepted or object existence leaked | I1 | **Mitigated for I1 personal boundary**; I7 expands authorization model |
| R-004 | multi-auth scope splits account identity or revocation | 4 | 4 | 16 | one UUID User; password/Google/Passkey as credential adapters; central AuthSession issuance/revocation; proof-required linking; fail-closed Google/WebAuthn configuration | provider creates second User, bypasses revocation or starts with an unsafe RP/origin | I1 | **Partially mitigated**; implementation/config tests complete, configured real-provider smoke remains |
| R-005 | frontend/backend contract drift | 3 | 4 | 12 | committed OpenAPI 3.1; reviewed hash; exact Django route-set equality; unknown-field rejection; stable errors; client/E2E evidence | route/schema/client changes without contract review | I1+ | **Mitigated for current I1 surface**; continuous risk |
| R-006 | PostgreSQL behavior hidden by SQLite/fakes | 3 | 4 | 12 | PostgreSQL integration/CI, constraints, clean/fresh DB migration | tests pass only against non-production DB semantics | I0+ | **Mitigated** |
| R-007 | timezone/day-boundary defects corrupt dates | 4 | 5 | 20 | UTC instants; IANA timezone preference validation; DST gap/fold primitives and Golden Time vectors; no I10 attribution in I1 | naive/fixed-offset/silent-DST behavior appears | I1/I4/I10 | **Mitigated for I1 preference/time primitives**; later business-day semantics remain with owners |
| R-008 | historical edits or sync overwrite user data | 3 | 5 | 15 | stable UUIDs, optimistic versions, create idempotency, recoverable Trash metadata; audit I2; sync/history I6 | lost update or non-reconstructable edit | I1/I2/I6 | **Partially mitigated**; I1 guards active, full history/sync remains open |
| R-009 | archive implementation silently becomes authority | 3 | 3 | 9 | canonical authority rules; ADR/DR review; implementation audit does not rewrite product decisions | design justified only by stale/archive text | all | **Mitigated** |
| R-010 | realtime/queue infrastructure adds premature complexity | 3 | 3 | 9 | no Redis/worker/realtime dependency before owning Increment | unused service required for startup | I0-I7 | **Mitigated through I1** |
| R-011 | dependency/runtime versions drift across machines | 3 | 4 | 12 | committed lockfiles/runtime pins, frozen installs, container builds, hosted CI | unpinned/floating dependency or non-reproducible install | I0+ | **Mitigated** |
| R-012 | migrations cause irreversible data loss or history drift | 2 | 5 | 10 | additive-first evolution, PostgreSQL schema/fresh-DB gates, append-only historical migration enforcement, explicit destructive-change review | existing migration edited/deleted/renamed; unsafe production upgrade | I1+ | **Partially mitigated**; append-only CI active, production upgrade/restore rehearsal pending |
| R-013 | AI/provider outage breaks core task management | 2 | 5 | 10 | provider adapter isolation; AI not core readiness dependency | core endpoint synchronously depends on AI/provider | I8+ | Open |
| R-014 | design handoffs/stale references become product decisions | 3 | 4 | 12 | authority chain + traceability + implementation-history reconciliation | code/schema follows historical OPEN wording against canonical docs | every Increment | **Partially mitigated**; continuous review required |
| R-015 | documentation drifts after implementation begins | 3 | 4 | 12 | increment reviews, changelog, traceability checks, full post-reset commit audit, implementation-status reconciliation | docs claim pending/done state that disagrees with branch | every Increment | **Partially mitigated** by 2026-09-16 reconciliation; continuous risk |
| R-016 | local-hosted/production path lacks recoverability | 3 | 5 | 15 | persistent volume, documented backup/restore procedure, release rehearsal requirement | no verified restore before production release | I0/I11 | Open; no production release claimed |
| R-017 | identity ceremonies permit brute force, enumeration or delivery abuse | 4 | 4 | 16 | short-lived single-use challenges; enumeration-safe responses; OpenAPI-classified shared edge policy with burst/sustained thresholds and trusted-IP requirements | protected operation bypasses edge policy, trusts caller-supplied forwarding headers or omits `Retry-After` | I1 deployment | **Partially mitigated**; contract/config tests complete, target-edge enforcement smoke remains |

## Increment 1 control evidence — reconciled 2026-09-20

### R-001 — scope control

I1 currently contains Identity + Account + Folder/List/Column + Basic Task and their required foundations. Executable scope/compatibility tests prevent premature Event, Routine, collaboration and full sync/history capabilities from leaking into the current schema/API.

### R-003 — owner isolation

Current HTTP/application tests use independent users and cover foreign read/write/move/delete/restore and foreign destination attempts. Owner/creator/source metadata is server-controlled, private lookups begin from the current actor scope, and ordinary staff does not receive a product-endpoint bypass.

### R-004 — multi-auth identity

Password, Google and Passkey resolve to the same stable internal User and database-backed revocable AuthSession model. Explicit linking proof, recent-auth requirements and provider failure tests exist. Remaining risk is target-environment configuration/smoke, not a missing shared-identity implementation.

Google configuration has no browser secret: server and client receive the same public client identifier, and missing configuration disables the path cleanly. WebAuthn production-like startup now requires a valid RP ID/name and HTTPS origin in the RP domain. These controls reduce configuration error risk but do not replace real-provider smoke.

### R-005 — contract drift

`docs/design/openapi.json` is now executable I1 contract evidence. CI validates OpenAPI 3.1, locks the reviewed canonical hash, verifies exact equality with published Django I1 routes, checks stable errors and requires identity-ceremony rate-limit metadata. The product client/E2E exercises the real API.

### R-007 — timezone handling

IANA timezone preferences are implemented and validated. Existing Golden Time vectors cover UTC/DST boundary primitives. Dotick-Day/business attribution is intentionally not implemented by I1 and remains with its owning increments.

### R-008 — future sync/history compatibility

I1 preserves stable UUID identity, server-owned optimistic versions, idempotent creation and recoverable Trash origin metadata. These are compatibility foundations only; they are not presented as the future branching History/offline reconciliation model.

### R-012 — migration safety

CI retains model/migration drift checks and fresh PostgreSQL reconstruction. It now additionally enforces append-only numbered migration history by rejecting modification, deletion or rename of existing migration files. Destructive production evolution still requires backup/restore and previous-release upgrade rehearsal.

### R-015 — documentation drift

The 2026-09-16 audit reviewed the complete **148-commit** implementation range from the documentation-only baseline `b61a54a` through audited implementation HEAD `7302ca3`. Tracking, contract, security, quality, development and deployment documentation was reconciled without promoting implementation details into canonical product requirements. See [`docs/tracking/development-commit-audit.md`](../tracking/development-commit-audit.md).

### R-017 — identity ceremony abuse

The OpenAPI contract and machine-readable deployment policy identify the protected identity/contact operations and define shared per-verified-client-IP burst and sustained thresholds. This materially narrows the implementation ambiguity, but risk remains open until a target proxy/CDN proves collective enforcement, trusted client-IP derivation, `429`/`Retry-After` behavior and recovery after each window.

## Hosted evidence

GitHub Actions run `35057831342` completed successfully against audited implementation HEAD `7302ca3b18a79af35058828102bb62e845a56645` before the documentation-reconciliation commits. The run included locked installs, static checks, traceability, migration/schema checks, backend/Golden Time tests, production settings, frontend tests, web export, desktop/mobile E2E, dependency audits, secret scan, container builds and persistence smoke.

Hosted CI is therefore not an open I1 engineering gate. Formal I1 closure still depends on configured real email/Google/WebAuthn/phone smoke, deployment-edge rate-limit enforcement and release publication.

## Review rule

- score 15+ must have explicit treatment in the owning Increment's readiness/review;
- a closed/mitigated risk stays in the register with its evidence rather than disappearing;
- accepted risk requires rationale and review date;
- implementation evidence may change risk status but may not override System Definition, Decision Register or SRS;
- future-Increment residual risk remains open even when the I1 portion is mitigated.
