# Dotick — Decision Register

> **Status:** Canonical Decision Rationale Register  
> **Purpose:** This document records Dotick's product, domain, and engineering baseline decisions in a self-contained manner. Each Decision Record must be understandable without needing to read another document: it first explains the problem statement and the previous model/assumption, then states the reason it was insufficient, and finally records the current decision, its implications, and open boundaries.

## Status definitions

- `CONFIRMED`: The current decision is definitive and must be the basis for subsequent documents and implementation.
- `RETAINED`: The decision has been kept from the previous baseline, and there is no sufficient reason in the current analysis to change it.
- `OPEN`: The problem is known, but a final solution has not yet been chosen; implementation must not implicitly close it.
- Phrases such as `IN CONCEPT`, `IN PRODUCT BEHAVIOR`, or `AS FUTURE CAPABILITY` specify the scope of certainty; that is, the principle of the decision is definitive, but design/timing details may remain open.

## Reading rule

The Decision Register maintains the history of "why." Behavioral and design documents may later reference DRs to avoid duplication, but each DR itself must sufficiently explain the problem, the previous option/model, the reason for the change, and the outcome.

## Behavioral authority rule

For current product behavior and Scope, the `System Definition` is the first authority. This Register is second: it explains rationale, constraints and design handoff for behavior already reflected in the System Definition. If wording here and the System Definition diverge, the System Definition governs and this Register must be reconciled rather than treated as a competing current-state source. The Formal SRS is third and translates the same behavior into testable requirements.

## Consolidation rule

When later analysis completes or materially refines an earlier decision on the **same product/domain concept**, the current Decision Register consolidates the full reasoning and final behavior into one canonical DR instead of keeping two simultaneously readable current-state entries. The consolidated DR retains the important previous alternatives and reasons for change inside its Context/Decision sections; previous duplicate entries are removed from the current body and remain available through repository revision history. This prevents a reader or implementation agent from finding an older still-present rule and mistaking it for current behavior.

---

## DR-001 — Canonical organization terminology is Folder > List > Column

**Status:** CONFIRMED

### Context and previous model

In early versions, the structure for organizing items was described using several overlapping terms: `Folder`, `List`, `Tab`, and `Section`. In some interpretations, `Tab` and `Section` were seen as a separate layer or entity, while in other places they expressed the same concept as a column within a List. This ambiguity made it unclear how many actual organizational levels the UI, Domain Model, and storage should have.

### Why the previous model was not good enough

Having multiple names for one concept without any real behavioral difference complicated the model, made migration and API naming ambiguous, and risked the UI building several separate controls or entities for something that, from the user's perspective, is a single concept. Also, `Schedulable` is a domain content type, not an organizational level on par with Folder/List/Column.

### Decision

The canonical organizational structure is:

```text
Folder
└── List
    └── Column
```

`Tab` and `Section` are historical aliases of `Column` and are not considered independent entities. Task/Event/Routine are content that resides within a List/Column; `Schedulable` is part of the content type hierarchy and is not a fourth organizational level.

### Implications

- Naming in the UI, API, Domain Model, and new documentation must use `Folder/List/Column`.
- Each List can have a default Column for Items without an explicit Column.
- Historical aliases are tolerable only for migration/reading legacy wording and must not create new entities.

---

## DR-002 — Routine does not have a shared Item status

**Status:** CONFIRMED

### Context and previous model

The initial model tended to define `status` as a shared `Item` field so that Task, Event, and Routine would all inherit it. This assumption seemed natural for Task and Event, but Routine is a "recurring definition," and the outcome of each day is independent of the Routine definition itself.

### Why the previous model was not good enough

If Routine had a single overall status like Done/Missed, it would be unclear which occurrence or which day the status refers to. A Routine could be Done today, have no outcome tomorrow, and be Won't_Do the day after, while the Routine itself remains active and valid. Keeping status on Item also forced subtypes to build different meanings for a shared field.

### Decision

`status` is removed from `Item`'s shared fields.

- Task status has its own dedicated lifecycle.
- Event status has its own dedicated lifecycle.
- Routine **has no status**.
- The Routine's daily outcome is stored in `RoutineCompletion.status`.

### Implications

- No API/schema/design should force Routine to have an Item-level status.
- If the active/inactive state of a Routine definition is needed, it must be modeled with another appropriate concept, such as a validity window or a separate lifecycle, not by reusing the daily outcome.

---

## DR-003 — RoutineCompletion identifies the business day with occurrence_date

**Status:** CONFIRMED

### Context and previous model

In an early model, `date` and `completed_at` were merged into a single `completed_at` field to represent both the occurrence day and the time the completion was recorded. As a result, one timestamp was meant to carry two different concepts simultaneously: "which day does this outcome belong to?" and "when was it recorded/edited?"

### Why the previous model was not good enough

A Routine's business day is not necessarily the same as the recording timestamp. A user can record or correct a past day's outcome later, the Dotick Day may cross midnight, and the edit history must also remain independent of the credited day. Using the timestamp as the day's identity made historical edits and sync ambiguous.

### Decision

`RoutineCompletion` explicitly keeps the business day via `occurrence_date`:

```text
routine_id
occurrence_date
status
amount
note
created_at
updated_at
version
```

`completed_at` is removed as a business field. The creation/edit time can be retrieved from metadata and the AuditLog.

### Implications

- Day attribution is separate from the audit timestamp.
- A historical entry can be recorded today while its `occurrence_date` refers to a different day.
- If a real action timestamp is later needed for analytics, it must be added as a separate concept with a clear rationale; it must not take the place of `occurrence_date`.

---

## DR-004 — One current RoutineCompletion row exists per routine and occurrence_date

**Status:** CONFIRMED

### Context and previous model

For partial progress on a Routine, each value change could be recorded as a new row; for example, 2 glasses, then 4 glasses, then 6 glasses. This model effectively mixed the day's current outcome with event history.

### Why the previous model was not good enough

Multiple current rows for one Routine/day meant reading the current state required aggregation, complicated reset and sync, and made it unclear which row represents the day's final outcome. Change history is also better handled as the AuditLog's responsibility, not the current source-of-truth table.

### Decision

For each Routine, at most one current row exists per `occurrence_date`:

```text
UNIQUE(routine_id, occurrence_date)
```

Partial progress updates that same row.

### Implications

- `RoutineCompletion` is the source of truth for a day's current state.
- Audit/history of previous changes is recorded in the AuditLog.
- Sync must preserve this same uniqueness and handle same-day duplicates as a conflict/error.

---

## DR-005 — Reset removes the current RoutineCompletion row but preserves history

**Status:** CONFIRMED

### Context and previous model

Several semantics were possible for "reverting" a Routine's completion: changing the status to Won't_Do, keeping a row with a neutral status, or deleting the current outcome. It was also necessary for history not to be lost.

### Why the alternatives were not good enough

`Won't_Do` is an explicit user decision and is not the same as "no outcome recorded." A neutral status also created an extra state that effectively duplicated the absence of a record. Deleting without an audit trail also destroyed the change history and was unsuitable for undo/sync troubleshooting.

### Decision

Reset means:

```text
DELETE current RoutineCompletion row for (routine_id, occurrence_date)
KEEP corresponding AuditLog history
```

`Won't_Do` is not a Reset and must remain as an explicit row.

### Implications

- The absence of a row means no current outcome has been recorded.
- The UI must treat Reset and Won't_Do as two semantically different actions.
- The historical trace remains retrievable after a Reset.

---

## DR-006 — Historical RoutineCompletion edits are allowed

**Status:** CONFIRMED

### Context and previous model

One possible choice was to make past days immutable once the day ends, so that streak/statistics calculations remain simple. In contrast, real-world usage requires the user to be able to correct a forgotten completion or a wrong value from previous days.

### Why immutable history was not good enough

The user may record a completion late, may have entered a wrong value, or may correct a past day's outcome. Locking the date deliberately kept the source of truth wrong and sacrificed statistics quality for implementation simplicity.

### Decision

The user can create, edit, Reset, or correct `RoutineCompletion` for past days.

### Implications

- The AuditLog must preserve significant historical changes.
- Statistics, streaks, and affected aggregates must be corrected.
- This freedom does not mean full-history recomputation after every edit; its strategy is specified in DR-036.

---

## DR-007 — A scheduled Routine day is a presentation/suggestion rule, not an execution prohibition

**Status:** CONFIRMED

### Context and previous model

Recurrence could be interpreted as "the Routine can only be performed on allowed days." For example, if a Routine is defined for Monday/Wednesday/Friday, a Tuesday completion might be considered invalid.

### Why strict prohibition was not good enough

In real life, the user may perform an activity outside its scheduled day and want to record it. Prohibiting the recording of this fact made the history and statistics incomplete. At the same time, the schedule is still needed to show expected opportunities and fixed-day streaks.

### Decision

Recurrence determines which days a Routine is **scheduled/suggested** on, not that completion is only allowed on those same days.

The user can also record a valid completion on an unscheduled `occurrence_date`.

### Implications

- The daily UI shows scheduled Routines as the primary suggestion.
- The Routine page/calendar can record and display unscheduled completions.
- The effect of this completion on the streak follows the separate rule in DR-008.

---

## DR-008 — Extra unscheduled completion does not repair a missed fixed-day occurrence

**Status:** CONFIRMED

### Context and previous model

After allowing completion on an unscheduled day, an important question arose: if the user misses a scheduled occurrence and performs the Routine the next day, should that completion repair the missed day and preserve the previous streak?

### Why retroactive repair was not good enough

In a fixed-day routine, the schedule itself is part of the commitment. If completion on another day could replace a missed occurrence, the meaning of "Monday/Wednesday/Friday" would be weakened, and the streak would no longer reflect adherence to the scheduled opportunities.

### Decision

For fixed-day routines:

- A missed scheduled occurrence breaks the previous streak.
- An unscheduled completion is valid.
- An unscheduled completion does not retroactively repair a previous missed occurrence.
- A new completion can start or continue a new sequence/streak.

### Frequency-based boundary

`N times per period` routines use different semantics from fixed-day routines. Their current canonical streak behavior is defined in DR-095; this DR does not apply fixed-day repair/break semantics to that model.

---

## DR-009 — Recurrence capability differs by entity even if the engine is shared

**Status:** CONFIRMED

### Context and previous model

A shared Recurrence Object for Task, Event, and Routine was proposed, and there was a risk that all entities would mechanically support every granularity.

### Why uniform capability was not good enough

Task/Event may have minute- or hour-level occurrences, but in the product model Routine is a day-level activity. Adding minute/hour/advanced recurrence to Routine would both complicate the UI and unnecessarily complicate the semantics of `RoutineCompletion.occurrence_date`.

### Decision

Capability matrix:

```text
Task:    minute / hour / day / week / month / year / advanced
Event:   minute / hour / day / week / month / year / advanced
Routine: day / week / month / year
```

The engine/config abstraction can be shared, but validation must enforce each entity's capability.

### Implications

- Reuse in implementation is allowed, but domain behavior is not assumed to be identical.
- Routine occurrence remains day-level.

---

## DR-010 — Task lifecycle separates time-driven states from user-driven outcomes

**Status:** CONFIRMED

### Context and previous model

Task has several time-related concepts: `due_at`, `deadline_at`, and `grace_period_days`. Without a clear state machine, statuses such as Overdue, Missed, and Skipped could overlap or become manually selectable.

### Why an unspecified lifecycle was not good enough

If transitions are not explicit, the API, scheduler, and UI might interpret the same Task in different states. Also, `Skipped` should be the result of a time-based policy, whereas the user manually abandoning a task has a different meaning.

### Decision

Time-driven baseline path:

```text
Todo -> Overdue -> Missed -> Skipped
```

- Before due: `Todo`
- After due and before deadline, or if there is no deadline: `Overdue`
- After deadline and within the grace window: `Missed`
- After the grace boundary: `Skipped`

User-driven paths:

- `Done`
- `Won't_Do`

`Skipped` is system-controlled.

### Implications

Boundary behavior must be precisely covered in tests and the scheduler. The special case of `grace_period_days = 0` is defined in DR-011.

---

## DR-011 — grace_period_days = 0 skips directly at deadline

**Status:** CONFIRMED

### Context and previous model

In the general Task lifecycle, `Missed` represents the interval between the deadline and the end of the grace period. If grace is zero, the implementation might still create a momentary or intermediate `Missed` state.

### Why an observable zero-length Missed state was not good enough

A state without a real interval has no product value for the user and creates unnecessary race conditions/edge cases in the scheduler, notifications, and UI.

### Decision

If `grace_period_days = 0`, the Task goes directly to `Skipped` upon passing `deadline_at`, and there is no observable `Missed` state.

### Implications

- Deadline boundary tests must confirm the direct transition.
- The user still uses `Won't_Do` for manually abandoning a task.

---

## DR-012 — Internal ownership is separate from provenance/source

**Status:** CONFIRMED

### Context and previous model

In an early model, in addition to indicating where the Item came from, `source` was also used to determine the Item's internal owner; for example, a username or account was placed inside Source.

### Why the previous model was not good enough

An Item can belong to one user but be created by another user, or be imported from Google Calendar/Email. Provenance and ownership are two independent questions. Combining them made authorization, group assignment, import, and future integrations ambiguous.

### Decision

Internal Item identity keeps at least these two concepts separate:

```text
owner_user_id
created_by_user_id
```

`Source` is provenance only.

### Implications

- Authorization must not be inferred from Source.
- An Item being imported does not determine internal ownership.
- Creator and owner can differ.

---

## DR-013 — Source has a minimal provenance-oriented shape

**Status:** CONFIRMED IN CONCEPT

### Context and previous model

After separating ownership from Source, it was necessary to determine what information Source actually carries. Keeping internal user identity or scattered provider-specific fields in Source could create coupling.

### Why an overloaded Source was not good enough

Source should only answer "which external system/account/record did this Item come from?" If it also carries authorization or domain identity, integration concerns would enter the core ownership model.

### Decision

Conceptual shape of Source:

```text
platform
external_account
external_id
```

Examples of `platform`: Manual, Google_Calendar, Email, Notion, TickTick, Other.

### Implications

- `external_account` and `external_id` are nullable.
- The exact enum/storage can be refined in Integration/Data Design.
- Source never takes the place of `owner_user_id` or `created_by_user_id`.

---

## DR-014 — Structural hierarchy must be directly queryable and indexable

**Status:** CONFIRMED

### Context and previous model

In a previous model, the subtask relationship could only be represented by embedding a Task inside a RichDescription; as a result, to understand a Task's children, the system had to parse the Description or maintain a derived index from it.

### Why the previous model was not good enough

List/Kanban/tree UI must query hierarchy quickly and directly. Depending on parsing RichDescription tied data integrity and performance to presentation content, and made rename/reorder/sync fragile.

### Decision

The structural parent/child relation must exist as a direct, queryable, and indexable domain/storage relation.

A RichDescription reference is not a substitute for hierarchy.

### Implications

- Child retrieval must not require a full scan/parse of the Description.
- The relation must have cycle validation.
- The exact child/reference table/schema is still a separate design decision.

---

## DR-015 — Task and Event each have at most one structural parent; references may be multiple

**Status:** CONFIRMED

### Context and evolution

The hierarchy model originally settled Task as single-parent while leaving Event structural multiplicity unresolved. Event also needed to appear in several project or description contexts, which made true multi-parent structure seem potentially useful. Later analysis separated two different needs: **structural membership** and **reference/mention**.

True multi-parent structure would make traversal, placement, move/delete behavior, authorization inheritance and cycle validation substantially more ambiguous. The requirement to show the same Event in several contexts is already satisfied by normal references and does not require several structural parents.

### Decision

- Every `Task` has at most one structural parent.
- Every `Event` has at most one structural parent.
- Task and Event may still participate in the supported cross-type structural hierarchy.
- A Task/Event may be referenced from multiple supported Descriptions/contexts; a reference never creates another structural parent.
- Structural cycles are invalid.

### Implications

- Task and Event use one consistent single-parent structural model.
- Multi-context presentation is solved by references rather than structural multi-parenting.
- Structural relationships must remain directly queryable/indexable; exact persistence representation remains a Design decision.

---
## DR-017 — Backend child/reference semantics must not force unnecessary UI complexity

**Status:** CONFIRMED

### Context and previous model

To preserve integrity, the backend must know the difference between a structural child and a normal reference. One direct approach was for the UI to build two explicit buttons, two modals, or two workflows for "Add child" and "Add reference."

### Why exposing the distinction directly was not good enough

In many contexts, the user simply wants to add/mention an Item. Exposing the data model's details in the UI increases cognitive load and complicates the usage experience without direct value.

### Decision

Backend semantics must keep child and reference separate, but the frontend does not have to always turn this difference into two independent controls. Context and interaction can determine the relation type.

### Implications

- Both domain correctness and UI simplicity are preserved.
- The exact interaction will be defined later in UI/UX design.
- This decision does not mean removing the distinction in the backend.

---

## DR-018 — Description block list defines capabilities, not the final schema

**Status:** CONFIRMED

### Context and previous model

A list of Text, Attachment, Location, and Task/Event was written in the initial model in the form of a field/class list, and it could have been taken as the final ContentBlock schema.

### Why freezing that list as schema was not good enough

At this stage, the requirements only state which capabilities the editor should have. Storage for rich text, ordering, block identity, attachments, links, and sync still needs design. Prematurely converting the capability list into a schema would lock the design before the constraints were understood.

