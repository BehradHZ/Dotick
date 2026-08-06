# Dotick — Stage 2 Spec: Core Task, Event, and Routine Management

> Process context: this spec is produced under an **Incremental development
> model** (see `ROADMAP.md` §2 for the full rationale). Stage 1 (basic
> foundation — Django/PostgreSQL/RN-Web wired together, health-check verified)
> is complete. This spec covers Stage 2, the first stage with real domain
> logic. Per the roadmap's progression rule, Stage 3 (Recurrence) does not
> begin until this stage has been used in real daily practice and its
> decisions documented.

---

## Problem Statement

The developer currently has no working system for tracking tasks, events, and
routines — Stage 1 only proved the technical pipe (browser → Django →
PostgreSQL) works, with no user-facing functionality.

Existing to-do tools don't distinguish cleanly between three different kinds
of schedulable things the developer actually needs to track:

- **Tasks** — one-off items with a target date and a hard deadline, whose
  urgency should escalate visibly and automatically the longer they're
  ignored, without silently disappearing or silently staying "not done"
  forever.
- **Events** — time-bound occurrences (a meeting, an appointment) that don't
  have a "completed" concept at all — they simply happen or don't.
- **Routines** — recurring commitments (habits) that need to be tracked one
  occurrence at a time.

Without a system that treats these as distinct entities with distinct
lifecycles, the developer either has to force everything into a single
generic "item" model (losing meaningful distinctions) or track them in
separate disconnected tools.

## Solution

Build the domain core for all three entity types on a shared underlying
schema (Class Table Inheritance), each with its own lifecycle logic:

- Tasks get a six-state status model that is almost entirely time-driven
  (`TODO → OVERDUE → MISSED → AUTO_WONT_DO`, with `DONE`/`WONT_DO` as
  explicit, reversible user overrides at any point), so the system itself
  surfaces neglected tasks without requiring the developer to manually triage
  a flat list.
- Events get a simple three-state, purely time-computed status
  (`UPCOMING`/`ONGOING`/`PAST`) with no completion concept, matching what an
  event actually is.
- Routines get single-occurrence tracking now (full recurrence generation is
  Stage 3), using the same explicit-override pattern as Task minus the
  overdue/missed distinction.
- A "Postpone" action lets the developer recover from a missed or overdue
  task in one step, with the system distinguishing between "just push the
  target date" (task still has deadline room) and "push the target date and
  extend the deadline" (task's deadline already passed).
- Every deadline change — whether from Postpone or a manual edit — is
  recorded in a full history table, so the developer can see how a task's
  deadline evolved over time, not just its current value.

This is deliberately scoped to single-user, manually-created routine
instances only. Full recurrence rules, organizational structure
(folders/lists/tags), and containerization are explicitly out of scope for
this spec — see **Out of Scope** below and `ROADMAP.md` §6 for their place in
the larger sequence.

## User Stories

**Task creation and viewing**
1. As a user, I want to create a task with a title, description, due date,
   and deadline, so that I can track something I need to do with both a
   target date and a hard limit.
2. As a user, I want to see a list of my tasks, so that I can review what's
   pending.
3. As a user, I want each task's current status to be visually distinct
   (`TODO`, `OVERDUE`, `MISSED`, `AUTO_WONT_DO`, `DONE`, `WONT_DO`), so that I
   can tell at a glance what needs attention.
4. As a user, I want a task's status to update automatically as time passes,
   without me having to do anything, so that I don't have to manually track
   which tasks have become overdue or missed.

**Task status transitions**
5. As a user, I want a task to remain `TODO` right up until its due date
   passes, so that reaching the due date doesn't itself change the task's
   urgency state — it should just start appearing in "today's" view.
6. As a user, I want a task to become `OVERDUE` once its due date has passed
   but its deadline hasn't, so that I can see it needs attention without it
   being treated as failed yet.
7. As a user, I want a task to become `MISSED` once its deadline has passed
   but is still within the grace period, so that I know it's now seriously
   late but can still act on it.
