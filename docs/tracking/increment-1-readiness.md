# Increment 1 readiness

> **Original baseline:** 2026-09-08
> **Reconciled:** 2026-09-18
> **Audited branch:** `increment`
> **Audited HEAD before this reconciliation:** `144f87bb29d540d110a3f6b78efac26fb7184f93`
> **Status:** **NOT CLOSED.** The current branch contains the I1 backend foundation for Identity + Folder/List/Column + Basic Task, but unresolved code/configuration blockers remain before the implementation slice can be considered ready for closure. Provider/device smoke and release evidence are later closure gates after those blockers are resolved.

## Goal and authority

Increment 1 remains restricted to:

```text
Identity
+ Folder / List / Column
+ Basic Task MVP
```

A registered user must be able to authenticate, see the Inbox, create an unscheduled Task, place it in a List/Column, edit it, mark it Done or Won't_Do, reopen/re-authenticate and retrieve it without gaining access to another user's private data.

Behavior and scope continue to follow System Definition first, then Decision Register, Formal SRS, and finally the Increment roadmap for execution order. This readiness document records implementation reality only; it does not introduce product behavior.

The following remain outside Increment 1 implementation scope:

- Event;
- Routine and RoutineCompletion;
- scheduling lifecycle and time-driven Task states;
- recurrence and reminders;
- hierarchy, rich Description/ContentBlock and Comments;
- collaboration, Sharing, Groups, Assignment and realtime collaboration;
- full Offline/Sync, branching History, Undo and selective recovery;
- AI-assisted creation, Goals, Daily Rings, scoring and statistics.

Known future compatibility constraints may shape I1 persistence/API design, but they must not cause those later capabilities to be implemented early.

## Current implementation reality

### Backend currently present

The current `increment` tree contains real PostgreSQL-backed implementation for the core I1 backend slice:

- verified email/password identity and revocable JWT sessions;
- account/profile/preferences/contact foundations;
- Google identity and Passkey adapters;
- account bootstrap for UserPreferences, Inbox and default Column;
- UUID Folder/List/Column persistence and owner-scoped organization APIs;
- exactly one Inbox per User at database level;
- exactly one default Column per List at database level;
- atomic List + default-Column creation;
- explicit Item/Task/Source composition;
- unscheduled Basic Task create/read/edit/move/status/Trash/restore;
- Task optimistic version checks and idempotent create semantics;
- stable error/request boundaries and an executable I1 OpenAPI document.

This does **not** mean the whole Increment is complete. The unresolved blockers below are part of the remaining I1 execution scope.

### Current client is not the I1 product client

At the audited HEAD, `apps/client` is the Increment 0 Foundation workbench:

- it authenticates to the developer-only Foundation API using HTTP Basic credentials kept in memory;
- it reads and writes `/api/v1/foundation/checkpoints`;
- the UI identifies itself as `INCREMENT 0 · DEVELOPMENT WORKBENCH`;
- current component tests exercise Checkpoint sign-in/create/retry/sign-out behavior rather than the I1 account-to-Task workflow.

Historical commits `006a5cbb87dbdd879ab98a16c673646f78c8c39f` (`feat(client): add usable increment 1 workspace`) and `0fc2f151e73adb2e382dfa8660e05ac276a78890` (`feat(auth): complete increment 1 sign-in client`) contain prior I1 client work, but that history diverges from the current `increment` lineage. Their behavior must not be treated as present merely because tracking documents previously described it.

The remaining client work must restore/port the required I1 product flow onto the **current** branch and reconcile it with the current backend contract rather than blindly assuming the historical implementation can be reused unchanged.

### Current Playwright coverage is Foundation-only

The checked-in Playwright E2E currently verifies the Foundation Checkpoint walking skeleton on desktop and mobile viewports. It does not currently prove the I1 account-to-Task acceptance path.

Therefore prior claims that the current branch has desktop/mobile Playwright evidence for sign-in -> bootstrap -> Inbox/List -> Task create/edit/status/move/Trash/restore are stale and are not closure evidence for the current HEAD.

### Current hosted CI does not verify `increment`

The checked-in GitHub Actions workflow still uses the historical push filter:

```yaml
branches: [main, codex, test]
```

It does not trigger on pushes to the current designated development branch `increment`. At the audited HEAD there is no hosted workflow run/check evidence for `increment`.

Historical green runs remain valid evidence for the commits they actually tested, but they must not be presented as verification of the current branch after the branch/history changes.

## Exact unresolved code-level blockers

These items are part of the remaining Increment 1 implementation scope and must be resolved before provider/device smoke can be treated as the only remaining work.

### I1-B01 — OpenAPI authentication contract is incomplete

Runtime I1 private APIs use authenticated application boundaries, but the OpenAPI document does not currently establish bearer authentication as the default/global security requirement for private operations. Only selected operations explicitly declare `bearerAuth`.

The strict compatibility test `test_private_i1_operations_inherit_bearer_authentication` is intentionally `xfail` because this mismatch is real.

Required completion condition:

- private I1 operations are represented as bearer-authenticated in OpenAPI;
- intentionally public identity ceremonies explicitly remain unauthenticated;
- contract tests pass without this `xfail`;
- runtime authentication/authorization behavior must not be weakened to match documentation.

### I1-B02 — Folder/List/Column mutation compatibility is incomplete

