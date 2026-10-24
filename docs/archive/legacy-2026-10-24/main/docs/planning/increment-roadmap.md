# Dotick — Development Roadmap

> **Status:** Transition to the approved engineering process (2026-10-20). Product scope and revised release boundaries remain subject to individual Product Owner review.
> **Process authority:** [Engineering Process](../development/engineering-process.md). This roadmap owns outcomes, order and dependencies—not the SDLC, verification policy, or product meaning.
> **Behavior authority:** [System Definition](../requirements/system-definition.md) → [Decision Register](../decision-register.md) → [Formal SRS](../requirements/srs.md) until explicitly revised.

---

# 0. Purpose and transition

The previously completed Increment 0/1 implementation and its v0.2.0 evidence remain historical facts, not proof that a Rust rebuild has been implemented. The rebuild itself has **not** started.

The old implementation-oriented Increment 0–11 sequence, future-track descriptions and feature/entity matrices are retained **verbatim below as a legacy scope inventory** while we review product decisions. They are **not** the active engineering workflow, mandatory document-production plan, or automatically approved new release order. No historical behavior, feature or verification obligation is silently discarded. Product behavior can change only by a deliberate product decision, reflected in its canonical documents.

# 1. Delivery model

- Group accepted **small, complete, user-visible behavior slices** into product-outcome releases. A slice (e.g. user signs in; user creates a Task) is the actual unit of discovery, design, implementation, verification and Product Owner acceptance.
- For **each new product-behavior slice**, the Agent first asks the Product Owner what should happen, proposes defaults, then jointly reviews observable acceptance scenarios, important edge cases and risk A/B/C. Obtain owner approval of behavior **and** scenario/assurance plan before coding; do not require the owner to approve internal individual test assertions.
- Use **Behavior Discovery → Approved Scenarios/Risk → Technical Design → Logic/Tests → Complete Base UI/Integration → Agent Verification → Owner Observation/Acceptance → Close**; see [Engineering Process](../development/engineering-process.md). The Agent never marks owner acceptance or starts the next behavior without the required approval.
- An engineering baseline covers consequential product/domain and early cross-cutting design choices, but **is not** an independent, open-ended implementation release. The first technical result must exercise a real user journey. Design intended UI behavior before it constrains backend contracts; a completed slice integrates a precise base UI with real logic/persistence.
- Do not require universal TDD, one report per stage, per-increment risk/traceability edits, exhaustive imaginary edge cases, fixed observation days, full repeated document sets, or a fixed number of commits. Preserve real contract, data-integrity, security and user-flow checks. Important bugs block closure; minor deferrals require explicit owner agreement.
- Review known later constraints (authorization, offline/sync, history/undo, time and data ownership) before choosing an early incompatible API/schema. Implementation of the full later feature may be deferred.
- The roadmap remains provisional where product decisions are under review; agents must not treat candidate features as permission to implement them.

# 2. Proposed outcome boundaries — **not yet approved product scope**

These are **optional grouping boundaries for multiple owner-accepted scenario slices**, replacing the old *type-of-entity* sequencing **only after** scope review and approval. They are planning candidates, not implementation authorization or individually indivisible delivery units.

| Candidate | Demonstrable outcome | Material dependency / note |
| --- | --- | --- |
| R1 — Personal Planner | A person can authenticate and manage a useful Inbox/Task/Event/Today workflow via real client/API/PostgreSQL | Establish Rust modular monolith and core contract; consider local persistence/versioning without claiming complete sync |
| R2 — Goals & First Recommendation | Goals connect to activities; the app can suggest useful next actions and capture feedback | Deliver a simple measurable baseline; keep normal Todo operation independent of the research model |
| R3 — Routines & Scheduling | Track routines, recurrence, reminders and relevant scheduling constraints | Specify calendar/day boundaries and recurrence invariants when implementing |
| R4 — Motivation | Progress, Daily Rings, streaks and scoring reinforce actual work | Verify derived state, finalization and user feedback |
| R5 — Offline & Recovery | Durable offline edits, sync/conflict resolution, history/undo and recovery work across real devices | High-risk integrity/authorization checks; baseline compatibility decided earlier |
| R6 — Collaboration | Users safely share/assign/manage work together | High-risk permission, revocation and cross-user negative scenarios |
| R7 — Production Release | System can be installed, operated, monitored, backed up and recovered | Deployment/security/performance validation and target-environment evidence |

**Coverage to explicitly place during product review:** rich description, hierarchy/references, comments/tags, AI-assisted item input, account/data export and deletion, notification controls, personalization, presentation/accessibility, privacy, and documented future/enterprise capabilities. A capability's absence from a candidate row does **not** remove it from the accepted product scope. Avoid claiming that the legacy roadmap has already been replaced by these candidates.

**Parallel recommendation research track:** define the research question, baseline, consent/data boundaries, reproducible evaluation and comparative metrics. Product acceptance and research claims are separate.

# 3. Implementation and verification status

- **Existing historical release:** v0.2.0 (I0/I1), Django/Expo/PostgreSQL, recorded in `docs/tracking/`.
- **Rebuild:** planning and document reconciliation only; Rust architecture/implementation is not yet accepted as delivered.
- **Actual CI:** existing workflows/checks remain unchanged by this documentation update. Any reduction must follow an evidence-based review, not the mere change of process text.
- **Branch/Git:** work only on the explicitly designated existing branch. No branch/PR creation, merge, force-push, destructive reset or history rewrite without explicit authorization.

# 4. Document and acceptance authority

- **Current behavior/scope:** System Definition, then Decision Register and testable SRS, until revised.
- **Core designs:** Domain Model, Architecture/ADRs and relevant data/API/security/time contracts.
- **Workflow, scenario approval, risk gates, observation and DoD:** [Engineering Process](../development/engineering-process.md) Sections 3–5.
- **Detailed testing/CI evidence:** [Test Strategy](../quality/test-strategy.md).
- **This roadmap:** reviewed delivery outcomes/order/dependencies/status. Modify it when these actually change; do not duplicate SDLC rules in every release.
- Existing traceability and historical review artifacts stay intact; extend them selectively when they provide actual audit/acceptance value, not as a per-slice paperwork gate.

---

# Legacy increment/feature inventory (historical, not active process)

**Sections 7–32 below are retained to prevent loss of prior scope analysis and detail.** Their old deadlines, 11-step repeated SDLC, blanket DoR/DoD, fixed document schedules, test mandates, and references to Django/old implementation are superseded by the current Engineering Process and risk-based Test Strategy. Old implementation status is historical; candidate new release placement must be reviewed against product decisions. Do not execute a legacy "Decision Gate" solely because it appears below.

---

# 7. Increment 0 — Formal Specification + Engineering Baseline

> **Implementation checkpoint — 2026-09-06:** scaffold, developer-only client/API/PostgreSQL walking skeleton, time baseline, and verification tooling now exist. See [the foundation review](../tracking/increment-0-foundation-review.md) for evidence and outstanding release gates.
>
> **Increment 1 closure — 2026-09-20:** identity, account, organization and Basic Task APIs plus the Expo product client are implemented and released at `v0.2.0`. Repository acceptance, migrations, security checks, desktop/mobile client-to-PostgreSQL E2E, hosted CI, traceability and formal review pass. Optional delivery and live provider/device/edge deployment smoke remain assigned to Increment 11. See [I1 readiness](../tracking/increment-1-readiness.md) and [formal review](../tracking/increment-1-review.md).

## Goal

تبدیل سه سند canonical فعلی به baseline مهندسی قابل اجرا، بدون Big Design Up Front.

---

## 7.1 Formal Specification Baseline

### Formalize / Replace Derived Reference — Completed

`docs/requirements/srs.md`

نسخه‌ی reconciled قبلی در Formal SRS Baseline v3.1 بازنویسی شده و فقط requirementهای قابل بیان/تست را normative می‌کند.

در این مرحله:

- Feature Priority وارد SRS نمی‌شود.
- Design proposalهای باز وارد Requirement قطعی نمی‌شوند.
- Design/Tuning Gateهای عمداً واگذارشده با owner مشخص trace می‌شوند؛ Product/Domain behavior فعلی بسته است.
- نسخه‌ی reconciled قبلی SRS مبنای merge خودکار نیست؛ Formal SRS باید از canonical sources استخراج شود.

### Created

`docs/requirements/traceability-matrix.md`

Baseline trace:

```text
System Definition section / Decision ID
↓
Formal Requirement
↓
Planned Increment
```

---

## 7.2 Initial Architecture Baseline

Technical baselines retained:

- PostgreSQL
- frontend/backend separation
- REST CRUD
- JSON
- HTTPS where practical in development
- lightweight WebSocket for notification/live update
- responsive installable PWA as the Current-Scope official User client
- developer-local execution is allowed, but supported end-user self-hosting is not a Current-Scope product capability
- Docker introduced early enough for reproducibility
- external AI failure must not break core task management

### New

- `docs/design/architecture.md`
- first ADRs
- `docs/operations/release-deployment.md`
- `docs/design/security-design.md`
- `docs/quality/test-strategy.md`
- `docs/planning/risk-log.md`

---

## 7.3 Data Design Baseline

`docs/design/domain-model.md` is conceptual and must not be copied mechanically into database tables.

### Confirmed persistence baseline

Personal V1 uses explicit composition rather than ORM/class inheritance for Item persistence. Increment 0 Data Design must implement/refine this baseline without reopening the product-level storage strategy; table/index details remain incremental Design work.

### Created in Increment 0 baseline

- `docs/design/data-model.md`

Physical ERD can start minimal and evolve.

---

## 7.3.1 Time Semantics Baseline

Create `docs/design/time-semantics-spec.md` before time-bearing domain choices are locked. Increment 0 baseline must define the shared vocabulary/invariants for:

- real/canonical instant;
- Calendar Day;
- Dotick Day and day-boundary attribution;
- `RoutineCompletion.occurrence_date` and other business dates;
- credited/effective date;
- all-day interval semantics;
- Account timezone vs device timezone;
- timezone changes and DST gaps/folds;
- Jalali/Gregorian date arithmetic, leap/invalid dates and recurrence anchors.

