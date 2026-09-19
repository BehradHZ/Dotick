# Increment 1 readiness

> **Original baseline:** 2026-09-08
>
> **Reconciled:** 2026-09-19
>
> **Audited branch:** `increment`
>
> **Implementation baseline before this documentation commit:** `d26e3c3`
>
> **Status:** **NOT CLOSED.** The repository implementation slice is present. Final hosted verification, real-provider/device/deployment smoke and release publication remain pending.

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

External email and SMS delivery are configurable adapters. Google OAuth and WebAuthn relying-party settings are environment-driven and fail cleanly when unavailable or invalid. These configuration paths do not constitute real-provider smoke.

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
| I1-B05 hosted CI for `increment` | **Open.** Workflow push branches remain `main`, `codex`, and `test`; no final-SHA hosted evidence exists for current `increment`. |

## Remaining closure gates

Increment 1 remains open until all applicable evidence exists:

1. update hosted CI targeting so the active `increment` branch/final I1 SHA runs the full repository gate set, then record a green final-SHA run;
2. configure and smoke-test real target-environment email delivery;
3. configure and smoke-test the real Google OAuth browser/provider path;
4. smoke WebAuthn with the target RP ID/origin and a real supported browser/authenticator;
5. configure and smoke-test phone delivery where enabled;
6. deploy and verify the shared proxy/CDN `identity-ceremony` rate-limit policy; repository policy variables/tests alone are not enforcement;
7. perform required supported-device/client smoke;
8. create the formal Increment 1 release record/publication.

Mocks, adapter tests, local provider simulations and historical CI runs do not replace these gates. No Git tag, GitHub Release or production deployment is claimed.

## Closure rule

Do not mark Increment 1 closed until final-SHA hosted verification, required real-provider/device/deployment evidence and formal release publication are recorded. Later-Increment scope remains deferred.
