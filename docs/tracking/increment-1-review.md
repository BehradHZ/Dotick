# Increment 1 formal review

Date: 2026-09-20. Scope: roadmap §8 — Identity + Folder/List/Column + Basic Task MVP.

**Status: RELEASE CANDIDATE — EXTERNAL VERIFICATION PENDING.** The Increment 1 repository implementation and executable in-repository evidence are reconciled. This review does not close Increment 1 and does not claim real-provider/device/edge verification, a final green release-candidate SHA, a `v0.2.0` tag, or a published GitHub Release.

Implementation baseline before this review: `09630b5dd4b9597562e0f7ef426b7bfce5bdeb73`.

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
- External email/SMS adapters are configurable but real target-provider delivery is not yet evidenced.

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
| authenticate | Implemented; backend identity tests, client auth tests and I1 E2E exist. Real Google/WebAuthn/provider smoke remains external. |
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

## Pending external and release evidence

This review remains open at release-candidate status until all applicable evidence below is recorded:

1. hosted CI is retargeted to `increment` and a final candidate SHA has a green full run;
2. the required local/Codex release-candidate verification is executed against the exact candidate SHA;
3. real email registration/resend/reset delivery succeeds;
4. real SMS verification succeeds, including invalid-code rejection;
5. real Google sign-in/account mapping and linking protection are exercised;
6. real WebAuthn enrollment/authentication/deletion/password fallback are exercised on a valid HTTPS origin;
7. deployed proxy/CDN edge rate limiting is exercised below/above threshold and after recovery window;
8. non-secret provider/device/deployment evidence is recorded;
9. `v0.2.0` is bound to the exact verified SHA, tagged and published.

Mocks, local adapters, provider simulations and historical CI runs do not satisfy these external gates.

## Accepted current limitations / technical debt

- Folder and custom-Column management remain API-first rather than full I1 client surfaces.
- Passkey enrollment, Google linking, profile/contact/session management remain API-first surfaces.
- Client credentials remain session-memory only; durable secure credential storage belongs to a later security-reviewed slice.
- Edge rate limiting is a deployment responsibility and intentionally has no process-local Django substitute.
- Provider-specific native Google/Passkey behavior is not claimed.
- Later-Increment scheduling, collaboration, Offline/Sync/History and permanent purge behavior remain deferred.

## Review decision

The checked-in Increment 1 implementation is coherent with the defined I1 boundary and has the required repository-side implementation/test assets for release-candidate verification. **Increment 1 is not CLOSED.** It remains **RELEASE CANDIDATE — EXTERNAL VERIFICATION PENDING** until the pending hosted/local/provider/device/edge checks and publication record are completed.