8. As a user, I want a task to automatically become `AUTO_WONT_DO` once the
   grace period after its deadline has fully elapsed with no action from me,
   so that stale tasks stop cluttering my active view without me having to
   manually close them.
9. As a user, I want to mark a task `DONE` from any status (including
   `MISSED`), so that finishing something late is still recorded as
   finished, not lost.
10. As a user, I want to mark a task `WONT_DO` from any status, so that I can
    explicitly abandon something instead of letting it silently expire.
11. As a user, I want to reverse a `WONT_DO` decision and reopen the task, so
    that a change of mind doesn't require recreating the task from scratch.

**Postpone**
12. As a user, I want to postpone a single `TODO` or `OVERDUE` task to today,
    so that I can push back something I haven't gotten to yet without
    touching its actual deadline.
13. As a user, I want to postpone a single `MISSED` task, which pushes both
    its due date to today and its deadline forward, so that a task that's
    already blown its deadline gets a genuinely fresh window rather than an
    immediately-expired one.
14. As a user, I want a "Postpone All" action that applies the correct
    postpone behavior to every `OVERDUE` and `MISSED` task at once, so that I
    can clear a backlog in one step instead of postponing tasks one at a
    time.
15. As a user, I want "Postpone All" to leave `TODO`, `DONE`, and `WONT_DO`
    tasks untouched, so that the bulk action can't accidentally reopen
    finished work or affect tasks that don't need it.

**Deadline history**
16. As a user, I want every change to a task's deadline (from Postpone or a
    direct edit) recorded with the old value, new value, and reason, so that
    I can later see how a task's deadline evolved, not just where it ended
    up.
17. As a user, I want a direct manual edit to a deadline (outside the
    Postpone flow) to be recorded distinctly from a postpone-triggered
    change, so that the history accurately reflects why each change
    happened.

**Events**
18. As a user, I want to create an event with a start time and end time, so
    that I can track things that happen rather than things I complete.
19. As a user, I want an event's status to be computed purely from the
    current time (`UPCOMING`/`ONGOING`/`PAST`), with no manual completion
    step, so that events behave correctly without me having to interact with
    them at all.

**Routines (manual, pre-recurrence)**
20. As a user, I want to manually create a single routine occurrence, so
    that I can track a recurring commitment one instance at a time before
    full recurrence support exists.
21. As a user, I want to mark a routine occurrence `DONE` or `WONT_DO`, with
    `WONT_DO` reversible, so that routine tracking follows the same
    reliable pattern as task completion.
22. As a user, I want a routine occurrence to automatically become
    `AUTO_WONT_DO` if its period elapses with no action, matching the
    self-cleaning behavior tasks have.

**Cross-cutting**
23. As a user, I want all of this to work correctly from both my laptop
    browser and my phone browser on the same network, so that Stage 2 is
    genuinely usable in daily practice, not just demonstrable on one device.
24. As a user, I want invalid input (e.g., a due date set after the
    deadline) to be rejected clearly, so that the data model's invariants
    can't be silently violated through the UI or API.

## Implementation Decisions

### Schema strategy: Class Table Inheritance (CTI)

A parent table `base_events` holds fields common to every schedulable item
(`id`, `title`, `description`, `created_at`, `updated_at`, shared timing
fields). Child tables `tasks`, `events`, and `routines` each hold a foreign
key back to `base_events` plus only the fields specific to that type.

**Rejected alternative:** Single Table Inheritance (one wide table with a
`type` discriminator). Rejected because it would leave every row full of
NULL columns for fields that don't apply to its type, working against the
per-entity-type clarity this schema needs (e.g., grace period and deadline
history attach naturally to Task specifically, not to Event). CTI also maps
more directly onto Django's multi-table inheritance / `OneToOneField`
pattern than STI does.

**Trade-off accepted:** queries spanning fields across types require a join.
Accepted as the right cost for schema clarity at this project's scale.

### Task and Event are independent entity types

Not variants of a shared "Item" type beyond the CTI parent itself. Routine is
a third, independent child type.

### Task status model

