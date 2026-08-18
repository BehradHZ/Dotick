# Dotick — Decision Register

> **Status:** Canonical Decision History  
> **Purpose:** This document records Dotick's product, domain, and engineering baseline decisions in a self-contained manner. Each Decision Record must be understandable without needing to read another document: it first explains the problem statement and the previous model/assumption, then states the reason it was insufficient, and finally records the current decision, its implications, and open boundaries.

## Status definitions

- `CONFIRMED`: The current decision is definitive and must be the basis for subsequent documents and implementation.
- `RETAINED`: The decision has been kept from the previous baseline, and there is no sufficient reason in the current analysis to change it.
- `OPEN`: The problem is known, but a final solution has not yet been chosen; implementation must not implicitly close it.
- `SUPERSEDED`: The decision is historical and no longer determines current behavior.
- Phrases such as `IN CONCEPT`, `IN PRODUCT BEHAVIOR`, or `AS FUTURE CAPABILITY` specify the scope of certainty; that is, the principle of the decision is definitive, but design/timing details may remain open.

## Reading rule

The Decision Register maintains the history of "why." Behavioral and design documents may later reference DRs to avoid duplication, but each DR itself must sufficiently explain the problem, the previous option/model, the reason for the change, and the outcome.

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

### Open boundary

`N times per period` routines have different semantics, and their exact streak still needs to be formalized separately.

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

## DR-015 — Task has at most one structural parent

**Status:** CONFIRMED

### Context and previous model

Because a Task can be viewed or mentioned in different contexts, the possibility of a multi-parent structure was also raised. These two concepts—"being a true member of the hierarchy" and "being seen in multiple places"—could have been conflated.

### Why true multi-parent Task hierarchy was not good enough

For Task, true multiple parents complicate navigation, ownership of position, cycle detection, and delete/move behavior, while the need to "display in multiple contexts" can be solved with a reference.

### Decision

Each Task has at most one structural parent.

A Task can be referenced in other contexts, but a reference does not create a new structural parent.

### Implications

- The main Task tree is deterministic.
- The UI can mention a Task elsewhere without changing the hierarchy.
- The exact parent target type/storage will be determined in the final design.

---

## DR-016 — Event may be referenced in multiple Descriptions; structural multiplicity remains open

**Status:** CONFIRMED for references / OPEN for structural multiplicity

### Context and previous model

An Event may be related to several Task/Event/Descriptions; for example, a meeting may be seen in several project contexts. The second question is whether this same Event can truly be the structural child of multiple parents, or have only one true parent.

### Why collapsing both questions was not good enough

Multi-reference is a simple linking need, but multi-parent structure has a much greater effect on navigation, delete/move semantics, permissions, and the data model. Finalizing one should not unintentionally impose the other.

### Decision

It is confirmed that an Event can be referenced in multiple Descriptions.

### Open boundary

It has not yet been finalized whether Event:

1. has only one structural parent + multiple references, or
2. has multiple true structural parents.

Until this decision is closed, implementation must not implicitly assume true multi-parent.

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
- The exact threshold/scoring definition is still closed in the Gamification design.

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

## DR-031 — An Item advances only the Daily Ring snapshot that selected it for the credited day

**Status:** CONFIRMED

### Context and previous model

If Goal and Item are related via Tag, the simplest implementation was for the completion of any Item tagged to a Goal, whenever performed, to increase that Goal's progress.

### Why global tag-based credit was not good enough

The Daily Ring is a daily, limited selection. If any related Item could give progress outside the day's selection, the day's selection snapshot becomes meaningless, and the user could fill the Ring with work outside the plan.

### Decision

A completion only advances a Ring if:

1. the completion belongs to the same `credited/effective_date`; and
2. the Item is a member of that Ring's `DailyRingItem` snapshot.

### Implications

- The Tag relation is an eligibility/semantic relation, not automatic daily credit.
- An Item outside that day's snapshot does not advance the daily Goal.

---

## DR-032 — DailyRing and DailyRingItem are historical snapshots

