# Dotick — Engineering Roadmap & Decision Record

<!-- ## 0. Purpose of This Document

This document is the single source of truth for how Dotick is built: the process
model governing development, the technology stack, the domain decisions already
made, and the stage-by-stage plan for building the system. It exists so that every
decision made in design discussion is captured as a concrete, buildable feature
before implementation starts — not lost in conversation history.

A companion document, `TESTING_PLAN.md`, breaks down the required tests for each
stage described here.

--- -->

## 1. Project Overview

### 1.1 Vision

Dotick is a task, event, and routine management platform, starting as a web
application and designed so its core domain logic can later extend into:

1. **A personal productivity tool** — the primary, immediate goal.
2. **A portfolio-quality software engineering artifact** — the process discipline
   and documentation in this repository are as much a deliverable as the running
   application.
3. **The reusable core of a future enterprise task/workflow product** — this
   constrains the domain layer to remain decoupled and free of premature
   single-user assumptions baked into the data model, even while the UI and
   scope stay personal-only for now.

### 1.2 Constraints That Shaped Every Decision Below

- **Solo developer.** No team, no fixed sprint cadence, no separate "customer"
  role — the developer is the only user for the foreseeable future.
- **No fixed deadline**, but a multi-month horizon. Time pressure is not a
  reason to skip engineering rigor.
- **First real experience** with formal software architecture and with
  disciplined testing. The plan below is written to *teach* these skills
  incrementally, not to assume them.
- **Deployment target for the early stages:** the developer's own laptop acting
  as the server, reachable from both the laptop's browser and a phone on the
  same network (or via a tunnel). Cloud deployment is out of scope until
  explicitly revisited.

---

## 2. Software Process Methodology

### 2.1 Process Model: Incremental Development

Dotick follows an **incremental process model**. The system is built as a
sequence of stages. Each stage:

- Adds one coherent, meaningful capability.
- Must be **used in actual daily practice** before the next stage begins.
- Is documented with a short written record of the decisions made and why
  alternatives were rejected — this document *is* that record for Stages 1–5,
  updated as each stage completes and the next is refined.

### 2.2 Why Not the Alternatives

| Model | Core assumption that fails here | Verdict |
|---|---|---|
| **Waterfall / V-Model** | Requires requirements to be fully known and fixed before design begins. ~20% of this project's requirements (sharing, organizational structure specifics) are explicitly still open and expected to evolve from real usage. | Rejected |
| **Scrum** | Assumes a fixed sprint cadence and a team to synchronize against. There is no team and no meaningful cadence to impose — sprint boundaries would be arbitrary process overhead with no one to coordinate with. | Rejected |
| **Extreme Programming (full)** | Assumes a customer role distinct from the developer, providing continuous prioritized input. Here the developer *is* the sole user — there is no second party for that negotiation loop to coordinate. | Rejected as a full methodology |
| **Unified Process / RUP** | Justifies its formal artifact set (Vision Document, SRS, SAD, SDP, Business Case, revised at every phase gate) through the need to coordinate multiple stakeholders. For a one-person project, maintaining that artifact machinery in parallel with the software would cost more time than it returns. | Rejected |
| **Incremental (chosen)** | Only requires the *problem* to be understood up front, not every implementation detail. The two core problem statements (task/routine/event separation with distinct lifecycles; non-corrupting recurrence and rollover handling) are stable. What remains open are implementation-design questions, which the incremental model is built to resolve stage by stage. | **Adopted** |

### 2.3 Practices Borrowed Informally (Not as Full Methodologies)

Some Scrum/XP practices are valuable independent of their parent methodology's
team scaffolding, and are adopted informally:

| Practice | How it's applied here |
|---|---|
| **User Stories** | Requirements for each stage are phrased as *"As a user, I want X so that Y"* before implementation, even though there's only one user. |
| **Test-First Development** | Tests are written before or alongside implementation for every stage, not bolted on afterward. See `TESTING_PLAN.md`. |
| **Continuous Refactoring** | Code is improved incrementally as understanding deepens, rather than requiring a complete upfront design. |
| **KISS (Keep It Simple, Stupid)** | The simplest design that satisfies the current stage's requirement is chosen; complexity is added only when a later stage demonstrates the need. This is the deciding principle behind several choices below (e.g., computed status fields instead of a cron worker). |
| **Personal Kanban** | Work within a stage is tracked on a simple `To Do → In Progress → Done` board (e.g., GitHub Projects), without sprint ceremonies. |

### 2.4 Documentation Rigor

- **Style:** living documentation — this file and its siblings are updated as
  decisions are made, not written once and frozen.