The baseline must include reusable golden test vectors. Increments 2, 4 and 10 refine the spec, but must not invent incompatible time semantics independently.

---

## 7.4 Development Environment

- Git/SCM
- repository structure
- linter
- formatter
- testing framework
- migration tool
- PostgreSQL development environment
- environment variable/secrets convention
- CI pipeline
- Docker/dev reproducibility baseline
- structured logging baseline
- health/readiness endpoint

---

## 7.5 Walking Skeleton

Walking Skeleton must cross actual layers:

```text
Client
↓
REST
↓
Application
↓
PostgreSQL
↓
Response
```

A `/health` endpoint alone is not sufficient.

---

## Deferred Design / Specification Gates

Current-Scope Product/Domain decisions from the review are closed. The following are **engineering design/tuning gates**, not OPEN product questions:

- ContentBlock physical schema and ordering/edit representation;
- child/dependency/reference relation schema/indexing;
- Sync metadata, trusted ordering/clock strategy, idempotency, tombstone and conflict representation;
- History-branch persistence compatible with Audit and Sync semantics;
- Time Semantics representation and comprehensive test-vector catalog;
- Daily Ring scoring formula/tuning and RingGroup/DailyAction persistence;
- exact Goal-selection algorithm/weights and tunable AI Goal warm-up/similarity parameters;
- adaptive Norm and motivational timing/rate tuning;
- Future trusted-automation authority-level/UX design before E3 auto-actions.

---

## Increment 0 Definition of Done

- Formal SRS baseline exists.
- Traceability baseline exists.
- architecture baseline exists.
- database design approach for Increment 1 is viable.
- project builds from clean clone.
- CI runs lint/tests/build.
- migration mechanism works.
- frontend ↔ backend ↔ DB vertical slice works.
- canonical documents are referenced, not duplicated blindly.
- remaining Design/Specification gates are assigned to their owning Increment without being treated as unresolved Product decisions.

---

# 7.6 Cross-Increment Foundation Guardrail

Dotick is developed incrementally, but foundational decisions are made with the **full known project model** in view. Increment 6 owns full Offline/Sync implementation; this does not allow Increments 1–5 to create entities, APIs or persistence semantics that are incompatible with known Sync/History requirements.

Before locking foundational design in Increments 1–5, teams must review the Increment 6 requirements for at least:

- stable entity/relation/block IDs;
- version/revision semantics;
- delete/tombstone/restore behavior;
- ordering and idempotency assumptions;
- branching History/Audit compatibility;
- server-authorization/revocation behavior for later reconciliation.

Likewise, time-bearing entities must follow the `docs/design/time-semantics-spec.md` baseline from the start even though recurrence and advanced time behavior are completed later. Implementation can be deferred; foundational incompatibility cannot.

Likewise, presentation/application boundaries in current increments must avoid making one specific UI component tree the only safe way to perform a core mutation. Important state-changing behavior should terminate at actor-aware, authorization-aware application/domain boundaries so a future default UI, validated generated experience, or authorized Agent can invoke the same product capability without duplicating domain rules. This is a compatibility constraint only; it does not require building the Future Agent/Experience runtimes early.

---

# 8. Increment 1 — Identity + Folder/List/Column + Basic Task MVP

## Goal

اولین usable vertical increment: user وارد سیستم شود و Task واقعی را در ساختار اصلی سازمان‌دهی ایجاد و مدیریت کند.

---


> **Increment 6 compatibility check:** Design in this Increment must follow Section 7.6 and review known Offline/Sync + branching History semantics before persistence/API choices are finalized.

## Scope

### Authentication

- Email/password
- secure password hashing
- JWT session
- Google OAuth
- email/password fallback when Google unavailable
- Passkey

Enterprise SSO is not current scope.

---

## User / Preferences Foundation

Create conceptual/physical support for:

- User
- basic UserPreferences
- timezone baseline

`day_boundary_offset_minutes` behavior is implemented later with Daily Rings.

---

## Folder / List / Column

Canonical terminology:

```text
Folder
└── List
    └── Column
```

- Tab/Section are not separate entities.
- default Inbox exists.
- every List has default Column for unassigned items.
- technical legacy name may be `not_sectioned`.
- if it is the only Column, technical name need not be shown to user.

### Design Decision

Exact ownership/scope for Folder/List/Column in group context can remain personal-only now and must be revisited before Increment 7.

---

## Item Identity / Ownership

Common foundation:

- id
- created_at
- updated_at
- is_trashed
- version
- title
- owner_user_id
- created_by_user_id

Important:

```text
ownership != source
```

---

## Basic Source

Source is provenance only:

- platform
- external_account optional
- external_id optional

Manual source is allowed.

---

## Basic Task

- create
- retrieve
- edit title/core metadata
- Todo
- Done
- Won't_Do
- soft delete
- persisted ownership
- placement in Inbox/List/Column

Full scheduling lifecycle comes in Increment 2.

---

## API Foundation

- REST
- JSON
- stable error envelope
- validation errors
- authentication errors
- ownership isolation in query/service layer
- pagination/filtering only where needed by current UI

Endpoints are designed here, not globally in advance.

---

## Analysis Outputs

- authentication use cases
- create/edit/complete Task use cases
- Folder/List/Column navigation model
- ownership/creator/source distinction
- basic Task state diagram

---

## Documents

### New

- `docs/design/api-contracts.md` or `openapi.yaml`
- initial physical ERD

### Update

- `docs/requirements/srs.md`
- `docs/design/data-model.md`
- `docs/design/architecture.md`
- `docs/design/ui-ux/`
- `docs/design/security-design.md`
- `docs/requirements/traceability-matrix.md`
- `docs/planning/risk-log.md`

### Canonical Documents

Only update if implementation work exposes a real domain/behavior change.

---

## Acceptance

User can:

1. authenticate,
2. see Inbox,
3. create a Task,
4. place it in List/Column,
5. edit it,
6. mark Done/Won't_Do,
7. reopen app and retrieve it,
8. never retrieve another user's private data through normal queries.

---

# 9. Increment 2 — Complete Schedulable Domain: Task + Event + Hierarchy + Description + Comments

## Goal

تکمیل مدل Task/Event و ساخت hierarchy مستقیم و Description block-based.

---


> **Increment 6 compatibility check:** Design in this Increment must follow Section 7.6 and review known Offline/Sync + branching History semantics before persistence/API choices are finalized.

# 9.1 Decision Gate — Must Resolve Before Implementation

## A. ContentBlock exact schema

Canonical requirement:

- stable `block_id`
- block type
- ordered content
- comment target support
- reorder/edit support
- sync-compatible identity

Exact storage schema must be decided here.

## B. Child vs Reference backend relation

System must distinguish:

- structural child
- normal reference

without forcing two complex UI workflows.

Exact relation schema must be decided.

## C. Structural parent invariant — already confirmed

Task and Event each have **at most one structural parent**. Both may be referenced from multiple authorized contexts. Increment 2 must implement/test this invariant and must not reopen Event multi-parenting as a Product decision.

---

# 9.2 Task Scheduling & Lifecycle

Fields/behavior:

- Task may remain completely unscheduled; date/time is not required for identity or persistence
- `due_at`
- optional `end_at`
- all-day representation
- `deadline_at`
- `grace_period_days`; when deadline exists and User does not set grace explicitly, default is `0`

State machine:

```text
before due                       → Todo
after due                        → Overdue
after deadline, grace > 0        → Missed
after deadline, grace = 0        → Skipped directly
after deadline + grace           → Skipped
```

User-driven:

- Done
- Won't_Do

`Skipped` is system-controlled, but a Task already moved to `Skipped` by the system may later be explicitly moved by the User to another allowed state.

Opening/viewing/editing a historical Task must not by itself re-evaluate its status against the current clock.

---

## Task Dependency

- `blocked_by_ids`
- a blocked Task cannot become `Done` until every active blocker is `Done`
- only `Done` satisfies a blocker
- deleting a blocker removes that dependency relation
- dependency and structural hierarchy are independent
- dependency validation
- cycle policy must be explicitly tested/designed

---

## Priority

- Urgent_Important
- Important
- Urgent
- None

This is Item priority, not feature priority.

---

# 9.3 Event

- start_at optional; absence of both start time and all-day date means the Event is valid but unscheduled
- end_at optional
- all-day date optional
- location
- scheduled Event lifecycle: Not_Arrived / Ongoing / Finished
- unscheduled Event has no applicable time-driven status
- schedule may be added or completed later without changing Event identity
- independent sub-event information
- structural hierarchy per resolved decision
- multiple Description references allowed

Location must support conceptually:

- coordinates
- address
- place identifier
- virtual meeting link

---

# 9.4 Direct Hierarchy

Hierarchy must be queryable without parsing Description.

For single-parent structures:

- parent relation directly indexed/queryable
- list tree query
- cycle prevention

Description references do not replace hierarchy.

Task completion behavior:

- by default, all structural children `Done` -> Parent `Done`; User may disable this Preference
- explicitly setting Parent Task to `Done` -> all structural descendants `Done`
- time-driven states do not cascade
- `Won't_Do` does not cascade by default; User may enable the optional descendant cascade

Cascade authorization and consistency:

- valid delete permission on Parent is sufficient for its intrinsic delete cascade
- valid `Done` permission on Parent is sufficient for its intrinsic completion cascade; the same applies to optional `Won't_Do` cascade when enabled
- intrinsic cascade authority does not create persistent/general permission on descendants
- move cascade requires move authority over every affected Resource
- destructive multi-Resource cascade shows affected scope and requires explicit confirmation
- multi-Resource consequences are atomic: no partial application

---

# 9.5 RichDescription

Capabilities:

- Text
- Bold
- Italic
- Underline
- Strikethrough
- Heading
- Highlight
- Bullets
- Numbers
- Indent
- Separator
- Code
- Quote
- link/phone/id recognition
- Attachment
- Location
- Item reference

