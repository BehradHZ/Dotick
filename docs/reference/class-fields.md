# Dotick — Derived Field Reference

> **Status:** Reconciled derived reference — non-canonical  
> **Authority:** `project-docs/decision-register.md` → `project-docs/02-requirements/system-definition.md` → `project-docs/03-design/domain-model.md` → this file.
> **Purpose:** A convenient field/capability index. This file is **not** the physical PostgreSQL schema, ORM mapping, or a database-inheritance decision. Exact storage details that are still `OPEN` remain open here as well.

---

# 1. Shared Item Fields

`Item` is the conceptual root for user-created `Task`, `Event`, and `Routine` content.

```text
id: UUID
created_at: DateTime
updated_at: DateTime
is_trashed: Boolean
version: Integer
title: String
owner_user_id: UUID -> User
created_by_user_id: UUID -> User
tags: relation<Tag>
recurrence_rule: RecurrenceObject | null
reminders: ReminderConfig
```

Important rules:

- `status` is **not** an `Item` field. Task and Event define their own statuses; Routine has no status.
- Ownership is not stored in `Source`.
- `recurrence_rule` is a shared capability, but the allowed granularity differs by entity.

---

# 2. Shared Schedulable Fields

`Task` and `Event` share the conceptual `Schedulable` capability.

```text
source: Source
start_at: DateTime / all-day representation
end_at: DateTime | null
priority: Priority
description: RichDescription
```

Task exposes `start_at` with the domain name `due_at`.

## 2.1 Structural hierarchy

Hierarchy must be directly queryable and indexable; the UI/list tree must never require parsing the complete Description.

Current domain rules:

- Task: at most one structural parent.
- Event: multiple Description references are allowed.
- Event structural multi-parent support is `OPEN`; one structural parent + multiple references is the current preferred direction, not a finalized constraint.
- The exact backend relation schema for structural-child vs normal-reference semantics is `OPEN` and belongs to the relevant design stage.

Do not treat Description text as the only storage mechanism for structural hierarchy.

---

# 3. Task Fields

## 3.1 Core / inherited

Task has all Item + Schedulable fields.

## 3.2 Scheduling

```text
due_at: DateTime / all-day representation   # domain alias of Schedulable.start_at
end_at: DateTime | null
deadline_at: DateTime | null
grace_period_days: Integer >= 0
```

Rules:

- Without `end_at`, `due_at` is a single due moment.
- With `end_at`, `due_at` is the start of a duration.
- If no time component is set, the Task is all-day.
- `grace_period_days` is meaningful only when `deadline_at` exists and defaults to `0` when a deadline is set.

## 3.3 Status

```text
Todo
Overdue
Missed
Done
Won't_Do
Skipped
```

Lifecycle baseline:

```text
before due                                -> Todo
after due and before deadline, or with no deadline -> Overdue
after deadline, when grace > 0            -> Missed
after deadline, when grace = 0            -> Skipped directly
after deadline + grace                    -> Skipped
```

`Skipped` is system-controlled. The user uses `Won't_Do` to abandon a Task manually.

## 3.4 Dependencies

```text
dependencies:
  blocked_by_ids: List<UUID(Task)>
```

Dependency-cycle policy must be formalized in design/test specification before the owning increment is accepted.

## 3.5 Priority

```text
Urgent_Important
Important
Urgent
None
```

---

# 4. Event Fields

Event has all Item + Schedulable fields.

## 4.1 Scheduling

```text
start_at: DateTime / all-day representation
end_at: DateTime | null
```

## 4.2 Status

```text
Not_Arrived
Ongoing
Finished
```

## 4.3 Location

```text
location: Location | null
```

Location must be able to represent coordinates, a human-readable address, a place identifier, or a virtual meeting link.

## 4.4 Relations

- Event can have structural sub-events.
- Event can be referenced in multiple Descriptions.
- Exact structural multiplicity is `OPEN` as described in §2.1.

---

# 5. RichDescription and ContentBlock Capabilities

```text
RichDescription
- content_blocks: Ordered List<ContentBlock>
```

Every ContentBlock needs stable identity for comment/reorder/sync use cases.

Minimum conceptual fields:

```text
block_id: UUID
block_type
data
position/order metadata
```

The exact storage schema remains `OPEN`.

Supported capabilities:

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
- Item reference (Task/Event)

An ItemReferenceBlock may represent either a structural-child context or a normal reference; backend semantics must distinguish them without requiring separate complex user workflows.

---

# 6. Comment Fields

Conceptual model:

```text
id: UUID
author_user_id: UUID -> User
target_item_id: UUID
target_block_id: UUID | null
body: Text
created_at: DateTime
updated_at: DateTime
```

