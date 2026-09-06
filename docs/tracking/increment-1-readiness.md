# Increment 1 readiness baseline

Date: 2026-09-06. Status: preparation for roadmap §8; product implementation has not started. I0's hosted CI and release gates remain open. This document refines implementation order and acceptance evidence; it does not change product scope.

## Goal and authority

A registered user signs in, sees their Inbox, creates an unscheduled Task, places it in a List/Column, edits it, marks it Done or Won't_Do, and retrieves it after reopening the app. Another account cannot access it.

Read System Definition §§6.1, 6.2, 6.13 and 8.3–8.6 first, then Decision Register, SRS v2.9, and roadmap §§7.6/8. The prototype supplies visual and interaction examples. Its demo data, toast-only actions and unfinished screens are not persistence or acceptance evidence.

## Delivery order within I1

1. **Verified email identity:** register, send/verify an email code, sign in with password, reset password, JWT session renewal/revocation and sign out. Use Django's existing password machinery. Select maintained JWT/authentication libraries during implementation; do not write cryptography. Keep the I0 Basic-auth workbench isolated until replacement is verified.
2. **Account bootstrap and first Task:** provision one Inbox and its default Column atomically, plus preferences with an IANA timezone. Create/read one real unscheduled Task through the authenticated client/API/PostgreSQL path. Account bootstrap must remain idempotent under retries.
3. **Organization and editing:** Folder/List/Column navigation, placement, title/status changes, recoverable deletion and draft-preserving failure states. Verify ownership and concurrent writes at the public API boundary.
4. **Complete I1 identity:** Google sign-in/linking and optional Passkey enrollment/sign-in, independent fallback recommendation, account presentation and session management. Google-only accounts must work without a password/Passkey. Provider failure must not invalidate otherwise valid sessions.
5. **Integration and release:** desktop/mobile acceptance, real delivery/provider configuration smoke, migrations, API contract verification, security failures and regression checks. Email-only success does not complete I1.

Scheduling, Event/Routine implementation, collaboration, full offline reconciliation, branching-history UI and additional views retain their owning increments. Their known invariants constrain this design now.

## Required corrections to older proposals

| Area | Implementation rule | Authority / evidence |
|---|---|---|
| Inbox | A real, special List, exactly one per user; cannot rename/delete. Create it and its default Column in one transaction. | SD §6.1; SRS-ORG-002/003 |
| Folder | Optional in the UI. Prefer a nullable List folder and explicit personal owner; do not require a visible synthetic Folder. | SD §6.1 |
| Titles and ordering | Duplicate container titles are valid. Stable UUID identity is independent of title/position. Support manual order; never use a display index as identity. | SD §6.1; SRS-ITEM-002 |
| Default Column | Exactly one per List, maintained transactionally with a partial unique constraint. Hide the technical default name when it is the sole Column. | SRS-ORG-003/004 |
| Account | Existing UUID identity is reusable; the foundation User is not the final profile/contact model. Add unique mutable handle, nonunique display name, optional picture and separately verified contacts. A pending contact must never become discoverable. | SD §6.13; SRS-AUTH-012..015 |
| Placement | Each Task has exactly one Column; its List is derived from that Column. Destination and source are checked against the current authenticated owner inside the write transaction. | SD §6.1; SRS-NFR-SEC-003 |
| Task composition | Item identity/metadata plus explicit one-to-one Task and Source rows. Task status is not on the shared Item table. Manual provenance never grants ownership. | DR-052; SRS-ITEM-006..009 |
| Delete | Item/Folder/List ordinary deletion is recoverable. Column has no independent Trash lifecycle. Column removal needs an explicit choice to move contents to the same List's default Column or delete contents. | SD §§6.1/8.4 |
| Restore/purge | Retain deletion time and enough origin metadata for later restore. Restore falls back to Inbox/default Column if old placement is gone. Thirty-day Trash retention and explicit Delete Permanently are canonical; purge preserves required audit evidence. | SD §8.4; roadmap I6 |

The older `data-model.md` tables are proposals, not a migration specification. `domain-model.md` §33 and `reference/class-fields.md` contain historical OPEN wording; current SRS §7 distinguishes design handoffs from closed product decisions. Do not reopen those decisions from the older references.

## I6 compatibility review before migrations/API are locked