### Decision

The current list is only a capability requirement. The exact `ContentBlock` schema will be designed later.

### Implications

- Text/Attachment/Location/Item reference must be supported.
- Naming, serialization, and storage format are still OPEN.
- The final design must respect DR-019 and comment/sync requirements.

---

## DR-019 — ContentBlock needs stable identity

**Status:** CONFIRMED IN DESIGN DIRECTION

### Context and previous model

If Description is simply an array of identity-less or position-based blocks, a block might lose its identity when moved or edited.

### Why identity-less blocks were not good enough

Commenting on a block, reordering, offline sync, and conflict resolution need to be able to identify the same block over time. An array index is not stable for this purpose.

### Decision

Every ContentBlock must have a stable identity; the minimal concept includes items such as:

```text
block_id
block_type
data
order/position metadata
```

### Open boundary

The exact field names, persistence format, ordering strategy, and sync metadata are still OPEN.

---

## DR-020 — Tracking is a shared capability, not mandatory inheritance

**Status:** CONFIRMED

### Context and previous model

Routine and Goal both have streak, total completions, and some shared presentation fields. An early model could have assumed `Trackable` as a shared database/ORM superclass.

### Why mandatory inheritance was not good enough

Sharing several fields does not necessarily imply an "is-a" relationship. Goal is not an Item at all, and Routine is an Item. Forcing both into one inheritance tree unnecessarily tied the conceptual model and storage together.

### Decision

Tracking is seen as a shared capability/state; current name:

```text
TrackingState
```

Routine and Goal use it, but this decision does not create a requirement for table inheritance or ORM inheritance.

### Implications

- The implementation can choose composition, an embedded object, or a suitable shared relation.
- The semantics of the fields must be clear for each consumer.

---

## DR-021 — Goal is not an Item

**Status:** CONFIRMED

### Context and previous model

Because Goal is related to Task/Routine/Event and is seen alongside them in the UI, Goal might also have been considered another subtype of Item.

### Why that model was not good enough

Goal is a long-term semantic objective, not something that is directly scheduled or completed like Task/Event/Routine. Goal lifecycle, AI discovery, tags, and Daily Rings behavior are different. Placing it in the Item hierarchy would impose unrelated fields and behaviors.

### Decision

Goal is an independent entity, outside the Item hierarchy.

Routine remains an Item and also has TrackingState.

### Implications

- Goal ownership/placement/relations must be explicitly designed.
- The Item-Goal relationship is established through a semantic/tagging model, not inheritance.

---

## DR-022 — Personal V1 uses only system-defined roles

**Status:** CONFIRMED

### Context and previous model

In the initial scope, both System Roles and Custom Roles were proposed for group/collaboration. This meant Personal V1 would need a role editor, permission composition, and an enterprise-grade authorization model from the start.

### Why Custom Roles were not good enough for current scope

Custom Roles create significant complexity for personal use/small groups, and there is still no real requirement for it in the current version. Introducing them earlier than needed would enlarge authorization and the UI.

### Decision

Personal V1 has only `System-defined Roles`.

`Custom Roles` are moved to Enterprise scope.

### Implications

- The current authorization model can be smaller and more testable.
- Group System-defined Roles are distinct from direct-sharing access profiles; both resolve to allowed collaboration capabilities as defined by the later sharing/authorization decisions.
- The future Enterprise design can add CustomRole without imposing it on Personal V1.

---

## DR-023 — Number of Goals is not globally capped

**Status:** CONFIRMED

### Context and previous model

Because Daily Rings are limited, the number of a user's own Goals might also have been limited to a small fixed number such as 3 or 4.

### Why a global Goal cap was not good enough

Goal is a long-term objective, and a user can have multiple meaningful areas. The Daily Ring limitation relates to daily focus, not the total number of Goals. Merging these two would discard the user's meaningful information for the sake of daily presentation.

### Decision

The number of identified/existing Goals has no fixed limit.

The limitation is applied only to the number of active Daily Rings per day.

---

## DR-024 — Daily Ring count is min(3, eligible goals)

**Status:** CONFIRMED

### Context and previous model

In previous wording, the number of daily Rings was expressed as "3 to 4" or an ambiguous range. This made it unclear exactly how many Goals per day the UI, algorithm, and acceptance tests should select.

### Why a 3-to-4 range was not good enough

A floating range without a defined policy makes daily focus unpredictable and increases layout and scoring complexity. The product goal is a small, stable focus.

### Decision

```text
eligible goals >= 3 -> exactly 3 rings
eligible goals = 2  -> 2 rings
eligible goals = 1  -> 1 ring
eligible goals = 0  -> 0 rings
```

### Implications

- Daily Ring selection has a cap of 3.
- "At most 3" is not enough; when at least 3 eligible Goals exist, exactly 3 must be selected.

---

## DR-025 — Goal.current_streak counts consecutive completed Goal days

**Status:** CONFIRMED

### Context and previous model

A Goal's streak could have been maintained by "any related activity," even if the Goal's daily progress is very small. This interpretation was easy for creating engagement but contradicted the product philosophy about meaningful progress.

### Why activity-only streak was not good enough

If doing one small task is enough to maintain the streak, the streak measures daily presence more than actual Goal progress. This behavior could encourage the user to do the minimum just to keep the streak.

### Decision

`Goal.current_streak` equals the number of consecutive Dotick Days on which the Goal was **actually completed** that day.

Minor activity is not enough; the day's completion threshold must be met.

### Implications

- The streak connects to `DailyRing.is_completed`/the equivalent final completion.
- Detailed scoring/tuning may be refined in the Gamification design, but completion must preserve the deterministic RingGroup/DailyAction semantics defined in DR-031.

---

## DR-026 — Goal.total_completions counts all completed Goal days

**Status:** CONFIRMED

### Context and previous model

It was necessary to separate the Goal's total historical progress from the streak. Using the streak for both concepts would remove old completions from the statistical view after the streak breaks.

### Why a single streak metric was not good enough

Streak shows continuity, not the total volume of success. The user may have completed the Goal many times, but the current streak may be short.

### Decision

`Goal.total_completions` is the total number of Dotick Days on which the Goal was completed, independent of whether they are consecutive.

### Implications

`current_streak` and `total_completions` are separate metrics with separate update semantics.

---

## DR-027 — Progress, completion, and performance score are separate concepts

**Status:** CONFIRMED

### Context and previous model

A single score could represent the progress bar, the completion threshold, and the bonus performance all at once. In that case, early/importance bonus might push progress past 100 very early.

### Why one score was not good enough

The user needs to know "how much of today's required work is done" without being misled by a bonus. At the same time, the system must also record overperformance. A single number mixed these two goals together.

### Decision

Three separate concepts:

```text
progress_percent: 0..100
is_completed: Boolean
final_score: >= 0 and may exceed baseline/100
```

`progress_percent` never exceeds 100 in the UI.

### Implications

- Overachievement is recorded in `final_score`.
- The completion threshold comes from progress semantics, not from the raw bonus.

---

## DR-028 — Performance bonus is hidden until day finalization

**Status:** CONFIRMED

### Context and previous model

Early completion and importance bonus could be added to the visible score at that same moment. This created immediate reward but might make the user feel the Ring is "enough" after doing one important Item very early.

### Why immediate bonus visibility was not good enough

The purpose of the Ring is to maintain motivation for doing a meaningful amount of related work throughout the day. If a bonus fills progress early or is displayed as a prominent number, the system could encourage the user to stop early.

### Decision

During the day, the user sees the required progress; performance bonuses that could change the perception of "being enough" remain hidden until Daily Finalization.

After finalization, `final_score` and the bonus are revealed.

### Implications

- The scoring engine can accumulate the bonus, but its presentation is delayed.
- Visible progress remains separate from final performance.

---

## DR-029 — Important Items completed earlier earn higher final performance

**Status:** CONFIRMED

### Context and previous model

If completing an Item always gives the same performance score regardless of when it was done, the system makes no distinction between doing an important task on time/early versus doing the same task late.

### Why timing-neutral performance was not good enough

One of the goals of gamification is encouraging useful behavior, not merely checking off items at the end. For important tasks, doing them earlier is usually more desirable behavior and should be reflected in performance.

### Decision

Completing an important Item earlier must be able to produce a higher `final_score` than completing the same Item later.

### Open boundary

The exact bonus formula, reference time, and interaction with due/deadline/difficulty are still OPEN.

---

## DR-030 — Late-day recovery preserves motivation without inflating progress beyond 100

**Status:** CONFIRMED IN PRODUCT BEHAVIOR

### Context and previous model

If scoring in the final hours of the day fully retains the same difficulty/weight as the start of the day, a user who has fallen behind might see reaching completion as practically impossible and lose motivation to do the remaining work. On the other hand, making it too easy could make completion meaningless.

### Why either extreme was not good enough

The system must not punish the user for a late start in a way that makes continuing pointless, but it also must not treat every small late-night action as equal to full completion.

### Decision

Near the end of the Dotick Day, doing the remaining related work should bring the user realistically and somewhat more easily closer to actual completion so that recovery is possible.

`progress_percent` is still capped at 100, and overachievement goes into `final_score`.

### Open boundary

The exact recovery formula is still OPEN and must be finalized together with the final scoring formula.

---

## DR-031 — Daily Ring is a feasible daily action plan and becomes an immutable historical snapshot after finalization

**Status:** CONFIRMED

### Context and evolution

The earlier Daily Ring model treated a Ring as a flat snapshot of selected Items. That correctly prevented every Goal-tagged Item from automatically earning daily credit, but it was too rigid for large Items, partial daily work, feasibility planning and controlled same-day replanning.

A historical Ring must also remain explainable: later edits to an Item must not rewrite what the system asked the User to do or how completion was evaluated on that finalized Dotick Day.

### Decision

The canonical plan structure is:

```text
Goal
↓
Daily Ring
↓
RingGroup
↓
DailyAction
↓
Original Item
```

- A `DailyAction` represents either completion of the full Original Item or a meaningful measurable portion of it for that Dotick Day.
- Completing a partial DailyAction does not complete the Original Item unless the Item's own full requirement is actually satisfied.
- Ring progress/completion is determined by deterministic RingGroup/DailyAction rules, even when AI estimates difficulty or proposes decomposition.
- A completion contributes only through a DailyAction belonging to the relevant current Ring/effective day; a semantic Goal/Tag relation alone does not automatically create daily credit.
- The current-day plan may be replanned in a controlled way when meaningful changes occur. Goal selection is not globally rerun for every Item change, and a Ring that is already complete must not become incomplete because of later replan.
- After Dotick Day finalization, the Ring, RingGroups, DailyActions, Original-Item linkage and required evaluation metadata form an immutable historical snapshot. Ordinary later Item changes do not rewrite that finalized meaning.

### Implications

- Daily planning remains feasible for large or divisible work.
- Historical decisions remain reconstructable and auditable.
- Physical persistence/serialization of RingGroup/DailyAction and replan concurrency are Design/Specification concerns, not separate product decisions.

---
## DR-033 — Dotick Day is distinct from Calendar Day and has stable prospective boundary semantics

**Status:** CONFIRMED

### Context and evolution

Strict midnight-to-midnight attribution does not always match user intent, especially for work completed shortly after midnight. At the same time, silently attributing every early-morning action to the previous day can also be wrong. Later analysis also showed that changing timezone or day-boundary settings must not retroactively move already-established historical periods.

### Decision

- Dotick has an independent logical `Dotick Day` concept; it is not identical to Calendar Day.
- User may configure an explicit day boundary.
- Boundary changes apply prospectively from the next Dotick Day and do not redefine the current or historical Dotick Day.
- If no explicit boundary is configured, the default ambiguity window is `00:00–01:00` local time.
- A completion in that ambiguity window requires an explicit per-completion `Today` / `Yesterday` attribution; there is no hidden credited-day default.
- Each established Dotick Day refers to a stable real-time interval. Later timezone changes alter local presentation and future boundaries, not the already-fixed start/end instants of the current or historical Dotick Day.
- Scoring/completion attribution may therefore require a `credited/effective_date` independent of the raw action timestamp.

### Implications

- Calendar date, raw timestamp, Dotick Day and business dates such as `RoutineCompletion.occurrence_date` must not be conflated.
- Day-finalization and recurrence/scheduling designs must use explicit timezone and boundary semantics.
- Time semantics require dedicated analysis and comprehensive boundary/edge-case test vectors before the owning implementations are considered ready.

---
## DR-035 — Previous day finalizes before new Daily Rings are generated

**Status:** CONFIRMED

### Context and previous model

Day rollover performs several tasks: closing previous progress, computing bonus, streak, and building new Rings. Without an explicit order, it was possible for the new day's Rings to be built before the previous day's state was finalized and use incomplete data.

### Why unordered rollover was not good enough

Goal streak, recent capacity, and the new day's selection may depend on the previous day's outcome. Building the new day with a semi-finalized state creates races and inconsistency.

### Decision

The conceptual order at the boundary is:

1. the previous Dotick Day is closed;
2. progress/completion is finalized;
3. final score and bonus are computed/revealed;
4. related streaks are finalized;
5. then the new day's Daily Rings are generated.

### Implications

Finalization must be designed to be idempotent and recoverable; the scheduler's exact details come in a later design.

---

## DR-036 — Historical domain data remains editable; open derived state is selectively recomputed and finalized statistical windows remain immutable

**Status:** CONFIRMED

### Context and evolution

Historical corrections are necessary because Users may record forgotten work, correct wrong values or repair old Item state. The first correctness approach was to recompute every affected statistic, potentially through the entire history. Later analysis clarified a more important distinction: editable source/domain truth is not the same thing as a finalized historical reporting artifact.

Perpetually rewriting closed Daily Rings or completed day/week/month/year reports after every historical edit would destroy the meaning of what was finalized at that time. Conversely, freezing source Items would preserve known incorrect data.

### Decision

- User-created historical domain data remains editable subject to normal validation, authorization and History/Audit rules.
- While a derived/statistical window is still open, a relevant correction may update it.
- Recalculation is selective: only affected metrics/windows are invalidated or recomputed; full-history rebuild is not the default write-path behavior.
- Simple counters may be incremented/decremented and expensive features may refresh outside the synchronous core path when semantics permit.
- Once a day/week/month/year statistical window or Daily Ring is explicitly finalized, its stored finalized outcome is immutable. Later edits to source Items do not reopen or rewrite that closed artifact.
- A later correction remains visible in domain History/Audit even when an older finalized report intentionally stays unchanged.
- Long-lived aggregates that depend on closed periods must consume finalized period outcomes rather than silently re-deriving and changing those closed contributions.

### Implications

- Raw/domain truth, open derived state and finalized historical artifacts are separate concepts.
- Maintenance/recovery may perform broader rebuilds, but ordinary historical editing must not default to full-history recomputation.
- Statistics tests must explicitly cover both open-window correction and closed-window immutability.

---
## DR-037 — Current-Scope AI-assisted Item Creation is Voice-only and always uses reviewable validated proposals

**Status:** CONFIRMED

### Context and evolution

AI-assisted creation began as Speech-to-Task, was then generalized conceptually to a reusable proposal pipeline, and was temporarily described as accepting both typed Text and Voice in Current Scope. The finalized product intent is narrower at the user-input surface: when the User is typing, ordinary manual creation is already the direct workflow; the AI shortcut exists to transform spoken intent into structured Item proposals.

The downstream proposal architecture remains intentionally reusable so future external/text-derived sources can reuse it if they are separately promoted into scope.

### Decision

Current Scope:

```text
Voice
↓
Speech-to-Text / Normalization
↓
Intent + Entity Analysis
↓
One or More Item Proposals
↓
Review / User Edit
↓
Confirm
↓
Create Real Item(s)
```

- Voice is the only direct User input modality for Current-Scope AI-assisted creation.
- Typed User input uses normal manual Item creation and is not an AI-assisted fallback.
- Voice creation requires microphone capability/permission. If unavailable, Dotick explains the requirement and provides the appropriate permission path when possible; manual creation remains available.
- Speech-to-Text is implementation-neutral: local, platform-provided or external transcription are all valid implementations.
- One Voice input may produce one or more proposals for `Task`, `Event` and/or `Routine`.
- Each proposal is independently reviewable, editable, acceptable or rejectable.
- Before `Confirm`, no proposal is a real Item.
- AI may infer valid fields when supported by evidence, including type, title, date/time, recurrence, location, description, Folder/List/Column, reminder, priority, deadline/grace and Tag.
- This flow does not infer/propose structural parent-child relations or Task dependencies.
- Review may show field provenance such as explicit speech, AI inference or preference inference.
- User may change the Item type and fields during review.
- Final payloads must pass the same domain, authorization and validation rules as manual creation regardless of model output.
- Rejected/cancelled draft sessions do not create persistent real Items; Current-Scope session-retention behavior follows the System Definition.
- AI/STT failure is isolated to this assisted flow and must not break manual Item creation or other independent core functionality.
- Where practical, the Voice action belongs next to ordinary Item creation rather than in a separate isolated product silo.

### Implications

- Future Email/external/text-derived automation can reuse the normalized proposal pipeline only after a separate scope decision.
- Provider/model choice must not change proposal semantics or validation authority.

---
## DR-041 — Learning from AI corrections is a future capability and current sessions must preserve the signal

**Status:** CONFIRMED AS FUTURE CAPABILITY

### Context and previous model

