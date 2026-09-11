# Increment 1 Basic Task Use Cases

> **Status:** Formal analysis artifact for Increment 1; this document does not assert implementation completion.
>
> **Date:** 2026-09-11
>
> **Authority:** System Definition §6.2 and related ownership/organization rules → Decision Register → SRS §§3.1–3.3 and §5.1 → this analysis artifact.
>
> **Design handoff:** `docs/design/data-model.md`, `docs/design/api-contracts.md` and `docs/design/openapi.json` define implementation-level persistence/API details. If this document conflicts with a higher-authority source, the higher-authority source wins.

## 1. Scope

These use cases formalize the Increment 1 **Basic Task MVP** analysis outputs required by the roadmap:

- Create Task;
- Edit Task;
- Complete Task, including the other user-driven outcome (`Won't_Do`) and reopening to `Todo`.

Increment 1 Task behavior is intentionally narrow. A Task can exist and remain **unscheduled**. The following are outside these use cases and remain owned by later increments:

- `due_at`, `end_at`, all-day scheduling, `deadline_at` and `grace_period_days`;
- system-driven `Overdue`, `Missed` and `Skipped` lifecycle behavior;
- dependency / `blocked_by`;
- priority;
- hierarchy;
- rich description/content blocks;
- comments;
- tags;
- recurrence and reminders;
- Event/Routine behavior;
- Group/shared-resource authorization.

Soft-delete/Trash/restore is part of the I1 persistence boundary but is not one of the three use cases requested by this analysis artifact.

## 2. Actors and shared terms

| Actor | Role |
|---|---|
| Authenticated User | Person operating on their own private Task data through a valid, non-revoked session. |
| Dotick Task Service | Server-side authority for Task identity, ownership, creator, placement, status, version and persistence. |
| Organization Service | Resolves the authenticated User's Inbox/List/Column destinations and enforces destination ownership. |

**Task identity** means the stable persisted Item/Task identity. Editing, moving, completing or reopening a Task must not recreate it under a new identity.

**Placement** means the Task belongs to exactly one Column. Its List is derived from that Column. If creation does not specify a destination, Dotick uses the authenticated User's Inbox/default Column.

**User-driven Task status in I1** is one of:

```text
Todo
Done
Won't_Do
```

## 3. Global Task invariants

These invariants apply to all use cases below.

1. Every Task has a stable UUID identity and retains that identity across edits, moves and status changes.
2. A Task title is required and must remain non-empty after normalization/validation.
3. `owner_user_id` and `created_by_user_id` are server-controlled concepts; the client cannot assign another User as owner/creator through these flows.
4. Source/provenance is separate from ownership and never grants access.
5. Every Task is placed in exactly one Column. If no Column is supplied during creation, the User's Inbox/default Column is used.
6. Any supplied destination Column must belong to the authenticated User in Increment 1. A foreign/private destination is rejected without leaking its existence.
7. Private Task lookup starts from the authenticated User's scope. A Task owned by another User is not returned merely because its UUID is known.
8. Persisted mutations are version-aware. The server owns the authoritative version; a stale edit must not silently overwrite a newer accepted mutation.
9. Retried creation uses the contract's stable operation identity/idempotency rule so a lost response does not create a duplicate Task.
10. I1 accepts only `Todo`, `Done` and `Won't_Do` as Task status values. Later lifecycle states are not implemented early.
11. I1 creation/editing does not require any date, time or all-day value. Absence of scheduling data is valid and means the Task remains unscheduled.
12. Unknown/server-owned request fields are rejected rather than silently accepted.

---

## UC-TASK-001 — Create Task

**Primary actor:** Authenticated User  
**Supporting actor:** Organization Service  
**Goal:** Persist a new private, unscheduled Task with a stable identity and valid placement.  
**Trace:** `SRS-ORG-002`, `SRS-ORG-003`, `SRS-ITEM-002`, `SRS-ITEM-003`, `SRS-ITEM-005`, `SRS-ITEM-006`, `SRS-ITEM-007`, `SRS-ITEM-008`, `SRS-TASK-001`, `SRS-TASK-020`, `SRS-NFR-SEC-003`

### Preconditions

- The User has a valid, non-revoked authenticated session.
- Account bootstrap has produced the User's Inbox and its default Column.
- The User supplies a creation operation identity required by the API idempotency contract.

### Trigger

- The User submits a request to create a Task with a title and optionally a destination Column.

