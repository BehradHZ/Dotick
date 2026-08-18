# Dotick — Development Roadmap

> **Status:** Updated Roadmap based on the canonical project documents  
> **Process:** Incremental + Iterative + Test-Driven Development (TDD)  
> **Canonical sources used by this roadmap:**  
> `project-docs/02-requirements/system-definition.md` — current system behavior, scope and product rules
>
> `project-docs/03-design/domain-model.md` — current conceptual domain model
>
> `project-docs/decision-register.md` — confirmed, retained, open and superseded decisions
>
> `project-docs/02-requirements/srs.md` اکنون **Formal SRS Baseline v2.0** است. این سند requirementهای رسمی را نگه می‌دارد، ولی در تعارض رفتاری همچنان پایین‌تر از منابع canonical قرار دارد. `project-docs/reference/class-fields.md` یک derived reference غیرcanonical باقی می‌ماند. See DR-052.

---

# 0. Purpose of This Roadmap

این فایل مشخص می‌کند:

- پروژه با چه ترتیب Incrementهایی ساخته می‌شود.
- هر Increment دقیقاً چه Scopeی دارد.
- چه تصمیم‌هایی باید قبل از هر Increment بسته شوند.
- در هر Increment چه مراحل مهندسی نرم‌افزار تکرار می‌شوند.
- خروجی هر مرحله سند جدید است یا Update سند قبلی.
- هر Feature و Entity فعلی در کدام Increment طراحی/پیاده‌سازی می‌شود.
- کدام قابلیت‌ها در Personal V1 هستند و کدام‌ها Future/Enterprise.
- چگونه Requirement → Analysis → Design → Code → Test → Release قابل Trace باشد.

این Roadmap جایگزین Specification یا Domain Model نیست.

```text
System Definition       = سیستم چه رفتاری دارد؟
Domain Model            = مفاهیم و Entityهای سیستم چیست؟
Decision Register       = چه تصمیم‌هایی قطعی/باز/منسوخ هستند؟
Formal SRS              = Requirementهای رسمی و قابل تست
Design Specifications   = چگونه ساخته می‌شود؟
Roadmap                  = چه زمانی و با چه ترتیب ساخته می‌شود؟
```

---

# 1. Source-of-Truth and Document Authority

اگر اسناد با هم تعارض داشته باشند، این ترتیب مبناست:

```text
Confirmed Decision Register entry
        ↓
System Definition
        ↓
Domain Model
        ↓
Derived/Formal SRS / Design Documents
        ↓
Reconciled non-canonical reference documents
```

نکته:

- `project-docs/decision-register.md` تاریخچه‌ی تصمیم است؛ تصمیم قدیمی حذف نمی‌شود، بلکه در صورت تغییر `SUPERSEDED` می‌شود و تصمیم جدید ثبت می‌شود.
- `project-docs/02-requirements/system-definition.md` رفتار و Scope محصول را نگه می‌دارد.
- `project-docs/03-design/domain-model.md` مدل مفهومی است و نباید با PostgreSQL schema یکی فرض شود.
- Database inheritance/storage strategy هنوز یک Design Decision است.

---

# 2. Project Development Model

مدل پروژه:

```text
Specification / Engineering Baseline
        ↓
Increment 1
        ↓
Feedback + controlled refinement
        ↓
Increment 2
        ↓
...
        ↓
Personal V1
        ↓
Enterprise / Integration / Native evolution
```

هر Increment خودش یک mini-SDLC دارد:

```text
1. Scope & Readiness
2. Requirements Refinement
3. Analysis
4. Just-enough Design
5. Test Design
6. TDD + Implementation
7. Integration
8. Acceptance / System Validation
9. Review + Refactor
10. Documentation Update
11. Increment Release / Feedback
```

بنابراین پروژه Waterfall نیست.

Architecture، Data Design، API، UI، Security و Test Design در ابتدای پروژه فقط **baseline** می‌گیرند و در Incrementهای مربوطه refine می‌شوند.

---

# 3. Document Lifecycle Rules

## 3.1 Canonical Working Documents

این سه فایل از قبل وجود دارند و فقط در صورت تغییر واقعی فهم سیستم Update می‌شوند.