Every AI draft could be discarded after Confirm, leaving only the final Item. In that case, the system would not know which fields the user repeatedly corrected.

### Why discarding proposal/final differences was not good enough

User corrections are a valuable signal for future personalization; for example, the user might always change the reminder for a dinner event from 1 day to 3 days. Without preserving the diff, this pattern cannot be learned.

### Decision

A future system must be able to compare `ai_proposal` with `user_final_payload` and learn user preferences. Current architecture/session data must preserve this possibility.

### Implications

- `AIItemCreationSession` must retain the proposal, final payload, and field-level changes to the extent necessary.
- The learning engine itself is not current scope.
- The privacy/control of this learning must be explicit in the future design.

---

## DR-042 — Email and other external sources are future inputs to the same creation/automation model

**Status:** CONFIRMED

### Context and previous model

AI creation initially came only from the internal UI. The product vision includes converting email/calendar/external events into Task/Event as well.

### Why designing external creation as unrelated features was not good enough

If each integration builds its own dedicated pipeline, validation, provenance, review, and mapping get duplicated. The shared abstraction from DR-037 can better normalize inputs.

### Decision

In the future, Email and other sources can be creation/automation inputs and connect to the shared normalized pipeline.

### Implications

- Source provenance is essential for external inputs.
- Trusted future auto-actions require explicitly scoped, tiered, revocable authority as defined in DR-091; exact trust levels and UX remain Future Design details rather than an OPEN Current-Scope product question.
- This capability is future and must not be a mandatory dependency of the Personal V1 core.

---

## DR-043 — Daily Goal selection optimizes for a balanced day, not just the highest backlog score

**Status:** CONFIRMED IN INTENT

### Context and previous model

A simple algorithm could select the three Goals with the highest urgency/backlog/score. This approach might give all focus every day to one type of work, such as urgent tasks.

### Why pure top-score selection was not good enough

The product wants to keep neglected areas and long-term growth alive alongside current work. Pure backlog/urgency can always exclude low-pressure but important Goals.

### Decision

The day's three Goals must form a balanced composition. Example quality target:

- current/important work
- neglected area
- growth/learning

These three are not hard-coded enums or buckets; they are the desired outcome of selection.

### Implications

The final algorithm must weigh balance/diversity alongside urgency and capacity. The exact method is still OPEN.

---

## DR-044 — Goal selection considers multiple behavioral and workload signals

**Status:** RETAINED + EXTENDED

### Context and previous model

The initial selection model focused mostly on priority/timing. As the behavioral system's goal became clearer, more signals were needed to prevent one-dimensional selection.

### Why priority-only selection was not good enough

A high priority does not necessarily indicate the user has capacity today to do it, that an area has been neglected for a long time, or account for weekday/holiday patterns being different. Also, difficulty and streak momentum can affect appropriate selection.

### Decision

The known inputs to selection include at least the following:

- due/timing
- priority
- neglect
- weekday behavior
- holiday context
- streak momentum
- workload
- difficulty/effort
- recent user capacity

### Open boundary

Weights, normalization, learning strategy, and the exact formula are still OPEN.

---

## DR-045 — Goal and Tag remain independent entities with explicit lifecycle

**Status:** RETAINED

### Context and previous model

The current semantic model treats Goal as an independent entity and Tag as an independent entity. Goal lifecycle includes `Active / Dormant / Archived`, and AI tags can be merged/archived in later reviews.

### Alternatives considered

Goal could have been treated as merely a string/tag, or Tag could have been kept as an embedded Item field. This would simplify the model but would weaken identity, lifecycle, AI change history, and many-to-many relations.

### Decision

The baseline is retained:

- Goal is an independent entity.
- Tag is an independent entity.
- Item ↔ Tag is many-to-many.
- Goal lifecycle: Active / Dormant / Archived.
- User-created tags are not automatically archived.
- AI tags can be merged/archived through semantic review.

### Implications

The exact Goal-Tag/storage details can be refined in Data Design without changing this semantics.

---

## DR-046 — GoalGenerationLog is append-only history for AI-driven Goal changes

**Status:** RETAINED

### Context and previous model

AI can initially create a Goal, re-evaluate it, or change its title/description. Without history, it is difficult to explain which model made which change and how the user evaluated it.

### Why overwrite-only Goal updates were not good enough

AI behavior must be auditable/evaluable. Overwriting title/description without keeping the previous value destroys debugging and model comparison.

### Decision

An append-only `GoalGenerationLog` history is kept for AI generation/review/reactivation, recording the model/version and the previous/new values on an actual change.

### Implications

- The log does not replace the current Goal state.
- User rating is only relevant when a meaningful change has occurred.

---

## DR-047 — Offline-first uses editable local replicas with ordered field-level reconciliation, server authorization and non-authoritative device clocks

**Status:** CONFIRMED

### Context and evolution

Offline-first in Dotick is a product behavior, not a read-only cache. The system therefore needs both a locally executable working state and deterministic convergence when several devices edit the same Account. Record-level replacement is too destructive for independent field changes, while naïve comparison of raw device wall-clock timestamps is unsafe because clocks may be wrong or manipulated.

Delete/edit conflicts also cannot be reduced to an unconditional "delete wins" rule; the operation order matters. Collaboration changes add another authority boundary because access may have been revoked while a device was offline.

### Decision

- Supported offline core flows execute against a local editable replica without waiting for network availability when required state is available locally.
- Supported offline changes remain pending locally and reconcile with the server after reconnect; the converged result propagates to the User's other devices.
- Independent field changes merge where possible. Same-field conflict baseline is field-level Last-Write-Wins using **trusted/robust ordering metadata**, not raw local wall-clock alone.
- Local device wall-clock may be recorded as context but is not authoritative for conflict resolution, authorization acceptance or historical integrity.
- Ordered operation semantics apply to delete/edit conflicts: a valid later edit after a delete can semantically restore the Resource and apply the edit; a later delete leaves it deleted.
- Current server authorization is authoritative for shared-resource operations. A locally queued operation is rejected if the actor no longer has valid permission when reconciliation occurs.
- Failed/rejected sync must not silently discard the local change; History/recovery must explain the resulting state.
- Sharing, invitation, membership administration and other operations requiring current remote authority remain online/server-authoritative.
- Audit/History, sync-operation metadata and user-visible branching history must share stable entity/version identities and compatible ordering semantics; they must not become independent contradictory sources of truth.

### Design boundary

Exact device identity, per-field metadata, logical/server/hybrid clock strategy, idempotency keys, relation/block conflict granularity, tombstone representation and transport protocol belong to Sync Design. Early entity/schema work must preserve the stable IDs/version/delete semantics needed by this later reconciliation model.

---
## DR-048 — Current authentication uses email/password, Google OAuth, JWT sessions and optional Passkey with recommended independent fallback

**Status:** CONFIRMED

### Context and evolution

Dotick needs independent product authentication even when an external identity provider is unavailable. The Current Scope also needs a low-friction Google sign-in path without requiring every Google-created Account to enroll another credential before first use.

### Decision

Current Scope supports:

- Email/password with secure hashing and required email verification;
- Google OAuth as the **only Current-Scope external identity provider**;
- JWT-based session/token handling;
- optional Passkey as an independent Dotick authentication method.

A User who signs in with Google is not required to configure email/password or Passkey before using the Account. Dotick must nevertheless make an independent fallback method available and should recommend adding one to reduce dependence on Google availability.

If Google is unavailable, email/password remains an independent product authentication method. A Google-only Account with no independent fallback may be unable to perform a new login during the outage; this does not invalidate an already-valid offline session or existing local data.

### Implications

- Additional external identity providers are not Current-Scope requirements.
- Exact account-linking, token/session hardening and credential-recovery mechanics belong to Authentication/Security Design.
- Enterprise SSO remains Future Scope.

---
## DR-049 — Global daily streak continues when at least one Daily Ring is completed on an evaluable Dotick Day

**Status:** CONFIRMED

### Context and evolution

The global streak was reconsidered because requiring only one completed Ring might seem easier than Goal-specific streak behavior. The final product model intentionally gives the two streak types different meanings: Goal streak measures consecutive completion of that particular Goal, while Global Streak measures maintaining at least one meaningful daily success.

### Decision

For each **evaluable** Dotick Day:

```text
at least one Daily Ring completed -> global streak + 1
no Daily Ring completed           -> global streak = 0
```

Completing all Daily Rings is not required.

If no Ring can validly be evaluated because there are no eligible Goals, or because a required system/AI dependency prevented generation and the User had no real completion opportunity, the Global Streak is paused: it neither increments nor resets.

### Implications

- Global Streak is finalized with Dotick Day finalization.
- Goal-level streak semantics remain independent.
- Tests must distinguish User failure on a valid Ring day from days where no valid Ring opportunity existed.

---
## DR-050 — Documents are reconciled under a System-Definition-first behavioral authority model

**Status:** CONFIRMED

### Context and previous model

Earlier documentation governance placed confirmed Decision Register entries above the System Definition and also preserved some derived files unchanged for historical reasons. That created two practical risks: an older decision record could be mistaken for current behavior, and a stale SRS/reference file could continue to contradict the actual product definition.

### Decision

Current product behavior and Scope use this authority order:

```text
System Definition
        ↓
Decision Register
        ↓
Formal SRS
        ↓
Domain Model / Design
        ↓
Roadmap / reconciled references
```

Rules:

- `System Definition` is the first current-state behavioral authority.
- `Decision Register` records the reasoning, constraints and clarification behind that behavior and must be reconciled when the System Definition changes.
- `Formal SRS` formalizes testable requirements and must not invent behavior absent from the higher sources.
- Domain/Design artifacts decide implementation/model details only within the behavioral constraints above.
- Roadmap owns implementation order/gates, not product meaning.
- Derived/reference documents may and should be reconciled when stale wording would otherwise remain active.
- When later analysis completes an earlier same-concept decision, the current Register consolidates the reasoning into one canonical DR; repository revision history preserves the previous text.

### Implications

Documentation history is preserved without forcing contradictory historical wording to remain in the current body. A behavior change is not considered fully canonical merely because a rationale record exists; it must be represented in the System Definition.

---
## DR-051 — Increment 0 technology and architecture baseline uses a modular monolith with explicit boundaries

**Status:** CONFIRMED

### Context and alternatives

Dotick must be both fast and manageable for Personal V1 and have enough architectural boundaries for later growth. Two extremes were unsuitable:

1. a monolith without boundaries that mixes domain/infrastructure together;
2. early microservices or infra-heavy architecture that creates excessive operational complexity for a personal product at the start of development.

The frontend must also be mobile-first and web-capable, the backend API must remain independent, and persistence must be relational.

### Why the rejected directions were not good enough

A monolith without boundaries reduces maintainability and testability. Early microservices unnecessarily complicate deployment, networking, tracing, data consistency, and local development. Also, adding Redis/queue/AI infrastructure before the Increment that owns them creates unnecessary dependencies and failure modes.

### Decision

Personal V1 baseline:

- Backend: **modular monolith** with domain/application/interface/infrastructure boundaries;
- Python 3.14 + Django 5.2 LTS + Django REST Framework;
- Dependency management: `uv` + lockfile;
- Frontend: TypeScript application based on Expo SDK 57, React Native, and React Native for Web;
- Node.js 24 LTS + npm workspace baseline;
- Persistence: PostgreSQL;
- HTTP/JSON/REST is the authoritative path for command/query;
- WebSocket only for lightweight notification/invalidation;
- Dependencies are locked in the scaffold, and supported versions are chosen;
- Redis, worker queue, Channels, and AI services are not mandatory until the Increment that owns them.

### Implications

- The architecture can have clear boundaries within one deployable backend.
- Infrastructure is added only when a real requirement arises.
- Significant future evolution must have a new ADR/decision, not an implicit change to the baseline.

---

## DR-052 — Item persistence uses explicit composition instead of ORM/class inheritance

**Status:** CONFIRMED

### Context and previous model

The Domain Model uses the conceptual hierarchy `Item -> Schedulable -> Task/Event` and `Item -> Routine`. One direct interpretation could map this hierarchy to Class Table Inheritance or ORM model inheritance. The opposite option was fully denormalizing each subtype and duplicating all common fields.

### Why both mechanical mappings were not good enough

Class inheritance in persistence can create implicit joins, ORM coupling, and migration complexity, turning Domain inheritance into a storage decision. Full denormalization also makes shared identity, cross-item queries, and consistency of shared fields difficult.

### Decision

For Personal V1, explicit composition is used:

- The base `items` table only holds identity, ownership, and truly shared metadata.
- Each subtype has its own explicit one-to-one table.
- Example: `tasks.item_id` is both PK and FK to `items.id`.
- The implementation does not rely on ORM/model inheritance.
- Relations and transaction boundaries are explicit.
- Capabilities such as Source, recurrence, reminder, and tracking are added as a component/relation only in the Increment that needs them.
- Denormalization is not the default and is only allowed after measurement, with a separate migration/ADR.

### Implications

This model preserves shared Item querying and subtype integrity, without mechanically turning conceptual inheritance into database inheritance.

---

## DR-053 — Feature implementation priority is owned by the Roadmap, not by the SRS

**Status:** CONFIRMED

### Context and previous model

In early versions of the requirements, features could have a build priority such as High/Medium/Low inside the SRS. At the same time, the Roadmap/Increment plan also determined the actual build order.

### Why keeping Feature Priority in both places was not good enough

Build priority is a relatively variable planning property, not product behavior. Keeping it in the SRS caused duplication and drift: the requirement might stay the same while the implementation order changes due to dependency, risk, or learning. This concept was also confused with the `Priority` field of Task/Event itself.

### Decision

Feature implementation priority is removed from the SRS/behavioral specification, and the Roadmap/Increment plan owns the build order.

`Priority` is retained as a domain field of Task/Event, and this decision has nothing to do with it.

### Implications

- The SRS states what the system must do, not which feature is built first.
- Changing the order of Increments does not require changing behavioral requirements unless the actual scope changes.

---


## DR-054 — Personal sharing is resource-based and does not require Group membership

**Status:** CONFIRMED

### Context and previous model

The existing collaboration model was centered on `Group`, `GroupMembership`, `SystemRole`, and `TaskAssignment`. This model is suitable for persistent team collaboration, but it implicitly treats Group membership as the main path for sharing data between users. That assumption does not fit common personal scenarios in which a user wants to expose only one Routine, Task, Event, List, or Folder to another person without creating a shared workspace or team relationship.

Examples include sharing a Routine's completion state with a coach, sharing an entertainment List with a friend for comments, or exposing a single Task/Event to another user for review.

### Why a Group-only sharing model was not good enough

Requiring a Group for every collaboration case adds unnecessary concepts and lifecycle to simple person-to-person sharing. It also conflates two different needs:

1. granting limited access to a specific resource; and
2. maintaining a persistent collaborative context with membership and roles.

This would make simple personal sharing feel like team administration and would force Group semantics into use cases that do not need them.

### Decision

A Dotick user is personal by default and retains normal access to personal capabilities.

Sharing is a resource-level capability independent of Group membership. A user may grant another user access to a specific shareable resource without creating or joining a Group.

Current shareable resource scopes are conceptually:

```text
Folder
List
Item
├── Task
├── Event
└── Routine
```

A `Group` remains a persistent collaboration context for cases where multiple users work together over time with membership, predefined roles, shared resources, assignment, and collaborative workflow.

Conceptually:

```text
Personal ownership
        +
Resource access grants
        +
Optional persistent Group membership
```

Group membership is therefore not a prerequisite for ordinary direct sharing.

### Implications

- Direct sharing and Group collaboration are separate product concepts.
- Sharing a resource does not by itself transfer ownership of that resource.
- Access can be revoked independently of Group membership.
- A Group can be granted access to shared resources as a collaboration context without making Group the universal sharing primitive.
- Organization hierarchy and Custom Roles remain Future Enterprise concerns.
- The exact persistence schema for access grants is a Design decision and is not fixed by this DR.

---

## DR-055 — Shared Item visibility is configurable through product-level field groups

**Status:** CONFIRMED

### Context and previous model

A user may want to share an Item while keeping some of its information private. For example, a Routine may expose today's completion and recorded amount to a coach while hiding personal notes; a Task may expose status and schedule while withholding parts of its Description.

One option was to define sharing directly against database or ORM fields.

### Why database-field sharing was not good enough

Physical fields contain implementation metadata and may change during schema evolution. Exposing concepts such as `version`, internal identifiers, sync timestamps, provenance metadata, or storage-specific columns in the sharing model would leak implementation details into product behavior and make permissions fragile across migrations.

### Decision

Field-level visibility is supported at the product/domain level through **shareable field groups** or equivalent user-facing capability groups, not through arbitrary physical database-column selection.

Examples of shareable groups may include, depending on the Item type:

```text
Basic information
Schedule
Progress / status
Description
Location
Attachments
Tags
Completion history
Recorded amount
Streak / statistics
Notes
```

The owner chooses which applicable groups are visible when sharing an Item.

Internal metadata, authorization data, sync metadata, audit metadata, and implementation-only fields are never made shareable merely because they exist in storage.

### Implications

- The exact field-group catalog can differ by Task, Event, and Routine.
- The UI works with meaningful product concepts rather than database columns.
- Schema refactoring must not silently change what another user is allowed to see.
- Authorization must enforce visibility consistently across normal views, comments, notifications, realtime updates, export, and other access paths.
- The exact storage representation of the visibility policy is deferred to Authorization/Data Design.