- **Core artifacts, in the order they will be produced:**
  1. This roadmap and decision record.
  2. Use-case diagram (scope confirmation before class modeling).
  3. State diagrams (per entity lifecycle — Task, Event, Routine instance).
  4. Class diagram / CRC cards (domain model structure).
  5. ER diagram (derived from the class model once entities are settled).
  6. REST API contract specification (per stage, as endpoints are added).
- **Why this order:** producing a class or ER diagram before a domain decision
  is finalized tends to *force* that decision implicitly through the notation
  itself (e.g., drawing inheritance arrows before deciding CTI vs. STI). Domain
  decisions are made in discussion first; diagrams document the decision
  afterward, precisely enough to catch edge cases.

### 2.5 Progression Rule

No new stage begins until:
1. The previous stage has been used in real daily practice for a meaningful
   period.
2. Its key decisions are documented (this file, updated).
3. At least one real lesson from using it has informed the plan for what comes
   next.

If a stage starts without these being true, that's a signal the roadmap is
being followed mechanically rather than being learned from — and a reason to
pause.

---

## 3. Technology Stack

| Layer | Choice | Reasoning |
|---|---|---|
| **Frontend** | React Native for Web | Single codebase now serves the web app; positions later native mobile builds to reuse the same business logic and component structure without a rewrite. |
| **Backend** | Python — Django | Chosen deliberately as a learning goal alongside the project. Django's batteries-included structure (ORM, migrations, admin panel, auth scaffolding) gives a solo developer, new to formal architecture, strong guardrails against structural drift. |
| **API style** | REST (Django REST Framework) | Simpler to learn and operate solo than GraphQL; DRF's maturity and documentation reduce first-time-architecture risk. GraphQL and WebSockets are not adopted for the early stages — see §3.1. |
| **Database** | PostgreSQL | Relational integrity, strong constraint support, and full compatibility with the CTI domain model (§4). |
| **Local environment** | Developer's laptop as server, reachable from phone and laptop browser on the same network | Matches the actual usage pattern needed for the early stages; no cloud infrastructure decisions are required yet. |
| **Containerization** | Docker, introduced at Stage 4 | Deliberately not adopted from day one — see Stage 4 rationale (§6.4). Learned close to the start of the project, but only once there's a working system worth containerizing. |
| **Version control** | Git / GitHub | Already in use; no change needed. |

### 3.1 Deferred Technical Decisions (Explicitly Out of Scope for Now)

These appeared in early technical brainstorming but are **not** part of the
current plan. They are recorded here so they aren't silently lost, and to be
explicit about *why* they're deferred — each depends on infrastructure or
usage data that doesn't exist yet:

| Deferred item | Depends on | Revisit when |
|---|---|---|
| WebSocket / SSE real-time sync | A working single-device system and a demonstrated need for live updates across devices | Multi-device usage is real and manual refresh is a proven pain point |
| Redis-backed inverted date index for dashboard queries | Query performance actually being a bottleneck | Real data volume exists and a plain indexed PostgreSQL query is measured as too slow |
| External LLM pipeline (voice/email → task) | All underlying structures (task, event, routine, recurrence, organization) being stable enough to be a reliable extraction target | After Stage 5, and only as its own dedicated stage |
| Enterprise email ingestion webhook | The LLM pipeline above | Same as above |
| GraphQL API layer | A concrete case where REST's fixed response shape becomes a real limitation | Not currently anticipated; REST is expected to be sufficient long-term for this domain |

---

## 4. Domain Model Decisions

These are the foundational, cross-cutting decisions that every stage below
builds on. They are recorded once here rather than repeated per stage.

### 4.1 Inheritance Strategy: Class Table Inheritance (CTI)

**Decision:** the domain uses Class Table Inheritance, not Single Table
Inheritance.

- A parent table `base_events` holds fields common to every schedulable item:
  `id`, `title`, `description`, `created_at`, `updated_at`, and shared timing
  fields.
- Child tables `tasks`, `events`, and `routines` each hold a foreign key back
  to `base_events` and only the fields specific to that type.

**Why CTI over STI:** STI (one wide table with a `type` discriminator column)
was considered and rejected. It would leave every row full of NULL columns
for fields that don't apply to its type (e.g., a `routine` row would carry
unused `due_date`/`deadline` columns), which works against the normalization
priorities already established (per-list grace periods, deadline history, and
future organizational structure all attach naturally to specific entity
types). CTI matches Django's ORM model more directly via multi-table
inheritance / `OneToOneField` relationships, and keeps each table's schema
honest about what actually applies to that entity type. The tradeoff —
queries that need fields across types require a join — is accepted as the
right cost for schema clarity at this project's scale.

### 4.2 Entity Relationship: Task and Event Are Independent Types

