# Increment 1 readiness

> **Original baseline:** 2026-09-08
> **Reconciled:** 2026-09-16
> **Status:** implementation and hosted CI are green for the defined I1 product slice; configured external-provider/delivery smoke and formal Increment 1 release/publication remain open.

Identity, account/profile/contacts/preferences, Inbox/Folder/List/Column and Basic Task are implemented against PostgreSQL. The Expo product client covers the initial account-to-Task workflow. The current hosted workflow verifies the branch end to end; this document records the remaining release evidence without changing product scope.

## Goal and authority

A registered user signs in, sees their Inbox, creates an unscheduled Task, places it in a List/Column, edits it, marks it Done or Won't_Do, and retrieves it after reopening/re-authenticating. Another account cannot access it.

Read System Definition §§6.1, 6.2, 6.13 and 8.3–8.6 first, then Decision Register, SRS v2.9, and roadmap §§7.6/8. The prototype supplies visual and interaction examples only. Implementation history is reconciled in [development-commit-audit.md](development-commit-audit.md).

## Delivered I1 boundary

1. **Verified email identity — implemented and tested:** register, send/verify/resend code, password sign-in, password reset, JWT renewal/revocation and sign out.
2. **Account and credential adapters — implemented and tested:** mutable profile fields, IANA timezone preference, Google assertion/linking, optional Passkey enrollment/sign-in/list/delete, independent password fallback, verified secondary contacts and session management.
3. **Account bootstrap — implemented and concurrency-tested:** UserPreferences plus exactly one Inbox and exactly one default Column are provisioned atomically/idempotently. Repeated and concurrent bootstrap requests converge on the same resources.
4. **Organization — implemented and tested:** personal Folder/List/Column CRUD, nullable Folder placement, manual ordering, immutable Inbox/default Column rules, recoverable Folder/List deletion/restore and explicit child-resolution behavior.
5. **Basic Task — implemented and tested:** explicit Item/Task/Source composition, stable UUIDs, owner/creator/provenance separation, unscheduled create/read/edit/move, Todo/Done/Won't_Do, optimistic versions, idempotent create and recoverable Trash/restore.
6. **Product client — implemented for the I1 slice:** signed-out email flows, sign-in/bootstrap, Inbox/List navigation, List/Task creation, Task edit/status/move/Trash/restore, refresh/sign-out, Persian/English titles, web Google/Passkey surfaces and Expo-Go LAN API discovery.
7. **Executable API contract — implemented:** OpenAPI 3.1 covers the exact published I1 route set and is guarded by schema validation, reviewed canonical hash, route-set equality, stable error-envelope checks and strict input/request-boundary tests.
8. **Hosted verification — green:** current GitHub Actions run `35057831342` succeeded for audited HEAD `7302ca3b18a79af35058828102bb62e845a56645` before this documentation reconciliation. It covered static checks, traceability, migrations, backend/Golden Time tests, production settings, frontend tests, web export, desktop/mobile E2E, dependency audits, secret scan, container builds and persistence smoke.

Scheduling, Event/Routine implementation, rich hierarchy/descriptions/comments/audit, collaboration, full offline reconciliation/history/undo, AI and later views retain their owning increments.

## Implementation rules confirmed by code and tests

| Area | Current I1 rule | Evidence |
|---|---|---|
| Inbox | A real special List; at most one per user at database level; write path bootstraps exactly one; cannot be renamed/deleted. | organization model/application + bootstrap/API tests |
| Folder | Optional; List may have no Folder. | organization model/API tests |
| Titles/order | Container UUID is identity; duplicate titles are valid; position is mutable ordering metadata. | model/API tests |
| Default Column | At most one per List at database level; List creation creates it atomically; bootstrap repairs a missing default. | constraint + transaction/concurrency tests |
| Technical default name | Internal default title is not exposed as legacy `not_sectioned`; when it is the sole Column the client does not present that technical concept. | bootstrap/client tests |
| Account | Stable UUID User with mutable unique handle, display name, optional picture reference and IANA timezone preference. | account API/tests |
| Contacts | Secondary email/phone stays pending until code verification; only verified contacts enter active flows; phone is E.164. | contact models/application/API tests |
| Placement | Each Task has one Column; destination ownership is checked from authenticated actor scope inside writes. | Task/organization negative tests |
| Task composition | Shared Item identity/metadata + explicit one-to-one Task and Source; Task status stays on Task. | Item/Task models/migrations/tests |
| Delete/restore | Item/Folder/List ordinary deletion is recoverable; Column has no independent Trash lifecycle; descendant handling is explicit. | API/application tests |
| Concurrency/retry | Server-owned positive version rejects stale writes; idempotency prevents duplicated create after retry. | Task HTTP tests |
| Migration history | Existing numbered migrations are append-only; modifications/deletes/renames fail CI and new schema changes require a new migration. | `scripts/check_migrations.py` + migration-history tests |