---

## DR-056 — Authorization is capability-based; roles and access profiles are predefined permission presets

**Status:** CONFIRMED IN PRODUCT/DESIGN DIRECTION

### Context and previous model

The collaboration model already requires System-defined Roles for Groups. Direct sharing also needs simple access levels such as viewing, commenting, editing, moving, assigning, or managing shared content. Implementing authorization as scattered checks against role names would tightly couple behavior to specific labels and make future Enterprise expansion difficult.

### Why role-name-driven authorization was not good enough

A role name does not itself describe what operation is allowed. If business logic depends on checks such as `role == manager`, adding or changing roles later requires widespread conditional logic and increases the risk of inconsistent authorization. Direct sharing also does not necessarily involve Group membership, so Group roles cannot represent every access case.

### Decision

Authorization is expressed conceptually through capabilities/permissions. System-defined roles and direct-sharing access profiles are predefined bundles of those capabilities.

Representative capabilities include:

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

Personal V1 does not provide a custom permission/role editor.

For ordinary sharing, the product may expose a small predefined set of access profiles such as:

```text
Viewer
Commenter
Contributor
Manager
```

Group membership continues to use System-defined Roles. The exact mapping between role/profile labels and individual capabilities is defined in the Authorization Model and may evolve without changing the principle that authorization is capability-based.

A lightweight `Nudge`/encouragement interaction is a distinct permission-controlled collaboration capability and does not have to be modeled as a Comment.

### Implications

- Group roles and direct-sharing profiles are distinct concepts even when some capabilities overlap.
- Custom Roles and arbitrary permission composition remain Enterprise scope.
- Realtime updates and notifications must not bypass the same authorization rules.
- Revoking a grant or losing membership removes the capabilities derived from that access path.
- The exact permission matrix and storage model belong to the Authorization Design.

---

## DR-057 — Container sharing can inherit to descendants, and assignment is separate from authorization

**Status:** CONFIRMED

### Context and previous model

Sharing every Item independently becomes impractical for collaborative Lists or Folders. At the same time, Task assignment can be mistaken for authorization: if a Task is assigned to someone, the system might implicitly assume that the assignee is allowed to access it.

### Why per-Item-only sharing and implicit assignment access were not good enough

A shared project List may contain many Tasks, and an entertainment Folder may contain multiple Lists and Items. Creating and maintaining a separate access grant for every descendant would be noisy and error-prone.

Assignment answers a different business question from authorization. Assignment expresses responsibility for work; authorization expresses whether an actor is allowed to see or modify the resource. Combining them makes permission changes difficult to reason about and can accidentally expose private data.

### Decision

Access granted to a shareable container may be inherited by its contained resources:

```text
Folder access
    -> contained Lists
        -> contained Items

List access
    -> contained Items
```

For Personal V1, inherited access is intentionally simple. Fine-grained explicit-deny exceptions for individual descendants of an otherwise shared container are not required. Content that must remain private should remain outside that shared container or be shared separately under an appropriate policy.

Task assignment remains independent from authorization:

```text
Authorization = may this actor access/operate on the Task?
Assignment    = who is responsible for the Task?
```

Assigning or claiming a Task does not replace the requirement for valid access.

### Implications

- Shared project Lists can support Kanban-style collaboration without one grant per Task.
- A Group can collaborate on a shared List while Task responsibility is represented separately through assignment.
- An implementation must resolve effective access from direct and inherited grants consistently.
- The exact inheritance-resolution algorithm, caching strategy, and persistence schema are Design concerns.
- More complex deny/override hierarchies may be reconsidered for Enterprise scope if a concrete requirement appears.

---

## DR-058 — System Definition is the primary canonical current-state layer for product behavior and scope

**Status:** CONFIRMED

### Context

Product behavior, decision rationale, testable requirements, conceptual models and implementation planning exist in different artifacts. They need distinct responsibilities so implementation or planning details cannot silently redefine the product.

### Decision

The `System Definition` is the **first and primary current-state document** for:

- what Dotick is;
- Current Scope and Future Scope;
- user/stakeholder concepts;
- system boundaries;
- high-level product/domain behavior;
- cross-cutting business rules and product constraints.

The Decision Register is subordinate to that current-state behavior and records why the behavior exists, alternatives considered, important constraints and design handoffs. The Formal SRS is derived from those two sources and expresses testable requirements.

At System Definition abstraction level, core concepts, Scope and expected behavior must be unambiguous. Physical storage/schema, exact API representation, implementation algorithm, coefficient and other engineering mechanics may be delegated to owning Design/Specification artifacts when they do not change behavior.

A potential behavior change may be analyzed in the Decision Register, but it becomes canonical current behavior only after the System Definition is updated consistently. Planning order, CI/CD and implementation workflow belong to the Roadmap/engineering artifacts and cannot redefine product behavior.

### Implications

- Product behavior can be reimplemented with different technology without changing this definition.
- A pure implementation change does not require a System Definition change.
- A real behavior/scope change requires System Definition update, then Decision Register/SRS reconciliation.
- Roadmap and Design must defer to the System Definition rather than use implementation convenience to resolve ambiguity.

---
## DR-059 — Current scope is personal use and non-organizational collaboration; Enterprise is defined by organizational governance, not group size

**Status:** CONFIRMED

### Context and previous model

Dotick is intended first for real personal use and collaboration with other people, while retaining a future path toward an organizational product. The phrase "small group" could be interpreted numerically, by relationship type, or by whether members happen to work for the same company. Another interpretation reduced the Enterprise boundary to the mere presence of an organizational hierarchy.

The current collaboration model already supports Direct Sharing, Group membership, predefined access profiles, System-defined Roles, assignment, and resource-level authorization. Future Enterprise concepts include Custom Roles, richer permission composition, organization hierarchy, manager/subordinate visibility, multi-tenancy, and organization-level administration/reporting.

### Why a numeric or hierarchy-only boundary was not good enough

A fixed member count is arbitrary: a larger informal group may still need only the simple current collaboration model, while a small corporate team may already require formal organizational governance.

Using hierarchy as the only Enterprise criterion is also incomplete. A system can require Enterprise-grade behavior because of Custom Roles, tenant isolation, organization-level administration, or formal visibility policies even when the hierarchy itself is shallow.

### Decision

Current Scope covers:

- personal use;
- Direct Resource Sharing;
- non-organizational Group collaboration;
- predefined Access Profiles;
- System-defined Group Roles;
- the current resource-level authorization model.

There is no fixed product-level member-count threshold that automatically turns a Group into an Enterprise context.

A capability belongs to Future Enterprise Scope when its required behavior depends on formal organizational governance, including one or more of:

- formal `Organization/Tenant` context or tenant isolation;
- organization hierarchy;
- Custom Roles or arbitrary permission composition;
- manager/subordinate visibility;
- organization-dependent team/department policy;
- enterprise administration/reporting or comparable organization-level controls.

The current Product Owner and primary target user is the founder-user whose real personal and non-organizational collaboration needs define the initial product baseline.

### Implications

- Being a company team does not by itself make a Group Enterprise; the required governance model is the deciding factor.
- Personal V1 must not preemptively implement Enterprise authorization complexity.
- Enterprise evolution must extend the simple current collaboration model rather than redefine ordinary personal accounts as organization-only accounts.

---

## DR-060 — Dotick uses one registered personal account model across collaboration contexts and does not support anonymous or guest use

**Status:** CONFIRMED

### Context and previous model

Collaboration can be modeled either by creating separate account types such as Personal User, Collaborator, Group User, or Administrator, or by keeping one user identity and deriving the user's effective role from the resource/group context.

The System Definition also requires personal capabilities to remain available when a user participates in collaboration.

### Why multiple collaboration account types were not good enough

A person can simultaneously own personal resources, have view-only access to another resource, comment on a third resource, and be a manager in one Group. Turning each situation into a different account type would make identity, session handling, permissions, and UI state unnecessarily complex.

Treating a collaboration Manager as a global administrator would also conflate two different scopes. Resource- and Group-level management authority must remain derived from the relevant Direct Share or Group context, while administration of the Dotick platform itself may require a separate system-wide privileged actor.

Anonymous/guest use would introduce another identity lifecycle and would make revocation, comments, history, assignment, and membership harder to reason about in the current model.

### Decision

Every normal human user in Current Scope uses one base `Registered Personal User` account.

`Direct Collaborator`, `Group Member`, and a user with collaboration-management permissions are **contexts of the same registered account**, not separate account types.

A user's personal capabilities remain available when the same user joins Groups or receives Direct Sharing access.

Current Scope does not support anonymous or guest application use. A valid registered/authenticated account is required before an invitation can become real access or Group membership.

Management authority obtained through Direct Sharing or GroupMembership is scope-dependent and does not turn a normal user into a global administrator.

A separate `Platform Administrator` / `System Administrator` actor exists with unrestricted system-wide administrative authority over the Dotick platform. This actor is distinct from collaboration roles such as Group Manager; its authority is not derived from a Resource Share, Access Profile, or GroupMembership. When acting in the platform-administration context, it may access or modify any Account, Resource, system state, configuration, or other Dotick-managed data and may perform any administrative or corrective operation required by the platform. Ordinary collaboration permissions do not constrain this platform-level authority.

### Implications

- One normal user can hold different effective permissions in different resources and Groups at the same time.
- End-user collaboration authorization is resolved from context and access paths, not from a global collaboration account type.
- Platform/System Administrator is a separate privileged system actor with unrestricted platform-wide authority and must not be conflated with Group Manager or Direct-Sharing Manager.
- Comments, assignment, history, and membership always resolve to a stable registered user identity.

---

## DR-061 — Collaboration discovery uses verified identity/contact identifiers; discovery never creates access or membership

**Status:** CONFIRMED

### Context and evolution

Dotick originally centered in-product discovery on username/handle and public identity fields, while email/phone were considered only delivery channels. Current product behavior allows email and phone to identify an intended collaboration recipient as well, but only with privacy-safe matching and verified ownership.

### Decision

Every registered User has a unique `username/handle`; display/name fields may also support ordinary collaboration search.

In Direct Sharing and Group invitation discovery, a destination may be found through:

- username/handle;
- supported name/display-name search;
- verified email address;
- verified phone number.

Email/phone rules:

- adding an email or phone to an Account requires successful ownership verification using a code delivered to that same destination;
- an unverified candidate value is not an active Account contact and cannot participate in contact-dependent discovery/invitation flows;
- email/phone discovery uses exact or normalized-exact lookup rather than broad partial search;
- a successful match may identify the Dotick Account needed for the collaboration flow but must not reveal the target User's private email/phone merely because the match occurred.

Discovery itself never creates a Share grant, effective access or `GroupMembership`. Collaboration becomes active only through the applicable authenticated invitation/acceptance flow.

### Design boundary

Normalization details, ranking for public identity search, verification-code format/expiry/retry, rate limiting, anti-enumeration/abuse controls and result presentation belong to Authentication/Collaboration/Security Design.

---
## DR-062 — Group creation and membership lifecycle are consent-based in Current Scope

**Status:** CONFIRMED

### Context and previous model

A Group is a persistent collaboration context. Its lifecycle requires explicit rules for who can create a Group, how membership begins, and how membership ends.

Without a defined consent rule, a manager could potentially add another registered user into a Group unilaterally. Conversely, requiring manager approval for every member exit in ordinary personal collaboration would make informal groups behave like organizations.

Future Enterprise contexts may require different exit governance because membership can be tied to a formal team structure.

### Why an unspecified membership lifecycle was not good enough

GroupMembership changes authorization and exposes shared resources. Creating that relationship without the target user's consent can surprise the user and create privacy problems.

For Current Scope, preventing an ordinary member from leaving freely would add unnecessary administrative control. For a future formal organization, however, immediate unilateral exit may conflict with organization-managed membership.

### Decision

In Current Scope:

- any `Registered Personal User` can create a Group;
- the Group creator becomes its initial Manager;
- joining an existing Group requires explicit acceptance by the target user;
- an invitation/request can originate from an invite link or from an authorized manager locating the target user through any collaboration discovery key allowed by the current discovery policy (DR-061);
- the target user can accept or reject the membership request;
- an ordinary member of a non-organizational Group can leave the Group unilaterally and immediately, subject only to the Manager-continuity rule in DR-063.

For Future Enterprise Scope, a proposed organizational membership still requires the target user's acceptance before it becomes active. Ending an organization-managed membership may use an approval-controlled leave request rather than immediate unilateral exit.

### Implications

- Membership is never created merely because another user selected the target account.
- Group authorization begins only after active membership exists.
- Enterprise membership lifecycle can become stricter without changing the consent principle for joining.

---

## DR-063 — A Group must always retain at least one Manager and the final Manager must transfer management before leaving

**Status:** CONFIRMED

### Context and previous model

Because Current Scope has no permanent global administrator account, Group-level collaboration management belongs to users who hold management capabilities inside that Group.

This raises a lifecycle edge case: if the final or only Manager leaves, the Group would remain with members and resources but nobody authorized to manage membership, sharing, or other management operations.

### Why allowing a managerless Group was not good enough

A managerless Group could become operationally stuck. Members might be unable to add/remove members, repair sharing configuration, or perform other Group-management actions. Relying on a hidden global administrator to repair such Groups would contradict the scope-dependent authorization model.

### Decision

Every active Group must have at least one member with Collaboration-Management Permission / the current Manager role.

If the last or only Manager attempts to leave, the leave operation cannot complete until another eligible member becomes Manager.

The outgoing Manager must be able to choose the successor either:

- directly by selecting an eligible member; or
- through a product-supported random assignment among eligible members.

Only after a valid successor exists can the final Manager's membership end.

### Implications

- Ordinary Group exit remains immediate for members who are not the final Manager.
- Manager continuity is a business rule, not a database-implementation detail.
- The exact UI for direct/random successor selection belongs to UI/UX Design.

---

## DR-064 — Public social-network features and commercial billing are outside Current Scope

**Status:** CONFIRMED AS SCOPE BOUNDARY

### Context and previous model

Dotick includes usernames, user discovery for collaboration, Direct Sharing, Groups, comments, and lightweight interactions. These capabilities could gradually be interpreted as the beginning of a general social network.

The product may also become commercially sellable in the future, but payment and subscription mechanics are independent from the current personal/productivity behavior.

### Why leaving these boundaries implicit was not good enough

Without an explicit boundary, collaboration features can expand into followers, public profiles, feeds, public discovery, or other social-product obligations that are unrelated to the current productivity model.

Likewise, introducing billing into Current Scope would add commercial identity, subscription state, payment-provider integration, and financial workflows before the business model has been decided.

### Decision

Current Scope does **not** include general public social-network behavior such as:

- following users;
- public feeds;
- public profiles as a social-discovery surface;
- public user/content discovery unrelated to an explicit collaboration action.

Username/handle search used to identify a collaboration recipient does not by itself create a social-network feature.

Current Scope also excludes payment, paid subscription, billing, and other commercial transaction behavior.

### Implications

- Collaboration remains purpose-specific to shared work/resources.
- Pricing, licensing, packaging, and billing are owned by the Business Track/future commercial scope.
- A future social or commercial feature requires a separate product decision rather than growing implicitly from current collaboration primitives.

---

## DR-065 — Direct productivity/calendar integrations and external assistant-agent integrations are Future Scope

**Status:** CONFIRMED AS FUTURE CAPABILITY

### Context and previous model

Dotick's domain already contains provenance concepts and future-facing examples such as Google Calendar, Email, Notion, and TickTick. The product also envisions interaction through external AI agents or voice assistants.

At the same time, Current Scope already uses or may use external services for specific current capabilities such as authentication and AI-assisted creation. Therefore, "all external services are future" is too broad and would contradict confirmed current behavior.

### Why treating every external service the same was not good enough

An authentication provider is not the same product capability as synchronizing user calendars. Likewise, an internal AI-assisted draft flow is different from allowing ChatGPT, Claude, Siri, Gemini, Bixby, or another external assistant to operate Dotick as an integration surface.

If these categories are collapsed, the scope becomes internally inconsistent.

### Decision

The following **productivity/integration surfaces** are Future Scope unless separately promoted by a later decision:

- direct Google Calendar integration/sync;
- Notion integration;
- TickTick integration;
- other calendar/productivity-system integrations;
- external AI-agent interaction such as Claude/ChatGPT acting as integration clients;
- external voice-assistant interaction such as Gemini, Siri, Bixby, or Alexa.

This decision does **not** classify every external dependency as Future Scope. Current-scope authentication providers and the current AI-assisted Item-creation capability remain governed by their own confirmed decisions.

### Implications

- `Source` may retain future provenance vocabulary without implying that the corresponding integration already exists.
- Integration-specific sync, authentication, conflict handling, and automation policy are defined only when the corresponding Future capability is activated.
- Manual/core productivity behavior must not depend on those Future integrations.

---

## DR-066 — Current User client is an installable responsive PWA; shared semantics remain client-independent and deeper native capabilities are Future

**Status:** CONFIRMED

### Context and evolution

Dotick's domain behavior must remain consistent across clients, while the first production surface needs a concrete Current-Scope client. The project does not intend to promise every native platform or supported end-user self-hosting before those capabilities are deliberately introduced.

### Decision