---

# 9.6 Comments

Concept:

```text
Comment
- item target
- optional block target
```

Rules:

- Task/Event independent thread
- block comment visible next to block
- same block comment visible in overall thread
- author identity retained

---

# 9.7 Manual Tags Foundation

- Tag entity
- source User / AI
- user-created tags supported now
- many-to-many Item ↔ Tag
- AI lifecycle deferred to Increment 9
- `goal_id` may remain null

---

# 9.8 AuditLog Foundation

Audit/history infrastructure starts here because later Routine reset and Sync depend on it.

AuditLog supports:

- important Item changes
- previous/new diff
- actor
- occurred_at
- optional device/source metadata

It is not full event sourcing.

---

## Performance Requirement

Hierarchy child retrieval must be direct/index-supported.

No RichDescription parse for List tree.

---

## Documents

### New

- ContentBlock/Description ADR
- hierarchy/reference ADR
- storage migration(s)

### Update

- `docs/requirements/srs.md`
- `docs/design/domain-model.md` **only if resolved design changes conceptual model**
- `docs/decision-register.md` only if a genuinely new Product/Domain question is discovered or canonical rationale must be reconciled
- `docs/design/data-model.md`
- ERD
- API
- UI/UX
- Security
- Traceability
- Risk Register

---

## Acceptance

- Task state transitions work at boundaries.
- completely unscheduled Task remains valid.
- grace=0 skips directly at deadline and unspecified grace defaults to zero when a deadline exists.
- historical Task viewing/editing does not silently re-evaluate status.
- blocked Task cannot be marked Done until every active blocker is Done; deleting blocker removes the relation.
- Skipped Task can be explicitly moved to another permitted state without making Skipped directly user-selectable.
- Event works as point/all-day/duration.
- hierarchy query never requires RichDescription parsing.
- Task structural parent count obeys constraint.
- Task completion cascades, Preferences, move authorization, destructive confirmation and atomic multi-Resource consequences pass their tests.
- Event multiplicity obeys newly confirmed decision.
- block comments render in block and global thread.
- references and children behave distinctly in backend while UI remains simple.

---

# 10. Increment 3 — Routine + RoutineCompletion + TrackingState

## Goal

پیاده‌سازی Routine به‌عنوان definition واحد و ثبت outcome روزانه با RoutineCompletion.

---


> **Increment 6 compatibility check:** Design in this Increment must follow Section 7.6 and review known Offline/Sync + branching History semantics before persistence/API choices are finalized.

# 10.1 Routine

Routine:

- extends Item conceptually
- is not Schedulable
- has no status
- uses TrackingState capability

Fields:

- start_date
- end_date
- target_goal
- recurrence_rule placeholder/interface
- reminders placeholder/interface
- tags
- tracking state

---

# 10.2 RoutineCompletion

Canonical model:

```text
id
routine_id
occurrence_date
status
amount
note
created_at
updated_at
version
```

Status:

- In_Progress
- Done
- Won't_Do

For Partial targets, a recorded `amount` below the applicable target is `In_Progress`; reaching or exceeding target automatically produces `Done`. Absence of a RoutineCompletion row remains distinct from `In_Progress`, and `amount` is not capped at target.

Constraint:

```text
UNIQUE(routine_id, occurrence_date)
```

Important:

- `completed_at` is not a business field.
- current day state is one row.
- Partial amount updates same row.

---

## Reset

Reset:

```text
delete current RoutineCompletion row
keep AuditLog history
```

Won't_Do is not Reset.

---

## Historical Edit

User can edit past RoutineCompletion freely.

This must:

- update the historical domain/source state;
- keep immutable History/Audit evidence;
- update only affected **open** derived/statistical windows where applicable;
- leave already-finalized day/week/month/year statistical outcomes and finalized Daily Rings unchanged.

No full-history recomputation by default.

---

## Scheduled vs Unscheduled Completion

Recurrence controls:

- suggestion/discovery
- which Routine appears as scheduled

It does **not** forbid completion on another date.

User can:

- manually complete an unscheduled date
- see it in Routine history
- reset it
- affect open statistics/derived state where applicable; finalized statistical windows remain immutable

---

# 10.3 Routine Target

Types:

- Achieve_All
- Partial

Partial metric:

- Daily / Weekly / Monthly / Yearly
- fix_amount
- unit
- is_incremental
- increment_amount

Baseline retained formula:

```text
current_target ≈ fix_amount + qualifying_completions × increment_amount
```

### Confirmed inactivity behavior / tuning handoff

After sufficiently long inactivity, an incremental target decays gradually toward its original baseline; only `Done` completions advance the target. The exact inactivity threshold and decay curve are tuning parameters owned by the later Routine/Gamification specification and must not be invented inconsistently in Increment 3.

---

# 10.4 TrackingState

Shared capability for Routine and later Goal:

- current_streak
- best_streak
- total_completions
- ai_quote optional
- illustration_url optional

No database inheritance is implied.

Implementation may use composition/embedded/shared table according to Data Design decision.

---

## Documents

### Update

- `docs/requirements/srs.md`
- `docs/design/data-model.md`
- ERD
- API
- UI/UX
- Traceability
- Risk Register

### New

- Routine/RoutineCompletion migration(s)
- TrackingState ADR if storage decision is significant

### Canonical

Decision Register updates only if incremental-target or TrackingState conceptual behavior is newly decided.

---

## Acceptance

- one Routine definition produces many dated outcomes.
- one current RoutineCompletion per routine/date.
- Reset removes current row and history remains.
- historical edit works.
- unscheduled date completion works.
- Routine itself has no status.

---

# 11. Increment 4 — Recurrence Engine + Routine Streak Semantics + Reminders + Time Semantics

## Goal

ساخت موتور recurrence مشترک با capability restriction هر entity و formalize کردن streak behavior روتین‌ها.

---


> **Increment 6 compatibility check:** Design in this Increment must follow Section 7.6 and review known Offline/Sync + branching History semantics before persistence/API choices are finalized.

# 11.1 Recurrence Capabilities

Calendar:

- Jalali
- Gregorian

Task/Event:

- minute interval
- hour interval
- day
- week
- month
- year
- advanced combined expression

Routine:

- day
- week
- month
- year only

Routine has day-level occurrence.

---

## Constant

- Daily
- Weekly
- Monthly
- Yearly

## Dynamic / Interval

- every x minutes
- every x hours
- every x days
- every x weeks on selected weekdays
- every x months on selected days / last_day
- every x years on selected month/day

## Advanced

Task/Event only where applicable:

```text
minutes + hours + days
```

---

# 11.2 Recurring Task Rule

Generation is time-based.

Creating next recurring Task must not depend on previous Task completion.

---

# 11.3 Routine Fixed-Day Streak

Example semantics:

- scheduled Done occurrences form streak.
- missed scheduled occurrence breaks sequence.
- extra unscheduled Done is valid.
- extra Done does not retroactively repair missed occurrence.
- it can start/continue a new sequence.

---

# 11.4 Frequency Routine Semantics — confirmed, formalize in specification/tests

Canonical behavior for `N times per period` is already closed: each valid `Done` can advance the streak, empty days inside the period do not by themselves break it, and failure to satisfy the period quota resets the streak at the next period boundary. Increment 4 must formalize period boundaries, quota accounting and RoutineCompletion interaction in `RECURRENCE_SPEC.md` and comprehensive tests without reopening the Product decision.

---

# 11.5 ReminderConfig

Multiple reminders per Item:

- trigger-before
- persistent flag

Persistent/alarm-like intent is represented in domain/API now. Current PWA delivery is best-effort within browser/OS capability and is not required to provide full native alarm semantics on every platform. Full-screen/ringing/background integration may be completed when native OS clients are built.

---

# 11.6 Time and Calendar Semantics

Must analyze in `docs/design/time-semantics-spec.md` and design/test comprehensively:

- distinction between real instant, Calendar Day, Dotick Day, `RoutineCompletion.occurrence_date` and credited/effective date
- UTC/canonical instant for shared schedulable items
- local timezone display
- all-day representation
- Jalali vs Gregorian recurrence calculation
- `last_day`
- leap years
- invalid calendar dates
- DST
- timezone change
- scheduler catch-up after downtime
- recurrence editing behavior
- occurrence identity
- Account timezone vs device timezone
- timezone changes without shifting established instants
- DST gaps/folds and offset changes
- cross-calendar Jalali/Gregorian edge cases
- day-boundary/finalization interaction

The specification must include reusable golden test vectors and boundary cases; this is a release/readiness requirement for time-sensitive increments.

---

## New Document

`RECURRENCE_SPEC.md`

Contains:

- formal recurrence schemas
- entity capability matrix
- edge-case behavior
- streak semantics
- test vectors

---

## Documents

### Update

- SRS
- Decision Register for resolved frequency semantics
- Domain Model only if conceptual recurrence model changes
- Data Design
- API
- Architecture
- Test Strategy if property-based testing is adopted
- Traceability

### New

- recurrence scheduler ADR
- migrations
- recurrence test-vector report if useful

---

# 12. Increment 5 — Product Navigation, Views, Responsive UI & Themes

## Goal

ساخت تجربه‌ی کاربری کامل برای domainهای ساخته‌شده.

---


> **Increment 6 compatibility check:** Design in this Increment must follow Section 7.6 and review known Offline/Sync + branching History semantics before persistence/API choices are finalized.

## Main Navigation

- Folder/List access
- daily entry point / Today
- Inbox
- list navigation

---

## List Views

Same underlying data:

- List
- Kanban
- Timeline

Changing View does not modify domain data.

---

## Dedicated Views

- Calendar
- Routine page
- Eisenhower/Priority Matrix

Routine UI must show:

- scheduled routines for selected day as primary suggestions
- manually completed unscheduled routines in historical/week context
- dedicated Routine calendar allowing manual completion on unscheduled date

---

## Responsive / Mobile-first