| Document | Role | Rule |
|---|---|---|
| `project-docs/02-requirements/system-definition.md` | Product/system behavior and scope | **Update only when behavior/scope changes** |
| `project-docs/03-design/domain-model.md` | Conceptual entities, relations, constraints | **Update when domain understanding changes** |
| `project-docs/decision-register.md` | Decision history and OPEN items | **Add/resolve/supersede decisions; do not silently rewrite history** |
| `project-docs/01-planning/increment-roadmap.md` | Increment plan | **Update after scope/order/decision changes** |

---

## 3.2 Formal Engineering Documents

این اسناد در زمان لازم ایجاد می‌شوند.

| Document | First Creation | Afterwards |
|---|---|---|
| `project-docs/02-requirements/srs.md` | Increment 0 formalization | **Replace/rewrite the reconciled derived reference into Formal SRS, then Update** |
| `project-docs/02-requirements/traceability-matrix.md` | Increment 0 | **Update every Increment** |
| `project-docs/01-planning/risk-log.md` | Increment 0 | **Update every Increment** |
| `project-docs/03-design/architecture.md` | Increment 0 | **Update when architecture evolves** |
| `project-docs/03-design/data-model.md` | Increment 0/1 | **Update** |
| `ERD.md` / ERD source | Increment 1 | **Update** |
| `project-docs/03-design/api-contracts.md` / `openapi.yaml` | Increment 1 | **Update Increment-by-Increment** |
| `project-docs/03-design/ui-ux/` | Increment 1 | **Update** |
| `project-docs/03-design/security-design.md` | Increment 0/1 | **Update every security-relevant Increment** |
| `project-docs/05-quality/test-strategy.md` | Increment 0 | **Update only when strategy changes** |
| `RECURRENCE_SPEC.md` | Increment 4 | **New, then Update** |
| `SYNC_AUDIT_SPEC.md` | Increment 6 | **New, then Update** |
| `AUTHORIZATION_MODEL.md` | Increment 7 | **New, then Update** |
| `AI_ITEM_CREATION_SPEC.md` | Increment 8 | **New, then Update** |
| `AI_GOAL_SPEC.md` | Increment 9 | **New, then Update** |
| `GAMIFICATION_SCORING_SPEC.md` | Increment 10 | **New, then Update** |
| `project-docs/06-operations/release-deployment.md` | Increment 0 | **Update** |
| `BUSINESS.md` | Parallel Business Track | **Update** |

---

## 3.3 New Artifact vs Update Existing Artifact

قاعده:

### Update existing document

وقتی «وضعیت فعلی سیستم» تغییر کرده:

- requirement changes
- domain model changes
- API contract changes
- architecture changes
- security design changes
- deployment reality changes

### Create a new artifact

وقتی یک رخداد تاریخی یا تصمیم مستقل ایجاد شده:

- ADR
- database migration
- release note
- Increment review
- benchmark report
- security review report
- test execution report

نمونه:

```text
DB schema changed
    → project-docs/03-design/data-model.md update
    → ERD update
    → new migration

Architectural decision made
    → project-docs/03-design/architecture.md may update
    → new ADR

Requirement behavior changed
    → Decision Register entry
    → System Definition update
    → Formal SRS update
    → Traceability update
```

---

# 4. Global Definition of Ready

یک Feature وارد Implementation نمی‌شود مگر اینکه:

- Scope آن برای Increment مشخص باشد.
- رفتار مورد انتظار در Specification روشن باشد.
- Acceptance Criteria قابل نوشتن باشد.
- OPEN Decisionهای blocking آن بسته شده باشند.
- Dependencyها مشخص باشند.
- Domain impact مشخص باشد.
- Data/API/UI impact در حد لازم بررسی شده باشد.
- Security impact بررسی شده باشد.
- تست Happy Path و مهم‌ترین Error/Edge Pathها قابل تعریف باشند.

همه‌ی OPEN Decisionهای کل پروژه لازم نیست از ابتدا بسته شوند؛ فقط Decisionی که Feature فعلی به آن وابسته است باید قبل از Implementation آن Feature resolved شود.

---

# 5. Global Definition of Done

Feature فقط وقتی Done است که:

- behavior مورد انتظار پیاده شده باشد.
- Acceptance Criteria پاس شده باشد.
- Unit tests پاس شوند.
- Integration/contract tests مرتبط پاس شوند.
- Regression tests پاس شوند.
- security checks مرتبط انجام شوند.
- migrations در صورت نیاز موجود و تست شده باشند.
- API/UI documentation در صورت تغییر Update شده باشد.
- Domain/Specification فقط در صورت تغییر واقعی Update شده باشند.
- Traceability Update شده باشد.
- CI سبز باشد.
- Code review یا Self-review انجام شده باشد.
- intentional technical debt ثبت شده باشد.

---

# 6. Repeated Stages Inside Every Increment

---

## Stage A — Increment Scope & Readiness

### Work

- انتخاب Featureهای Increment
- تعریف Increment Goal
- تعریف Out-of-Scope
- بررسی dependency
- بررسی OPEN decisions
- بررسی risks

### Documents

- `project-docs/01-planning/increment-roadmap.md` → **Update if scope/order changes**
- `project-docs/01-planning/risk-log.md` → **Update**
- `project-docs/02-requirements/traceability-matrix.md` → **Update**

### Output

`Increment Scope Baseline`

---

## Stage B — Requirements Refinement

### Work

- استخراج Requirementهای قابل تست از System Definition
- clarification فقط برای رفتارهای همان Increment
- Happy / Alternate / Error Flow
- Acceptance Criteria
- NFRهای مرتبط
- تصمیم‌گیری روی OPEN itemهای blocking

### Documents

اگر clarification فقط Formalization است:

- `project-docs/02-requirements/srs.md` → **Update**

اگر رفتار محصول واقعاً تغییر کرد:

- `project-docs/decision-register.md` → **New/updated decision entry**
- `project-docs/02-requirements/system-definition.md` → **Update**
- `project-docs/02-requirements/srs.md` → **Update**

### Output

Refined testable requirements

---

## Stage C — Analysis

### Work

بر اساس نیاز Increment:

- Use Case Specification
- Activity Diagram
- Sequence Diagram
- State Diagram
- Domain relationship refinement
- conceptual data flow

### Documents

- `project-docs/reference/analysis/...` → **New or Update**
- `project-docs/03-design/domain-model.md` → **Update only if domain understanding changes**
- `project-docs/02-requirements/traceability-matrix.md` → **Update**

### Output

Analysis sufficient for Design

---

## Stage D — Just-enough Design

### Work

- architecture impact
- module boundaries
- database design
- indexes
- API contract
- UI flow
- permission/security rules
- concurrency behavior
- external integration design

### Documents

- `project-docs/03-design/architecture.md` → **Update if needed**
- `project-docs/03-design/data-model.md` → **Update**
- ERD → **Update**
- API/OpenAPI → **Update**
- `project-docs/03-design/ui-ux/` → **Update**
- `project-docs/03-design/security-design.md` → **Update**
- relevant specialized spec → **New/Update**
- ADR → **New for significant decision**

### Output

Implementable design

---

## Stage E — Test Design

### Work

- Acceptance tests
- Unit tests
- Integration tests
- API contract tests
- failure tests
- security tests
- performance tests where applicable

### Rule

Acceptance Criteria باید قبل از کامل شدن Implementation قابل ارزیابی باشند.

### Documents

- `project-docs/05-quality/test-strategy.md` → **usually unchanged**
- test code/cases → **New/Update**
- `project-docs/02-requirements/traceability-matrix.md` → **Update**

---

## Stage F — TDD + Implementation

```text
RED
↓
GREEN
↓
REFACTOR
```

### Artifacts

- production code
- automated tests
- migration
- config
- fixtures
- schemas/contracts

---

## Stage G — Integration & Acceptance

### Work

- DB integration
- frontend/backend integration
- auth/permission integration
- external service simulation
- System/E2E workflow
- regression suite
- failure/recovery flows

---

## Stage H — Review & Refactor

Review:

- cohesion
- coupling
- duplication
- naming
- unnecessary abstraction
- query quality
- security
- performance
- architecture boundary violations
- technical debt

---

## Stage I — Documentation, Release & Feedback

### Update

- Traceability
- API
- Data Design
- Architecture
- UI/UX
- Security
- specialized spec
- Roadmap/backlog where needed

### Created in Increment 0 baseline

- `releases/vX.Y.Z.md`
- `reviews/increment-N.md`

---

# 7. Increment 0 — Formal Specification + Engineering Baseline