- The Current-Scope official User-facing client is a responsive installable **Progressive Web Application (PWA)** usable through supported desktop and mobile browsers.
- Shared domain data and business semantics must remain client-independent; platform-specific presentation/capabilities may differ without redefining the domain.
- The PWA uses browser/platform notification/push capabilities where supported; unsupported platform-specific delivery may degrade or be unavailable.
- Native Android/iOS, desktop-native clients, OS/application widgets and deeper platform-specific integrations remain Future Scope until promoted by a later decision.
- Current Scope does not include a supported production self-hosting product for arbitrary end users. Source availability or developer-local execution does not create that product commitment.

### Implications

- Offline-first design must work through the supported PWA constraints.
- Full persistent/alarm-like OS integration may be completed when native clients exist; the PWA phase may provide only the best behavior the target browser/platform safely supports.
- Future native clients consume the same canonical domain behavior rather than inventing new semantics.

---
## DR-067 — Gamification must reinforce a professional productivity experience rather than become the product's dominant game layer

**Status:** CONFIRMED IN PRODUCT INTENT

### Context and previous model

Dotick uses streaks, Daily Rings, scoring, feedback, and other motivational mechanics to make meaningful daily progress more engaging. A gamified productivity product can take two broad directions: make the game layer the primary identity of the product, or keep the productivity system primary and use gamification as a supporting behavioral layer.

### Why an unrestricted game-first direction was not good enough

The target product is intended for serious recurring daily planning, not only entertainment. If game mechanics dominate the interaction model or obscure task/event/routine semantics, users may perceive the tool as less suitable for professional or long-term use.

This does not mean removing strong motivational mechanics; it means those mechanics must reinforce useful behavior rather than replace the productivity model.

### Decision

Dotick's gamification is a supporting product layer.

It may provide visible motivation, progress feedback, streaks, Daily Rings, performance scoring, and other engaging mechanics, but the core experience must remain a coherent professional productivity system for Task, Event, Routine, Goal, and collaboration management.

Gamification must not require the product to adopt an RPG-like identity or make game state more authoritative than the underlying productivity/domain state.

### Implications

- Product/UI design can be expressive and motivating while preserving professional clarity.
- Progress and performance semantics remain tied to real user work, consistent with the existing Daily Ring decisions.
- Visual style and motivational presentation can evolve without changing the underlying domain rules.

---

## DR-068 — AI inference is external; Dotick owns orchestration/provider policy and supports optional BYOK with service fallback

**Status:** CONFIRMED

### Context and evolution

Dotick does not need to train its own foundation model, but external inference must not make an AI vendor authoritative over Dotick's domain behavior. The product also supports User-provided credentials without coupling normal UX to provider/model selection or making a personal credential failure a hard stop when the managed service can continue.

### Decision

- AI model inference is an external responsibility; Dotick owns context selection, prompt/instruction construction, provider routing policy, expected structured output, validation, interpretation and all product/domain authority.
- In normal service-managed mode, Dotick selects the supported provider/model according to service policy; the User does not need to choose or normally see the exact service-managed provider/model.
- A User may configure personal API credentials for a supported provider and enable BYOK/personal-credential mode.
- While enabled, compatible requests first use the User credential. User can explicitly return to service-managed mode.
- If the personal credential cannot be used, Dotick may automatically continue/retry through the service-managed AI path and must disclose that fallback in a visible but non-blocking way; a separate confirmation dialog is not required.
- If both paths fail, the owning AI capability follows normal AI failure behavior.
- The User is responsible for the right to use personal credentials and for the external provider Account's quota, billing and provider-side commercial limits. Dotick does not guarantee remaining quota, provider-account availability or provider pricing.
- Dotick remains responsible for secure handling of credentials within the supported flow and for validating AI output before it can affect product state.

### Design boundary

Provider catalog, credential storage/protection, service-provider routing, adapter implementation, timeout/retry details, rotation/key validation and usage accounting are Design/Security concerns as long as they preserve the behavior above.

---
## DR-069 — Product breadth and expert flexibility are preserved through context-aware UX rather than capability removal

**Status:** CONFIRMED

### Context and previous model

A common way to keep a productivity application simple is to reduce the number of available capabilities or aggressively hide advanced actions. Dotick, however, is intended to support a broad range of workflows and personalization needs, including users who need significantly more control than a minimal task manager provides.

### Why capability reduction was not good enough

Treating simplicity as the primary product goal would conflict with the intended breadth of Dotick and would make expert users lose useful flexibility. The opposite extreme—showing every control in every context—would also produce a poor experience by increasing cognitive load and making routine actions harder to scan.

### Decision

Dotick is intentionally a feature-rich and highly customizable product. Product breadth must not be reduced merely to make the interface appear minimal.

The UX should manage complexity intelligently through context, information hierarchy, progressive disclosure, sensible placement, and workflow-specific presentation. A capability should be visible when it is relevant and discoverable when needed, without requiring every action to be permanently exposed or permanently hidden behind generic overflow controls.

When a real trade-off exists between artificial interface simplicity and useful flexibility for advanced users, preserving meaningful user flexibility has the higher priority.

### Implications

- UI simplicity is a presentation goal, not a reason to remove valid product capability.
- Advanced behavior may use contextual or progressive disclosure rather than separate heavyweight workflows.
- Expert users must be able to reach deeper configuration without forcing that complexity on every user at all times.
- Backend complexity should still not be surfaced when it provides no user value; this decision extends rather than contradicts DR-017.

---

## DR-070 — Dotick provides usable defaults while remaining user-configurable and behavior-adaptive

**Status:** CONFIRMED IN PRODUCT DIRECTION

### Context and previous model

A highly configurable system can require too much setup before it becomes useful, while a strongly opinionated system can force every user into the same workflow. Dotick is intended to support substantial personalization while also being immediately usable by a new user.

### Why either extreme was not good enough

Requiring users to configure every behavior creates friction and makes the application difficult to start using. On the other hand, fixed defaults with little configurability do not fit the intended breadth of workflows. Static configuration alone also misses the opportunity to make behavior increasingly suitable to the individual user over time.

### Decision

Where configuration is meaningful, Dotick should provide sensible default values so the feature works without mandatory setup, while still allowing the user to override and personalize the behavior.

In features where behavioral adaptation is part of the product, the system may adapt recommendations, defaults, difficulty, or other eligible behavior based on the user's observed preferences and usage patterns. Explicit user configuration remains authoritative over inferred preferences where both address the same setting or behavior.

Adaptation must remain bounded by the semantics and safety constraints of the feature. Exact learning mechanisms, thresholds, and per-feature adaptation rules belong to the owning specification.

### Implications

- New features should define both a usable default and the meaningful customization surface.
- Personalization should reduce repeated user effort rather than silently remove control.
- Adaptive behavior is not a requirement for every feature; it applies where the owning product behavior explicitly supports it.
- Gamification adaptation may use lower and upper bounds so ordinary goals remain realistically attainable while higher achievements can remain challenging.

---

## DR-071 — Recorded domain reality is authoritative until a derived artifact is explicitly finalized

**Status:** CONFIRMED

### Context and evolution

Dotick must distinguish between what was planned and what actually happened. Recurrence, schedule, validity windows and deadlines can define expectation and consequences, but they must not force the system to erase a valid real-world action. The same distinction later proved essential for historical analytics: editable domain truth remains authoritative until a derived artifact is deliberately finalized.

### Decision

- Valid recorded reality takes precedence over strict adherence to the plan.
- Schedule/recurrence/validity rules may affect suggestion, eligibility, reminder, streak, scoring or consequence, but do not by themselves prohibit recording a valid fact.
- User-created domain state remains correctable historically according to normal rules.
- Derived state may change while it is open and based on current domain truth.
- Once a derived artifact is explicitly finalized, that finalized artifact becomes historical evidence of what was closed at that time and is no longer automatically rewritten by later source edits.

### Implications

Examples include unscheduled/out-of-window RoutineCompletion recording, historical Item correction and immutable finalized Daily Ring/statistical outcomes.

---
## DR-072 — Persistent changes are traceable and recoverable through an immutable branching History model compatible with Audit and Sync

**Status:** CONFIRMED

### Context and evolution

A simple linear AuditLog is sufficient for troubleshooting but not for the intended user workflow where a User can inspect an older meaningful version, return to it, continue from there and still preserve the previous path. Offline reconciliation also requires history/version semantics that do not conflict with sync metadata.

### Decision

- Meaningful persistent domain state changes create immutable History/Audit evidence; ordinary reads are not part of this product-level change history.
- Normal Users cannot edit or delete existing history entries.
- Authorized Users can view the history allowed by Resource authorization.
- Supported historical versions can be checked out/restored.
- Continuing edits from a historical version creates a new branch; the previous path is preserved rather than overwritten.
- Branches and meaningful versions remain navigable and may be checked out again.
- Checkout/restore itself creates new history instead of erasing prior history.
- Reset/delete/conflict resolution must preserve enough evidence to explain the current state.
- User-visible History, Audit evidence and synchronization operation/version metadata must be designed as compatible layers using stable identities/order semantics; none may silently contradict the others as an independent source of truth.

### Implications

This behavior does not require Git, full event sourcing or a particular graph storage engine. The exact persistence model belongs to History/Sync/Data Design, but it must preserve branching, traceability, recovery and reconciliation semantics.

---
## DR-073 — AI autonomy is capability-specific; reviewable proposals are never silently auto-applied

**Status:** CONFIRMED

### Context and previous model

A broad product principle such as "AI always proposes and the user always confirms" is too general for Dotick. Some AI capabilities, such as AI-assisted Item creation, produce a proposal for an explicit user-authored action. Other capabilities, such as semantic Goal discovery and AI Tag lifecycle, are intrinsically AI-managed system functions.

### Why one global confirmation rule was not good enough

Requiring confirmation for every AI-managed semantic operation would undermine capabilities whose purpose is to operate automatically. Conversely, allowing every AI output to mutate user-authored data without review would contradict the confirmed Item-creation flow and could apply an inference the user never accepted.

### Decision

AI authority is defined per capability rather than by one global confirmation rule.

For AI-assisted Item creation and any other flow explicitly defined as a reviewable proposal, AI output must not be silently applied: the user reviews the proposal and confirms the resulting action.

AI-managed semantic capabilities such as Goal discovery, AI Tag assignment, and their defined review/cleanup lifecycle may operate automatically according to their own product rules; they do not require per-change user confirmation merely because AI is involved.

Trusted external automation remains a separate future decision and is not implicitly authorized by this DR.

### Implications

- DR-037 remains the rule for AI-assisted Item creation.
- System Definition wording must not imply that every AI capability requires confirmation.
- AI is a specialized tool for defined tasks, not a general authority that directs the user's behavior.
- If an AI-dependent capability is unavailable, that capability may report an availability error while unrelated core functionality remains usable.

---

## DR-074 — Productivity truth and recovery-oriented motivation outrank game mechanics

**Status:** CONFIRMED

### Context and previous model

Gamification can increase engagement through streaks, achievements, motivational pressure, rewards, or even deliberately critical messaging. If engagement metrics become the primary objective, however, the product may be tempted to make progress easier to claim or to distort the meaning of completion.

### Why engagement-first gamification was not good enough

Dotick is a productivity system first. A streak or achievement that does not correspond to real progress weakens trust in the product and encourages behavior aimed at preserving game state rather than completing meaningful work. At the same time, overly punitive mechanics can make recovery feel impossible after a poor day.

### Decision

Gamification may actively motivate, pressure, encourage, or criticize the user, but it must not falsify or inflate actual productivity progress merely to preserve engagement.

When engagement and accurate representation of real progress conflict, accurate progress wins.

The motivational system should also preserve a realistic path back after failure: previous misses may have consequences, but they should not make continued effort feel pointless. Ordinary success should remain realistically attainable, while higher levels of achievement may remain meaningfully challenging.

### Implications

- This decision extends DR-067 and is consistent with DR-025, DR-027, and DR-030.
- Critical/scolding messaging is allowed in product direction; its exact triggers, tone, frequency, and relationship to global streak behavior remain part of the owning Gamification decision/specification.
- Recovery mechanics must not manufacture fake completion or allow visible progress above its real cap.
- Difficulty/adaptation thresholds still require formalization in the scoring design.

---

## DR-075 — Inherited sharing must expose its affected scope and require initiating-user confirmation

**Status:** CONFIRMED

### Context and previous model

Container sharing can intentionally propagate access from a Folder to Lists/Items or from a List to its Items. This inheritance keeps Personal V1 simple, but a single sharing action can therefore expose more data than the initiating user may realize if the UI treats it like a single-resource action.

### Why silent inherited expansion was not good enough

Access inheritance is valid only when the user understands the scope of the action. Applying descendant access without making that scope clear creates an avoidable privacy and expectation risk, even if the authorization model itself is correct.

### Decision

Before a sharing action or sharing-policy change causes access to be inherited across multiple descendant Resources, Dotick must present the initiating user with an understandable summary of the affected scope and require explicit confirmation before applying the change.

This confirmation is distinct from recipient-side invitation or membership acceptance rules already defined elsewhere.

### Implications

- Folder/List sharing UI must communicate that descendant Resources will become accessible under the inherited policy.
- Revoke or permission-expansion flows that materially affect inherited scope should provide equivalent clarity before execution.
- The product does not need to expose raw database objects or every descendant identifier; the confirmation must be understandable at the product/domain level.

---

## DR-076 — Intelligent and personalized layers are optional relative to core productivity management

**Status:** CONFIRMED

### Context and previous model

Dotick contains AI-assisted creation, semantic Goal discovery, adaptive Daily Rings, and other personalized behavior, but the core application also manages Task, Event, and Routine data directly. If intelligent layers became mandatory for ordinary management, an AI outage, user preference, or algorithmic disagreement could make the core product unusable.

### Why mandatory intelligence was not good enough

AI and personalization are intended to improve selected workflows, not to become a prerequisite for basic productivity management. Users must be able to continue using the ordinary management capabilities even if they do not want algorithmic/personalized features or if an external AI service is unavailable.

### Decision

Core Task/Event/Routine management must remain usable without AI, gamification, or personalized recommendation layers.

The user must be able to disable applicable intelligent/personalized layers and continue using Dotick as a conventional productivity manager.

A capability whose intrinsic purpose is algorithmic—such as automatic Goal discovery or Daily Ring selection—does not have to provide a non-algorithmic substitute inside that same feature. Disabling the intelligent layer may therefore disable that feature itself rather than allow the user to override its defining algorithm.

### Implications

- AI outages must degrade AI-dependent capabilities rather than disable unrelated core flows.
- Manual Item management remains independent from AI availability.
- Settings/UX must distinguish disabling an optional intelligent layer from manually overriding every individual recommendation generated by that layer.
- Exact controls and which layers can be toggled independently belong to the relevant UI/Product specifications.

---

## DR-077 — Measured responsiveness can justify simplifying expensive product behavior

**Status:** CONFIRMED

### Context and previous model

Dotick is intended to be feature-rich, but it is also used repeatedly throughout the day. Rich UI, adaptive behavior, analytics, synchronization, and visual effects can impose runtime cost.

### Why either "performance at any cost" or "features at any cost" was not good enough

Removing capability preemptively in the name of performance would conflict with the product's breadth. Conversely, keeping an expensive behavior after it causes a clearly noticeable slowdown would damage the frequent-use experience.

### Decision

Dotick should preserve useful capability by default, but responsive interaction is a high-priority quality attribute. When practical measurement demonstrates material user-visible performance degradation, simplifying, deferring, asynchronously executing, or removing the expensive behavior is justified.

Performance trade-offs must be driven by observed or benchmarked impact rather than by speculative optimization alone.

### Implications

- Performance-sensitive behavior should be measured in representative flows.
- Heavy computation may be moved off the synchronous interaction path where semantics allow it.
- Feature richness does not override a repeatedly measured poor user experience.
- The exact performance budgets and acceptance thresholds belong to performance/test specifications.

---

## DR-078 — Architecture must preserve future evolution through bounded coupling and replaceable technology boundaries

**Status:** CONFIRMED IN DESIGN DIRECTION

### Context and previous model

Dotick is being built first for Personal V1 but is expected to evolve into broader clients, integrations, and future product scopes. A design optimized only for the immediate increment can make later migration prohibitively expensive, while over-engineering every possible future can also make the current system unnecessarily complex.

### Why short-term coupling or unlimited future-proofing were not good enough

Deep coupling to one framework, provider, client, or implementation detail can make future changes invasive. At the same time, pretending every technology must be instantly swappable leads to unnecessary abstraction and speculative complexity.

### Decision

Current design may accept reasonable additional structure when it materially reduces foreseeable future migration cost or prevents the current implementation from blocking future product evolution.

Core domain semantics and module boundaries should minimize unnecessary dependence on specific frameworks, vendors, clients, or external providers. Technology-specific code should be localized behind appropriate boundaries when doing so has clear architectural value.

The goal is bounded coupling and practical replaceability—not zero-cost replacement of every technology.

### Implications

- This principle is consistent with the modular-monolith direction in DR-051, client-independent semantics in DR-066, and provider independence in DR-068.
- Platform-specific capabilities are allowed when they improve the client experience, provided shared domain semantics remain consistent.
- Significant framework/provider choices should avoid leaking implementation-specific concepts into the core domain without need.
- A slightly more complex current design is acceptable when the future benefit is concrete and proportional; speculative Enterprise complexity remains out of Current Scope unless otherwise decided.
- Early-Increment schema/API/entity choices must be reviewed against already-known later cross-cutting semantics—especially Offline/Sync, branching History/Audit, authorization/revocation, and Time Semantics—even when the full feature is implemented in a later Increment. Implementation may be deferred; foundational incompatibility may not.