Task already provides the I1 reference behavior for server-owned optimistic versions and idempotent creation, but Folder/List/Column do not yet carry equivalent compatibility foundations.

The strict compatibility test `test_organization_resources_are_versioned_and_idempotent_before_implementation` remains `xfail` because the gap is real.

Required completion condition for the organization mutation surface:

- Folder, List and Column expose a positive server-owned `version` where required for stale-write detection;
- accepted mutations advance the version atomically;
- stale/conflicting writes fail rather than silently overwriting newer state;
- Folder/List/Column creation has retry identity/idempotency semantics appropriate to the current contract;
- reuse of an idempotency/operation identifier with conflicting intent is rejected;
- update/delete/restore preconditions are represented consistently in implementation and OpenAPI;
- concurrency, retry, ownership-boundary and conflict tests cover the real database behavior;
- any schema change uses new append-only migrations only;
- the strict compatibility `xfail` is removed only after the behavior is genuinely implemented.

This work is a foundational compatibility requirement for later Sync/History. It does **not** authorize implementing full Sync, branching History, field clocks, tombstone protocols or Offline reconciliation in I1.

### I1-B03 — I1 product client is absent from the current branch

The current checked-in client must be replaced or evolved from the I0 Foundation workbench into the current I1 product flow.

Required completion condition:

- product authentication uses the current I1 identity/session contract rather than Foundation HTTP Basic;
- first authenticated use performs the required account bootstrap;
- Inbox/List navigation uses the real organization API;
- the client can create and retrieve an unscheduled Basic Task;
- supported I1 Task editing, Todo/Done/Won't_Do, placement/move and recoverable Trash/restore use the current versioned backend contract;
- sign-out removes private client state;
- client tests validate the current product behavior and relevant failure/retry paths;
- no Event, Routine, scheduling, recurrence, collaboration, Sync/History or AI surface is introduced as part of this restoration.

Historical I1 client commits may be used as implementation reference, but current code and contracts are authoritative.

### I1-B04 — I1 E2E acceptance coverage is absent from current Playwright tests

Current Playwright tests prove the Foundation Checkpoint path only.

Required completion condition:

- desktop and mobile E2E exercise the real I1 client -> Django API -> PostgreSQL path;
- the scenario covers authentication, bootstrap/Inbox, Basic Task creation, persistence across reload/re-entry, at least one versioned edit/status mutation, and private-state cleanup on sign-out;
- tests use real application boundaries rather than mocked Task persistence;
- later-Increment behavior is not pulled into the E2E merely to broaden coverage.

### I1-B05 — hosted CI is not wired to the current development branch

The workflow still targets the historical `test` branch and therefore provides no automatic push verification for `increment`.

Required completion condition:

- the active CI workflow runs for the current designated development branch `increment`;
- the workflow continues to enforce the existing relevant static, migration, backend, frontend, build, security and E2E gates;
- migration-history protection remains append-only;
- a green run is obtained for the actual current I1 implementation after the blockers above are resolved.

Historical references to branch `test` in changelogs/reviews remain historical evidence and are not themselves implementation blockers. The operational CI branch filter is the stale reference that requires correction.

## Remaining execution order

Unless a smaller prerequisite is discovered, finish the remaining I1 implementation in this order:

1. correct the OpenAPI authentication contract and retire I1-B01;
2. add organization version/idempotency foundations and retire I1-B02;
3. restore/port the I1 product client against the current backend and retire I1-B03;
4. replace/extend Foundation-only Playwright coverage with the I1 acceptance path and retire I1-B04;
5. wire hosted CI to `increment`, run the complete relevant gate set, and retire I1-B05;
6. only then perform the environment/provider/device closure smoke listed below.

This ordering keeps code-level correctness separate from deployment-specific evidence and prevents external credentials or device availability from hiding implementation gaps.

## Provider/device and deployment closure gates

The following are **later closure gates**, not substitutes for the unresolved code-level blockers above. They may require credentials, a real browser/authenticator, a real device, or deployment infrastructure unavailable to automated repository tests.

After I1-B01 through I1-B05 are green:

- configure and smoke-test real email delivery in the target environment;
- configure the real Google OAuth client/origin/redirect environment and smoke the real provider path;
- smoke WebAuthn/Passkey using the target relying-party ID and trusted origins with a real supported browser/authenticator;
- configure and smoke-test the phone-contact delivery adapter where that delivery path is enabled;
- perform relevant real-device/client smoke for the supported I1 authentication and account-to-Task path, including platform-specific provider behavior that cannot be proven by repository-only tests;
- deploy/verify the edge rate-limit implementation corresponding to the declared `identity-ceremony` policy;
- create the formal Increment 1 release record/publication only after implementation, hosted CI and required provider/device/deployment evidence are green.

A provider or device smoke failure must not be hidden by mocks, skipped tests or documentation claims. Repository-test substitutes may validate adapters deterministically, but they do not count as real-provider/device evidence.

## Closure rule

Increment 1 must **not** be marked closed while any of I1-B01 through I1-B05 is unresolved.

After those code/configuration blockers are fixed, Increment 1 still remains open until the required provider/device/deployment smoke and formal release evidence are completed or explicitly re-scoped through the canonical project process.

No current document should claim that the present `increment` HEAD already has a green I1 product client, I1 Playwright account-to-Task flow, or hosted CI run when those statements are not true of the checked-in branch.