### Main success flow

1. Dotick authenticates the request and resolves the current User.
2. Dotick validates the request shape and rejects unknown/server-owned fields.
3. Dotick validates that the title is non-empty.
4. If the User supplied a destination Column, Dotick resolves that Column inside the current User's ownership scope.
5. If no destination Column was supplied, Dotick resolves the User's Inbox/default Column.
6. Dotick derives `owner_user_id` and `created_by_user_id` from the authenticated User rather than client input.
7. Dotick records manual/basic Source provenance without using Source as an ownership authority.
8. Dotick creates one stable Task identity with initial status `Todo`, an initial positive server-owned version and server timestamps.
9. Dotick persists the Task as unscheduled; no scheduling value is required.
10. Dotick returns the authorized Task representation.

### Alternate / error flows

**A1 — Empty or invalid title**

- Dotick rejects the request as validation failure.
- No Task is created.

**A2 — Foreign or inaccessible destination Column**

- Dotick does not place the Task in that Column.
- The response uses the normal inaccessible/not-found surface and must not disclose another User's private structure.
- No Task is created in a fallback destination as a side effect of the rejected request.

**A3 — Client attempts to set server authority**

- Inputs such as Task ID, owner, creator, authoritative version, timestamps, trash state or privileged provenance fields are rejected when they are not part of the public create contract.
- Dotick does not trust or persist forged authority metadata.

**A4 — Retried create after response loss**

- Repeating the same creation operation with the same intent returns/resolves to the already-created logical Task rather than creating a duplicate.
- Reusing the same operation identity for a different creation intent is rejected as an idempotency conflict.

**A5 — Authentication/session invalid or revoked**

- Creation is rejected.
- No Task is persisted.

### Postconditions

- Exactly one Task exists for the accepted creation operation.
- The Task has a stable identity, owner, creator, Source, placement, status `Todo`, positive version and timestamps.
- The Task is retrievable by its owner after reauthentication.
- The Task remains unscheduled until a later increment supplies scheduling behavior.

---

## UC-TASK-002 — Edit Task

**Primary actor:** Authenticated User  
**Supporting actor:** Organization Service  
**Goal:** Change I1-editable Task data without changing Task identity or silently overwriting a newer mutation.  
**Trace:** `SRS-ITEM-002`, `SRS-ITEM-003`, `SRS-ITEM-005`, `SRS-ITEM-006`, `SRS-ITEM-007`, `SRS-TASK-001`, `SRS-TASK-020`, `SRS-NFR-SEC-003`

### Preconditions

- The User has a valid, non-revoked authenticated session.
- The target Task exists inside the authenticated User's private scope and is available for ordinary editing.
- The client supplies the expected current version required by the mutation contract.

### Trigger

- The User saves changes to the Task's I1-editable data, such as title and/or destination Column.

### Main success flow

1. Dotick authenticates the request and scopes Task lookup to the current User.
2. Dotick validates the request shape and rejects fields outside the I1 edit contract.
3. Dotick compares the supplied expected version with the authoritative current version.
4. Dotick validates every changed field; an edited title must remain non-empty.
5. If placement changes, Dotick resolves the destination Column inside the same authenticated User's scope.
6. Dotick applies the accepted changes without replacing the Task identity, owner, creator or provenance authority.
7. Dotick increments the server-owned version atomically with the accepted mutation and updates the server timestamp.
8. Dotick returns the updated authorized Task representation.

### Alternate / error flows

**A1 — Task belongs to another User or does not exist**

- Dotick returns the same inaccessible/not-found surface.
- No information about the foreign Task is disclosed.

**A2 — Stale version**

- Dotick rejects the mutation as a version/conflict error.
- The newer persisted Task is not overwritten.
- The client draft remains a client concern and may be reconciled/retried explicitly; I1 does not invent future sync merge semantics.

**A3 — Empty or invalid edited title**

- Dotick rejects the mutation.
- Previously persisted Task state remains unchanged.

**A4 — Foreign destination Column**

- Dotick rejects the entire placement mutation.
- The Task stays in its prior authorized Column.

**A5 — Attempt to edit I2+ or server-owned fields**

- Scheduling, priority, dependency, hierarchy, recurrence/reminder and other out-of-scope fields are rejected as unsupported/unknown I1 input.
- Owner, creator, ID, authoritative version/timestamps and trash authority cannot be forged through the normal edit payload.