- mobile-responsive
- touch-friendly
- loading state
- empty state
- validation state
- error state
- confirmation for destructive behavior
- accessibility baseline

---

## Themes

Retained vision:

- Minimal customizable
- Liquid Glass style
- Material 3 Expressive inspired
- Dot-matrix style

Theme architecture should use shared tokens/components, not four separate applications.

### Future Generative-Experience Compatibility Guardrail

Increment 5 still implements the retained conventional themes above; it does **not** implement the Future Generative Experience Runtime.

However, its UI architecture must avoid placing authoritative domain rules only inside theme-specific components. Current themes should reuse shared tokens/primitives/components and invoke stable application/domain actions so a later validated generated surface can compose the same product capabilities without bypassing authorization or business rules.

Do not add the future Experience DSL engine, AI theme generator, Preview sandbox, or extension runtime in Increment 5 merely to anticipate E6/E7.

---

## Error Presentation

Technical API error is translated into understandable UI message.

---

## Documents

### Update

- `docs/design/ui-ux/`
- API for query/filter/sort needs
- Data Design for user view preference if persisted
- Security for rich content rendering
- Traceability

### New

- UI architecture ADR where necessary

---

# 13. Increment 6 — Offline-first Sync + History + Undo + Selective Recovery

## Goal

offline use, field-level conflict baseline, reliable history and recovery.

---

# 13.1 Offline Operation

User can at least:

- create
- edit
- complete
- reset supported state
- perform supported deletes

while offline.

Local state syncs after reconnect.

---

# 13.2 Conflict Strategy

Baseline retained:

```text
Field-level Last-Write-Wins
```

Not record-level LWW.

---

# 13.3 Sync Metadata Design Gate

Must finalize engineering representation for the already-confirmed sync semantics:

- per-field timestamps or alternative trusted ordering metadata
- authoritative clock strategy
- clock skew
- device identity
- idempotency
- delete/update conflict
- relation conflict
- ContentBlock conflict granularity
- compatibility between Sync operation metadata, immutable Audit evidence and branching user-visible History
- comment conflict
- RoutineCompletion conflict
- recurrence edit conflict
- tag relation conflict

Decision goes to `docs/decision-register.md`.

---

# 13.4 Audit / History / Undo

Expand AuditLog to support:

- history view
- Reset trace
- Undo/restore where product allows
- sync troubleshooting

Still not necessarily event sourcing.

---

# 13.5 RoutineCompletion Sync

- unique routine/date current state
- amount edits same row
- Reset/delete must sync safely
- Won't_Do remains explicit state

---

# 13.6 Selective Recovery

Failure paths:

- interrupted sync
- retry
- duplicate request
- local/server partial failure
- app restart
- reconnect
- stale version

---

## New Document

`SYNC_AUDIT_SPEC.md`

---

## Documents

### Update

- SRS
- Decision Register
- Domain Model if sync metadata becomes conceptual
- Data Design
- API
- Architecture
- Security
- Test Strategy
- Risk Register
- Traceability

### New

- sync ADR(s)
- failure test report
- migrations

---

# 14. Increment 7 — Direct Sharing + Groups + Authorization + Assignment + Realtime

## Goal

اضافه کردن collaboration فعلی با تفکیک Direct Sharing از Group Collaboration، بدون وارد کردن Enterprise complexity.

---

# 14.1 Direct Resource Sharing

Personal user باید بتواند بدون ساخت Group، Resource مشخصی را با user دیگری Share کند.

Current shareable scopes:

```text
Folder
List
Item
├── Task
├── Event
└── Routine
```

Rules:

- Sharing ownership را به‌تنهایی منتقل نمی‌کند.
- Share می‌تواند مستقل از GroupMembership revoke شود.
- Group membership prerequisite برای Direct Sharing نیست.

---

# 14.2 Field Visibility

برای Item shared، owner باید بتواند visibility را با field groupهای سطح product/domain محدود کند.

نمونه:

- basic information
- schedule
- progress/status
- description
- location
- attachments
- tags
- completion history
- amount
- streak/statistics
- notes

Database/ORM fields و metadata داخلی مستقیماً user-facing sharing controls نیستند.

Exact field-group catalog و storage representation در Authorization/Data Design refine می‌شود.

---

# 14.3 Current Access / Role Scope

Confirmed baseline:

- Direct Sharing از predefined Access Profile استفاده می‌کند.
- GroupMembership از **System-defined Roles** استفاده می‌کند.
- Access Profile و Group Role یک مفهوم واحد نیستند.
- Custom Roles در current scope نیستند.
- Custom Roles و arbitrary permission composition به Enterprise منتقل می‌شوند.
- authorization در design باید capability-based باشد، نه scattered role-name checks.

Representative capabilities:

```text
view
comment
edit
move
claim
assign
manage_structure
manage_members
manage_sharing
send_nudge
```

Exact profile/role permission matrix در `AUTHORIZATION_MODEL.md` تعیین می‌شود.

---

# 14.4 Container Sharing & Inheritance

Shared container access باید بتواند به descendants برسد:

```text
Folder
└── List
    └── Item
```

Personal V1 به explicit-deny exception پیچیده برای هر descendant نیاز ندارد.

Design باید مشخص کند:

- direct و inherited grants چگونه resolve می‌شوند؛
- effective access چگونه محاسبه می‌شود؛
- revoke یک parent grant چه اثری بر inherited access دارد؛
- move کردن Resource بین shared/private container چه اثری دارد؛
- cache/index strategy برای authorization چیست.

این موارد Design concern هستند و نباید semantics نهایی محصول را تغییر دهند.

---

# 14.5 Group Domain

- Group
- GroupMembership
- SystemRole
- TaskAssignment

Rules:

- user can belong to multiple groups
- membership has a system role
- Group is a persistent collaboration context
- Group can collaborate on shared resources
- Task can be assigned to multiple authorized members
- authorized member can claim Task where the relevant capability is granted
- group data/access isolation

---

# 14.6 Confirmed Group Ownership Model

The Product decision is already closed:

- collaborative containers/resources created directly in Group context are Group-owned;
- a personal Resource may be attached to Group context while retaining its personal owner;
- leaving the Group does not delete Group-owned Resources;
- the personal owner controls detaching their personal Resource from Group context;
- Group-owned Resource access must not be bypassed by Direct Sharing to an actor outside the Group.

Increment 7 owns the persistence/authorization implementation and tests for these confirmed semantics.

---

# 14.7 Authorization

Must design and test:

- direct resource access
- inherited container access
- Group membership access
- field visibility enforcement
- comment permission
- edit/move permission
- claim/assignment permission
- sharing-management permission
- Nudge/encouragement permission
- cross-group/cross-user isolation
- creator vs owner behavior
- effective access after revoke
- permission changes while a client is connected

`Assignment` must remain separate from authorization. Assigned or claimed Task does not grant access by itself.

---

# 14.8 Realtime

WebSocket only for:

- live update
- notifications
- lightweight collaboration events such as permitted Nudge delivery

REST remains CRUD authority.

Must test:

- stale socket authorization
- revoked direct share
- membership removal
- inherited-access change
- reconnect
- permission change
- field-visibility filtering of realtime payloads

---

# 14.9 Shared Time

Shared Task/Event uses an absolute instant baseline and displays according to each viewer's timezone.

---

## New Document

`AUTHORIZATION_MODEL.md`

Must formalize at least:

- shareable resource scope
- access profiles
- system-role permission mapping
- capability matrix
- field visibility policy
- direct vs inherited access
- effective-access resolution
- Group access
- assignment/claim authorization
- revoke behavior
- realtime authorization behavior

---

## Documents

### Update

- SRS
- Domain Model
- Data Design
- API
- Architecture
- Security
- UI/UX
- Traceability
- Risk Register

### New

- authorization ADR(s) where required
- WebSocket ADR if needed
- security test report
- migrations

---

## Acceptance

- user can share a Task/Event/Routine directly with another user without creating a Group.
- user can share a List or Folder and descendant access is inherited according to the confirmed model.
- owner can limit visible Item information through supported field groups.
- Viewer/Commenter/Contributor/Manager-style access profiles enforce their configured capabilities.
- Group collaboration continues to use System-defined Roles.
- authorized user can comment, move, claim or assign only where the effective permission permits it.
- assignment or claim alone never grants access.
- revoking direct or inherited access removes authorization without changing ownership.
- realtime updates never expose fields or resources outside the viewer's effective access.
- Custom Roles and organization hierarchy are not required for Increment 7.

# 15. Increment 8 — AI-Assisted Item Creation: Voice Draft/Review

## Goal

پیاده‌سازی AI به‌عنوان پیشنهاددهنده برای ایجاد Item، نه creator خودکار.

این feature دیگر صرفاً Speech-to-Task نیست.

---

# 15.1 Supported Current Entry Point

Current Scope AI-assisted input:

- **Voice input only**.

Typed User input belongs to ordinary manual Item creation and is not an AI-assisted fallback. Voice option should be available near the normal Item creation entry point where practical. If microphone capability/permission is unavailable, the UI explains the requirement and keeps manual creation usable; it does not switch to typed-text AI creation.

Email/external/text-derived automated input remains Future Integration scope.

---

# 15.2 Pipeline

```text
Voice
↓
Speech-to-Text / Normalization
↓
Intent + Entity Analysis
↓
One or More AI Item Proposals
↓
Review UI
↓
User edits
↓
Confirm
↓
Create real Item
```

No real Item before Confirm.

---

# 15.3 AI Inference

At minimum infer when possible:

- Task / Event / Routine
- title
- date/time
- location
- description
- Folder
- List
- Column
- reminders
- other inferable fields

All inferred fields remain editable.

---

# 15.4 AIItemCreationSession

Conceptual entity:

- user
- source_type (`Voice` for Current-Scope direct User input)
- original_input
- normalized_transcript
- AI proposal payload
- user final payload
- field-level changes
- model version
- accepted state
- timestamps

Used for:

- review flow
- debugging
- evaluation
- future personalization

