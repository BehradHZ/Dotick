# Increment 1 formal review

Date: 2026-09-20. Scope: roadmap §8 — Identity + Folder/List/Column + Basic Task MVP.

**Status: CLOSED at `v0.2.0`.** Increment 1 repository implementation, executable evidence and documentation are reconciled. Live provider/device/edge deployment verification is not claimed; it is retained for Increment 11.

Immutable release boundary: Git tag and GitHub Release `v0.2.0`.

## Scope reviewed

Increment 1 is limited to:

- Identity and account foundation;
- Folder/List/Column organization with Inbox/default-Column invariants;
- Item identity/ownership/source foundation required by I1;
- unscheduled Basic Task create/read/edit/move/status/Trash/restore;
- the usable I1 web/Android client surface and its current API-first boundaries.

Event, Routine, scheduling, recurrence, reminders, rich descriptions/comments, collaboration, full Offline/Sync, branching History/Undo, AI, Goals, Daily Rings and scoring remain outside this review.

## Repository result

### Identity

- Email/password registration, verification/resend, sign-in and password-reset paths are implemented with disclosure-safe failure behavior.
- Rotating/revocable JWT sessions and recent-authentication checks are implemented.
- Google identity and WebAuthn Passkey boundaries are implemented and environment-driven; password fallback remains available.
- Account profile/timezone and verified secondary-contact APIs are present.
- External email/SMS adapters are optional, configurable and unavailable by default; I1 does not require a live delivery provider.

### Organization

- Bootstrap is retry-safe and creates UserPreferences plus exactly one Inbox and its default Column.
- Folder/List/Column ownership, ordering, Trash/restore and child-resolution behavior are implemented.
- Database constraints enforce at most one Inbox per User and one default Column per List.
- List/default-Column creation is atomic.
- Folder/List/Column versions, stale-write rejection and operation idempotency are implemented without introducing full Increment 6 Sync/History behavior.
- `Tab` and `Section` are not modeled as product entities, and the legacy technical default-Column name is not exposed as the only-column product label.

### Basic Task

- Explicit Item/Task composition provides stable UUID identity, owner/creator/source metadata and optimistic versioning.
- Basic unscheduled Tasks support create, retrieve, title edit, Todo/Done/Won't_Do status changes, placement/move and Trash/restore.
- Retry-safe creation and stale-write rejection are covered at the API/application boundary.
- Owner isolation is enforced by normal query/application paths.

### Client and integration

- The current Expo client is the I1 product workspace rather than the Increment 0 Checkpoint workbench.
- Signed-out identity flows, bootstrap, Inbox/List navigation and Basic Task workflows are implemented.
- Client conflict handling refreshes server-authoritative state; failed saves preserve drafts.
- Playwright contains desktop and mobile-viewport I1 paths through the real client, Django API and PostgreSQL, plus draft-preservation and cross-account isolation scenarios.
- The retained I0 Checkpoint E2E is regression evidence only and is not treated as I1 acceptance evidence.

## Acceptance reconciliation

| Increment 1 acceptance behavior | Repository evidence state |
|---|---|
| authenticate | Implemented; backend identity tests, client auth tests and password-authenticated I1 E2E pass. Live Google/WebAuthn smoke belongs to Increment 11. |
| see Inbox | Implemented through bootstrap/organization APIs and workspace E2E. |
| create a Task | Implemented in API/client and I1 E2E. |
| place Task in List/Column | Implemented in organization/task APIs and client workflow/E2E coverage. |
| edit Task | Implemented with optimistic version checks and client recovery. |
| mark Done/Won't_Do | Implemented and covered by task/client tests. |
| reopen/reload and retrieve persisted Task | Repository E2E path exists; final local/hosted release-candidate execution is still to be recorded. |
| do not retrieve another User's private data through normal queries | Implemented with owner scoping and isolation tests/E2E scenarios. |

## In-repository verification assets

The current repository contains gates for:

- append-only migration history, schema drift and fresh PostgreSQL reconstruction;
- Django/backend tests, including OpenAPI and compatibility contracts;
- client unit/component/network tests;
- Ruff, TypeScript, ESLint and Prettier checks;
- web export;
- desktop/mobile Playwright projects;
- dependency/security audits and secret scanning;
- API/web container builds, smoke and restart-persistence verification.

The two former I1 compatibility gaps — OpenAPI bearer protection and Folder/List/Column version/idempotency behavior — are represented by ordinary tests rather than expected failures.

## Closure evidence

Closure uses repository-owned proof and an immutable release boundary:

1. full local verification covers migrations, backend/frontend suites, production settings, web export, desktop/mobile I1 E2E, dependency audits, secret scanning, containers and restart persistence;
2. GitHub Actions runs the same complete gate set on the exact `v0.2.0` commit;
3. `v0.2.0` binds and publishes that verified commit;
4. the readiness, traceability, risk, security and release records agree on the I1 boundary.

Email/SMS delivery is intentionally not required and remains unavailable unless configured. Live Google/WebAuthn, authenticator, edge and production-device smoke is Increment 11 deployment evidence. No such live evidence is claimed here.

## Accepted current limitations / technical debt

- Folder and custom-Column management remain API-first rather than full I1 client surfaces.
- Passkey enrollment, Google linking, profile/contact/session management remain API-first surfaces.
- Client credentials remain session-memory only; durable secure credential storage belongs to a later security-reviewed slice.
- Edge rate limiting is a deployment responsibility and intentionally has no process-local Django substitute.
- Provider-specific native Google/Passkey behavior is not claimed.
- Self-service email registration/reset and phone-contact verification require a deployment-provided delivery adapter; the `v0.2.0` release does not configure one.
- Later-Increment scheduling, collaboration, Offline/Sync/History and permanent purge behavior remain deferred.

## Review decision

The checked-in Increment 1 implementation is coherent with the defined I1 boundary. Scope, acceptance, regressions, relevant repository security checks, traceability, design reconciliation and review pass at `v0.2.0`. **Increment 1 is CLOSED.** Deployment-specific provider/device/edge work remains with Increment 11.
