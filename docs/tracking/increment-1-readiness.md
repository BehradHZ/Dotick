# Increment 1 readiness

> **Original baseline:** 2026-09-08
>
> **Reconciled:** 2026-09-20
>
> **Audited branch:** `increment`
>
> **Release boundary:** `v0.2.0`
>
> **Status:** **CLOSED.** Scope, acceptance, regressions, security checks, traceability, design reconciliation and formal review are complete at the `v0.2.0` release boundary.

## Scope and authority

Increment 1 remains restricted to:

```text
Identity
+ Folder / List / Column
+ Basic Task MVP
```

System Definition, Decision Register and Formal SRS define behavior. The roadmap defines implementation order. This document reports current implementation evidence only.

Event, Routine, scheduling, recurrence, reminders, rich content/comments, collaboration, full Offline/Sync, branching History/Undo, AI, Goals, Daily Rings and scoring remain outside I1.

## Current implementation

### Backend

The checked-in Django/PostgreSQL implementation includes:

- verified email/password registration, verification, reset and enumeration-safe resend/request responses;
- rotating revocable JWT sessions, session listing/revocation and recent-authentication checks;
- Google ID credential sign-in/linking and WebAuthn Passkey registration/authentication adapters;
- account/profile/timezone and verified secondary-contact APIs;
- Inbox/default-Column bootstrap plus owner-scoped Folder/List/Column CRUD, ordering, Trash/restore and child-resolution rules;
- positive server-owned versions, stale-write rejection and retry-safe `operation_id` semantics for Folder/List/Column/Task creation and mutation boundaries;
- unscheduled Basic Task create/read/edit/move/status/Trash/restore;
- stable request/error boundaries and an executable OpenAPI 3.1 contract with global bearer authentication and explicit public exceptions.

External email and SMS delivery are optional configurable adapters and remain unconfigured by default. Google OAuth and WebAuthn relying-party settings are environment-driven and fail cleanly when unavailable or invalid. Automated adapter, configuration and security tests satisfy I1 repository acceptance; enabled target-provider smoke belongs to Increment 11 deployment hardening.

### Client

The checked-in Expo client is the I1 product client, not the I0 Foundation workbench. It supports web and Android and currently provides:

- registration, email verification/resend, password reset and password sign-in;
- configured web Google and Passkey sign-in;
- bootstrap, Inbox/List navigation, List creation and Basic Task creation/edit/status/move/Trash/restore;
- in-memory session handling, refresh rotation and private-state cleanup on sign-out;
- network/conflict recovery and draft preservation.

Folder management, custom Column management, Passkey enrollment, Google linking, profile/contact/session management and provider-specific native sign-in remain API-first or later client work; they are not claimed as current UI features.

### Acceptance and compatibility evidence present

- OpenAPI compatibility tests require bearer protection for private operations and explicit public authentication exceptions.
- Folder/List/Column/Task compatibility tests require stable UUIDs, versions, idempotent creation and recoverable deletion without pretending I1 implements full Sync/History.
- Client tests cover signed-out identity flows, provider availability, session privacy, workspace/list/task behavior, conflicts and recovery.
- Playwright covers the real I1 client-to-Django-to-PostgreSQL path on desktop/mobile projects, including sign-in, bootstrap, List/Task creation, status, Trash/restore, reload persistence and sign-out.
- Separate E2E coverage checks draft preservation and cross-account isolation. The retained I0 Checkpoint regression is regression coverage only, not I1 acceptance evidence.

Historical test counts and hosted runs belong only to the exact commits that produced them. They are not presented as proof for the current local HEAD.

## Resolved blockers from the 2026-09-18 audit

| Audit item | Current state |
|---|---|
| I1-B01 OpenAPI bearer contract | Resolved; strict compatibility test is an ordinary passing test. |
| I1-B02 Folder/List/Column version/idempotency | Resolved in implementation, migrations, OpenAPI and PostgreSQL concurrency/conflict coverage. |
| I1-B03 product client absent | Resolved; current `apps/client` is the I1 product client. |
| I1-B04 product E2E absent | Resolved; current Playwright suite contains I1 product acceptance and isolation scenarios. |
| I1-B05 hosted CI for `increment` | Resolved; the workflow targets `increment`, and the exact `v0.2.0` commit is the canonical hosted verification boundary. |

## Closure evidence

Increment 1 closes at `v0.2.0` with:

1. full local verification of migrations, backend and client suites, production settings, web export, desktop/mobile I1 E2E, dependency audits, secret scanning, containers and restart persistence;
2. the complete hosted repository workflow on the exact tagged commit;
3. traceability and design documents reconciled to implemented behavior;
4. this readiness record and the formal Increment 1 review;
5. the `v0.2.0` tag and GitHub Release as the immutable publication record.

Real email/SMS transport is not required for this release and remains disabled unless configured. Live Google/WebAuthn provider, authenticator, proxy/CDN and supported production-device smoke remains explicit Increment 11 deployment work. This deferral does not claim those checks occurred.

## Closure rule

Increment 1 is closed only at the immutable `v0.2.0` release boundary after its exact-commit hosted workflow and publication complete. Later-Increment scope and deployment evidence remain deferred to their owning increments.