---

# 15.5 Draft Field Provenance

Draft/session should be able to distinguish:

- explicit spoken User input
- AI inferred
- user-preference inferred
- external source provenance only for future integrations if/when that source enters Scope

Exact storage belongs in design.

---

# 15.6 External AI Context Acknowledgement

Before external AI processing is enabled/first used, the User must be informed and accept that authorized context—including shared data within effective field visibility—may be transmitted to third-party AI infrastructure. Security/Privacy design must ensure unauthorized fields are never included. Legal allocation of third-party processing/retention risk belongs to the release Privacy Policy/Terms gate.

---

# 15.7 Failure Isolation

AI/STT failure:

- must not break normal manual item creation
- must provide understandable fallback

---

# 15.8 Future Learning Boundary

Learning from proposal corrections is a confirmed future capability, not required for this Increment.

Current Increment must retain the accepted proposal/final diff needed for evaluation/future learning without preserving rejected/cancelled sessions contrary to Current-Scope privacy/retention semantics.

---

## New Document

`AI_ITEM_CREATION_SPEC.md`

---

## Documents

### Update

- SRS
- Domain Model only if session model changes
- Data Design
- API
- UI/UX
- Security/privacy section
- Risk Register
- Traceability

### New

- AI integration ADR
- model/prompt/output schema version artifact
- evaluation test set/report

---

# 16. Increment 9 — Goal + AI Tagging + Semantic Discovery + Goal Lifecycle

## Goal

ساخت Goal/Tag semantic foundation before Daily Ring selection.

---

# 16.1 Goal

Goal is not Item.

Fields/capabilities:

- id
- title
- optional description
- tracking_state
- Active / Dormant / Archived
- List relation
- optional Column relation
- Tags

No fixed maximum number of Goals.

---

# 16.2 Tag

- standalone entity
- User / AI source
- Item many-to-many
- Goal one-to-many current model
- User tags are not auto-archived
- AI tags can be merged/archived

---

# 16.3 Goal Tracking Semantics

Confirmed:

```text
Goal.current_streak
= consecutive Dotick Days where Goal is actually completed
```

A small activity is not enough.

```text
Goal.total_completions
= count of completed Goal days
```

Exact Daily Ring completion logic is implemented in Increment 10.

---

# 16.4 Initial Goal Discovery

AI analyzes:

- List
- Column
- actual Item content
- existing user tags
- semantic coherence

Do not create Goal for random/non-coherent grouping.

---

# 16.5 Warm-up Tuning Gate

Time-based warm-up behavior is confirmed. The exact duration is a tunable/model-versioned parameter that must be calibrated and recorded in `AI_GOAL_SPEC.md` before production auto-discovery.

---

# 16.6 Reactive Review

Retained baseline:

- 12-hour delayed recheck for new/dormant context
- only affected context re-evaluated

---

# 16.7 Weekly Global Review

- merge very similar Goals where appropriate
- AI tag cleanup/archive
- semantic refresh

---

# 16.8 Similarity Tuning Gate

Tiered similarity behavior is confirmed. `AI_GOAL_SPEC.md` must define/version the numeric reactivation/merge thresholds and evaluation behavior without changing the canonical product tiers.

---

# 16.9 Goal Lifecycle

Dormant:

- no meaningful active work
- excluded from Ring eligibility
- streak frozen, not reset
- can be re-evaluated

Archived:

- historical
- no automatic reactivation

---

# 16.10 GoalGenerationLog

Append-only:

- goal
- Initial_Generation / Weekly_Review / Reactivation_Check
- AI model/version
- changed
- previous/new title/description
- user rating when real change occurs
- created_at

---

## New Document

`AI_GOAL_SPEC.md`

---

## Documents

### Update

- SRS
- Decision Register for warm-up/similarity decisions
- Domain Model only if conceptual relation changes
- Data Design
- API
- Architecture
- Security/privacy
- Risk Register
- Traceability

### New

- semantic evaluation dataset/report
- Goal AI ADR
- migrations

---

# 17. Increment 10 — Daily Rings + Dotick Day + Scoring + Norm + Statistics

## Goal

پیاده‌سازی اصلی‌ترین motivational/analytics layer بر پایه‌ی snapshot تاریخی و Dotick Day.

---

# 17.1 Decision / Design Gates — Must Resolve Here

Product behavior already fixed before this Increment includes:

- Daily Ring count and system-controlled Goal selection;
- Global Streak behavior;
- AI-owned difficulty/effort estimation;
- Daily Ring plan structure based on `RingGroup` and `DailyAction`;
- controlled current-day replan with immutable finalized history.

Before implementation, the owning specifications must finalize the remaining design/tuning details:

1. exact Ring scoring formula
2. exact representation/serialization of RingGroup completion rules
3. exact DailyAction persistence and linkage to Original Item
4. exact Goal selection algorithm implementation
5. learning/adaptation parameters for selection weights
6. adaptive Norm thresholds/windows
7. day-finalization/replan concurrency edge cases
8. AI decomposition output contract and fallback behavior

These are implementation/specification gates and must not redefine the confirmed product semantics.

---

# 17.2 DailyRing Count

Confirmed business rule:

```text
active eligible goals >= 3 → exactly 3 Rings
eligible goals = 2         → 2 Rings
eligible goals = 1         → 1 Ring
eligible goals = 0         → 0 Rings
```

No 3-to-4 ambiguity remains.

---

# 17.3 Daily Goal Selection Quality

Selection inputs:

- due/timing
- priority
- neglect
- weekday behavior
- holiday context
- streak momentum
- workload
- difficulty
- recent user capacity

Quality intent:

- balanced daily composition
- not simply biggest backlog
- mixture may include current/important, neglected, growth/learning patterns

Those are not hard-coded categories unless later explicitly decided.

---

# 17.4 DailyRing Snapshot

Concept:

```text
DailyRing
- user
- goal
- effective_date
- target
- progress_percent
- is_completed
- final_score
- is_finalized
- algorithm/version metadata
- timestamps
```

Historical Ring meaning must not be rewritten by normal future Item changes.

---

# 17.5 RingGroup + DailyAction Plan

Daily Ring is implemented as a daily plan rather than a flat Item-membership set:

```text
Goal
↓
DailyRing
↓
RingGroup
↓
DailyAction
↓
Original Item
```

`DailyAction` can represent either:

- completion of the full Original Item;
- a meaningful measurable part of a larger Item for that Dotick Day.

A partial DailyAction must not automatically complete the Original Item.

`RingGroup` expresses deterministic completion/contribution rules such as:

- all members;
- minimum count;
- minimum credit;
- one-of-many;
- credit cap;
- hard requirement.

AI may estimate difficulty/effort and propose decomposition, but progress/completion evaluation must remain deterministic and reconstructable.

---

# 17.5.1 Current-day replan

The initial plan is generated at Dotick Day start.

During the same day:

- newly created relevant Items may become DailyActions;
- deleted Original Items remove dependent Actions from the current plan;
- materially harder commitment changes require controlled replan;
- Goal selection is not globally rerun for every Item change;
- a Ring already completed must not become incomplete due to later replan.

Finalized RingGroup/DailyAction state becomes the immutable historical snapshot.

---

# 17.6 Progress vs Completion vs Performance

Separate:

```text
progress_percent = 0..100
is_completed     = Boolean
final_score      = may exceed baseline
```

UI progress never exceeds 100.

Final score may exceed 100/baseline.

---

# 17.7 Hidden Bonus

During day:

- user sees progress
- early/importance bonus must not make user think enough work is done too early

At day finalization:

- final score computed
- bonus revealed

---

# 17.8 Early Reward + Late-day Recovery

Behavioral requirements:

- important Item completed early gives higher final performance.
- near end of day, completing remaining relevant work should still make real progress toward completion.
- recovery does not push progress bar >100.
- overachievement belongs to final score.

Exact formula belongs in Gamification spec.

---

# 17.9 Dynamic Norm / Daily Capacity

Daily target not manually set.

Behavior:

- repeated miss → temporary reduction
- recovery → gradual return
- repeated success → gradual increase
- new observations → updated user norm

---

# 17.10 Dotick Day

Calendar Day and Dotick Day differ.

UserPreferences:

- timezone
- optional explicit day boundary

Default if boundary not explicitly configured:

- 60-minute ambiguity window after midnight
- completion inside window asks Today / Yesterday attribution

Explicit boundary:

- automatic attribution relative to chosen boundary

---

# 17.11 Credited / Effective Date

Completion scoring needs an effective date separate from raw timestamp where necessary.

Exact storage depends on completion type and Data Design.

---

# 17.12 Day Finalization

At Dotick Day boundary:

1. close previous Daily Rings
2. finalize progress/completion
3. compute final score
4. reveal bonus
5. finalize Goal streak
6. finalize global streak according to the confirmed at-least-one-completed-Ring rule, with pause semantics when no valid Ring opportunity exists
7. generate new day's Rings

After finalization, Ring snapshot is historical.

---

# 17.13 Statistics / Selective Recalculation

Raw sources include:

- Task/Event state changes
- RoutineCompletion
- DailyRing / RingGroup / DailyAction
- AuditLog

Derived statistics may include:

- Today
- Weekly
- Monthly
- recent behavior
- lifetime

Historical edit:

- only affected windows/metrics recomputed
- simple counters increment/decrement where possible
- streak local recomputation
- expensive behavior features may refresh asynchronously
- no default full-history recomputation

---

# 17.14 Goal-level Reminder

Separate from Item reminder.

May trigger on meaningful decline from Goal Norm.

Frequency/rate-limit UX must be designed/tested.

---

## New Document

`GAMIFICATION_SCORING_SPEC.md`

Must include:

- Dotick Day lifecycle
- DailyRing state
- selection algorithm
- scoring formula
- progress/final score separation
- Norm adaptation
- streak definitions
- historical correction rules
- Goal reminder behavior
- test vectors

---

## Documents

### Update