**Stored field:** `user_status` — nullable, only two non-null values:
`DONE` or `WONT_DO`. `NULL` means no explicit user decision has been made,
and the effective status falls through to computation.

**Computed effective status** (evaluated at read time, when `user_status`
is `NULL`):

| Status | Condition |
|---|---|
| `TODO` | `now <= due_date` |
| `OVERDUE` | `due_date < now <= deadline` |
| `MISSED` | `deadline < now <= deadline + grace_period` |
| `AUTO_WONT_DO` | `now > deadline + grace_period` |

Reaching `due_date` changes *which list a task appears in* (e.g., today's
view), not its status — this is a deliberate distinction, not an oversight.

**Rejected alternative:** an eager cron worker that periodically writes
status to the database. Rejected for this stage because the time-driven
states are pure functions of `now` and the task's own fields — no
background process is needed to keep them accurate. Revisit only if a
concrete need arises to trigger something (e.g., a notification) at the
exact moment a transition occurs, which a purely computed field can't do.

**Why a nullable two-value field instead of a full status enum stored
directly:** storing `DONE`/`WONT_DO`/`NULL` and deriving the rest keeps the
time-driven states from ever going stale relative to the stored value — there
is no code path where the computed and stored states can disagree, because
only one of them is ever actually written for the time-driven cases.

### Grace period

Configurable duration (e.g., 1 week, 1 month) determining how long a task
stays `MISSED` before becoming `AUTO_WONT_DO`. Intended to be a per-list
setting long-term, but Organizational Hierarchy (Stage 5) doesn't exist yet.
**For this stage:** store `grace_period` at the task level with a sensible
default; migrate to a list-level setting when Stage 5 introduces lists.

### Event status model

Purely computed, no stored status field at all — events aren't "completed."

| Status | Condition |
|---|---|
| `UPCOMING` | `now < start_time` |
| `ONGOING` | `start_time <= now <= end_time` |
| `PAST` | `now > end_time` |

### Routine instance status model (manual entry, pre-Stage-3)

Same `NULL`/`DONE`/`WONT_DO` explicit-field pattern as Task, without the
`OVERDUE`/`MISSED` distinction (a single manually-created occurrence doesn't
have a separate due-date-vs-deadline structure):

| Status | Condition |
|---|---|
| `TODO` | Occurrence not yet resolved |
| `DONE` | User marked complete |
| `WONT_DO` | User explicitly skipped, reversible |
| `AUTO_WONT_DO` | Occurrence's period elapsed with no action |

### Postpone behavior — two branches

1. **Task is `TODO` or `OVERDUE`** (deadline hasn't passed): Postpone sets
   `due_date = today`. `deadline` is untouched.
2. **Task is `MISSED`** (deadline has passed): Postpone sets `due_date =
   today` **and** advances `deadline` forward.

**Open item, not yet resolved:** the exact rule for how far `deadline`
advances in branch 2 (e.g., preserve the original due-to-deadline gap vs. a
fixed offset). Must be resolved before implementation of branch 2 begins —
flagged explicitly rather than guessed at here.

Two entry points: single-task Postpone (task detail view) and "Postpone
All" (bulk action over every `OVERDUE`/`MISSED` task, dispatching each to
the correct branch individually — not one rule applied indiscriminately).

### Deadline history

Full history retained via a dedicated table, not a lightweight counter —
chosen over a simpler `postpone_count` + `original_deadline` field pair
because the ability to reconstruct *when* each change happened (not just how
many times) was judged worth the added schema complexity for this project's
portfolio and future-analytics goals.

```
TaskDeadlineHistory
├── id (PK)
├── task_id (FK → tasks)
├── old_deadline (TIMESTAMPTZ)
├── new_deadline (TIMESTAMPTZ)
├── changed_at (TIMESTAMPTZ)
└── reason (ENUM: POSTPONE_SINGLE, POSTPONE_ALL, MANUAL_EDIT)
```

**Open item, not yet resolved:** whether this table should also cover
`due_date` changes, or stay scoped to `deadline` only. Must be resolved
before the history write-path is implemented.