---

## DR-080 — Task dependency cycles are forbidden and must produce an understandable diagnostic

**Status:** CONFIRMED

### Context and previous model

Task dependencies use `blocked_by` relations. Without an explicit cycle rule, a chain such as `A -> B -> C -> A` could make every Task in the chain permanently blocked and create contradictory dependency semantics.

### Decision

The Task dependency graph must be acyclic.

Any create/edit operation that would introduce a dependency cycle must be rejected. The user-facing error should explain that the requested relation would create a loop and, where practical, identify the existing dependency chain responsible for the conflict.

### Implications

- Direct self-dependency is forbidden.
- Indirect cycles of any length are forbidden.
- Cycle detection is part of domain validation, not merely a UI safeguard.

---

## DR-081 — Task temporal fields follow monotonic ordering

**Status:** CONFIRMED

### Context and previous model

Task supports `due_at`, optional `end_at`, and optional `deadline_at`. Their individual meanings were defined, but invalid combinations had not been closed as a domain rule.

### Decision

When the relevant values exist, Task temporal ordering must satisfy:

```text
due_at <= end_at <= deadline_at
```

If `end_at` is absent but `deadline_at` exists:

```text
due_at <= deadline_at
```

A Task cannot end before it begins, and a deadline cannot precede the Task's due/start point or its explicit end.

### Implications

- Invalid combinations are rejected during validation.
- Equality is allowed at boundaries unless a later specialized specification has a stronger requirement for a particular workflow.

---

## DR-082 — Recurring Task generation is schedule-driven, not completion-driven

**Status:** CONFIRMED

### Context and previous model

Recurring Task generation could either wait for the previous occurrence to be completed or generate occurrences according to the recurrence schedule regardless of the previous Task's state.

### Why completion-driven generation was not good enough

Coupling generation to completion changes the meaning of calendar recurrence and can hide missed/overdue occurrences. The recurrence definition should describe when work is expected, while completion state describes what happened to an individual occurrence.

### Decision

Recurring Task occurrence generation is time/schedule-driven. A later occurrence is generated according to the recurrence rule even if the previous occurrence remains `Todo`, `Overdue`, `Missed`, or otherwise incomplete.

### Implications

- Individual recurring Task occurrences may coexist with different statuses.
- Exact occurrence identity and persistence representation belong to Recurrence/Data Design.

---

## DR-083 — Incremental Routine targets advance only on Done completions and decay gradually after inactivity

**Status:** CONFIRMED IN PRODUCT BEHAVIOR

### Context and previous model

Incremental Routine targets have a base `fix_amount` and may increase over time. Two boundaries were still open: which completions qualify for increasing the target, and what happens after long inactivity.

### Decision

Only a `RoutineCompletion` whose status is `Done` qualifies to advance an incremental target.

A valid `Done` on an unscheduled date qualifies in the same way as a scheduled `Done`. `Won't_Do`, absence of a completion, and incomplete partial progress do not advance the target.

After sufficiently long inactivity, the target should **decay gradually** toward `fix_amount`; it must not reset abruptly to the base value and must not remain permanently at the previous peak regardless of inactivity.

### Open design parameters

The inactivity threshold, decay curve/rate, and exact update formula are tuning/design parameters owned by the Routine/Gamification specification and should be validated empirically.

---

## DR-085 — Initial AI Goal discovery uses a time-based warm-up, not a minimum Item-count gate

**Status:** CONFIRMED IN PRODUCT BEHAVIOR

### Context and previous model

The initial AI Goal discovery warm-up could be gated by elapsed time, a minimum count of existing Tasks/Items, or both. A hard minimum Item count risks preventing Goal discovery for users whose natural workload is small.

### Decision

Initial Goal discovery uses a **time-based warm-up measured in hours**. It must not require a fixed minimum number of Tasks/Items before the first analysis is allowed to run.

### Open design parameter

The exact number of warm-up hours is a tunable AI Goal parameter and should be selected/adjusted through evaluation rather than treated as a permanent product-level constant.

---

## DR-086 — Goal similarity behavior is tiered; numeric thresholds are model-versioned tuning parameters

**Status:** CONFIRMED

### Context and previous model

Goal merge/reactivation needed similarity thresholds, but a single canonical numeric score would couple product behavior to a particular embedding/model and could become invalid when the model changes.

### Decision

Product behavior uses semantic similarity tiers rather than a permanent model-independent numeric constant:

- **High similarity:** eligible for automatic merge/reactivation according to the relevant lifecycle flow.
- **Intermediate similarity:** keep separate for now and allow later semantic review to re-evaluate.
- **Low similarity:** treat as independent.

The exact numeric/model-specific thresholds must be calibrated and versioned for the AI model/representation in use.

### Implications

- Threshold values belong to `AI_GOAL_SPEC.md`/evaluation artifacts, not the stable product semantics.
- Model changes may recalibrate numeric cutoffs without changing this Decision Record.

---

## DR-088 — Graduated motivational intensity is a tunable Gamification design direction

**Status:** CONFIRMED IN DESIGN DIRECTION

### Context and previous model

Current product behavior allows motivational, critical, or scolding messaging as part of Gamification, but the System Definition intentionally leaves exact timing, frequency, cooldown, copy, and escalation behavior to tuning. Earlier wording could be read as making a particular within-day escalation schedule a mandatory Current-Scope behavior.

### Decision

A graduated tone is the preferred starting design direction for motivational messaging: earlier messages may use mild/encouraging language, while later messages may become stronger when relevant work remains unfinished.

A late-evening point around **21:00 local time** may be used as an initial experiment for stronger messaging, but neither that time nor a specific graduated sequence is a canonical behavioral requirement. Exact timing, frequency, copy, cooldown, and escalation rules are versioned/tunable UX/Gamification parameters and must remain consistent with the System Definition's productivity-truth and user-control principles.

### Implications

- Current-Scope acceptance must not fail merely because a particular 21:00 or graduated-intensity schedule is changed during tuning.
- Gamification may apply behavioral pressure, but it must preserve truthful productivity state and the applicable notification controls.
- The owning Gamification specification records and evaluates the chosen timing/copy/rate-limit configuration.

---

## DR-089 — Goal-level motivational reminder frequency is an empirical tuning parameter, not an unresolved product rule

**Status:** CONFIRMED IN DESIGN DIRECTION

### Context and previous model

Goal-level reminders may trigger when performance meaningfully declines relative to the Goal Norm. The remaining question was the exact daily frequency/rate limit.

### Decision

The existence and trigger concept of Goal-level motivational reminders are retained, but their exact frequency, cooldown, and rate limits are **not fixed as canonical product constants**.

They must be determined through product testing, user feedback, and experimentation in the Gamification specification.

### Implications

- This item is removed from the product Decision backlog.
- Implementation must still define explicit safe/default limits before release; those values are versioned/tunable configuration, not a permanent Decision Register rule.

---

## DR-091 — Trusted AI/automation authority is explicitly scoped, tiered, and revocable

**Status:** CONFIRMED AS FUTURE CAPABILITY

### Context and previous model

Current AI-assisted Item creation requires review/confirmation, while future external-source automation may need to act without confirmation for every individual action. A binary trusted/untrusted flag would not provide enough user control.

### Decision

Future trusted AI agents/automation may operate without per-action confirmation only after the user explicitly grants authority.

Authority must be:

- **scoped** to defined capabilities/resources/actions;
- able to support **multiple permission/trust levels** rather than a single unrestricted trust state;
- **revocable by the user at any time**;
- auditable so automated actions remain traceable.

Without an applicable prior grant, the default remains review/confirmation for flows whose current product behavior requires it.

### Open design parameters

The exact trust levels, permission matrix, UI, and credential/external-source mechanics belong to the Future Automation/Authorization design stage.

---

## DR-092 — Recurring occurrence identity representation is delegated to Recurrence/Data Design

**Status:** CONFIRMED IN DESIGN OWNERSHIP

### Context and previous model

Recurring Task/Event behavior requires individual occurrences to be addressable for status, edit, exception, and history behavior. The open question was whether this must be represented through a particular product-level identity model such as a standalone row per occurrence or another series/occurrence representation.

### Decision

The product semantics do not mandate one physical occurrence-identity representation in the Decision Register.

The Recurrence/Data Design stage must choose an implementation that preserves the already-confirmed behavior of recurring entities, independent occurrence state where required, historical traceability, sync correctness, and exception/edit semantics.

### Implications

- This is removed from the product Decision backlog.
- The final representation must be documented in `RECURRENCE_SPEC.md`, Data Design, and any necessary ADR.

---

## DR-093 — Group collaboration containers are Group-owned

**Status:** CONFIRMED

### Context and previous model

The collaboration model allows a Group to act as a persistent context for shared work, but ownership of Folder/List/Column resources inside that context had remained open. One option was to keep every container owned by an individual user and merely share it with the Group; another was to let the collaborative resource belong to the Group itself.

### Why user-owned shared containers are not sufficient

A resource created for the Group should not depend on the continued membership of the individual who originally created it. If the creator leaves the Group, collaborative structure and content must remain available to the Group according to its authorization rules. Treating such resources as merely personal resources shared outward would make ownership lifecycle and continuity unnecessarily fragile.

### Decision

Folder, List, and Column resources created within Group collaboration context are **owned by the Group**. Their contained collaborative resources follow the applicable Group/resource ownership model rather than becoming personal property of the creating member solely because that member performed the create action.

The creator identity may still be recorded separately for audit/history purposes.

### Implications

- A member leaving the Group does not remove or transfer Group-owned Folder/List/Column resources merely because that member originally created them.
- Authorization to view, edit, move, or manage Group-owned resources follows Group/resource permissions, not creator identity.
- Personal resources may still be shared with a Group through the Direct Sharing model; doing so does not automatically convert their ownership to Group ownership unless an explicit future transfer operation is defined.
- Exact persistence fields and ownership foreign-key strategy belong to Data/Authorization Design.

---

## DR-094 — Daily Ring difficulty/effort is an AI-estimated internal signal

**Status:** CONFIRMED IN PRODUCT BEHAVIOR

### Context and previous model

Daily Ring selection/scoring includes difficulty/effort among its candidate signals, but the product had not decided whether this value should be manually entered by the user, derived from simple metadata, or estimated automatically.

### Decision

Difficulty/effort for candidate Task, Event, and Routine occurrences used by Daily Ring selection/scoring is **estimated by the AI system** and provided as a numerical signal to Dotick.

It is not a required user-authored field in the normal Item workflow.

### Implications

- The user does not need to manually assign a difficulty value for ordinary use.
- The AI model/pipeline may use Item content and other allowed context to estimate the number.
- The numeric scale, calibration method, model prompt/schema, confidence handling, and fallback behavior belong to `AI_GOAL_SPEC.md` / `GAMIFICATION_SCORING_SPEC.md` and evaluation artifacts.
- AI unavailability must not disable core Item management; where the difficulty signal is unavailable, the owning scoring/selection design must define a safe fallback.


---

## DR-095 — Frequency-based Routine streak increments per completion and is validated at period boundary

**Status:** CONFIRMED

### Context and previous model

For a frequency-based Routine such as `3 times per week`, the required completions may occur on any days within the period. The remaining ambiguity was whether streak should count successful periods, successful individual completions, or break immediately on any calendar day without a completion.

### Why period-count streak or daily-break semantics were not correct

Counting one streak unit per successful week would under-represent the user's actual sequence of completions. On the other hand, resetting the streak on a day without completion would incorrectly impose fixed-day semantics on a flexible frequency target whose only requirement is to satisfy the quota before the period ends.

### Decision

For a frequency-based Routine such as `N times per period`:

- `current_streak` increases by **one for each valid `Done` completion**.
- The user may place those completions on any valid dates within the current period; an uncompleted calendar day does not by itself break the streak.
- The period quota is evaluated when the period closes.
- If the number of qualifying `Done` completions in that period is **less than `N`**, the streak resets to `0` at the start of the next period.
- If the quota is satisfied, the accumulated streak carries into the next period and continues increasing with subsequent valid completions.
- Valid extra completions beyond the minimum quota remain real completions and may continue increasing the completion-based streak; they do not reduce or invalidate the period result.

Example:

```text
Routine: 3 times per week

Week 1:
  completion 1 -> streak 1
  completion 2 -> streak 2
  completion 3 -> streak 3
  quota satisfied

Week 2:
  completion 1 -> streak 4
  completion 2 -> streak 5
  completion 3 -> streak 6

If Week 3 ends with only 2 qualifying completions:
  period closes below quota
  start of Week 4 -> streak 0
  next valid completion -> streak 1
```

### Implications

- Frequency-based Routine streak semantics remain distinct from fixed-day Routine streak semantics.
- A missed arbitrary day inside a flexible period does not break the streak.
- The recurrence engine must know the exact period boundary according to the Routine's selected calendar.
- Period-closing evaluation must be deterministic and covered by boundary tests.
- The exact persistence/caching strategy for streak state remains a design concern.


## DR-096 — Information organization uses mandatory List/Column placement with a special Inbox

**Status:** CONFIRMED

### Context and previous model

The organizational hierarchy was already defined as `Folder > List > Column`, but several product behaviors were still implicit: whether a List could exist without a visible Folder, whether Inbox was a real List or only a view, whether an Item could belong to multiple Lists/Columns, and what should happen to contained Items when a container is removed.

### Why leaving placement and deletion implicit was not good enough

Creation, move, offline sync, sharing, hierarchy, and deletion all depend on deterministic placement. Allowing an Item to have no List/Column or silently deciding what happens to a deleted Column would make the UI and data semantics diverge.

### Decision

- A List may exist without a user-visible Folder. A hidden/default Folder may be used internally if implementation benefits from it, but that is not user-facing product semantics.
- Every User has one special real `Inbox` List. It is the default List and cannot be renamed or deleted.
- Every Task and Event belongs to exactly one List and exactly one Column of that List at a time. Routine uses its dedicated Routine space and does not use Folder/List/Column placement.
- Task/Event creation defaults to Inbox and the default Column unless creation is initiated directly in another Column/context.
- Folder, List, and Column ordering is user-controlled and duplicate titles are allowed.
- Deleting a Column requires choosing whether contained Items are deleted or moved to the List's default Column.
- Deleting a List includes its Items; deleting a Folder includes its Lists and their contents. Normal deletion follows Trash/recovery semantics.
- The organizational hierarchy has no additional Folder-in-Folder or Column-in-Column level in Current Scope.

### Implications

Physical use of a hidden default Folder remains a design choice. Product behavior must remain the same regardless of that implementation.

---

## DR-097 — Task dependency gates Done and Task hierarchy has configurable completion cascade

**Status:** CONFIRMED

### Context and previous model

Task dependency and structural parent/child were already distinct relations, but their operational consequences were incomplete. It was unclear whether a blocked Task could still be completed, what terminal state resolves a blocker, and whether completing parent/children should cascade.

### Decision

- A blocked Task cannot be changed to `Done` until every active blocker is `Done`.
- Only `Done` satisfies a dependency.
- Deleting a blocker removes the corresponding dependency relation.
- Dependency cycles are rejected with an explanation that the new relation would close an existing chain into a cycle.
- Dependency and structural hierarchy remain independent.
- By default, when all structural children are `Done`, the parent becomes `Done`; the User may disable this preference.
- Explicitly setting a parent to `Done` sets its structural descendants to `Done`.
- Time-driven states do not cascade from parent to descendants.
- `Won't_Do` does not cascade by default, but the User may enable a preference that cascades it to structural descendants.
- Viewing/reopening a historical Task does not by itself recalculate its status. Defined time-driven transitions and explicit state changes remain separate from mere viewing.
- A Task that is currently `Skipped` may be explicitly moved by the User to another allowed state; `Skipped` itself remains a time-driven system state.

---

## DR-098 — Event status is time-driven and overlaps are advisory

**Status:** CONFIRMED

### Context and previous model

Event had `Not_Arrived`, `Ongoing`, and `Finished`, but the exact handling of missing end time, all-day events, manual status changes, and overlapping schedules was not fully fixed.

### Decision

- A scheduled Event's status is time-driven and is not manually selected by the User; an unscheduled Event has no applicable time-driven status.
- For a scheduled Event: before start -> `Not_Arrived`; during its interval -> `Ongoing`; after end -> `Finished`.
- If an Event has a start date but no explicit end, the end of that Calendar Day is its effective end.
- All-day Event semantics follow the local Calendar Day, not the Dotick Day.
- Schedule overlaps are allowed. The system may warn the User but does not prohibit creating or moving overlapping Items.
- Reaching `Finished` can satisfy the full-Event Daily Action corresponding to that Event.
- Event has a single Location concept rather than a list of independent locations.

### Boundary

An Event may be created, saved, retrieved, and edited while completely unscheduled: neither a start time nor an all-day date is required for the Event to exist. An unscheduled Event has no applicable time-driven status; `Not_Arrived`, `Ongoing`, and `Finished` are derived only after a valid start schedule exists. Adding or completing the schedule later must not require replacing the Event or changing its identity.

---

## DR-099 — Task/Event hierarchy is cross-type, unbounded in domain depth, and placement-coupled

**Status:** CONFIRMED

### Context and previous model