- SRS
- Decision Register
- Domain Model if finalized concepts change model
- Data Design
- API
- UI/UX
- AI Goal Spec
- Security
- Risk Register
- Traceability

### New

- algorithm ADR(s)
- simulation/evaluation report
- scoring golden test vectors
- migrations

---

# 18. Increment 11 — Personal V1 Production Readiness & Deployment

## Goal

تبدیل تمام Incrementهای Personal V1 به release قابل اتکا برای استفاده‌ی واقعی.

---

# 18.1 Performance

Validate retained baseline:

- approximately 30 concurrent users on local instance without noticeable degradation
- WebSocket near-real-time experience
- direct hierarchy query performance
- DailyRing generation latency
- sync recovery performance

This is a test target, not SLA.

---

# 18.2 Security Hardening

Verify:

- password hashing
- JWT/session security
- OAuth
- Passkey
- HTTPS
- authorization isolation
- Group isolation
- attachment safety
- rich content/XSS handling
- rate limiting
- secret handling
- dependency vulnerabilities
- AI data exposure/privacy, including recorded User acknowledgement for external processing and authorized shared context only
- WebSocket authorization
- upload limits

---

# 18.3 Reliability / Data Safety

- backup
- restore test
- migration test
- rollback
- offline recovery
- sync conflict tests
- historical edit correctness, including immutable finalized statistical windows
- branching History ↔ Audit ↔ Sync consistency
- comprehensive `docs/design/time-semantics-spec.md` golden vectors across timezone/DST/Jalali/Gregorian/Dotick-Day boundaries
- Routine Reset + AuditLog correctness
- day finalization idempotency
- AI service outage fallback

---

# 18.4 Observability

- structured logs
- health checks
- error tracking
- API metrics
- DB health
- sync failures
- WebSocket failures
- scheduler failures
- AI failures
- DailyRing generation/finalization failures

---

# 18.5 Deployment

Environments:

- development
- staging/test-equivalent
- personal production

Deployment:

- reproducible container/image
- configuration
- secrets
- migrations
- smoke test
- rollback

---

# 18.6 Documentation Quality Gate

Verify consistency between:

- System Definition
- Decision Register
- Domain Model
- Formal SRS
- Roadmap
- Architecture
- Data Design
- API
- UI/UX
- specialized specs
- implemented system

---

## New Reports

- Performance benchmark report
- Security review report
- Backup/restore report
- Personal V1 release note

---

## Personal V1 Exit Criteria

- all Personal V1 requirements traced.
- all current-scope entities implemented as required.
- no unresolved Current-Scope Product/Domain question blocks release.
- all required Design/Specification gates for implemented features are finalized and traced; Future-only design work remains explicitly Future.
- regression suite green.
- backup/restore demonstrated.
- offline/online core flows verified.
- deployment reproducible.
- AI outage does not disable manual core use.
- DailyRing history remains stable.
- documentation matches code.

---

# 19. Parallel Business Track

This track can proceed in parallel but must not force unnecessary Enterprise complexity into Personal V1.

---

## B1 — Market / Product Positioning

- target organizations
- buyer/user distinction
- competitors
- product positioning
- packaging

### New / Update

`BUSINESS.md`

---

## B2 — Pricing & Licensing

Open:

- personal/free tier
- subscription
- per-user
- per-org
- enterprise contract
- license terms

`BUSINESS.md` → **Update**

---

## B3 — Customization Strategy

Define possible Enterprise customization:

- branding
- theme
- workflow
- integrations
- role model
- deployment

Do not implement until a real requirement exists.

---

## B4 — Support / SLA

Define when Enterprise offering becomes concrete:

- support channels
- severity
- response targets
- uptime commitment
- maintenance
- backup/restore commitment

### Future New Document

`SLA.md`

---

# 20. Future Increment E1 — Enterprise Identity, Multi-tenancy & Custom Authorization

## Scope

- Organization/Tenant
- Enterprise SSO
- choose SAML or OIDC
- Custom Roles
- richer permission model
- org hierarchy
- manager/subordinate visibility
- full tenant isolation
- data retention
- enterprise privacy/compliance
- GDPR analysis where applicable

### New

- Enterprise SRS or Enterprise Supplement
- Privacy/Compliance spec
- enterprise threat model

### Update

- Domain Model
- Data Design
- Authorization Model
- API
- Security
- Architecture

---

# 21. Future Increment E2 — Enterprise Administration, Reporting & Documentation

## Scope

- admin controls
- organization configuration
- management reporting
- advanced access/reporting
- enterprise onboarding
- user/admin documentation
- troubleshooting/install/support guides where relevant

---

# 22. Future Increment E3 — External Integrations, Email Automation & Personalization

## Scope

### Google Calendar

- import/sync
- Source external_account/external_id mapping
- conflict rules

### Email / External Sources

```text
External Source
↓
Normalized Input
↓
AI Analysis
↓
Draft or allowed automation
↓
Item Model
```

### Trusted Automation Future Design Gate

The authority principle is already canonical: automation without per-action confirmation must be explicit, scoped, revocable and auditable. Before any E3 automatic action is implemented, Future Design must define the concrete authority levels, trusted-source/rule model, per-field limits and review/override UX without weakening that principle.

### AI Correction Learning

Use stored AIItemCreationSession data to learn user preferences.

Examples:

- reminder preferences
- location/list mapping
- event/task classification patterns

Learning must remain user-safe and reversible.

---

# 23. Future Increment E4 — Native Mobile / OS-specific Capabilities

After initial mobile-first experience is validated.

## Android

Evaluate Kotlin-native only if justified.

## iOS

Evaluate Swift-native only if justified.

## Native capabilities

- full persistent/alarm-like notifications and OS-specific full-screen/ringing behavior deferred from PWA limitations
- background scheduling
- push notification if needed
- OS permission handling
- local database integration
- platform-specific offline behavior

---

# 24A. Future Increment E5 — Built-in AI Agent Runtime

## Goal

Add a Dotick-operated Agent that can inspect and act on Dotick through explicit User authority without creating a second business-logic path.

## Scope

- authority presets: `Observe`, `Ask`, `Assist`, `Autonomous`;
- grant lifetimes where applicable: `Once`, `This session`, `Always` until revoked;
- capability classification and gateway;
- sensitive/destructive action classification and confirmation policy;
- revocation and permission inspection;
- Agent origin in History/Audit;
- Agent use of the same authorization/domain/application path as ordinary User actions;
- origin-neutral Undo/recovery for equivalent planning mutations;
- Agent failure isolation and privacy/context controls.

## Non-goals

- no direct ORM/database mutation tool for the Agent;
- no authority inferred merely from an AI prompt;
- no public unrestricted API implied by the built-in Agent.

## New / Updated Future Artifacts

- `AI_AGENT_SPEC.md` — New
- Architecture — Update
- Authorization Model — Update
- Security Design — Update
- API/capability contracts — Update
- UI/UX — Update
- Test Strategy / Agent evaluation suite — Update/New

---

# 24B. Future Increment E6 — Generative Experience Runtime

## Goal

Allow the User to describe and iteratively edit a validated Dotick experience while preserving the stable product kernel.

## Scope

- transformation distance: `Recolor`, `Restyle`, `Transform`, `Reimagine`;
- declarative Experience Specification/DSL;
- registered design primitives/components/actions;
- versioned Experience artifacts;
- AI generation/edit/repair outside the ordinary interaction loop;
- deterministic structural/schema validation;
- required-capability reachability contracts;
- functional simulation using representative synthetic Dotick state;
- accessibility validation against the measurable baseline selected for that release;
- AI UX review after deterministic checks;
- fully interactive synthetic-data Preview before Apply;
- protected recovery/default experience and previous-valid-version restore;
- controlled link/file/package sharing;
- generated/User-provided/external asset provenance and trust policy;
- explicit per-device/form-factor adaptation, validation, Preview and Apply; no cross-device auto-activation.

## Hard Boundary

The Experience Runtime does not execute unrestricted AI-generated JavaScript, React/native code, unrestricted CSS, or another arbitrary executable theme payload. Generated presentation maps permitted interactions to registered Dotick capabilities; it does not redefine domain operations.

## New / Updated Future Artifacts

- `GENERATIVE_EXPERIENCE_SPEC.md` — New
- Experience DSL/schema + versioning artifact — New
- UI architecture / renderer ADR — New
- synthetic preview/test-workspace specification — New
- Architecture — Update
- UI/UX — Update
- Security Design — Update
- Accessibility/Quality specification — Update/New
- Test Strategy — Update

---

# 24C. Future Increment E7 — Generated Extensions / Personal Productivity Environment

## Goal

Extend Generative Experience with bounded experience-specific state/rules only after the safe presentation runtime is mature.

## Scope candidate

```text
Extension State
Extension Events
Extension UI
Extension Rules
```

This phase may support experience-specific progression or other bounded mini-functionality driven by real Dotick events. It must remain sandboxed and must not become an alternate source of truth for core Task/Event/Routine, authorization, Sync, or History semantics.

Exact extension state/event/rule security model is a mandatory Future Design Gate before implementation.

---

# 24. Canonical Feature Coverage Matrix

This matrix maps the current canonical specification to an implementation location.

