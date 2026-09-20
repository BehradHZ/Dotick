# Development Commit Audit

> **Audit date:** 2026-09-16
> **Branch:** `test`
> **Documentation-only baseline:** `b61a54a8a52abcfbe2a200ca76bdf198a86be860`
> **First implementation commit:** `a0a16baad9ec0477b608c559f276538413a5c316`
> **Audited HEAD:** `7302ca3b18a79af35058828102bb62e845a56645`
> **Audited implementation commits:** **148** (`b61a54a..7302ca3`, exclusive of the baseline)

## Purpose

This record reconciles the complete implementation history after the repository was reset to documentation and empty implementation placeholders. It records what the commits collectively made true in the current branch and which documentation families must reflect those facts.

This is an implementation-evidence document, not a new product-behavior authority. Product behavior remains governed by System Definition -> Decision Register -> SRS. A commit cannot silently redefine product scope.

## Audit method

Every commit in the 148-commit range was classified by its net effect and checked against the current `test` tree so that temporary implementations, later fixes, formatting-only commits, and merges are not misreported as current behavior.

- `feat` / behavior-changing `fix`: reconcile design, contract, development, operations, risk, tracking, or release evidence as appropriate.
- `test`: record verification/evidence changes; do not invent product behavior from a test alone.
- `ci` / operational `chore`: reconcile quality, migration, deployment, or development procedures.
- `docs`: retain the intended authority of the edited document and reconcile later implementation status separately.
- `style` / formatting-only changes: no behavioral documentation delta.
- merge commits: no independent behavior claim unless the merge introduced a net state not already represented by its parents.

## Phase 1 — Increment 0 scaffold and engineering baseline

The first implementation sequence established Django/DRF, the Expo universal client, locked Python/Node dependency management, environment configuration, Ruff/ESLint/Prettier/TypeScript checks, PostgreSQL, the Identity module, UUID custom User, case-insensitive email uniqueness, Argon2-first password hashing, and the first migrations.

Increment 0 then added the developer-only persisted Checkpoint resource, migration checks, developer account provisioning, `/health`, PostgreSQL-backed `/ready`, the versioned foundation API, stable error envelopes, request correlation IDs, no-cache API behavior, structured safe logging, Golden Time execution, client component/network tests, desktop/mobile Playwright coverage, Docker/Compose topology, dependency/secret audits, production deployment checks, and hosted CI. The verified foundation snapshot and `releases/v0.1.0.md` formally close Increment 0; no public GitHub Release or production deployment is implied.

**Documentation impact:** Increment 0 review/release records, environment setup, quality strategy, deployment/operations, and changelog must describe hosted evidence rather than a planned scaffold.

## Phase 2 — Increment 1 scope, analysis and design guards

Before the main I1 implementation, commits added executable scope guards and analysis/design traces for authentication, Folder/List/Column navigation, basic Task behavior, ownership/creator/source separation, physical ERD constraints, I6 compatibility, and risk controls. These guards intentionally keep Event, Routine, collaboration, full offline sync/history and other later-Increment capabilities out of the I1 schema/API.

**Documentation impact:** I1 readiness and risk treatment must distinguish closed product decisions from historical/open design references and keep later-Increment capabilities deferred.

## Phase 3 — Product identity and account

The Identity implementation evolved through verified email registration, single-use verification/resend flows, password sign-in and reset, short-lived access tokens, rotating database-backed refresh sessions, logout/session revocation, Google identity assertion and explicit linking, optional WebAuthn Passkey registration/authentication/list/delete, recent-auth/user-verification protections, account profile fields, IANA timezone preferences, verified secondary email/phone contacts, and account authentication-method presentation.

Later fixes ensure pending contacts do not enter active/discoverable flows, phone contacts use E.164 validation, Passkey operations re-check recent authentication, and Google transport no longer depends on a requests-only path.

**Documentation impact:** authentication design, security design, OpenAPI, I1 readiness/reviews, environment provider configuration, risk controls, and changelog must describe the implemented adapters while retaining configured real-provider smoke as a release gate.

## Phase 4 — Account bootstrap and organization

The organization slice added UUID Folder/List/Column persistence with owner scope, nullable Folder placement, manual positions, recoverable Folder/List trash state, exactly one Inbox per owner, exactly one default Column per List, atomic List+default-Column creation, and idempotent/concurrent account bootstrap for UserPreferences + Inbox + default Column. The bootstrap path can repair a pre-existing Inbox that lacks its default Column.

Folder/List/Column HTTP boundaries were then completed with owner-isolated CRUD, ordering, container Trash/restore rules, child-resolution behavior, immutable Inbox/default-Column rules, and query indexes including List `(folder, position)`.

No `Tab` or `Section` entity was introduced. The sole technical default Column name is not exposed as the legacy `not_sectioned` concept.

**Documentation impact:** organization/API/design tracking must describe actual constraints, transaction boundaries, recovery behavior and indexes rather than planned endpoints.

## Phase 5 — Basic Task MVP