Task and Event are both children of `base_events` but are otherwise
independent entities — not variants of a shared "Item" superclass with a type
flag beyond the CTI structure itself. Routine is a third, independent child
type.

### 4.3 Task Status Model

A task's status is derived primarily from **time**, with a small stored field
capturing explicit user intent. This keeps the time-driven states computed
(no background worker required for them) while still letting the user
override outcome explicitly.

**Stored field:** `user_status` — nullable, with only two possible non-null
values: `DONE` or `WONT_DO`. `NULL` means "the user hasn't made an explicit
completion decision" and the effective status falls through to the
time-based computation below.

**`deadline` is a toggleable field, not a plain nullable date (revised —
see §4.7):** a task has a `deadline_enabled` boolean alongside `deadline`.
Turning the toggle off does **not** clear the stored `deadline` value — the
date is preserved but ignored by status computation until the toggle is
turned back on. This means `deadline_enabled = false` is the only condition
that matters for status purposes; the underlying `deadline` value is inert
while disabled, and can be re-enabled by the user without re-entering a date.

**Effective status (computed at query/render time when `user_status` is
`NULL`):**

| Status | Condition | Meaning |
|---|---|---|
| `TODO` | `now <= due_date`, OR `deadline_enabled = false` | Not yet due, or the task currently has no active deadline (e.g., after a MISSED-postpone — see §4.7). Reaching `due_date` (when a deadline is active) changes *which list the task appears in*, not its status. |
| `OVERDUE` | `deadline_enabled = true` AND `due_date < now <= deadline` | Due date has passed but the hard deadline hasn't. Still straightforwardly actionable. |
| `MISSED` | `deadline_enabled = true` AND `deadline < now <= deadline + grace_period` | Deadline has passed. The task is tagged as missed but still recoverable — the grace period (see §4.4) hasn't elapsed. |
| `AUTO_WONT_DO` | `deadline_enabled = true` AND `now > deadline + grace_period` | Grace period elapsed with no user action; the system closes the task automatically. |

**Note:** a task with `deadline_enabled = false` can never become `MISSED` or
`AUTO_WONT_DO` — it behaves like a plain due-date-only task until the user
re-enables the deadline or sets a new one.

**Explicit field (when `user_status` is not `NULL`):**

| Status | Set by | Notes |
|---|---|---|
| `DONE` | User action, from any prior state | Terminal in normal use, but can be changed back if the user reopens it (see below). |
| `WONT_DO` | User action, from any prior state | Explicitly reversible — the user can change a `WONT_DO` task back to active at any time by clearing `user_status`. |

This gives six user-visible statuses total (`TODO`, `OVERDUE`, `MISSED`,
`AUTO_WONT_DO`, `DONE`, `WONT_DO`) from a data model that only ever stores one
of three values (`NULL`, `DONE`, `WONT_DO`) plus the two timestamps already
needed for scheduling (`due_date`, `deadline`) and one per-list configuration
value (`grace_period`, see §4.4).

**Why computed rather than stored for the time-driven states:** no background
cron worker is needed to keep `TODO`/`OVERDUE`/`MISSED`/`AUTO_WONT_DO`
accurate — they're pure functions of `now` and the task's own fields,
evaluated whenever a task is read. This is deliberately the simpler of two
options considered (the alternative being an eager cron worker that
periodically writes the status); the cron approach is deferred until there's
a concrete reason a computed field isn't sufficient (e.g., needing to trigger
a notification exactly *at* the moment a task becomes `MISSED`, which a
purely computed field can't do).

### 4.4 Grace Period

Each list has a configurable **grace period** (e.g., 1 week, 1 month, or any
user-chosen duration) that determines how long a task stays in `MISSED`
before automatically becoming `AUTO_WONT_DO`. This is a per-list setting, not
global — different lists can have different tolerances for staleness.

### 4.5 Event Status Model

Events use a separate, purely time-driven three-state model — no stored
status field at all, since events aren't "completed" the way tasks are:

| Status | Condition |
|---|---|
| `UPCOMING` | `now < start_time` |
| `ONGOING` | `start_time <= now <= end_time` |
| `PAST` | `now > end_time` |

### 4.6 Routine Status Model

Each routine **instance** (one occurrence — e.g., "today's" entry for a daily
routine) uses the same `NULL` / `DONE` / `WONT_DO` explicit-field pattern as
Task, without the `OVERDUE`/`MISSED` distinction (routines don't have a
separate due date vs. deadline within a single occurrence):

| Status | Condition |
|---|---|
| `TODO` | Occurrence not yet resolved |
| `DONE` | User marked complete |
| `WONT_DO` | User explicitly skipped, reversible |
| `AUTO_WONT_DO` | The occurrence's period elapsed with no action |

### 4.7 Postpone Behavior