| Canonical Feature / Rule | Increment |
|---|---|
| Product vision / personal-first architecture | 0, all |
| Folder > List > Column terminology | 1 |
| Inbox | 1 |
| default Column / legacy not_sectioned | 1 |
| List/Kanban/Timeline/Calendar/Routine/Eisenhower views | 5 |
| same data across views | 5 |
| Item common identity metadata | 1 |
| owner_user_id | 1 |
| created_by_user_id | 1 |
| ownership separate from Source | 1 |
| Source platform/external_account/external_id | 1/2 |
| Basic Task CRUD | 1 |
| Task unscheduled identity/persistence | 2 |
| Task due/end/all-day | 2 |
| Task deadline/grace lifecycle + default grace=0 | 2 |
| grace=0 direct Skipped | 2 |
| Done/Won't_Do user-driven | 1/2 |
| Task dependency + blocked-Done gate + blocker deletion | 2 |
| Task hierarchy completion cascade + Preferences | 2 |
| hierarchy cascade authorization/confirmation/atomicity | 2 |
| Task/Event priority | 2 |
| Event timing/location/status | 2 |
| Event sub-event | 2 |
| Event multi-reference | 2 |
| Task/Event single structural parent invariant | 2 |
| direct queryable hierarchy | 2 |
| Task single structural parent | 2 |
| child vs reference semantics | 2 |
| RichDescription capabilities | 2 |
| ContentBlock stable identity | 2 |
| ContentBlock exact schema decision | 2 Gate |
| Item/block comments | 2 |
| Manual Tag | 2 |
| AuditLog foundation | 2 |
| Routine definition record | 3 |
| Routine has no status | 3 |
| Routine start/end validity | 3 |
| Routine target Achieve_All/Partial | 3 |
| incremental Routine baseline target | 3 |
| RoutineCompletion occurrence_date | 3 |
| no completed_at business field | 3 |
| one RoutineCompletion row per day | 3 |
| Reset deletes current row, AuditLog remains | 3 |
| historical Routine edits | 3 |
| unscheduled Routine completion | 3 |
| TrackingState capability/composition | 3 |
| Jalali/Gregorian recurrence | 4 |
| Task/Event minute-hour-day-week-month-year-advanced | 4 |
| Routine day-week-month-year only | 4 |
| recurring Task independent of completion | 4 |
| fixed-day Routine streak | 4 |
| extra completion does not repair missed scheduled occurrence | 4 |
| N-times-per-period Routine semantics | 4 Gate + implementation |
| multiple reminders / trigger-before | 4 |
| persistent reminder domain capability | 4, E4 OS behavior |
| timezone/UTC shared time semantics | 4/7 |
| responsive mobile-first UI | 5 |
| four retained themes | 5 |
| shared token/component theme foundation compatible with later generated surfaces | 5 guardrail |
| built-in AI Agent authority profiles | E5 |
| Agent Once / Session / Always grants, revocation and audit | E5 |
| Agent uses ordinary domain/authorization/Undo path | architecture guardrail now; E5 runtime |
| Generative Experience transformation distance | E6 |
| declarative Experience Specification/DSL | E6 |
| deterministic capability/structural validation + functional simulation | E6 |
| interactive synthetic-data Preview before Apply | E6 |
| explicit cross-device adaptation; no auto-apply | E6 |
| generated experience sharing/package validation | E6 |
| bounded generated Extension State/Events/UI/Rules | E7 |
| offline use | 6 |
| field-level LWW baseline | 6 |
| sync metadata design | 6 Gate |
| history / Undo | 6 |
| selective sync recovery | 6 |
| Direct Resource Sharing without Group | 7 |
| Item field-group visibility | 7 |
| Folder/List inherited sharing | 7 |
| predefined Direct Sharing Access Profiles | 7 |
| capability-based authorization model | 7 |
| Nudge / encouragement permission | 7 |
| multi-group membership | 7 |
| System-defined Group Roles current version | 7 |
| Custom Roles | E1 |
| multi-assignee Task | 7 |
| Task claim | 7 |
| assignment independent from authorization | 7 |
| group/user resource isolation | 7 |
| Folder/List/Column group ownership decision | 7 Gate |
| WebSocket live updates/notifications | 7 |
| Email/password auth | 1 |
| Google OAuth + fallback | 1 |
| JWT | 1 |
| Passkey | 1 |
| Enterprise SSO | E1 |
| AI item creation generalized beyond speech | 8 |
| Voice beside create flow | 8 |
| infer Task/Event/title/time/location/description/location tree/reminders | 8 |
| AI proposal requires review/confirm | 8 |
| AIItemCreationSession | 8 |
| field provenance in draft | 8 |
| learning from AI corrections | E3 |
| Email/external AI input | E3 |
| Goal independent from Item | 9 |
| unlimited Goals | 9 |
| AI Tag lifecycle | 9 |
| Goal Active/Dormant/Archived | 9 |
| Goal current_streak meaning | 9/10 |
| Goal total_completions meaning | 9/10 |
| semantic coherent List/Column Goal discovery | 9 |
| initial AI Goal warm-up | 9 Gate |
| 12h reactive review | 9 |
| weekly semantic review | 9 |
| Goal similarity thresholds | 9 Gate |
| GoalGenerationLog | 9 |
| Daily Ring count = min(3, eligible goals) | 10 |
| balanced Goal selection quality | 10 |
| Goal selection inputs | 10 |
| Goal selection exact algorithm | 10 Gate |
| DailyRing historical snapshot | 10 |
| RingGroup / DailyAction snapshot and replan | 10 |
| Item only credits credited-day Ring | 10 |
| progress_percent 0..100 | 10 |
| is_completed separate | 10 |
| final_score may exceed baseline | 10 |
| bonus hidden until finalization | 10 |
| early completion reward | 10 |
| late-day recovery | 10 |
| adaptive Norm | 10 |
| Dotick Day != Calendar Day | 10 |
| configurable day boundary | 10 |
| default 60-minute ambiguity window | 10 |
| credited/effective date | 10 |
| finalize old Rings before new generation | 10 |
| historical correction: selective recomputation of open windows + immutable finalized windows | 10 |
| Goal-level Norm reminder | 10 |
| confirmed global daily streak rule (>=1 completed Ring on evaluable day) | 10 |
| motivational/scolding rule revalidation | 10 Gate |
| ~30 local concurrent users target | 11 |
| WebSocket latency validation | 11 |
| Docker portability | 0/11 |
| backup/restore | 11 |
| AI failure isolation | 8/9/11 |
| user documentation formal | E2 |
| pricing/licensing | Business Track |
| support/SLA | Business Track |
| Enterprise multi-tenancy | E1 |
| enterprise management reporting | E2 |
| Google Calendar | E3 |
| trusted automation | E3 Gate |
| native Android/iOS evaluation | E4 |

---

# 25. Entity / Concept Coverage Matrix

| Entity / Concept | First Introduced | Completed / Expanded |
|---|---|---|
| User | 1 | E1 enterprise expansion |
| UserPreferences | 1 | 10 day boundary |
| Folder | 1 | 7 group scope |
| List | 1 | 7 group scope |
| Column | 1 | 7 group scope |
| Item | 1 | 2/3/4 |
| Schedulable | 2 | 4 |
| Task | 1 | 2/4/6/7/10 |
| Event | 2 | 4/7/10 |
| RichDescription | 2 | 6 sync expansion |
| ContentBlock | 2 | 6 sync expansion |
| Comment | 2 | 7 permission expansion |
| AuditLog | 2 | 3/6 |
| Tag | 2 | 9 AI lifecycle |
| Routine | 3 | 4/10 |
| RoutineCompletion | 3 | 4/6/10 |
| TrackingState | 3 | 9/10 |
| RecurrenceObject | 4 | 4 |
| ReminderConfig | 4 | 8 AI suggestion / E4 native |
| ShareGrant | 7 | 7 |
| AccessProfile | 7 | E1 permission expansion |
| FieldVisibilityPolicy | 7 | E1 permission expansion |
| Group | 7 | E1 |
| GroupMembership | 7 | E1 |
| SystemRole | 7 | 7 |
| TaskAssignment | 7 | 7 |
| CustomRole | — | E1 |
| AIItemCreationSession | 8 | E3 learning |
| Goal | 9 | 10 |
| GoalGenerationLog | 9 | 9 |
| DailyRing | 10 | 10 |
| RingGroup / DailyAction | 10 | 10 |
| Statistics caches/features | 10 | future analytics |
| Sync metadata | 6 | 6 |
| Agent Authority Grant/Profile | — | E5 |
| Experience Specification / validated variant | — | E6 |
| Extension State / Events / Rules | — | E7 |
| Organization/Tenant | — | E1 |

---

# 26. Design / Specification Gate Schedule

No unresolved Current-Scope Product/Domain decision remains in the current canonical review. The schedule below tracks only implementation/design/tuning work that must be completed before its owning Increment can be considered ready.

| Design / Specification Gate | Must Be Finalized By |
|---|---|
| API endpoint/contracts | per owning Increment |
| ContentBlock physical schema/order/edit representation | before Increment 2 implementation |
| structural child/dependency/reference schema and indexing | before Increment 2 implementation |
| Time Semantics baseline + golden test vectors | baseline in Increment 0; refine before Increments 2/4/10 |
| Sync field/version/order/clock/idempotency/tombstone metadata | before Increment 6 implementation; foundational compatibility reviewed in Increments 1–5 |
| History branch persistence compatible with Audit/Sync | before Increment 6 acceptance |
| exact AI Goal warm-up duration and similarity numeric thresholds | before Increment 9 production automation |
| exact Goal-selection algorithm/weights | before Increment 10 |
| scoring formula + late-day/bonus tuning | before Increment 10 |
| adaptive Norm thresholds/windows | before Increment 10 |
| RingGroup/DailyAction persistence/rule representation/replan concurrency | before Increment 10 |
| Future trusted-automation authority-level/UX design | before E3 auto-actions |
| Future built-in Agent capability matrix, risk classification, grants/revocation and confirmation UX | before E5 |
| Experience DSL/versioning, registered primitives/actions, reachability contracts, validation suite and Preview isolation | before E6 |
| Generative Experience accessibility acceptance baseline and asset provenance/trust policy | before E6 production release |
| Generated Extension state/event/rule sandbox and integrity/security model | before E7 |
| Enterprise SSO SAML/OIDC choice | before E1 |

---

# 27. Cross-Cutting Activities — Every Increment

---

## SCM / Configuration Management

- Git from first commit
- atomic changes
- requirement/issue references
- release tags
- migration versioning
- dependency pinning where appropriate
- environment config control
- no secrets in repository

---

## Requirement / Decision Management

When behavior changes:

```text
System Definition (canonical current behavior)
↓
Decision Register (rationale/constraints reconciled)
↓
Formal SRS (testable requirements)
↓
Roadmap if schedule affected
↓
Traceability
```