The I1 Task slice added explicit Item/Task/Source composition, stable UUID identity, ownership/creator/provenance separation, unscheduled Task creation, Todo/Done/Won't_Do status, read/edit/move, optimistic server-owned versions, idempotent create semantics, recoverable Trash/restore, owner-scoped destination validation, and recovery metadata compatible with later history/sync work.

Public-boundary tests cover cross-account denial, stale-version conflict, duplicate-retry prevention, forged metadata rejection, container/Column deletion behavior, and restore fallback rules.

**Documentation impact:** I1 readiness/reviews, OpenAPI, test strategy, risk register and changelog must treat Basic Task as implemented rather than prospective.

## Phase 6 — Product client integration

The Expo client moved off the I0 workbench and onto the I1 product API. It now covers signed-out email identity flows, sign-in/bootstrap, Inbox/List navigation, List and Task creation, Task edit/status/move, Trash/restore, refresh/sign-out, Persian and English titles, LAN API discovery for Expo Go, and configured web Google/Passkey sign-in surfaces. Tokens intentionally remain session-memory only.

Desktop and mobile Playwright workflows exercise the real client -> Django API -> PostgreSQL path for the account-to-Task slice. Web export and Android bundle checks are part of verification.

**Documentation impact:** the historical backend review's old claim that the client still used the I0 workbench is superseded; client integration is locally and in hosted CI verified, while configured external-provider/device smoke remains open.

## Phase 7 — Contract and API hardening

The published Increment 1 OpenAPI 3.1 document now covers the complete currently published I1 route set for Identity, Account, Folder/List/Column, Task and Trash. Regression tests validate OpenAPI 3.1, lock a reviewed canonical contract hash, and require the contract paths to exactly match Django's published I1 routes.

The API also gained stable error codes/envelopes, strict rejection of unknown input fields, a versioned JSON request boundary, a 16 KiB request-body limit, explicit rejection of non-JSON/malformed bodies and malformed `Content-Length`, and CORS support for version preconditions such as `If-Match` without enabling wildcard origins or credentialed cross-origin access.

Identity-sensitive ceremonies are marked in OpenAPI with `x-edge-rate-limit-policy: identity-ceremony`. This is a deployment/edge enforcement contract; it does not claim an in-process limiter exists merely because the metadata is present.

**Documentation impact:** API contracts, security design, test strategy, deployment notes and changelog must reflect the executable contract and transport boundary.

## Phase 8 — Production/security hardening

Production-like configuration now requires explicit host, CSRF trusted-origin and CORS allowlists; wildcard host/origin trust is rejected. Non-local trusted/CORS/WebAuthn origins must use HTTPS. Secure redirect/cookie/HSTS/proxy settings are exercised by the production deployment check.

Safe structured request logging keeps a generated request ID and an allowlisted field set while excluding credentials, tokens, bodies and free-form exception content. External providers remain adapters and are not allowed to make core manual task management unavailable.

**Documentation impact:** security, monitoring, deployment and environment docs must treat these as implemented guardrails, while reverse-proxy deployment and configured provider smoke remain Increment 11 concerns.

## Phase 9 — CI, migration and query hardening

The hosted workflow now runs locked dependency installs, Ruff/ESLint/Prettier/TypeScript, traceability, migration/schema-drift checks, backend and Golden Time tests, production Django checks, frontend tests, web export, desktop/mobile E2E, Python/npm audits, secret scanning, non-root container builds, container smoke and persistence-after-restart checks.

The latest audited HEAD workflow (`35057831342`) completed successfully. Historical numbered Django migrations are now append-only: CI diffs migration history against the appropriate base and rejects modification, deletion or rename of an existing migration; schema changes must be expressed as new migrations. A fresh-database verification path remains in place.

**Documentation impact:** hosted CI is no longer an open I1 engineering gate. Optional delivery and live provider/device/edge smoke remain Increment 11 deployment concerns. Formal Increment 1 publication was completed later at `v0.2.0`.

## Canonical-document conclusion

The audit found no implementation change that requires redefining current product behavior in System Definition, Decision Register or SRS. The implementation follows the current I0/I1 scope and the Traceability Matrix remains a requirement-to-authority/planned-Increment artifact rather than a commit log.

Therefore this reconciliation updates implementation/design/quality/operations/tracking status without promoting implementation accidents into product requirements.

## Historical status after this audit

- **Increment 0:** formally closed in repository tracking; hosted CI evidence exists.
- **Increment 1 backend:** implemented for the defined I1 boundary.
- **Increment 1 minimal client:** implemented for the account-to-Task workflow.
- **Increment 1 hosted CI:** green at audited HEAD `7302ca3` (run `35057831342`).
- **Superseded closure status:** Increment 1 later closed at `v0.2.0`; deployment-specific real delivery, Google, WebAuthn and edge evidence remains assigned to Increment 11.
- **Not pulled forward:** Event/Routine, rich hierarchy/descriptions/comments/audit, full offline sync/history/undo, collaboration, AI, goals/rings/statistics and other later-Increment scope.