Task and Event were both allowed to have structural children, and each now has at most one structural parent, but cross-type parenting, child placement, move/delete behavior, and reference behavior required a single coherent rule.

### Decision

- `Task -> Task`, `Task -> Event`, `Event -> Task`, and `Event -> Event` structural relations are valid.
- Domain nesting depth has no fixed limit; cycle creation remains prohibited.
- UI may limit inline tree presentation to five levels without limiting the underlying hierarchy.
- A structural child shares the parent's List/Column placement.
- Moving the parent moves its structural descendants.
- Moving a child to an incompatible independent placement breaks the structural parent relation rather than creating multi-placement hierarchy.
- Deleting a parent also deletes its structural descendants through the normal deletion/Trash flow.
- Removing only the relation preserves both Items.
- RichDescription may reference Task, Event, and Routine; Goal is not referenceable in Description in Current Scope.
- References are live for current title/state. If the referenced Item is deleted, the reference remains as a deleted-item indication using its known title.

---

## DR-100 — Routine comments are collaboration comments; personal daily notes remain RoutineCompletion notes

**Status:** CONFIRMED

### Context and previous model

Comments were primarily specified for Task/Event. Adding collaboration to Routine raised the question of whether the owner should use comments as personal journaling and how comments on a specific Routine day should differ from the Routine's own daily note.

### Decision

- Task/Event comments remain available to authorized actors on the whole Item or a ContentBlock.
- An authorized collaborator may comment on a shared Routine as a whole or on a specific Routine day/completion context.
- The Routine owner does not use comments on their own Routine for personal notes; personal daily notes belong to `RoutineCompletion.note`.
- Comments are editable, deletable, replyable, and can mention eligible collaborators by username.
- Replies notify the target comment's author.
- Deleting a ContentBlock removes its block comments from current state, while audit/history preserves the creation/deletion trail.
- Deleted comments disappear from ordinary UI but remain traceable in history.

---

## DR-101 — RoutineCompletion uses In_Progress for partial recorded progress

**Status:** CONFIRMED

### Context and previous model

`RoutineCompletion.status` previously had only `Done` and `Won't_Do`, while Partial routines can record a real amount before reaching the target. A row such as `3 / 8` is not “no outcome,” is not `Done`, and is not `Won't_Do`.

### Why nullable or ambiguous status was not good enough

Treating a row with amount as status-less would blur the difference between “nothing was recorded” and “the User has started and recorded progress.” It also complicates UI and sync state.

### Decision

`RoutineCompletion.status` is:

```text
In_Progress
Done
Won't_Do
```

- No row means no progress/outcome has been recorded for that date.
- A Partial Routine with recorded amount below target uses `In_Progress`.
- Reaching or exceeding the target automatically changes the current row to `Done`.
- `amount` stores the actual amount and may exceed target, e.g. `10 / 8`.
- For multi-day periods, progress is the sum of daily RoutineCompletion amounts.
- `Won't_Do` is explicit and breaks the relevant streak.
- The scheduling validity window controls expected presentation, not whether reality may be recorded; completion may be entered before start date, on unscheduled days, or after end date.

---

## DR-102 — Recurrence edits distinguish calendar-anchored occurrences from interval-chain shifts

**Status:** CONFIRMED

### Context and previous model

A generic “edit this occurrence vs series” rule is not sufficient for all recurrence semantics. Moving one Monday in a weekday pattern should not move every future weekday, while moving an occurrence in a strict every-three-days chain may intentionally shift the future sequence.

### Decision

- Recurrence may be endless, date-bounded, or occurrence-count-bounded.
- In calendar-anchored recurrence, an occurrence may be overridden independently without shifting the pattern of other occurrences.
- In interval-chain recurrence, when one occurrence is moved, the User chooses between changing only that occurrence or preserving the interval by shifting future occurrences.
- Deleting a recurring occurrence must at least offer “this occurrence only” or “end future recurrence.”
- Historical occurrences are not rewritten by later recurrence/calendar edits.
- Recurring Event occurrence generation is not blocked by the previous occurrence's completion/end state.
- All-day recurrence uses date/calendar semantics without requiring a time-of-day.

---

## DR-103 — Reminder delivery is explicit, relative, snoozable, and multi-device aware

**Status:** CONFIRMED

### Decision

- No Reminder exists unless the User configured it or accepted an AI-proposed Reminder.
- Task/Event reminders may trigger at the relevant scheduled time or at an offset before it; relative reminders move when the schedule moves.
- Routine reminders use user-selected times on valid days.
- For frequency-based Routine, reminders may continue on remaining days of the period until quota is reached; after quota completion, remaining reminders for that period are unnecessary.
- Reminder can be snoozed.
- Persistent/alarm-like intent is represented in the domain independently of platform capability. In the Current-Scope PWA, delivery is best-effort within browser/OS constraints and full native ringing/full-screen behavior is not guaranteed. Future native clients may implement stronger platform-specific alarm behavior, including explicit acknowledgement and configurable ringing duration where supported.
- Future reminders are cancelled once the Item reaches an appropriate final outcome.
- With multiple devices, delivery may continue until an interaction is recorded on one device; after that, new delivery of the same reminder to the other devices stops.

---

## DR-104 — Goal identity/title and AI tags are AI-managed; user control is feature-level

**Status:** CONFIRMED

### Context and previous model

Goal discovery is an AI-managed capability, but it was not explicit which Goal/Tag fields the User may directly override and whether AI artifacts could be individually deleted or protected.

### Decision

- User cannot manually create a Goal.
- User cannot manually rename the Goal title generated by the Goal-discovery process.
- User may edit Goal description to provide semantic context.
- User does not manually Archive or Reactivate Goal.
- Each Goal belongs to one List or one Column context.
- An Item has at most one active Goal attribution for Daily Ring behavior at a time.
- User-created Tags can be renamed/deleted.
- AI-created Tags cannot be individually renamed/deleted/locked by the User.
- User control over this AI behavior is at the feature level: disabling Goal discovery removes AI-created Tags and disables dependent Goal/Ring behavior while leaving core Item management available.

---

## DR-108 — Group context distinguishes Group-owned resources from personal resources attached to a Group

**Status:** CONFIRMED — extends DR-093

### Decision

- Folder/List/content created directly in Group context is Group-owned.
- A personal Resource may also be placed/shared into a Group context while retaining the identity of its prior personal owner.
- While attached to Group context, that Resource follows Group authorization/collaboration rules.
- Only its prior personal owner may detach that personal Resource from the Group context.
- Group-owned Resource is not visible to an outsider who lacks valid Group access; direct sharing must not bypass that Group boundary.
- A personal Resource may be shared with a Group, with the Resource owner remaining visible.
- Deleting a Group warns the Manager that its Resources will be deleted unless moved first. If confirmed, Resources enter Trash rather than being automatically transferred.
- The Manager who deleted the Group can restore it and its Resources during the 30-day Trash retention window.
- Broad inherited sharing and broad inherited revoke both require clear scope disclosure and explicit initiating-user confirmation.

---

## DR-109 — Offline collaboration edits are accepted only if current server authorization still permits them

**Status:** CONFIRMED

### Context and previous model

Offline-first allows local edits to shared data, but access can change while a device is disconnected. Comparing only local edit timestamps to the revoke time would allow a disconnected actor to apply changes after their authorization has already been removed server-side.

### Decision

- Core Task/Event/Routine and organization management, plus comments on previously accessible Resources, may be performed offline.
- Sharing, invitation, membership management, and operations whose nature requires current server authorization remain online-only.
- A previously authenticated User can open and use the local working set offline.
- Devices need not keep unlimited historical data offline; old history may be fetched on demand when online.
- Conflict resolution normally converges automatically at field level.
- Losing values in a conflict remain traceable in history with actor/change information.
- If access was revoked before an offline edit reaches the server, the edit is rejected regardless of when the device claims it was made.
- Rejected offline edits must not disappear silently; recovery/history must preserve enough information to explain the outcome.

---

## DR-111 — Creator identity, ownership, and collaboration scope remain separate concepts

**Status:** CONFIRMED

### Context and previous model

As personal Resources can be placed into Group contexts and Group-owned Resources can also be created directly inside a Group, treating creator identity, owner identity, and current collaboration scope as one value would make later transfer, access removal, and Group lifecycle ambiguous.

### Why one ownership/scope field was not good enough

The User who initially created a Resource is a historical fact, but that fact must not automatically grant permanent access. A personal Resource may participate in Group collaboration while remaining personally owned, while a Resource created directly for the Group must survive independently of the individual who created it.

### Decision

- `created_by` preserves the original creator identity and is not rewritten by later ownership/scope changes.
- Creator identity by itself grants no authorization.
- A personal Resource can enter a Group context while retaining its personal owner and following Group authorization rules while attached.
- Only that retained personal owner can detach the personal Resource from the Group context unless a later explicit transfer rule says otherwise.
- Resources created directly in Group context are Group-owned and do not become personally owned by their creator.
- Resource ownership may differ from container ownership; containment alone does not transfer ownership.
- Source/provenance remains separate from creator and ownership identity.

### Implications

Authorization must evaluate the Resource's current valid access paths rather than infer access from `created_by`. Group participation and containment do not silently rewrite ownership.

---

## DR-113 — Task/Event structural placement is local while references may cross authorized contexts

**Status:** CONFIRMED

### Context and previous model

The organization model previously used broad `Item` wording that could imply Routine also belonged to List/Column placement. Structural relations and normal references also have different placement and access semantics.

### Decision

- Each Task and Event belongs to exactly one List and one Column at a time.
- Routine does not belong to Folder/List/Column and uses its own product area.
- Structural Task/Event parent-child relations require compatible List/Column placement.
- Moving a Parent carries structural descendants; independently moving a child to incompatible placement breaks that structural relation.
- Cycle prevention remains relation-specific rather than a universal rule for every relation type.
- References may cross List/Column contexts when the viewer has valid access.
- If access to a referenced Resource is later revoked, the reference may retain the last title/state the viewer was authorized to see, must indicate that the Resource is no longer accessible, and must not reveal subsequent updates.

### Implications

Structural hierarchy is constrained by placement, while references remain non-structural and authorization-sensitive.

---

## DR-114 — Intrinsic delete/completion cascades use Parent authority, while move cascades require authority over every affected Resource

**Status:** CONFIRMED

### Context and previous model

Parent actions can affect descendants. The product already defines delete and completion cascades, but the authorization rule for those consequences differed from the rule needed for moving a hierarchy between organizational locations.

### Decision

- Valid permission to delete a structural Parent is sufficient for the Parent's intrinsic delete cascade over its structural descendants.
- Valid permission to `Done` a Parent is sufficient for the intrinsic `Done` cascade defined for its descendants; the same applies to the optional `Won't_Do` cascade when that setting is enabled.
- These cascades do not grant general or persistent permission over descendants.
- Move is different: because it changes each affected Resource's organizational placement, the actor must have the required move authority for every Resource whose placement changes.
- A destructive cascade must disclose its affected scope and receive explicit confirmation before execution.
- Any multi-Resource consequence that cannot be applied consistently must fail atomically; partial application is not allowed.

### Implications

Authorization and domain consistency are evaluated according to the semantics of each action rather than through one universal relation rule.


## DR-115 — Timed and all-day scheduling preserves real instants across Account timezone changes

**Status:** CONFIRMED

### Context and previous model

Dotick previously distinguished local calendar dates and timed values, but the cross-client behavior of timezone changes was not fully defined. Treating a timezone change as a request to preserve the old local clock/date would move the real moment represented by existing Items.

### Decision

- Every timed Task/Event refers to a real instant independently of Sharing.
- Each Account has one effective timezone. The initial value is proposed from the device, while the User may override it manually.
- A later device-timezone change does not silently rewrite Account timezone; Dotick asks whether the Account timezone should also change.
- Changing Account timezone changes local presentation but does not move already-established Item instants.
- An all-day Item is converted from its selected Calendar Day in the effective scheduling timezone into the corresponding real start/end interval. Later timezone changes preserve that interval even if its local representation spans different calendar dates or clock times.
- Timed recurrence likewise preserves the real occurrence instants when Account timezone changes. Re-anchoring future occurrences to a new local clock requires an explicit schedule edit.

### Required engineering analysis

The owning Time Semantics specification must explicitly analyze real instants, Calendar Day, Dotick Day, `occurrence_date`, credited/effective date, all-day intervals, Account/device timezone, timezone changes, DST, Jalali/Gregorian recurrence, leap/invalid dates and boundary/finalization behavior. Comprehensive test vectors and edge-case tests are required for these interactions; they are not optional implementation detail.

### Implications

Account timezone is product state rather than merely a client display preference. Storage and recurrence implementation remain Design concerns, but implementations must preserve the same real temporal meaning.

---

## DR-118 — Trash applies to recoverable Resources with 30-day automatic retention and explicit permanent deletion

**Status:** CONFIRMED

### Decision

- Folder, List, Task, Event, Routine, Group, Comment, and Tag can enter Trash.
- Column and RoutineCompletion do not use the general Trash lifecycle. Goal remains governed by its AI-managed lifecycle rather than general Trash.
- Trash retention is 30 days and permanent deletion may happen automatically after the retention window.
- User can explicitly permanently delete an eligible Resource before the retention window expires.
- Delete offers immediate Undo.
- Restoring a deleted container restores its recoverable subtree and structure when available.
- Restoring a Task/Event whose original placement no longer exists falls back to Inbox and its default Column.
- Permanent deletion removes operational Resource state while the required audit/history of prior change activity remains.

---

## DR-121 — Notification delivery is category-configurable and interaction state is synchronized across devices

**Status:** CONFIRMED

### Decision

- Users can independently configure major notification categories such as reminders/alarms, comments/mentions, Group/Sharing/invitations, Nudge/collaboration interactions, and gamification/motivational notifications.
- Dotick provides an in-app Notification Center for workflow/collaboration notifications that require application-level review or action, including invitations and accept/reject flows.
- Ordinary Item Reminder history is intentionally not shown in that Notification Center and is delegated to OS/push notification presentation.
- Notification interaction state is synchronized across devices for all notification types.
- A final interaction on one device prevents later delivery of the same original notification on other devices, including devices that reconnect later.
- Snooze/remind-later is not final acknowledgement; it schedules a new notification that can again be delivered to all eligible devices.

---

## DR-122 — Failure handling distinguishes local-first operations from server-authoritative operations

**Status:** CONFIRMED

### Decision

- Failure must not create silent data loss, false success, or partially applied domain state.
- Offline-capable actions continue locally and may show valid local success while awaiting synchronization.
- Validation failure preserves the previous valid domain state and, where practical, retains User input so it can be corrected.
- Online-only operations such as Sharing/Invitation do not show local success when server outcome is unknown or failed.
- If an online-only operation has uncertain outcome because connectivity was interrupted, the client re-verifies authoritative server state before presenting final success.
- Atomic multi-Resource operations either complete fully or do not apply.
- User-facing errors explain the product-level problem without requiring exposure of raw infrastructure/provider failures.

---

## DR-123 — AI failures preserve prior semantic state and pause Ring-dependent streak evaluation when no valid Ring can be generated

**Status:** CONFIRMED

### Decision

- AI failure remains isolated from core manual/offline productivity behavior.
- In multi-proposal AI Item Creation, valid proposals remain reviewable even if sibling proposals fail validation; invalid proposals fail independently.
- Goal Discovery, semantic review, or AI Tag failure leaves the last valid Goal/Tag state unchanged until a valid later result exists.
- Daily Ring generation has no reduced-quality deterministic fallback in Current Scope when required AI is unavailable.
- If required AI/system dependency prevents a valid Ring from being generated, the Dotick Day and core app still operate, but Ring generation waits for AI availability.
- While no evaluable Ring exists solely because of this system/AI failure, Global Streak is paused: it neither increments nor resets.
- Once a valid Ring exists and the User has a real opportunity to complete it, ordinary Global Streak rules apply.

### Implications

Provider routing, retries, timeouts and fallback-provider selection remain Design concerns and cannot change these product semantics.

---

## DR-126 — Effective view access is sufficient for AI context; Users can globally disable external AI processing

**Status:** CONFIRMED

### Context and previous model

Dotick already restricts AI context by authorization, but it was not explicit whether data merely shared with a User could be sent to an external AI provider, or whether AI processing required ownership or a separate permission. The product also had feature-specific AI controls without a single account-level switch for external AI processing.

### Decision

For Current Scope:

- Any Resource/field the acting User is currently authorized to **view** may be used as context by an AI capability that is otherwise allowed to use that context, including data shared by another User.
- Ownership is not required for AI context use.
- AI context selection must still respect effective authorization and field visibility; hidden or revoked data must not be sent merely because some other part of the Resource is visible.
- AI processing does not create a new authorization path and cannot expand the User's access.
- The User has a global control to disable external AI processing.
- When global external AI processing is disabled, AI-assisted Item Creation, Goal Discovery/AI Tag processing, and Daily Ring capabilities that require AI are disabled/unavailable.
- Core Task/Event/Routine management, organization, collaboration, offline-capable operations, and other non-AI capabilities remain usable.
- Feature-specific disable behavior, such as Goal-discovery cleanup/lifecycle rules, continues to apply when the global control disables that feature.

For the current pre-public baseline, Dotick does not yet impose a product-level requirement on external provider training use or retention policy for submitted data. That policy must be revisited before public release, but it is intentionally not a Current-Scope pre-public constraint.