A new question may be analyzed in the Decision Register before this sequence, but analysis alone does not become canonical behavior until the System Definition is updated.

Do not modify code behavior and leave specification stale.

---

## Risk Management

Every Increment:

- identify
- probability
- impact
- mitigation
- contingency
- status

Important recurring risks:

- data loss
- sync conflict
- time/calendar correctness
- AI dependency
- authorization leakage
- recurrence scheduling
- historical correction semantics: selective recomputation only for open derived state; finalized windows immutable
- DailyRing finalization

---

## Security

Continuous:

- auth
- authorization
- input validation
- secrets
- privacy
- uploads
- rich content
- dependency scanning
- external AI data
- WebSocket authorization
- query isolation

Increment 11 is hardening, not the first time security is considered.

---

## SQA

- TDD
- regression after bug fix
- code/self review
- static checks
- automated CI
- acceptance evidence
- design/code consistency
- documentation consistency

---

## Technical Debt

Record:

- shortcut
- reason
- scope
- risk
- repayment trigger

Do not rely only on TODO comments.

---

## Documentation

Every Increment asks:

- Product behavior changed? → Decision Register/System Definition/SRS
- Domain understanding changed? → Domain Model
- Architecture changed? → Architecture + possible new ADR
- DB changed? → Data Design + ERD + new migration
- API changed? → OpenAPI/API
- UI changed? → UI/UX
- specialized subsystem changed? → owning spec
- release happened? → new release note
- requirement implemented? → Traceability

---

# 28. Traceability Model

Every implemented requirement should eventually trace:

```text
Canonical source
(System Definition section / DR ID)
        ↓
Formal SRS Requirement ID
        ↓
Increment
        ↓
Analysis Artifact
        ↓
Design / ADR
        ↓
Code Module
        ↓
Automated Test
        ↓
Acceptance Evidence
        ↓
Release
```

Example:

```text
DR-003 / RoutineCompletion occurrence_date
↓
SRS-ROUTINE-...
↓
Increment 3
↓
Routine completion use case
↓
DATA_DESIGN + migration
↓
routine_completion service
↓
unit + API + DB constraint test
↓
Increment 3 acceptance
↓
release
```

---

# 29. Suggested Documentation Layout

```text
/
├── README.md
├── docs/
│   ├── 00-README.md
│   ├── decision-register.md
│   ├── 01-planning/
│   ├── 02-requirements/
│   ├── 03-design/
│   │   ├── ui-ux/
│   │   └── adr/
│   ├── 04-development/
│   ├── 05-quality/
│   ├── 06-operations/
│   ├── 08-tracking/
│   └── reference/
├── src/
├── tests/
├── migrations/
└── ...
```

---

# 30. Final Increment Order

```text
Increment 0
Formal Specification + Engineering Baseline + Walking Skeleton
        ↓
Increment 1
Identity + Folder/List/Column + Basic Task MVP
        ↓
Increment 2
Complete Task/Event + Hierarchy + Description + Comments + Audit Foundation
        ↓
Increment 3
Routine + RoutineCompletion + TrackingState
        ↓
Increment 4
Recurrence + Routine Streak + Reminders + Time/Calendar Semantics
        ↓
Increment 5
Navigation + Views + Responsive UI + Themes
        ↓
Increment 6
Offline-first Sync + History + Undo
        ↓
Increment 7
Direct Sharing + Groups + Authorization + Assignment + Realtime
        ↓
Increment 8
AI-Assisted Item Creation — Voice Draft + Review
        ↓
Increment 9
Goal + AI Tags + Semantic Discovery + Goal Lifecycle
        ↓
Increment 10
Daily Rings + Dotick Day + Scoring + Norm + Statistics
        ↓
Increment 11
Personal V1 Production Readiness + Deployment
        ↓

Business Track runs in parallel

        ↓
Future E1
Enterprise Identity + Multi-tenancy + Custom Roles
        ↓
Future E2
Enterprise Admin + Reporting + Formal User Documentation
        ↓
Future E3
Google Calendar + Email/External Integrations + Trusted Automation + AI Personalization
        ↓
Future E4
Native Mobile / OS-specific Capabilities
        ↓
Future E5
Built-in AI Agent Runtime
        ↓
Future E6
Generative Experience Runtime
        ↓
Future E7
Generated Extensions / Personal Productivity Environment
```

---

# 31. Key Changes from the Previous Roadmap

This revision intentionally changes earlier planning assumptions:

1. `docs/requirements/system-definition.md`, `docs/design/domain-model.md`, `docs/decision-register.md` are now canonical.
2. Formal SRS requirement layer is below System Definition/Decision Register; non-canonical reference files remain derived and must be reconciled when stale.
3. Increment 0 no longer contains obsolete contradiction-reconciliation work.
4. Current role model is System-defined Roles; Custom Roles move to Enterprise.
5. Task hierarchy is a direct queryable relation, not a cache derived from Description.
6. Task and Event each have at most one structural parent; multi-context visibility is handled through references.
7. Description block types are capabilities; exact ContentBlock schema is a Design Gate.
8. Routine has no status.
9. RoutineCompletion uses `occurrence_date`, not `completed_at`.
10. Reset deletes current RoutineCompletion row while AuditLog preserves history.
11. Unscheduled Routine completion is valid.
12. Fixed-day missed occurrence is not repaired by extra completion.
13. ownership/creator are separate from Source provenance.
14. TrackingState is a shared capability, not assumed DB inheritance.
15. Custom Roles are removed from Personal V1.
16. AI-assisted Item Creation becomes a dedicated current-scope Increment.
17. Email/external AI creation remains Future Integration scope.
18. DailyRing count is `min(3, eligible goals)`.
19. Finalized DailyRing/RingGroup/DailyAction state is a historical snapshot; current-day plans may be replanned in a controlled way.
20. Ring credit is limited to membership in that credited day.
21. progress, completion and final performance score are separate.
22. Bonus is hidden until day finalization.
23. Dotick Day and configurable boundary are explicit roadmap scope.
24. historical correction uses selective recomputation for open derived state, while finalized statistical windows/Daily Rings remain immutable.
25. global daily streak is already confirmed: on an evaluable Dotick Day, at least one completed Daily Ring continues the streak; no completed Ring resets it, while days with no valid Ring opportunity pause it.

---

26. Future built-in Agent authority is standardized around Observe/Ask/Assist/Autonomous with Once/Session/Always grant lifetimes where applicable; the exact capability matrix remains a Future Design Gate.
27. Future Agent mutations use the same authorization/domain/History/Undo path as equivalent User operations rather than a privileged AI mutation path.
28. Future Generative Experience uses Recolor/Restyle/Transform/Reimagine transformation distance and a validated declarative Experience Specification rather than unrestricted generated executable client code.
29. Generated experiences require deterministic validation, functional simulation, release-appropriate accessibility checks, AI UX review and interactive synthetic-data Preview; cross-device activation requires explicit adaptation and Apply.
30. Generated Extension State/Events/UI/Rules is intentionally deferred beyond the initial safe Generative Experience Runtime.

---

# 32. What Must Not Happen

- Do not treat Domain Model inheritance as automatic DB table inheritance.
- Do not copy derived/reconciled SRS or field-reference wording over canonical decisions.
- Do not invent new Product behavior inside implementation. Complete the remaining Design/Specification gates at their owning Increment and return only genuinely new Product/Domain questions to the Decision Register.
- Do not store ownership inside Source.
- Do not rebuild hierarchy by parsing RichDescription.
- Do not make Routine status a shared Item field.
- Do not reintroduce `completed_at` as RoutineCompletion business identity.
- Do not treat unscheduled Routine completion as invalid.
- Do not let an extra Routine completion rewrite a missed fixed-day occurrence.
- Do not expose backend child/reference complexity as unnecessary UI complexity.
- Do not allow AI draft to create a real Item before user confirmation in current scope.
- Do not let AI outage disable manual Item management.
- Do not let current Item field edits silently rewrite finalized Daily Rings or their RingGroup/DailyAction plans.
- Do not let progress UI exceed 100.
- Do not reveal hidden performance bonus early if it changes user behavior against the product rule.
- Do not run full-history statistics recomputation for every historical edit; do not rewrite finalized statistical windows after later source edits.
- Do not bring Enterprise Custom Roles/multi-tenancy into Personal V1 prematurely.
- Do not move ordinary UI interactions into a continuous LLM request loop when a validated local Experience Runtime can execute them deterministically.
- Do not execute unrestricted AI-generated JavaScript/React/native code/CSS as a generated theme contract.
- Do not let a generated experience or Agent bypass ordinary authorization, domain validation, History/Audit, Sync, or Undo semantics.
- Do not auto-activate a device-specific generated experience on another device/form factor without explicit adaptation, validation, Preview, and Apply.
- Do not implement the E7 extension engine prematurely merely because the Future concept is known.

---

# 33. Current completion rule

The Definition of Done and release evidence policy are owned by [Engineering Process](../development/engineering-process.md#6-definition-of-done) and the applicable [Test Strategy](../quality/test-strategy.md). The historical 11-item per-increment checklist is not a current gate. Each behavior requires Product Owner approval of behavior **and** important acceptance/test scenarios before implementation; complete logic plus base UI and integration, demonstrate fresh risk-appropriate verification, then obtain **explicit owner acceptance after appropriate firsthand use**. Distinguish In Observation from Accepted/Closed; disclose unrun checks/residual risk and do not silently close critical/high-severity defects. Keep critical permission/data integrity/recovery assurance.

---

# 34. Core principle

Deliver the **smallest complete behavior**, agreed in dialogue and supported by reviewed scenarios, risk-proportionate assurance and a real integrated UI; observe and explicitly accept before closing. Release candidates R1–R7 group accepted slices rather than imposing large indivisible increments. Keep continuous engineering and improve from escaped defects/rework instead of paperwork. Review candidate scope/order with the Product Owner before implementation.