**Status:** CONFIRMED

### Context and previous model

Daily Ring could have been recomputed each time from the current state of the Goal/Items; in that case, if an Item's priority, due date, tags, or difficulty changed later, the history of previous days would effectively also change.

### Why live recomputation of history was not good enough

The user and analytics must be able to understand "what the system selected that day and why." A future change must not rewrite a past decision. This also matters for algorithm debugging and trust.

### Decision

DailyRing and its membership/scoring inputs are snapshotted into DailyRingItem for each Dotick Day.

Ordinary future field changes do not rewrite the historical snapshot.

### Implications

- The snapshot must retain enough data/metadata to reconstruct the meaning of the day.
- Explicit historical corrections require a separate policy and are not the same as ordinary Item edits.

---

## DR-033 — Dotick Day is distinct from Calendar Day

**Status:** CONFIRMED

### Context and previous model

The simple day model is based on midnight to midnight. For a user who still finishes "yesterday's" tasks after midnight, this boundary can record completion and streak on the wrong day.

### Why strict calendar-day semantics were not good enough

Everyday behavior does not always align with 00:00. A task at 00:30 might, from the user's perspective, be the end of the previous day's plan. Calendar day alone does not show the user's intent.

### Decision

The system has an independent `Dotick Day` concept, and the day boundary can be user-configurable.

### Implications

- Completion/scoring needs a `credited/effective_date`.
- The scheduler/day finalization must consider the user's timezone and boundary.
- The default behavior is defined in DR-034.

---

## DR-034 — Without an explicit boundary, the default ambiguity window is one hour after midnight

**Status:** CONFIRMED

### Context and previous model

When the user has not set a personal day boundary, there were two extreme options: count all completions after midnight as the new day, or attribute a fixed hidden boundary such as 01:00 to the previous day without user input.

### Why both extremes were not good enough

The first option loses late-night intent; the second might incorrectly attribute a real early-morning completion to yesterday. In the absence of an explicit preference, the system must expose the ambiguity.

### Decision

If the user has no explicit boundary:

- The default ambiguity window is from 00:00 to 01:00 local time.
- A completion within this window gets attribution via a `Today` / `Yesterday` choice.

### Implications

- The 01:00 default boundary applies for finalization in the unset state.
- If the user sets an explicit boundary, automatic attribution follows that same boundary.

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

## DR-036 — Historical corrections use selective recomputation, not default full-history rebuilds

**Status:** CONFIRMED

### Context and previous model

With historical edits allowed, the simplest correctness approach was to recompute all of the user's statistics and streak history from the beginning after every change.

### Why full-history recomputation was not good enough

As data grows, this approach creates unnecessary cost and latency, and a small edit from five weeks ago could involve the entire history. Also, many metrics are incremental or window-local.

### Decision

A historical change only invalidates/recomputes the affected metric(s)/window(s).

Example:

- Simple counters are incremented/decremented;
- The affected week/month is refreshed;
- The streak is recomputed locally within the necessary range;
- Expensive features can be refreshed asynchronously.

### Implications

Full-history recomputation is usable only for specific maintenance/recovery, not as the default behavior for every edit.

---

## DR-037 — AI-assisted Item creation is a general draft pipeline, not only Speech-to-Task

**Status:** CONFIRMED

### Context and previous model

The initial feature was envisioned as Speech-to-Task: the user speaks, and the system creates a Task. As the vision expanded, it became clear the same analysis/mapping is also useful for text and, later, email/external inputs.

### Why a voice-specific feature was not good enough

If business logic becomes dependent on voice, duplicate pipelines would need to be built for Text, Email, or integrations. Voice is just one input modality; intent extraction and draft creation capability are more general.

### Decision

A general AI-assisted creation pipeline is defined:

```text
Input (Text / Voice / future external source)
-> normalization
-> intent/entity inference
-> editable draft
-> review
-> confirm
-> real Item
```

### Implications

- Text and Voice are current scope.
- Email/external sources are future scope.
- STT is only a preprocessing stage for Voice, not a core domain feature.