## Goal

تبدیل سه سند canonical فعلی به baseline مهندسی قابل اجرا، بدون Big Design Up Front.

---

## 7.1 Formal Specification Baseline

### Formalize / Replace Derived Reference — Completed

`project-docs/02-requirements/srs.md`

نسخه‌ی reconciled قبلی در Formal SRS Baseline v2.0 بازنویسی شده و فقط requirementهای قابل بیان/تست را normative می‌کند.

در این مرحله:

- Feature Priority وارد SRS نمی‌شود.
- Design proposalهای باز وارد Requirement قطعی نمی‌شوند.
- OPEN decisionها با وضعیت مشخص trace می‌شوند.
- نسخه‌ی reconciled قبلی SRS مبنای merge خودکار نیست؛ Formal SRS باید از canonical sources استخراج شود.

### Created

`project-docs/02-requirements/traceability-matrix.md`

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
- React Native / responsive mobile-first initial direction
- local-hosted server acceptable
- Docker introduced early enough for reproducibility
- external AI failure must not break core task management

### New

- `project-docs/03-design/architecture.md`
- first ADRs
- `project-docs/06-operations/release-deployment.md`
- `project-docs/03-design/security-design.md`
- `project-docs/05-quality/test-strategy.md`
- `project-docs/01-planning/risk-log.md`

---

## 7.3 Data Design Baseline

`project-docs/03-design/domain-model.md` is conceptual and must not be copied mechanically into database tables.

### Blocking Decision

**Database inheritance/storage strategy** must be chosen at least enough to support Increment 1.

Possible implementation is a Design decision; Roadmap does not prescribe Class Table Inheritance.

### Created in Increment 0 baseline

- `project-docs/03-design/data-model.md`

Physical ERD can start minimal and evolve.

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

## Open Decisions That Do NOT Need Resolution Yet

These stay in Decision Register until their owning Increment:

- Event structural multi-parent
- ContentBlock exact schema
- child/reference relation schema
- scoring formula
- difficulty/effort model
- global daily streak
- frequency-routine streak semantics
- incremental routine inactivity reset
- AI Goal warm-up
- Goal similarity thresholds
- Goal selection algorithm
- sync metadata design
- trusted automation confirmation policy

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
- OPEN decisions are assigned to future decision gates.

---

# 8. Increment 1 — Identity + Folder/List/Column + Basic Task MVP

## Goal

اولین usable vertical increment: user وارد سیستم شود و Task واقعی را در ساختار اصلی سازمان‌دهی ایجاد و مدیریت کند.

---

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

- `project-docs/03-design/api-contracts.md` or `openapi.yaml`
- initial physical ERD

### Update

- `project-docs/02-requirements/srs.md`
- `project-docs/03-design/data-model.md`
- `project-docs/03-design/architecture.md`
- `project-docs/03-design/ui-ux/`
- `project-docs/03-design/security-design.md`
- `project-docs/02-requirements/traceability-matrix.md`
- `project-docs/01-planning/risk-log.md`

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

## C. Event structural multiplicity

Must decide:

- one structural parent + multiple references
- OR true structural multi-parent

Task is already confirmed:

- max one structural parent.

---

# 9.2 Task Scheduling & Lifecycle

Fields/behavior:

- `due_at`
- optional `end_at`
- all-day representation
- `deadline_at`
- `grace_period_days`

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

`Skipped` is system-controlled.

---

## Task Dependency

- `blocked_by_ids`
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

- start_at
- end_at optional
- all-day
- location
- Not_Arrived
- Ongoing
- Finished
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

- `project-docs/02-requirements/srs.md`
- `project-docs/03-design/domain-model.md` **only if resolved design changes conceptual model**
- `project-docs/decision-register.md` for resolved OPEN decisions
- `project-docs/03-design/data-model.md`
- ERD
- API
- UI/UX
- Security
- Traceability
- Risk Register

---

## Acceptance

- Task state transitions work at boundaries.
- grace=0 skips directly at deadline.
- Event works as point/all-day/duration.
- hierarchy query never requires RichDescription parsing.
- Task structural parent count obeys constraint.
- Event multiplicity obeys newly confirmed decision.
- block comments render in block and global thread.
- references and children behave distinctly in backend while UI remains simple.

---