**A6 — Authentication/session invalid or revoked**

- Editing is rejected and no Task mutation occurs.

### Postconditions

- The Task keeps the same stable identity.
- Only accepted I1 fields are changed.
- A successful mutation has a newer server-owned version/timestamp.
- Ownership and creator identity remain unchanged by ordinary edit/move operations.
- The Task remains unscheduled unless/until scheduling is introduced by its owning later increment.

---

## UC-TASK-003 — Complete Task

**Primary actor:** Authenticated User  
**Goal:** Set a user-driven Task outcome and, when requested, reopen it to `Todo` without replacing its identity.  
**Trace:** `SRS-ITEM-002`, `SRS-ITEM-005`, `SRS-TASK-001`, `SRS-TASK-014`, `SRS-TASK-020`, `SRS-NFR-SEC-003`

### Preconditions

- The User has a valid, non-revoked authenticated session.
- The target Task exists inside the authenticated User's private scope.
- The client supplies the expected current version required by the mutation contract.

### Trigger

- The User marks a Task `Done`, chooses `Won't_Do`, or reopens a user-completed Task to `Todo`.

### Main success flow — mark Done

1. Dotick authenticates the request and scopes Task lookup to the current User.
2. Dotick confirms the supplied expected version matches the current Task version.
3. Dotick validates that `Done` is a user-selectable I1 status.
4. Dotick changes Task status to `Done` without changing Task identity, ownership, creator, Source or placement.
5. Dotick increments the server-owned version atomically and updates the server timestamp.
6. Dotick returns the updated Task representation.

### Alternate flows

**A1 — Mark Won't_Do**

- Instead of `Done`, the User selects `Won't_Do`.
- Dotick applies the same ownership, version and persistence rules.
- `Won't_Do` is a deliberate user outcome and must not be converted to `Done`.

**A2 — Reopen to Todo**

- The User changes a Task from `Done` or `Won't_Do` back to `Todo`.
- Dotick preserves the same Task identity and placement.
- The mutation receives a new server-owned version/timestamp.

### Error flows

**E1 — Task belongs to another User or does not exist**

- Dotick returns the same inaccessible/not-found surface.
- No status mutation occurs.

**E2 — Stale version**

- Dotick rejects the status change as a conflict.
- The current persisted status/version is not overwritten.

**E3 — Client requests a system-controlled/later status**

- `Overdue`, `Missed` and `Skipped` are not valid direct I1 user status selections.
- Dotick rejects the request rather than introducing Increment 2 lifecycle behavior early.

**E4 — Client combines status change with unsupported I2+ fields**

- The request is rejected according to strict input validation.
- No partial mutation is committed.

**E5 — Authentication/session invalid or revoked**

- The status change is rejected and persisted state remains unchanged.

### Postconditions

- On success, status is exactly `Done`, `Won't_Do` or reopened `Todo` as requested.
- Task identity, owner, creator, provenance and placement are preserved.
- The mutation produces a newer authoritative version/timestamp.
- No system-driven scheduling state is inferred in Increment 1.

---

## 4. Acceptance mapping

| Use case | Primary observable acceptance |
|---|---|
| `UC-TASK-001` | Authenticated User creates an unscheduled Task using only a title; omitted placement uses Inbox/default Column; retry does not duplicate; another User's Column cannot be targeted. |
| `UC-TASK-002` | Owner edits title and/or moves the Task to an owned Column while preserving Task ID; stale version and foreign destination are rejected. |
| `UC-TASK-003` | Owner marks Task `Done` or `Won't_Do` and can reopen it to `Todo`; stale/cross-user/later-status mutations are rejected. |

Together these cases refine the I1 Task portion of acceptance scenarios `I1-AC-04`, `I1-AC-05`, `I1-AC-06` and `I1-AC-07` without adding Increment 2 scheduling semantics.

## 5. Design handoff constraints

Implementation/API design following this analysis must preserve these boundaries:

- Task creation supports title-only creation and optional I1 placement.
- Create is idempotent under the committed operation identity contract.
- Edit/status mutations use optimistic version checks.
- Private lookup and destination validation are owner-scoped server-side.
- Server-owned identity/ownership/version/timestamps cannot be assigned by clients.
- `Todo`, `Done` and `Won't_Do` are the only I1 Task status values exposed by the Basic Task contract.
- I2+ Task scheduling/dependency/priority/content fields must not be added to the I1 schema/API merely to reserve them for later use.