---

## DR-038 — Voice input belongs next to normal Item creation where practical

**Status:** CONFIRMED

### Context and previous model

Voice creation could have been a separate page/feature. But the user's intent is the same "create Item," just with a different input modality.

### Why a separate voice silo was not good enough

Separating Voice from the create flow would complicate navigation and feature learning, and would hide the shared pipeline from DR-037 in the UI.

### Decision

Wherever the user creates an Item, a microphone/voice option can be placed next to the create input in the appropriate UIs.

### Implications

- Voice must reach the same draft/review flow.
- Platforms without microphone capability can offer only the text flow.

---

## DR-039 — AI draft should infer all reasonably derivable Item fields

**Status:** CONFIRMED

### Context and previous model

AI could have extracted only title and date, leaving the rest of the form to the user. But natural user examples usually contain more information, such as location, event type, and reminder intent.

### Why minimal extraction was not good enough

If the model ignores information present in the input, the assistant's value decreases, and the user is forced to manually re-enter the same information.

### Decision

When derivable, AI proposes at least the following:

- Task/Event type
- title
- date/time
- location
- description
- Folder/List/Column
- reminders
- other inferable fields

### Implications

All fields are proposals and must have appropriate provenance/validation. AI must not display a field with false certainty.

---

## DR-040 — AI output is a reviewable draft; real Item creation requires user confirmation

**Status:** CONFIRMED

### Context and previous model

A frictionless experience could have let AI directly create a Task/Event immediately after analyzing voice/text.

### Why direct creation was not good enough for current scope

AI can incorrectly infer type, date, location, or reminder. Direct creation of real data causes clutter, missed appointments, or corrective edits, and reduces user control.

### Decision

AI first creates a Draft/Proposal. The user sees all details in a review UI, can change them, and the real Item is only created after `Confirm`.

### Implications

- Cancel/reject must not leave a real Item behind.
- Trusted automation, if added in the future, requires a separate decision.

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
- The confirmation policy for trusted auto-actions is still OPEN.
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

## DR-047 — Offline sync baseline is field-level Last-Write-Wins until Sync Design formalizes metadata

**Status:** RETAINED

### Context and previous model

For offline-first, the conflict-resolution baseline was defined as field-level LWW. The simpler alternative was record-level LWW, where a small edit could overwrite an independent change from another device.

### Why record-level LWW was not good enough

If device A changes the title and device B changes the reminder, record-level LWW might discard one of the two independent changes. The field-level strategy allows better merging of independent edits.

### Decision

Current baseline:

```text
Conflict unit: field
Resolution baseline: Last-Write-Wins per field
```

### Open boundary

Timestamp/clock strategy, field metadata, relation conflicts, deletes, ContentBlock granularity, and idempotency are still OPEN in Sync Design.

---

## DR-048 — Authentication baseline includes email/password, Google OAuth, JWT, and Passkey

**Status:** RETAINED

### Context and previous model

The product needs reliable personal login, and Google sign-in alone creates an external dependency. At the same time, Passkey and OAuth provide a better experience and more security options.

### Decision

Personal V1 authentication baseline includes:

- Email/password
- Google OAuth
- JWT-based session/token model
- Passkey

If Google is unavailable, email/password must be an active fallback.

Enterprise SSO is future scope.

### Open boundary

The exact Enterprise SSO protocol (SAML/OIDC) and session-hardening details are determined at the relevant design/security stage.

---

## DR-049 — Global daily streak is not yet a confirmed current requirement

**Status:** OPEN / RETAINED FROM LEGACY

### Context and previous model

An old rule defined a global streak as follows: if the user completes at least one Daily Ring in a day, the global streak continues. Later, the Goal-level streak was refined so that its condition became the actual completion of that same Goal.

### Why the legacy global rule is questionable

When a user has three Rings, completing only one Ring to maintain the global streak may be inconsistent with, or too easy relative to, the philosophy of meaningful daily progress. On the other hand, completely removing the global streak might eliminate a useful motivational layer.