### API style

REST via Django REST Framework. GraphQL and WebSockets are explicitly not
adopted for this stage — see `ROADMAP.md` §3.1 for the full list of
deliberately deferred technical decisions and why each is deferred.

### Frontend scope for this stage

React Native for Web. Functional correctness takes priority over visual
polish for this stage — every status must display correctly and
distinctly before any attention goes to styling. Layout must work on both
laptop and phone browsers (the real usage pattern), but responsive polish
is deferred.

Required screens: task list (all six statuses visually distinct), task
detail (Done / Won't Do / Postpone actions), a visible "Postpone All"
trigger, create/edit forms for Task/Event/Routine, event list reflecting
the three time-driven states, and a simple manual routine-occurrence view.

## Testing Decisions

Full detail lives in `TESTING_PLAN.md` §3 (Stage 2). Summary of approach:

- **What makes a good test here:** because Task and Event status are pure
  functions of `now`, the highest-value tests are boundary-condition tests
  at every `<`/`<=` transition point in the status tables above (e.g., `now`
  exactly equal to `deadline`, not just clearly-before or clearly-after).
  Tests must control "now" directly (a mockable/injectable clock) rather
  than depending on real wall-clock time during the test run — otherwise
  boundary tests are flaky by construction.
- **Modules to be tested:**
  - CTI schema wiring (parent/child creation, inherited-field access,
    cascade behavior on delete) — unit and integration.
  - Task status computation — unit, exhaustively covering every boundary in
    the table above, plus confirmation that `user_status` always overrides
    the computed value regardless of how stale the timestamps are.
  - Event status computation — unit, same boundary-exhaustive approach.
  - Routine instance status — unit, confirming it shares Task's
    explicit-override pattern rather than a subtly different
    reimplementation.
  - Postpone logic — unit for the two branches individually, integration
    for "Postpone All" dispatching correctly across a mixed set of tasks,
    and integration confirming Postpone correctly triggers (or correctly
    doesn't trigger) a `TaskDeadlineHistory` write depending on whether
    `deadline` actually changed.
  - Deadline history — integration tests confirming both Postpone-triggered
    and manual-edit-triggered writes get the correct `reason`, and that a
    sequence of multiple changes to the same task stays coherent.
  - CRUD endpoints — integration, including a test that invalid input
    (`due_date` after `deadline`) is rejected, not silently accepted.
- **Prior art:** none yet — this is the first stage with real domain logic,
  so the time-mocking pattern established here should be reused as-is for
  Stage 3's recurrence tests rather than reinvented.

## Out of Scope

- Full recurrence rule generation (daily/every-N-days/weekday/day-of-month,
  dual calendar support) — Stage 3.
- Containerization (Docker) — Stage 4.
- Organizational Hierarchy (folders/lists/tags), including migrating
  `grace_period` from a task-level default to a genuine per-list setting —
  Stage 5.
- Multi-user support and any sharing features.
- Native mobile/desktop builds beyond React Native for Web.
- Real-time (WebSocket/SSE) sync across devices.
- External LLM-based natural language input.
- Performance optimization (specialized indexing, caching) — revisit only
  once real usage data shows an actual bottleneck.

See `ROADMAP.md` §3.1 and §7 for the full list of deliberately deferred
items and the reasoning for each.

## Further Notes

- This spec assumes Stage 1 is complete and verified (health-check endpoint
  proven to round-trip through PostgreSQL, confirmed reachable from both
  laptop and phone browsers).
- Per the roadmap's progression rule (`ROADMAP.md` §2.5), Stage 3 does not
  begin until this stage has been used in real daily practice for a
  meaningful period, including deliberately letting some tasks go
  overdue/missed to verify the transitions hold up under real conditions —
  not just synthetic test data.
- The two open items flagged above (Postpone's exact deadline-shift rule;
  deadline history's scope) block full implementation of their respective
  areas and should be resolved as the first sub-task of this stage, before
  writing the Postpone and history code.