### User acknowledgement for external processing

Before external AI processing is enabled/used for the Account, Dotick must present a clear acknowledgement that authorized context—including data shared with the User when it is within effective field visibility—may be transmitted to third-party AI infrastructure. External-AI use requires acceptance of this processing boundary. Provider retention/training behavior and contractual allocation of third-party data-processing risk belong to the applicable Privacy Policy/Terms rather than being silently inferred from the product specification.

### Implications

- Authorization and field-visibility enforcement must occur before external AI context is constructed.
- Shared data is not automatically excluded from AI processing merely because the acting User is not its owner.
- Public-release privacy/provider requirements require a later release/security decision rather than being silently assumed now.

---

## DR-128 — External delivery and integration responsibilities remain narrow; STT is implementation-neutral and productivity/agent integrations remain Future Scope

**Status:** CONFIRMED

### Context and previous model

Section 9 of the System Definition needs one consistent rule for several external dependencies that are easy to conflate: email/SMS transport, OS/push delivery, Speech-to-Text, calendar/productivity integrations, and future external agents. A broad statement that "external services are Future Scope" would be incorrect because some external delivery/inference infrastructure is already part of Current Scope.

### Decision

- Email verification and password-reset semantics are owned by Dotick. An external email provider, if used, only transports the message; token/state validity and Account changes remain Dotick responsibilities.
- Invitation messages sent through email or, when supported, phone/SMS follow the same boundary: transport is external, while recipient matching, invitation state, acceptance, and authorization changes remain Dotick-controlled.
- Notification/push delivery through supported OS/push infrastructure is Current Scope. Dotick owns notification meaning, recipient, category, trigger, and interaction state; external infrastructure only performs delivery/display within platform constraints.
- Speech-to-Text in the Voice creation flow is implementation-neutral at the System Definition level and may be local, platform-provided, or external. The transcription method must not redefine downstream AI-assisted Item Creation semantics.
- Google Calendar, Notion, TickTick, and other direct calendar/productivity integrations remain Future Scope. No current one-way/two-way sync behavior is implied.
- External AI agents and voice assistants remain Future Scope. If introduced later, their access must be explicitly user-authorized, resource/capability-scoped, revocable, and auditable. They must not receive unrestricted general-purpose access merely because an integration surface exists.

### Implications

- External dependency does not automatically mean Future Scope; scope depends on the delegated capability.
- Delivery providers are not sources of truth for Dotick workflow state.
- Vendor/protocol choice remains Design unless a later product constraint explicitly fixes it.

---

## DR-130 — Current security quality baseline requires at-rest protection and auditable administrator access without adding a separate 2FA factor

**Status:** CONFIRMED

### Context and previous model

The existing security baseline already required secure network transport, credential hashing, authorization isolation and unrestricted Platform Administrator authority. It did not yet state whether stored operational replicas require at-rest protection, whether administrator reads of private data are auditable, whether Current Scope adds TOTP/SMS-based 2FA, or whether offline use has a fixed product-level expiry.

### Decision

- Server-side user data, operational backups and client local replicas must use appropriate encryption/protection at rest for their environment. Exact algorithms, key management and storage mechanisms belong to Security Design.
- Platform Administrator authority remains unrestricted at the product level, but both state-changing administrative actions and administrator access to User-private data must be traceable through administrative audit.
- Current Scope does not require a separate TOTP or SMS-based second-factor feature beyond the confirmed Email/Password, Google and Passkey authentication baseline.
- Previously authenticated offline use does not have a fixed `N-day` expiry defined by product semantics. Security/session design may require revalidation for server-dependent operations or on reconnect, but mere elapsed offline time must not arbitrarily invalidate the supported local working set at a fixed product-defined threshold.

### Implications

- At-rest protection is a product security expectation without locking the implementation to a specific cryptographic/storage design.
- Full administrator authority is compatible with accountability rather than invisible privileged access.
- A future TOTP/SMS 2FA capability requires a separate scope decision.
- Session hardening may evolve without redefining the offline-first product principle.

---

## DR-131 — Disaster recovery, manual data export, and recoverable account deletion are Current-Scope data-protection behaviors

**Status:** CONFIRMED

### Context and previous model

Dotick already protects individual Items through Trash/history and requires recovery-aware sync, but catastrophic server/database loss and full Account deletion were not defined. The product also lacked a direct User-facing way to obtain a portable copy of the User's own data.

### Decision

- Server-side user data must have backup/recovery suitable for disaster or infrastructure failure. Exact backup frequency, retention, RPO/RTO and restore procedure belong to Operations/Security Design.
- A User can manually request/export the User's own Dotick data in a portable, machine-readable form. The exact format and attachment packaging are Design concerns. Scheduled export, automatic third-party backup destinations and import/restore from that export are not Current-Scope requirements.
- A User can request Account deletion.
- Account deletion enters a **30-day recovery window**. During this period, the User can cancel deletion and recover the Account.
- After the recovery window, the Account and personal operational data owned by that User are permanently removed from active persistence.
- Direct Sharing does not change ownership; therefore User-owned resources do not become immortal merely because another User had access to them.
- Group-owned resources or data owned by another entity/User do not disappear merely because their original creator deletes an Account.
- Audit/history required to preserve integrity for other Users may remain with minimal identity or in anonymized form after Account deletion.
- Disaster-recovery backup retention after active deletion is an Operations/Security concern, but deleted data must not silently return to ordinary active product state outside a controlled recovery policy.

### Implications

- Account deletion is a lifecycle distinct from ordinary Item Trash even though both currently use a 30-day recovery window.
- Export is a portability capability, not a promise of full backup/restore tooling.
- Ownership rules continue to determine what survives deletion.

---

## DR-133 — Current UI language is English while Persian user content is supported with language-sensitive typography

**Status:** CONFIRMED

### Context and previous model

Calendar support for Jalali/Gregorian does not determine interface language. The product had no explicit Current-Scope localization boundary even though Users may create content in Persian.

### Decision

- The Dotick product interface/chrome in Current Scope is English.
- Full UI localization into Persian or other languages is not a Current-Scope requirement.
- User-generated textual content may contain Persian as well as English in applicable fields such as titles, descriptions, comments and notes.
- Presentation must be able to choose typography/font treatment appropriate to the displayed content language so Persian and English content are rendered with suitable fonts.
- Exact font families, language detection and typography implementation belong to UI/UX Design.

### Implications

- UI language and content-language capability are separate concerns.
- Jalali calendar support does not imply Persian UI localization.
- Storage and presentation must not impose an English-only content character set.

---

## DR-135 — Notification permission controls delivery only; reminders do not accumulate in the in-app Notification Center

**Status:** CONFIRMED

### Context and previous model

Dotick supports OS/browser push delivery and an internal Notification Center. It was necessary to distinguish loss of delivery permission from disabling the underlying Reminder/Notification behavior and to prevent the internal inbox from becoming a second reminder-history system.

### Decision

- Denying or revoking browser/OS notification permission does not disable the underlying Reminder/Notification domain behavior or other Dotick capabilities.
- When external notification presentation is not permitted, the delivery step simply cannot show that message outside the application.
- Missed ordinary Item Reminders/alarms are not accumulated in the in-app Notification Center as a fallback inbox.
- The in-app Notification Center is for application-level workflow/messages such as sharing and Group membership requests, invitations, review/action flows, and relevant product/system updates.
- Dotick may expose current permission state and a platform-supported path to request permission again.

### Implications

- Notification state and notification delivery are separate concepts.
- A platform permission failure must not mutate Task/Event/Routine state.
- Notification Center storage must not be designed as a duplicate reminder archive.

---

## DR-136 — Attachment binaries use a device-local cache with global policy and Folder/List overrides

**Status:** CONFIRMED

### Context and previous model

Offline-first requires Item metadata and core state to remain usable locally, but keeping every Attachment binary on every device forever would create uncontrolled storage growth. Familiar cloud-media products use local retention and cache-size policies while preserving the remote copy; Dotick needs the same principle adapted to Folder/List organization.

### Decision

- Attachment metadata can remain in the local working set even when the binary is not stored on that device.
- A file selected/uploaded from a device remains locally openable from its existing local copy while that copy is present; it does not require an immediate round-trip download.
- Another device downloads the binary when needed unless its local auto-download policy has already fetched it.
- Attachment cache is device-local.
- User controls must support a device-wide default for automatic download, cache retention including `keep indefinitely`, and maximum local cache size.
- User can override cache policy for a specific Folder or List; the more specific applicable policy takes precedence.
- Cache cleanup/eviction removes only the local binary and never deletes the server-side Attachment, its metadata or its relation to the Item.
- An evicted/missing binary can be downloaded again when connectivity is available.
- A Resource remains usable offline even if one of its non-local Attachment binaries cannot currently be opened.

### Open design boundary

Exact attachment categories, cache accounting, eviction ordering, quota handling and storage APIs are Offline/Storage Design concerns.

---

## DR-140 — Profile Picture is Account identity presentation, not a public social profile

**Status:** CONFIRMED

### Context and previous model

Dotick intentionally excludes general social-network behavior from Current Scope, including public profiles, public feeds, follower graphs and public discovery unrelated to collaboration. At the same time, collaboration flows benefit from a recognizable visual identity so Users can distinguish recipients, members, commenters and assignees.

### Decision

- A Registered Personal User may have an optional `Profile Picture` on the Account.
- Profile Picture is Account identity-presentation data, alongside Display Name and username/handle.
- It may be displayed wherever Dotick legitimately presents that User's identity, including collaboration discovery results, Share/Group requests, Group member lists, Comments, Assignment and similar collaboration contexts.
- A Profile Picture does not create a standalone Public Profile, follower/following relationship, public feed, social graph or general public-discovery surface.
- Contact identifiers such as email/phone remain subject to the separate discovery privacy rules; showing a Profile Picture does not authorize exposing matched private contact values.

### Implications

- Dotick can provide human-recognizable collaboration identity without becoming a social network.
- Future public/social profile behavior would require a separate canonical product decision.

---

## DR-141 — Out-of-scope capabilities are not automatically Future commitments

**Status:** CONFIRMED — refines DR-064, DR-066, DR-133 and DR-037

### Context and previous model

A Future/Out-of-Scope section can accidentally turn every missing capability into an implied roadmap promise. Several capabilities have been discussed only to define the current boundary, not because they are planned product directions.

### Decision

The following are **not Planned Future Capabilities** under the current product direction and may enter Future Scope only through a new canonical decision:

- general public social-network behavior such as follower graphs, public feeds, standalone public profiles or public content/user discovery unrelated to collaboration;
- supported self-hosting / production deployment by arbitrary end users;
- typed-text AI-assisted Item creation as a direct User input mode; typed User input remains ordinary manual creation;
- a general-purpose public developer API for arbitrary third-party clients;
- full UI localization to Persian or other languages beyond the confirmed English UI baseline;
- an additional TOTP/SMS-based independent 2FA feature beyond the confirmed authentication baseline.

This decision does not prohibit future external text-derived automation inputs such as Email from entering a controlled automation pipeline. Those external-source inputs are separate from direct typed-text AI creation by the User.

External integrations that are promoted in the future must use controlled, permission-based integration surfaces unless a later decision explicitly establishes a broader public API model.

### Implications

- Documentation must distinguish `not current` from `planned future`.
- Architecture must not be burdened with promises to support these capabilities merely because source code, browser technology or existing internal APIs make them technically possible.
- Adding any of these capabilities later is allowed, but requires an explicit product/scope decision rather than being treated as fulfillment of an existing promise.

---

## DR-142 — Commercialization is possible but billing/subscription is not yet a product commitment

**Status:** CONFIRMED AS SCOPE BOUNDARY

### Context and previous model

Billing, subscription and payment behavior are outside Current Scope. Describing them simply as Future Scope could imply that Dotick has already committed to a specific commercial model even though pricing, licensing, packaging and monetization have not been decided.

### Decision

- Dotick may become a commercial product in the future.
- The monetization model is currently undecided.
- Subscription, billing, payment, license enforcement, pricing tiers and related commercial transaction flows are not Current-Scope requirements and are not Planned Future Capabilities until a separate Business/Product decision selects a model.
- Current architecture must not assume a specific monetization mechanism as a product invariant.

### Implications

Commercial strategy can evolve without rewriting core productivity semantics. If billing or licensing becomes real scope, its account, entitlement, payment-provider and failure semantics require their own canonical decisions.

---

## DR-143 — Accessibility is a Future product-quality direction, with exact conformance deferred

**Status:** CONFIRMED AS FUTURE CAPABILITY

### Context and previous model

Current Scope does not yet establish a formal accessibility baseline or a specific WCAG/conformance level. Completely omitting accessibility from future direction, however, would make it easy for a mature/public product to defer it indefinitely.

### Decision

Accessibility is a Future product-quality direction for a more mature/public Dotick release. Expected areas include, where applicable:

- keyboard-accessible interaction;
- meaningful screen-reader semantics;
- scalable/readable text;
- adequate contrast and non-color-only communication of important state.

No specific standard version, conformance level, browser matrix or acceptance threshold is fixed by the current System Definition. The owning future UX/Quality specification must define those measurable requirements before they become release acceptance criteria.

### Implications

- Accessibility is intentionally future, not a Current-Scope acceptance requirement.
- Current implementation should avoid gratuitous design choices that make later accessibility work structurally impossible, without prematurely imposing an undefined compliance target.

---

## DR-144 — Section 13 tracks only intentionally unspecified Current-Scope design/tuning details

**Status:** CONFIRMED

### Context and previous model

The System Definition contains a final section for `Open Questions / Intentionally Unspecified Details`. Without an explicit boundary, that section could become a mixed backlog containing unresolved product questions, Enterprise/Future design topics, implementation details and tuning parameters. That would conflict with the document rule that Current-Scope product/domain behavior must already be resolved before it is treated as canonical.

### Decision

Section 13 of the System Definition is limited to **Current-Scope** details whose product behavior is already defined but whose exact implementation, representation, algorithm, coefficient, threshold or tuning remains intentionally delegated to an owning Design/Specification artifact.

It must not include:

- unresolved Product/Domain decisions;
- Enterprise-only design details;
- Future capability implementation details;
- speculative ideas merely because they are not implemented yet.

If a genuine Current-Scope Product/Domain question appears, the alternatives/rationale may be analyzed in this Register, but the resulting behavior becomes canonical only when recorded in the appropriate behavioral section of the System Definition; this Register and the SRS are then reconciled to that current state. Future/Enterprise uncertainty remains with the corresponding Future Scope and future design work rather than Section 13.

### Implications

- Section 13 is a bounded handoff to Design/Tuning, not a product backlog.
- A Current-Scope implementation must not silently choose behavior that Section 13 intentionally leaves at implementation/tuning level.
- Future and Enterprise details do not clutter the Current-Scope unspecified-detail inventory.

---

# Decision coverage and remaining design handoff

## Current Product/Domain decision state

No unresolved Current-Scope Product/Domain decision remains from the current review pass. The current Register body contains consolidated decisions only: when one concept evolved through several intermediate records, the final reasoning and behavior were merged into the surviving canonical DR rather than retaining contradictory old/current entries side by side.

The repository revision history remains the historical source for previous wordings and intermediate alternatives.

## Current-Scope matters delegated to owning Design/Specification

The following are **not Product/Domain OPEN decisions**. Their behavior is already fixed by the System Definition and the relevant DR; the exact implementation, representation, algorithm or tuning must be completed in the owning engineering artifact:

- Description/ContentBlock physical schema, ordering, serialization and edit storage.
- Structural-child/dependency/reference relation schema and indexing.
- Recurrence rule serialization, series/occurrence persistence, exception/override representation and scheduler implementation.
- Sync metadata, device identity, trusted ordering/clock strategy, idempotency, tombstones and relation/block conflict representation.
- Branching History persistence and its compatibility with immutable Audit evidence and Sync operation/version metadata.
- `TIME_SEMANTICS_SPEC.md` representation and comprehensive test vectors for real instant, Calendar Day, Dotick Day, `occurrence_date`, credited/effective date, all-day interval, timezone/DST and Jalali/Gregorian recurrence interaction.
- Daily Ring scoring coefficients/formula, late-day recovery and hidden-bonus tuning.
- RingGroup/DailyAction persistence, rule serialization and replan concurrency.
- Exact Goal-selection algorithm/weights, learning parameters, AI Goal warm-up duration and numeric Goal-similarity thresholds.
- Adaptive Norm thresholds/windows and motivational-message/reminder rate tuning.
- Incremental-Routine inactivity threshold and decay curve.
- API endpoint/payload/versioning design per owning Increment.
- Email/phone normalization plus verification-code format, expiry, retry/rate-limit and anti-abuse mechanics.
- Attachment cache accounting/eviction/quota/platform-storage implementation.
- Encryption-at-rest algorithms/key management, backup/restore parameters and manual-export packaging.
- Session hardening, account-linking and credential-recovery mechanics.
- Service-managed AI routing/retry/timeout, BYOK credential protection and exact STT/provider integration.
- PWA service-worker/install/offline-storage/browser matrix and best-effort reminder delivery before full native alarm integration.
- Notification transport/provider/device-registration/retry implementation.
- AI prompt/model-specific evaluation and tuning parameters.

If engineering analysis exposes a genuinely new Product/Domain question, it must first be reflected through the System-Definition-first decision workflow before implementation silently chooses a behavior.