### Current decision state

No final decision has been made to keep, redesign, or remove the global daily streak.

### Required future decision

Before gamification implementation, it must be determined:

- Does a global streak exist?
- If so, what is the condition for its continuation?
- What message/behavior does breaking it have?

Until then, the "at least one Ring" rule must not be treated as a definitive requirement.

---

## DR-050 — Derived/reference documents may be reconciled, but canonical authority remains separate

**Status:** CONFIRMED

### Context and previous model

At the start of the documentation rebuild, the conservative policy was for the original SRS and Class Fields to remain untouched and be kept only as legacy/source material, because overwriting them could destroy history and raw information. At the same time, System Definition, Domain Model, and the Decision Register formed as working canonical sources.

Later, a new problem arose: if derived/reference documents were never updated, known contradictions within them would remain active, and any reader or AI could again interpret superseded wording as current behavior.

### Why the previous "never overwrite/reconcile" policy was not good enough

Preserving history is valuable, but keeping an incorrect current requirement in a reference file costs more. Historical wording can remain in the revision history, while a file's current body must not directly contradict canonical decisions.

### Decision

Derived/reference documents **can, and when necessary must,** be reconciled during consistency passes, without their authority rising above canonical sources.

Authority order:

```text
Confirmed Decision Register entry
        ↓
System Definition
        ↓
Domain Model
        ↓
Formal/Derived SRS and reference documents
        ↓
Historical legacy wording
```

Rules:

- The reference SRS can be rewritten/formalized.
- Class Fields is a derived field reference, not a physical DB schema or architecture.
- An `OPEN` decision must not be implicitly closed for the sake of making files consistent; wording must remain OPEN/neutral.
- Important history is preserved in the revision history or decision records.

### Implications

"Preserving history" and "preventing active contradiction" are both necessary; history must not be confused with keeping an outdated current requirement.

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

# Decision backlog and resolution status

The following items still require a final decision. Their presence in the backlog does not mean an option has been chosen.

1. **Event structural multiplicity** — one structural parent + multiple references, or true multi-parent.
2. **Description/ContentBlock exact schema** — storage, ordering, serialization, and edit model.
3. **Backend child/reference relation schema** — the exact representation of a structural relation versus a normal reference.
4. **Exact Daily Ring scoring formula** — progress contribution, final score, early reward, and late-day recovery.
5. **Difficulty/effort model** — representation and estimation strategy.
6. **Global daily streak** — confirm, redesign, or remove; along with motivational/scolding behavior.
7. **Frequency-based Routine streak semantics** — `N times per period`, quota, and streak across periods.
8. **Incremental Routine inactivity reset** — defining qualifying completion and reset/no-reset after inactivity.
9. **AI Goal warm-up duration**.
10. **Goal similarity thresholds** — reactivation/merge/archive behavior.
11. **Exact Goal selection algorithm** — weights, balance, and adaptation/learning.
12. **API endpoint design** — per owning Increment.
13. **Sync metadata design** — per-field timestamps/clock/device/idempotency/conflicts.
14. **Trusted automation confirmation policy** — review vs. auto-action for future external sources.
15. **Enterprise SSO protocol** — SAML/OIDC in Enterprise scope.

## Resolved backlog item

- **Database inheritance/storage strategy** — resolved for Personal V1 by DR-052.

---

# Register integrity note

In one of the intermediate revisions, two old decisions were removed from the beginning of the Register, and the numbering of subsequent DRs shifted. At the same time, some documents still referenced the old numbers. To avoid breaking existing references again, this version does not renumber the current DR-001 through DR-052. The document authority/reconciliation policy is fully stated in DR-050, and the decision to remove Feature Priority, which had fallen out of the Register, has been restored as DR-053.

Until all canonical/reference documents have undergone a final consistency pass, **the content of the Decision Record itself is more important than the historical reference number**. After the entire document set is stabilized, a separate pass can be done to canonicalize cross-reference IDs.