`target_block_id = null` means the comment belongs to the whole Task/Event. A block comment must also appear in the overall item thread.

---

# 7. Routine Fields

Routine is an Item but **not** a Schedulable and has **no status**.

```text
start_date: Date | null
end_date: Date | null
target_goal: RoutineTarget
tracking_state: TrackingState
```

Inherited Item fields include title, tags, recurrence, reminders, ownership metadata, versioning, and soft-delete state.

## 7.1 Validity window

- `start_date`: validity start; if absent, defaults to the Routine creation date.
- `end_date`: validity end; if absent, the Routine is indefinite.
- `end_date` stops future scheduled occurrences after that date; it does not by itself imply a separate archive state.

## 7.2 RoutineTarget

```text
RoutineTarget
- type: Achieve_All | Partial
```

For `Partial`:

```text
metric:
  period: Daily | Weekly | Monthly | Yearly
  fix_amount: Number
  is_incremental: Boolean
  increment_amount: Number | null
  unit: Count | Cup | Liter | Minute | Hour | Meter | Kilometer | Page | Step | Custom
```

Incremental target direction retained:

```text
current_target ≈ fix_amount + qualifying_completions * increment_amount
```

The exact definition of `qualifying_completions` and whether long inactivity resets the target are still `OPEN`. Do not silently equate it with every historical completion unless that decision is explicitly finalized.

---

# 8. TrackingState

Shared conceptual capability used by Routine and Goal:

```text
current_streak: Integer
best_streak: Integer
total_completions: Integer
ai_quote: String | null
illustration_url: String | null
```

This is a shared capability/state. Database inheritance, composition, embedding, or a shared table remain a storage-design decision.

---

# 9. RoutineCompletion Fields

`RoutineCompletion` is the source of truth for the current outcome of a Routine on a particular date.

```text
id: UUID
routine_id: UUID -> Routine
occurrence_date: Date
status: Done | Won't_Do
amount: Number | null
note: Text | null
created_at: DateTime
updated_at: DateTime
version: Integer
```

Constraint:

```text
UNIQUE(routine_id, occurrence_date)
```

Rules:

- `completed_at` is not a business field.
- No row means no outcome has been recorded for that date; it must not be interpreted as an explicit `Won't_Do`.
- Partial progress updates the same row.
- Reset deletes the current row for that Routine/date and AuditLog preserves the history.
- A completion may be recorded on an unscheduled date.

---

# 10. Source

`Source` describes provenance only.

```text
platform: Manual | Google_Calendar | Email | Notion | TickTick | Other | ...
external_account: String | null
external_id: String | null
```

Internal identity is stored separately through `owner_user_id` and `created_by_user_id`; `Source` must not be used to decide ownership.

---

# 11. ReminderConfig

Conceptual model:

```text
ReminderConfig
- reminders: List<ReminderRule>

ReminderRule
- trigger_before_minutes
- is_persistent
```

Persistent/alarm-like delivery depends on platform capabilities; the domain can represent the intent independently of OS delivery details.

---

# 12. RecurrenceObject

All recurrence calculations use one selected calendar:

```text
Jalali
Gregorian
```

## 12.1 Task/Event supported granularity

- minute interval
- hour interval
- day interval
- week recurrence
- month recurrence
- year recurrence
- advanced combined expression

## 12.2 Routine supported granularity

- day
- week
- month
- year

Routine recurrence is day-level; minute/hour/advanced combined recurrence does not apply to Routine.

## 12.3 Retained categories

```text
Constant
Dynamic / Interval
Advanced
```

Constant:

- Daily
- Weekly
- Monthly
- Yearly

Dynamic/Interval:

- every x minutes
- every x hours
- every x days
- every x weeks on selected weekdays
- every x months on selected days or `last_day`
- every x years on selected month/day

Advanced, where supported:

- combined minutes + hours + days expression

The exact final config schema is still `OPEN`.

---

# 13. Tag Fields

```text
id: UUID
title: String
source: User | AI
goal_id: UUID | null -> Goal
archive_status: Active | Archived   # primarily meaningful for AI tags
created_at: DateTime
updated_at: DateTime
```

Relations:

- Item ↔ Tag: many-to-many.
- Goal → Tag: one-to-many in the current domain model.
- User-created tags are not automatically archived.

---

# 14. Goal Fields

Goal is **not** an Item.

```text
id: UUID
created_at: DateTime
updated_at: DateTime
version: Integer
title: String
description: optional/current design
tracking_state: TrackingState
archive_status: Active | Dormant | Archived
list_id: UUID
column_id: UUID | null
tags: relation<Tag>
```