# 10. Increment 3 — Routine + RoutineCompletion + TrackingState

## Goal

پیاده‌سازی Routine به‌عنوان definition واحد و ثبت outcome روزانه با RoutineCompletion.

---

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

- Done
- Won't_Do

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

- update relevant state
- keep audit trail
- later trigger selective statistics recomputation

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
- have it affect statistics

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

### OPEN

Long-inactivity reset is not invented here.

Until a later confirmed decision exists, implementation must not silently introduce an automatic reset rule.

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

- `project-docs/02-requirements/srs.md`
- `project-docs/03-design/data-model.md`
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

# 11.4 Frequency Routine Decision Gate

Feature exists conceptually:

```text
N times per period
```

Before implementation, formalize:

- period completion
- carry/no carry
- streak across periods
- relationship between quota and RoutineCompletion rows

Decision Register must be updated.

---

# 11.5 ReminderConfig

Multiple reminders per Item:

- trigger-before
- persistent flag

Persistent/alarm-like delivery is platform capability; domain/API support is implemented now and OS-specific behavior may be completed in native/mobile evolution.

---

# 11.6 Time and Calendar Semantics

Must design/test:

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

---

## Error Presentation

Technical API error is translated into understandable UI message.

---

## Documents

### Update

- `project-docs/03-design/ui-ux/`
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

# 13.3 Decision Gate — Sync Metadata

Must resolve:

- per-field timestamps or alternative
- authoritative clock strategy
- clock skew
- device identity
- idempotency
- delete/update conflict
- relation conflict
- ContentBlock conflict granularity
- comment conflict
- RoutineCompletion conflict
- recurrence edit conflict
- tag relation conflict

Decision goes to `project-docs/decision-register.md`.

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

# 14. Increment 7 — Groups + System Roles + Assignment + Realtime

## Goal

اضافه کردن collaboration فعلی بدون Enterprise complexity.

---

# 14.1 Current Role Scope

Decision is already confirmed:

- current version uses **System-defined Roles**
- Custom Roles are not current scope
- Custom Roles move to Enterprise

No role contradiction remains for this Increment.

---

# 14.2 Group Domain

- Group
- GroupMembership
- SystemRole
- TaskAssignment

Rules:

- user can belong to multiple groups
- membership has a system role
- Task can be assigned to multiple members
- group data isolation

---

# 14.3 Decision Gate — Folder/List/Column Group Ownership

Before implementation resolve:

- can Folder/List/Column belong to user, group, or both?
- transfer/ownership semantics
- membership removal impact

Update Decision Register and Domain Model if needed.

---

# 14.4 Authorization

- object access
- membership access
- assignment permissions
- comment permission
- cross-group isolation
- creator vs owner behavior

---

# 14.5 Realtime

WebSocket only for:

- live update
- notifications

REST remains CRUD authority.

Must test:

- stale socket authorization
- membership removal
- reconnect
- permission change

---

# 14.6 Shared Time

Shared Task/Event uses an absolute instant baseline and displays according to member timezone.

---

## New Document

`AUTHORIZATION_MODEL.md`

---

## Documents

### Update

- SRS
- Domain Model if group ownership model is resolved
- Decision Register
- Data Design
- API
- Architecture
- Security
- Traceability
- Risk Register

### New

- authorization ADR
- WebSocket ADR if needed
- security test report
- migrations

---

# 15. Increment 8 — AI-Assisted Item Creation: Text + Voice Draft/Review

## Goal

پیاده‌سازی AI به‌عنوان پیشنهاددهنده برای ایجاد Item، نه creator خودکار.

این feature دیگر صرفاً Speech-to-Task نیست.

---

# 15.1 Supported Current Entry Points

Current scope:

- Text input
- Voice input

Voice option should be available near Item creation input where practical.

Email/external automated input remains Future Integration scope.

---

# 15.2 Pipeline