| Concern | I1 design constraint | Verification / later handoff |
|---|---|---|
| Stable identity | UUIDs for persisted entities; never recreate Items on move/rename. No kind-changing API. | Create, move, edit and reload preserve ID. I2 adds relation/block IDs. |
| Revision/order | Positive server-owned version, incremented atomically with every accepted mutation; UTC server timestamps. Clients supply expected version, never authoritative time/version. | Two writers using the same version cannot silently overwrite each other. I6 adds field-level reconciliation metadata. |
| Conflict response | Reject stale online edits with a stable conflict error and current authorized state/version; keep the local draft. This is an online concurrency guard, not the future field-level LWW algorithm. | Conflict/retry API and UI test. No fabricated device-clock winning write. |
| Retry/idempotency | Specify retry semantics before enabling automatic mutation retries. Creation needs a stable operation identity or equivalent deduplication; reused identity with different intent must not create a second resource. | Lost-response/retry test. Final operation retention policy belongs with the implemented contract. |
| Tombstone/restore | Preserve identity across Trash/restore. Do not immediately hard-delete operational state on ordinary deletion, and do not use blind container cascades. | Delete isolation and restore tests; I2 audit and I6 history/purge compatibility. |
| Branching history | A mutable integer version is not a complete History model. Preserve a path to stable change IDs, parent links and new restore events without destructive rewrites of old branches. | I2 audit design, then I6 branching-history contract. No Undo/history claim from a version field alone. |
| Authorization | Check the current account and ownership on every server operation; never trust stale client permission, supplied owner ID or Source. Do not grant a staff bypass through ordinary endpoints. | Cross-user, inactive account, revoked session and forged metadata tests. I7 expands effective permissions. |

## Acceptance plan at public boundaries

These cases are the roadmap's Stage E plan. They are not executed product tests yet. Implement one failing behavior test and its vertical slice at a time during Stage F.

| ID | Observable scenario | Boundary / trace |
|---|---|---|
| I1-AC-01 | Unverified email cannot authenticate as verified or appear in contact discovery; expired/replayed/incorrect verification codes fail; successful verification enables password sign-in. | Identity HTTP API; SRS-AUTH-001/008/012/013 |
| I1-AC-02 | Password reset works through email; credentials/tokens never enter ordinary logs. JWT renewal and session-specific/all-session revocation reject revoked credentials. | Identity HTTP API; SD §6.13; SRS-AUTH-002/004; SRS-NFR-SEC-001/002 |
| I1-AC-03 | Repeat/concurrent bootstrap produces exactly one Inbox/default Column. Inbox rename/delete fails. Lists can appear without a Folder and allow duplicate titles. | Organization HTTP API; SD §6.1; SRS-ORG-001..005 |
| I1-AC-04 | Create a Task with only a title, without dates. Read it after reauthentication; UUID, ownership, creator and manual provenance remain intact. | Desktop/mobile client → API → PostgreSQL; SRS-TASK-001/020; SRS-ITEM-002/006..009 |
| I1-AC-05 | Move a Task, edit title, choose Done/Won't_Do and reopen it. Invalid/empty title and forged server metadata fail. Failed save retains the draft. | Task HTTP API and client; SRS-TASK-001/014; SRS-ITEM-003 |
| I1-AC-06 | Another user cannot list/read/edit/move/delete the Task or place their Task in the first user's Column; ordinary staff endpoints remain scoped. | HTTP API with two real accounts; SRS-NFR-SEC-003 |
| I1-AC-07 | A stale version cannot silently replace a newer edit; a retried create after response loss does not duplicate the Task. | HTTP API with independent clients; SRS-ITEM-005; roadmap §7.6 |
| I1-AC-08 | Ordinary delete disappears from active queries, preserves its recovery metadata, and respects container/Column rules. | HTTP API and UI; SRS-ITEM-004; SD §8.4 |
| I1-AC-09 | Google-only sign-in works; fallback is offered, not mandatory. Configured password/Passkey works during Google outage; wrong account-linking proof cannot take over an account. | Provider simulation plus configured integration smoke; SRS-AUTH-003/005..010 |
| I1-AC-10 | Desktop/mobile account-to-Task workflow stores Persian and English titles, hides the sole technical Column, and retains data across app restart. | Browser E2E; SRS-VIEW-006/010/011; roadmap §8 acceptance |

## Remaining engineering inputs

- Commit an executable I1 OpenAPI contract alongside the first endpoint implementation, including error/version/idempotency behavior. `foundation-api.md` documents only I0 checkpoints.
- Select auth library versions and record account-linking, challenge expiry/rate limits, JWT storage/rotation, CSRF/CORS and session revocation in the authentication/security design before exposing product auth.
- Supply deployment-specific email delivery settings, Google client/redirect configuration and WebAuthn relying-party/origin settings for real integration smoke. Automated tests can use local mail capture and provider simulations; those are not evidence of configured external delivery.
- Finish I0's hosted green CI and release record. The [I0 review](increment-0-foundation-review.md) remains the source for foundation evidence and its limits.