Lifecycle:

- `Active`: eligible for normal behavior.
- `Dormant`: no meaningful active tagged Item relevant to Goal progress currently exists; Goal is excluded from Daily Ring selection and its streak state is frozen, not reset.
- `Archived`: historical/superseded and not automatically reactivated.

Goal streak semantics:

```text
current_streak = consecutive Dotick Days where that Goal's DailyRing was completed
total_completions = total number of completed Goal days
```

---

# 15. GoalGenerationLog Fields

Append-only:

```text
id: UUID
goal_id: UUID -> Goal
event_type: Initial_Generation | Weekly_Review | Reactivation_Check
ai_model_used: String
changed: Boolean
previous_title: String | null
new_title: String | null
previous_description: String | null
new_description: String | null
user_rating: Integer | null
created_at: DateTime
```

`user_rating` is relevant when a real change occurred.

---

# 16. Folder / List / Column

Canonical terminology:

```text
Folder
└── List
    └── Column
```

Conceptual fields:

```text
Folder
- id
- owner/group scope
- title

List
- id
- folder_id
- title

Column
- id
- list_id
- title
- order
```

`Tab` and `Section` are legacy aliases for Column and are not separate entities.

Every List has a default Column for Items without an explicit Column. The legacy technical name is `not_sectioned`; it need not be shown in the UI.

Exact Item → List/Column storage and group ownership semantics are design decisions scheduled in the Roadmap.

---

# 17. UserPreferences / Dotick Day

```text
user_id: UUID
timezone
day_boundary_offset_minutes: Integer | null
...
```

If no explicit boundary is configured, the retained default ambiguity window is 60 minutes after midnight. Credited/effective-date storage varies by completion type and is finalized in the owning design stage.

---

# 18. DailyRing Fields

```text
id: UUID
user_id: UUID
goal_id: UUID
effective_date: Date
target_value / target_score: Number
progress_percent: Number [0..100]
is_completed: Boolean
final_score: Number | null
is_finalized: Boolean
selection_reason_metadata: JSON/Object | optional
algorithm_version: String | null
created_at: DateTime
finalized_at: DateTime | null
```

Conceptual uniqueness:

```text
UNIQUE(user_id, effective_date, goal_id)
```

Daily active-ring count:

```text
count = min(3, eligible_active_goals)
```

When at least 3 eligible active Goals exist, exactly 3 Rings are selected.

---

# 19. DailyRingItem Fields

```text
id
daily_ring_id
item_id
item_type: Task | Event | RoutineOccurrence
base_score
priority_weight
urgency_weight
timing_weight
difficulty_estimate
expected_effort
progress_contribution_rule
snapshot_payload | optional
```

Rule:

> A completion advances only a Ring whose `DailyRingItem` snapshot contains that Item for the credited day.

The exact `RoutineOccurrence` representation and scoring fields are finalized in the Gamification/Data Design stage.

---

# 20. AuditLog Fields

```text
id
actor_user_id
entity_type
entity_id
action
previous_value / diff
new_value / diff
occurred_at
source/device metadata | optional
```

AuditLog is preferably append-only and supports history, reset trace, undo support, and sync troubleshooting. It does not require full event sourcing.

---

# 21. AIItemCreationSession Fields

```text
id
user_id
source_type: Text | Voice | Email | ...
original_input
normalized_transcript | null
ai_proposal_payload
user_final_payload | null
field_level_changes | null
model_version
accepted: Boolean | null
created_at
finalized_at | null
```

The real Item is created only after user confirmation in current scope. This session preserves draft/review/evaluation data and future personalization signals.

---

# 22. Group / Role / Assignment Concepts

Current conceptual entities:

```text
Group
GroupMembership
SystemRole
TaskAssignment
```

Current scope:

- user can belong to multiple groups;
- membership has a system-defined role;
- Task can be assigned to multiple members;
- CustomRole is not current-scope.

Custom roles, richer permissions, organization hierarchy, and full multi-tenancy are future Enterprise scope.

---

# 23. Storage / Inheritance Note

The hierarchy in this reference is conceptual. It must **not** be interpreted as a requirement for Class Table Inheritance.

The following remain design decisions:

- whether `items` / `schedulables` / shared tracking state become physical tables;
- composition vs inheritance vs selective denormalization;
- exact ContentBlock storage;
- exact structural child/reference relation tables;
- per-field sync metadata;
- indexes and ORM mapping.

The physical design should optimize query simplicity, integrity, migration safety, and performance while preserving the domain rules above.