```text
Text / Voice
↓
Speech-to-Text if needed
↓
Intent + Entity Analysis
↓
AI Draft Proposal
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

- Task vs Event
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
- source_type
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

- explicit user input
- AI inferred
- user-preference inferred
- external source

Exact storage belongs in design.

---

# 15.6 Failure Isolation

AI/STT failure:

- must not break normal manual item creation
- must provide understandable fallback

---

# 15.7 Future Learning Boundary

Learning from proposal corrections is a confirmed future capability, not required for this Increment.

Current Increment must collect enough data so future learning is possible without rewriting the creation flow.

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

# 16.5 Decision Gate — Warm-up Duration

Exact warm-up duration is OPEN.

Must be decided before production implementation of initial automatic discovery.

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

# 16.8 Decision Gate — Similarity Threshold

Define:

- reactivation threshold
- merge threshold
- low-similarity behavior

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

# 17.1 Decision Gates — Must Resolve Here

Before implementation finalize:

1. exact Ring scoring formula
2. difficulty/effort representation
3. exact Goal selection algorithm
4. learning/adaptation approach for selection weights
5. adaptive Norm thresholds/windows
6. global daily streak: confirm, redesign or remove
7. motivational/scolding behavior: confirm exact product rule
8. incremental Routine inactivity reset if it should interact with daily behavior
9. day-finalization edge cases
10. RoutineOccurrence representation inside DailyRingItem

Each final product decision goes into Decision Register.

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

# 17.5 DailyRingItem Snapshot

Stores credited Item membership and scoring features for that day.

Eligible types:

- Task
- Event
- RoutineOccurrence

Important rule:

> Item only advances a Ring if it is a member of that credited day's DailyRingItem set.

Completing unrelated Item does not advance a daily Goal.

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
6. finalize global streak only if confirmed
7. generate new day's Rings

After finalization, Ring snapshot is historical.

---

# 17.13 Statistics / Selective Recalculation

Raw sources include:

- Task/Event state changes
- RoutineCompletion
- DailyRing / DailyRingItem
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
- AI data exposure/privacy
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
- historical edit correctness
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
- all blocking OPEN decisions resolved.
- intentionally deferred OPEN decisions clearly marked Future/non-blocking.
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

### Trusted Automation Decision

Confirmation policy is OPEN:

- always review?
- trusted source?
- rule-based auto-create?
- per-field thresholds?

Must be decided before automatic action.

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

- persistent/alarm-like notifications
- background scheduling
- push notification if needed
- OS permission handling
- local database integration
- platform-specific offline behavior

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
| Task due/end/all-day | 2 |
| Task deadline/grace lifecycle | 2 |
| grace=0 direct Skipped | 2 |
| Done/Won't_Do user-driven | 1/2 |
| Task dependency | 2 |
| Task/Event priority | 2 |
| Event timing/location/status | 2 |
| Event sub-event | 2 |
| Event multi-reference | 2 |
| Event structural parent multiplicity decision | 2 Gate |
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
| offline use | 6 |
| field-level LWW baseline | 6 |
| sync metadata design | 6 Gate |
| history / Undo | 6 |
| selective sync recovery | 6 |
| multi-group membership | 7 |
| System-defined Roles current version | 7 |
| Custom Roles | E1 |
| multi-assignee Task | 7 |
| group data isolation | 7 |
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
| DailyRingItem snapshot | 10 |
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
| selective statistics recomputation | 10 |
| Goal-level Norm reminder | 10 |
| global daily streak decision | 10 Gate |
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
| Group | 7 | E1 |
| GroupMembership | 7 | E1 |
| SystemRole | 7 | 7 |
| TaskAssignment | 7 | 7 |
| CustomRole | — | E1 |
| AIItemCreationSession | 8 | E3 learning |
| Goal | 9 | 10 |
| GoalGenerationLog | 9 | 9 |
| DailyRing | 10 | 10 |
| DailyRingItem | 10 | 10 |
| Statistics caches/features | 10 | future analytics |
| Sync metadata | 6 | 6 |
| Organization/Tenant | — | E1 |

---

# 26. OPEN Decision Resolution Schedule

| OPEN Decision | Must Be Resolved By |
|---|---|
| database inheritance/storage strategy | enough for Increment 1; refine incrementally |
| API endpoint design | per owning Increment |
| Event structural multi-parent | before Increment 2 implementation |
| ContentBlock exact schema | before Increment 2 implementation |
| backend child/reference schema | before Increment 2 implementation |
| dependency cycle policy | before Increment 2 acceptance |
| frequency Routine streak formalization | before Increment 4 implementation |
| incremental Routine inactivity reset | by Increment 10 if it affects daily behavior; otherwise explicitly defer |
| Folder/List/Column group ownership | before Increment 7 |
| sync field metadata design | before Increment 6 |
| AI Goal warm-up duration | before Increment 9 auto-discovery |
| Goal similarity thresholds | before Increment 9 lifecycle automation |
| exact Goal selection algorithm | before Increment 10 |
| difficulty/effort representation | before Increment 10 |
| scoring formula | before Increment 10 |
| adaptive Norm thresholds | before Increment 10 |
| global daily streak | before Increment 10 |
| motivational/scolding behavior | before Increment 10 release |
| trusted automation confirmation policy | before E3 auto-actions |
| Enterprise SSO SAML/OIDC | before E1 |

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
Decision Register
↓
System Definition
↓
Formal SRS
↓
Roadmap if schedule affected
↓
Traceability
```

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
- historical recomputation
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
DR-005 / RoutineCompletion occurrence_date
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
├── project-docs/
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
Groups + System Roles + Assignment + Realtime
        ↓