Two related but distinct actions, both called "Postpone" in the UI:

1. **Postpone a task that is `TODO` or `OVERDUE`** (i.e., `due_date` has
   passed or is approaching, but `deadline` has not): sets `due_date = today`.
   `deadline` is untouched.
2. **Postpone a task that is `MISSED`** (i.e., `deadline` has passed):
   sets `due_date = today` **and turns `deadline_enabled` off**. The stored
   `deadline` value itself is left untouched — it is not shifted forward and
   not cleared — so the user can re-enable it later (see §4.3) if they want
   to set a new one, without losing the old date as a reference point.
   **(Revised from the original "advance deadline forward" design — see the
   resolution of Open Item §10.1, now closed.)**
   - Once past deadline, the deadline is considered elapsed; Postpone on a
     MISSED task is a due-date-only recovery action, not a deadline
     recalculation.

Two entry points trigger this behavior:
- **Single-task Postpone**, from within a task's detail view.
- **Postpone All**, a bulk action that applies the same logic to every
  `OVERDUE`/`MISSED` task at once.

### 4.8 Deadline History — Superseded by System Logging

**Original decision (superseded):** a dedicated `TaskDeadlineHistory` domain
table, writing a row on every deadline change (Postpone or manual edit).

**Revised decision:** `TaskDeadlineHistory` is **removed from the design
entirely.** No domain-level history table is maintained for `deadline` or
`due_date` changes. Because `deadline` is now a toggleable field that
preserves its stored value when disabled rather than being overwritten or
cleared (§4.3, §4.7), the main case the history table existed to serve — not
losing the old deadline when it changes — is already handled by the toggle
itself for the Postpone case. What remains (a full change-by-change audit
trail, including manual edits) is delegated to **application-level system
logging**, introduced as its own stage — see the new **Stage 1.5 — Logging**
in §6, inserted immediately after Stage 1 and before Stage 2, since Stage 2's
domain logic (this section) now depends on it.

This keeps a full reconstructable trail available if it's ever needed
(surfaced through logs rather than a queryable domain table), while removing
a bespoke table and its `reason` ENUM from the domain model — consistent with
KISS (§2.3): the dedicated table added a queryable, domain-modeled audit
trail that this project doesn't currently have a use case exercising, and
building it up front is the kind of decision this project's incremental
principle is built to postpone until a real need is demonstrated (§8).

**Resolved:** this closes Open Item §10.2 (deadline history scope) — the
question is now moot, since there is no domain history table to scope.

### 4.9 Recurrence Model (Stage 3 — Design Direction, Detailed at Implementation)

The recurrence system must support, fully user-configurable per routine or
recurring task:

- Every day.
- Every N days.
- Specific days of the week (e.g., every Tuesday, Wednesday, and Friday).
- A specific day of the month, in **either** the Gregorian or the Persian
  (Jalali) calendar.

**Calendar choice is per-recurrence-rule, not app-wide.** There is no global
"the app uses Jalali" or "the app uses Gregorian" setting. Each individual
day-of-month recurrence rule carries its own calendar system, chosen by the
user at the time that rule is created. This means two different recurring
tasks can legitimately use two different calendars at the same time — e.g.,
one task set to recur on the **19th of every Jalali month**, and a separate
task set to recur on the **26th of every Gregorian month** — and both are
valid, independent, simultaneously-active rules. The calendar is a property
of the rule, not a property of the user, the app, or any other rule.

**Key constraint:** the calendar system the user originally specified (Jalali
or Gregorian) must be stored and preserved, not derived by converting between
calendars on the fly. If a converted date and a stored date ever disagree due
to conversion edge cases, the originally specified calendar's date is the
source of truth. This prevents silent drift if the two calendar systems don't
convert perfectly onto each other for a given recurrence rule.

**End-of-month handling:** when a target day doesn't exist in a given month
(e.g., the 31st in a 30-day month), the occurrence clamps to the last valid
day of that month in the relevant calendar, and returns to the exact target
day automatically once a month containing that day occurs again.

Full implementation-level detail (data model for recurrence rules, exact
clamping algorithm, timezone handling) is deferred to Stage 3 design, per the
incremental principle of resolving implementation detail when the stage that
needs it begins — not speculatively now.

---

## 5. Frontend Expectations

The frontend is not treated as an afterthought bolted onto a finished
backend — each stage below includes a frontend deliverable, because a stage
isn't "usable in daily practice" (the progression rule, §2.5) unless it has a
working UI. That said, the frontend's job at each stage is to **expose the
backend decisions made for that stage clearly and correctly** — visual polish
is explicitly deferred in favor of correctness and completeness of the
underlying logic.

### 5.1 General Frontend Principles