## I6 compatibility retained by I1

- Persisted entities use stable UUIDs; moving/renaming does not recreate identity.
- Item mutation version is server-owned and incremented atomically; clients do not provide authoritative timestamps/version values.
- Stale online edits fail with a stable conflict surface instead of silently overwriting newer state.
- Retry identity/deduplication exists for I1 creation; future full sync retention policy stays with I6.
- Trash/restore preserves enough origin metadata for later recovery/history work.
- I1 versioning is not presented as the complete future History model.
- Every private operation begins from authenticated owner scope; ordinary staff receives no product-endpoint bypass.

## Acceptance evidence

| ID | Observable scenario | Current evidence |
|---|---|---|
| I1-AC-01 | Unverified email cannot authenticate/discover; verification error paths fail; successful verification enables password sign-in. | backend HTTP tests + signed-out client tests + hosted CI |
| I1-AC-02 | Password reset works; JWT sessions renew/revoke; credentials/tokens stay out of normal structured logs. | identity/session tests + logging controls + hosted CI |
| I1-AC-03 | Repeat/concurrent bootstrap yields exactly one Inbox/default Column; Inbox is immutable; Lists may have no Folder and duplicate titles. | PostgreSQL concurrency/API tests + hosted CI |
| I1-AC-04 | Title-only Task persists without dates; UUID/owner/creator/manual provenance survive re-authentication. | real client/API/PostgreSQL E2E + hosted CI |
| I1-AC-05 | Move/edit/status/reopen works; invalid input/forged metadata fail; failed client save retains draft. | Task API + client component/E2E tests |
| I1-AC-06 | A second account cannot read/write/move/delete or use foreign destinations; staff has no ordinary endpoint bypass. | two-account HTTP matrix |
| I1-AC-07 | Stale version cannot overwrite newer data; retried create does not duplicate. | PostgreSQL/API conflict and idempotency tests |
| I1-AC-08 | Ordinary delete leaves active queries, preserves recovery metadata and respects container/Column rules. | API/application/client tests |
| I1-AC-09 | Google/Passkey/password share one internal account/session model and linking proof is checked. | deterministic provider/WebAuthn tests; **configured real-provider smoke still open** |
| I1-AC-10 | Desktop/mobile account-to-Task workflow stores Persian/English titles, hides sole technical Column concept and persists across server/app re-entry. | Playwright desktop/mobile against Django + PostgreSQL |

## Security and contract hardening already delivered

- explicit host, CORS and CSRF trusted-origin allowlists; wildcard host/origin trust rejected;
- HTTPS-only non-local trusted/CORS/WebAuthn origins with secure redirect/cookie/HSTS/proxy settings;
- JSON-only `/api/v1/` write boundary with 16 KiB body cap and stable malformed/unsupported-media errors;
- stable error code/envelope and unknown-field rejection;
- CORS permits `If-Match` for versioned mutations without enabling credentials or untrusted origins;
- identity-sensitive operations carry OpenAPI `x-edge-rate-limit-policy: identity-ceremony` metadata. Thresholds/enforcement are deployment-edge responsibilities, not an in-process limiter claim;
- OpenAPI document validity, reviewed hash and exact Django route set are CI-guarded;
- historical migrations are immutable through the append-only CI gate.

## Remaining gates for formal Increment 1 closure

- Configure and smoke-test real email delivery in the target environment.
- Configure the real Google OAuth client/redirect environment and smoke the real provider path.
- Smoke WebAuthn using the target relying-party ID/origins with a real browser/authenticator.
- Configure and smoke-test the phone-contact delivery adapter.
- Define/deploy the edge rate-limit implementation matching the declared identity-ceremony policy and verify its thresholds in the target environment.
- Create the formal Increment 1 release record/publication after the configured-provider/release evidence is green.

Hosted CI itself is **not** an open gate anymore. Increment 0 is already formally closed in repository tracking. No GitHub Release or production deployment is claimed for Increment 1 yet.