Increment 8
AI-Assisted Item Creation — Text/Voice Draft + Review
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
```

---

# 31. Key Changes from the Previous Roadmap

This revision intentionally changes earlier planning assumptions:

1. `project-docs/02-requirements/system-definition.md`, `project-docs/03-design/domain-model.md`, `project-docs/decision-register.md` are now canonical.
2. Reconciled SRS/Class Fields are derived references, not roadmap sources of truth; their stale contradictions were removed under DR-052.
3. Increment 0 no longer contains obsolete contradiction-reconciliation work.
4. Current role model is System-defined Roles; Custom Roles move to Enterprise.
5. Task hierarchy is a direct queryable relation, not a cache derived from Description.
6. Task has one structural parent; Event multi-parent remains a scoped OPEN decision for Increment 2.
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
19. DailyRing/DailyRingItem are historical snapshots.
20. Ring credit is limited to membership in that credited day.
21. progress, completion and final performance score are separate.
22. Bonus is hidden until day finalization.
23. Dotick Day and configurable boundary are explicit roadmap scope.
24. selective statistics recomputation is part of Daily/Gamification implementation.
25. global daily streak is not treated as confirmed until Increment 10 decision gate.

---

# 32. What Must Not Happen

- Do not treat Domain Model inheritance as automatic DB table inheritance.
- Do not copy derived/reconciled SRS or field-reference wording over canonical decisions.
- Do not resolve all OPEN decisions before coding; resolve them at owning Increment.
- Do not store ownership inside Source.
- Do not rebuild hierarchy by parsing RichDescription.
- Do not make Routine status a shared Item field.
- Do not reintroduce `completed_at` as RoutineCompletion business identity.
- Do not treat unscheduled Routine completion as invalid.
- Do not let an extra Routine completion rewrite a missed fixed-day occurrence.
- Do not expose backend child/reference complexity as unnecessary UI complexity.
- Do not allow AI draft to create a real Item before user confirmation in current scope.
- Do not let AI outage disable manual Item management.
- Do not let current Item field edits silently rewrite historical Daily Rings.
- Do not let progress UI exceed 100.
- Do not reveal hidden performance bonus early if it changes user behavior against the product rule.
- Do not run full-history statistics recomputation for every historical edit.
- Do not bring Enterprise Custom Roles/multi-tenancy into Personal V1 prematurely.

---

# 33. Completion Rule for Each Increment

An Increment closes when:

1. Scope is implemented.
2. Blocking decisions are resolved.
3. Acceptance Criteria pass.
4. regression suite passes.
5. relevant security checks pass.
6. Traceability is current.
7. design docs match implementation.
8. canonical docs match actual product behavior.
9. technical debt is recorded.
10. Increment review is written.
11. next Increment is re-planned using learned information.

---

# 34. Core Principle

Dotick should evolve as a sequence of usable, verified increments.

```text
Understand current scope
↓
Resolve only blocking decisions
↓
Specify enough
↓
Analyze enough
↓
Design enough
↓
Write tests
↓
Build
↓
Integrate
↓
Validate
↓
Update living documents
↓
Learn
↓
Next Increment
```

The measure of progress is not the number of documents or diagrams.

The measure of progress is that after every Increment the system is:

- more usable,
- more correct,
- more tested,
- more traceable,
- more documented,
- and still architecturally understandable.