- **Functional correctness before visual design.** Every stage's frontend
  must correctly reflect the domain logic decided for that stage (e.g., a
  task's computed status must display correctly for all six states before any
  attention goes to how it's styled).
- **One shared codebase, web-first.** Built with React Native for Web;
  components should avoid web-only APIs where reasonably possible, so that a
  future native build doesn't require rewriting core logic — but this is a
  soft guideline, not a blocker, for the early stages.
- **No premature responsive/native polish.** Layout should work on both a
  laptop browser and a phone browser (since that's the real early usage
  pattern per §1.2), but pixel-level responsive design work is deferred until
  the underlying feature set stabilizes.
- **State management approach** is an open item — see §10.

### 5.2 Per-Stage Frontend Deliverables

Each stage section below (§6) includes what the frontend must expose for that
stage to be genuinely usable in daily practice, not just what the backend
must implement.

---

## 6. Stage-by-Stage Plan

### Stage 1 — Basic Foundation

**Goal:** confirm the technical foundation works, end to end, before any
user-facing feature is built.

**Backend:**
- Django project scaffolding, project structure decided (app layout,
  settings split for local development).
- PostgreSQL connection configured and verified.
- Basic authentication (single user is sufficient for now — full multi-user
  auth is not required yet, since Stage 1–5 remain single-user by design).
- A minimal health-check or smoke-test endpoint proving the full path
  (browser → Django → PostgreSQL → response) works.

**Frontend:**
- React Native for Web project scaffolding.
- A single screen that calls the health-check endpoint and displays the
  result, proving the frontend-to-backend connection works over the local
  network from both laptop and phone.

**No user-facing task/event/routine features are built in this stage.** Its
only purpose is to confirm the pipe works.

**Definition of done:** the developer can open the app from both laptop and
phone browsers on the same network and see a live response from the backend.

**Status (2026-08-08): Stage 1 complete.** Backend was already done
(`backend/` — health-check endpoint, PostgreSQL wired up, env-based
settings). The frontend deliverable has now been added at `frontend/`: an
Expo (React Native for Web) app with a single screen (`App.js`) that calls
`/api/health/` and shows loading / success / error state with a Retry
button. The backend URL is read from `EXPO_PUBLIC_API_URL` (see
`frontend/.env.example`) rather than hardcoded, so the same build works from
both `localhost` (laptop browser) and the laptop's LAN IP (phone browser),
matching the backend's existing `DJANGO_ALLOWED_HOSTS` pattern. Verified end
to end via `npx expo export --platform web`, which bundled successfully with
the env var correctly embedded. See `frontend/README.md` for setup and run
instructions. Stage 1.5 can now begin once this has been used in real daily
practice for a meaningful period, per the progression rule (§2.5).

---

### Stage 1.5 — Application Logging

**Goal:** introduce cross-cutting, application-level system logging before
any domain feature depends on it. This stage exists because Stage 2's
revised deadline-change tracking (§4.8) relies on logging instead of a
dedicated domain history table — logging must be in place first.

**Why its own stage, not folded into Stage 1 or Stage 2:** logging is a
cross-cutting infrastructure concern, not specific to Task/Event/Routine —
future entities and features will also want it. Folding it into Stage 2
would give that stage two unrelated goals (the domain model, and
infrastructure); folding it into Stage 1 would conflate "prove the pipe
works" with "instrument the pipe," which are different concerns even though
both are infrastructural.

**Backend:**
- Structured application logging configured for the Django backend (a
  standard logging setup is sufficient — e.g., Python's `logging` module
  configured with structured/JSON output; no external log-aggregation
  service is required at this stage).
- Logging calls added at the points that previously would have written to
  `TaskDeadlineHistory`: every `deadline` value change and every
  `deadline_enabled` toggle, with enough context (task id, old/new value,
  timestamp, triggering action — Postpone-single, Postpone-all, or manual
  edit) to reconstruct what happened after the fact.
- Log output location decided as part of this stage (e.g., local file under
  the developer's laptop setup); revisited if it conflicts with Stage 4's
  containerized setup once that stage begins.

**Frontend:** none — this stage is backend/infrastructure only.

**Definition of done:** log output can be inspected and a deadline change
(e.g., from a test Postpone action) can be reconstructed from the logs
alone, before Stage 2 begins.

---

### Stage 2 — Core Task, Event, and Routine Management

**Goal:** implement the full domain core decided in §4 — CTI schema, all
three entity types, complete status logic, Postpone behavior, and deadline
history — as a genuinely usable single-user task manager.

**Backend:**
- CTI schema implemented: `base_events` parent table; `tasks`, `events`,
  `routines` child tables (§4.1, §4.2).
- Task status logic implemented exactly as specified in §4.3: `user_status`
  field (`NULL`/`DONE`/`WONT_DO`) plus computed effective status
  (`TODO`/`OVERDUE`/`MISSED`/`AUTO_WONT_DO`) evaluated at read time.
- Per-list `grace_period` configuration (§4.4) — even if "per-list" for now
  just means a single default value, since Organizational Hierarchy (lists)
  doesn't exist until Stage 5; store it at the task level for now with a
  sensible default, and migrate it to a list-level setting once Stage 5
  introduces lists.
- Event status logic implemented as specified in §4.5 (fully computed, no
  stored status).
- Routine status logic implemented as specified in §4.6, for manually-created
  single occurrences (full recurrence generation is Stage 3 — Stage 2 should
  support creating and completing individual routine instances by hand).
- `deadline_enabled` boolean field on Task, alongside `deadline` (§4.3) —
  disabling it preserves the stored `deadline` value rather than clearing it.
- Postpone logic (§4.7): single-task postpone and bulk "Postpone All"
  endpoints, with the due-date-only-shift vs. due-date-shift-plus-
  deadline-disable branching behavior.
- Deadline-change logging (§4.8): every `deadline` value change and every
  `deadline_enabled` toggle writes a structured log entry via the logging
  infrastructure from Stage 1.5, rather than a domain history table.
- CRUD endpoints for Task, Event, and Routine.

**Frontend:**
- Task list view showing all six statuses with clear visual distinction
  (at minimum: distinct labels/colors — polish deferred per §5.1).
- Task detail view with Done, Won't Do (reversible), and Postpone actions.
- A visible way to trigger "Postpone All" from the list view.
- Basic create/edit forms for Task, Event, and Routine, including a toggle
  control next to the deadline field (§4.3): switching it on reveals a date
  picker; switching it off hides the active date input but retains the
  underlying stored value for when it's switched back on.
- Event list/view reflecting the three time-driven states.
- Simple manual routine occurrence view (create and mark done/won't-do by
  hand — no recurrence UI yet, that's Stage 3).

**Definition of done:** the developer uses this as their actual daily task
list — creating tasks and events, letting some go overdue/missed
intentionally to verify the status transitions, and postponing tasks — for a
meaningful period before Stage 3 begins.

---

### Stage 3 — Recurrence Engine

**Goal:** implement the full recurrence system described in §4.9, replacing
Stage 2's manual routine-instance creation with automatic generation.

**Backend:**
- Recurrence rule data model (design detail resolved at this stage, per the
  incremental principle — see §4.9 and the open item in §10).
- Support for all four recurrence patterns: every day, every N days, specific
  weekdays, specific day-of-month (Gregorian or Jalali, calendar choice
  preserved per §4.9).
- End-of-month clamping logic implemented and tested against real edge cases
  (e.g., a 31st-of-the-month recurrence across months of varying length,
  Esfand/February boundaries).
- Automatic generation of routine (and recurring task, if applicable)
  instances from a recurrence rule, replacing Stage 2's manual creation.
- Migration path for any Stage 2 manually-created routine instances into the
  new recurrence-backed model.

**Frontend:**
- Recurrence rule configuration UI covering all four pattern types.
- Clear display of which calendar system (Gregorian/Jalali) a recurrence was
  originally defined in.
- Routine/recurring-task views updated to show auto-generated instances
  rather than requiring manual entry.

**Definition of done:** the developer sets up their actual recurring routines
and tasks (daily habits, weekly commitments, monthly recurring items) through
the new system and uses it in practice, including living through at least one
real end-of-month edge case, before Stage 4 begins.

---

### Stage 4 — Containerization (Docker)

**Goal:** package the working system (Django backend + PostgreSQL) into
containers, learned deliberately early — once there's a real system worth
containerizing, but before the system grows complex enough to make
containerizing it retroactively painful.

**Backend / Infrastructure:**
- Dockerfile for the Django application.
- Docker Compose configuration wiring the backend and PostgreSQL together.
- Environment-variable-based configuration (replacing any hardcoded local
  settings from Stages 1–3) so the containerized setup doesn't silently
  depend on the developer's local machine state.
- Verification that the full system runs identically via
  `docker compose up` as it did running natively.

**Frontend:**
- No new frontend features in this stage — the goal is operational, not
  functional. If time allows, verify the frontend can also run containerized,
  but this is optional for Stage 4 and not a blocker.

**Definition of done:** the developer can stop running the app natively and
run it entirely through Docker Compose for real daily use, with no
functionality lost, before Stage 5 begins.

---

### Stage 5 — Organizational Hierarchy (Folders, Lists, Tags)

**Goal:** introduce the organizational layer above individual tasks/events/
routines. Exact structure (e.g., Folder → List → Tab, or a flatter model) is
a decision already made by the developer separately and should be documented
here in detail once implementation for this stage begins — this roadmap
entry is intentionally left as a placeholder for that detail rather than
guessing at it.

**Backend (to be detailed at Stage 5 design time):**
- Organizational entity schema (folders/lists/tags as decided).
- Migration of the per-task `grace_period` default (introduced provisionally
  in Stage 2) to a genuinely per-list setting, per §6 Stage 2 notes.
- Association between organizational entities and Task/Event/Routine.

**Frontend (to be detailed at Stage 5 design time):**
- Navigation and views for the organizational structure.
- Per-list settings UI, including grace period configuration.

**Definition of done:** to be defined when this stage's detailed design is
recorded, following the same process as Stages 1–4 — used in daily practice
before any Stage 6 is planned.

**Note:** from around this point onward, the gamification track described in
§7 can begin running as its own line of small sub-stages alongside whatever
core stage comes next — see §7.5.

---

## 7. Gamification Layer (Cross-Cutting, Post-Core-Stages)

### 7.1 Intent and Positioning

Gamification is a **deliberately separate concern** from the core stages
above (§6), not a feature bolted onto Stage 2 or Stage 3. It should begin
only once the core task/event/routine system (through roughly Stage 3–4) is
built, stable, and genuinely used daily — because every gamification
mechanic described below depends on having real behavioral data (completion
times, streaks, per-goal activity) to work from. Once that foundation
exists, gamification work can proceed as its **own track of small,
incremental sub-stages**, following the same "use it before extending it"
discipline as the rest of the roadmap (§2.5), rather than as one large
feature dump.

### 7.2 Core Design Principle: Contained, Not Pervasive

The single guiding rule for this layer: **gamification must be optional and
spatially contained, not woven through the whole app.**

- The main task list (the everyday working screen) shows only plain task
  data and lightweight progress rings — no XP bars, levels, currencies, or
  characters anywhere in that view.
- A dedicated **"Play" tab** houses everything explicitly game-flavored
  (collectibles, avatars, social/competitive features, narrative elements).
- A separate **"Stats" / analytics area** houses serious, numeric
  self-comparison data (trends, personal bests) — useful on its own without
  any game framing.
- This split means a user who wants zero fantasy elements can use Dotick
  purely as a serious tool, while a user who wants the motivational layer
  can opt into it in one place. This is a direct, deliberate reaction to
  Habitica's core weakness: it is effective but so immersively game-like
  that it stops feeling usable as a serious daily driver.

### 7.3 Anti-Gaming Principle

Every scoring mechanic introduced under this layer must be designed
alongside its abuse case before being implemented — e.g., splitting one task
into many to farm points, or padding low-effort days to hit a quota. Scoring
logic should be based on effort/consistency signals that resist this kind of
manipulation, not raw counts alone. This is treated as a first-class design
constraint for every sub-idea below, not an afterthought.

### 7.4 Candidate Mechanics (Proposals — to Be Individually Evaluated)

The following are **proposals**, not commitments. Each will be individually
scoped, weighed against the anti-gaming principle (§7.3), and either adopted,
adapted, or dropped once this layer's design actually begins:

- **Behavioral pattern inference** — infer from a user's own task-completion
  history (day/time patterns) which days tend to be "work days" vs. "personal
  project days" per goal, without the user configuring this manually.
- **Randomized, inferred-context bonus multipliers** — occasionally boost
  points for a goal on the days the system infers are naturally suited to
  it, kept unpredictable so it feels like a pleasant surprise rather than a
  gameable rule.
- **Non-zero starting progress** — progress bars/rings start partially
  filled rather than at zero, since people are more motivated to finish
  something already in progress than to start from nothing.
- **Apple-Watch-style activity rings** — one ring per goal area on the main
  screen, filling as related tasks are completed, with a minimum-activity
  threshold before a day counts, and a non-linear fill curve so later tasks
  in a day fill more of the ring than earlier ones.
- **Oscillating cross-goal difficulty** — a goal that's been getting a lot of
  attention gradually gets "harder to fill" while neglected goals get
  "easier," so the balance of effort naturally drifts back toward whatever's
  being ignored, and the cycle repeats.
- **Shareable progress** — let a user share read-only progress on a specific
  task or goal with someone else via a link or view.
- **Friend circles and gentle competition** — Duolingo-style small groups of
  people who choose to work alongside each other, with the ability to nudge
  one another (a wave, a reminder notification) rather than direct
  leaderboard-style comparison.
- **Comparison against one's own past, not just others** — periodic
  (daily/weekly) reports highlighting the specific areas where the user has
  improved relative to their own recent history, framed positively.
- **A living collectible/growth visual** (e.g., a tree, similar to the Forest
  app) confined entirely to the Play tab, potentially tied to collaborative
  or shared effort with friends rather than solo pressure alone.
- **Serious analytics dashboard** — the numeric backbone behind the reports
  above (consistency trends, recovery-after-a-bad-day patterns, per-goal
  balance over time), living in the Stats area independent of any game
  framing, so the same underlying data serves both the playful and the
  serious presentation.

### 7.5 Relationship to the Core Roadmap

This layer does not get its own single "Stage N" the way §6 does. Once the
core stages have matured enough to produce real usage data, gamification
work is expected to proceed as a series of **small, independent sub-stages**
running alongside (not blocking) further core-stage work — each sub-stage
picking one mechanic from §7.4, scoping it, building it, and using it in
practice before the next is started, per the same progression rule as
everywhere else in this document (§2.5).

---

## 8. Deliberately Postponed Items

Consistent with the incremental principle of not building ahead of
demonstrated need, the following are explicitly out of scope until a later,
not-yet-numbered stage, and should not be designed prematurely:

- Multi-user support and any collaborative/sharing features (folder, list,
  tag, or item sharing).
- Native mobile and desktop applications (React Native for Web remains the
  only target through the stages above).
- Real-time (WebSocket/SSE) synchronization across devices.
- External LLM-based natural language input (voice memos, forwarded emails).
- Enterprise-specific features (workspace admin roles, team hierarchies).
- Performance optimization work (e.g., specialized indexing strategies) —
  deferred until real usage data shows an actual bottleneck, per §3.1.

These are not rejected outright — several (the LLM pipeline, real-time sync)
are explicitly part of the longer-term vision in §1.1 — but designing them
now, before the stages above are built and used, would violate the same
principle that ruled out Waterfall and RUP in §2.2: designing ahead of
understood need.

---

## 9. Diagram Backlog

Per the ordering principle in §2.4, diagrams are produced as each stage's
design questions are resolved, not all at once upfront:

| Diagram | Scope | Produced at |
|---|---|---|
| Logging architecture note | What gets logged and where (§4.8, Stage 1.5) — lightweight, not a formal diagram | Start of Stage 1.5 |
| Use-case diagram | Stage 2 functional scope (Task/Event/Routine CRUD, statuses, postpone) | Start of Stage 2 |
| State diagrams | Task, Event, and Routine lifecycle (per §4.3, §4.5, §4.6) | Start of Stage 2, refined if Stage 3 changes routine lifecycle |
| Class diagram / CRC cards | CTI structure (§4.1) | Start of Stage 2 |
| ER diagram | Full Stage 2 schema, including the `deadline`/`deadline_enabled` pair (no `TaskDeadlineHistory` table — removed, see §4.8) | End of Stage 2, once schema is stable |
| Recurrence rule class/ER diagram | Stage 3 recurrence data model | Start of Stage 3 |
| Sequence diagram | Postpone flow (single + bulk), since it touches status, deadline, and logging simultaneously | Start of Stage 2 |
| Deployment diagram | Docker Compose architecture | Start of Stage 4 |
| Deferred: organizational hierarchy diagrams | Stage 5 structure | Start of Stage 5 |

---

## 10. Open Items to Resolve Before or During Relevant Stages

These are known unresolved questions, tracked explicitly so they aren't lost.
Resolved items are kept (struck through in spirit, not deleted) so the
decision trail stays visible.

1. ~~**Postpone-on-MISSED deadline shift rule** (§4.7)~~ — **RESOLVED.**
   `deadline` is never shifted forward. Postponing a `MISSED` task sets
   `due_date = today` and turns `deadline_enabled` off, preserving the old
   stored `deadline` value untouched. See §4.3 and §4.7.
2. ~~**Deadline history scope** (§4.8)~~ — **RESOLVED, and moot.**
   `TaskDeadlineHistory` is removed from the design entirely; deadline
   changes are tracked via application-level logging (Stage 1.5) instead of
   a domain history table, so the due_date-vs-deadline scoping question no
   longer applies. See §4.8.
3. **State management approach for the frontend** (§5.1): not yet decided;
   to be resolved early in Stage 2 once there's real UI state (task lists,
   statuses) to manage.
4. **Organizational Hierarchy structure detail** (§6, Stage 5): the developer
   has made this decision separately; it should be transcribed into this
   document in full before Stage 5 implementation begins, replacing the
   current placeholder.
5. ~~**Frontend not yet built** (§6, Stage 1)~~ — **RESOLVED.** The Expo /
   React Native for Web scaffold and health-check screen have been created
   at `frontend/`. This was the one item blocking Stage 1 from being fully
   closed out; Stage 1 is now complete. See §6 Stage 1 notes above.