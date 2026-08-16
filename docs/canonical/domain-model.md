# Dotick — Working Domain Model

> **وضعیت:** Canonical Working Domain Model  
> این فایل مدل مفهومی، entityها، relationها، فیلدهای فعلی، state machineها و constraintهای شناخته‌شده را ثبت می‌کند. این فایل schema نهایی PostgreSQL یا ORM mapping نیست.

---

# 1. نمای کلی Domain

```text
User
│
├── UserPreferences
│
├── Folder
│   └── List
│       └── Column
│
├── Item
│   ├── Routine
│   └── Schedulable
│       ├── Task
│       └── Event
│
├── Goal
├── Tag
├── RoutineCompletion
├── DailyRing
│   └── DailyRingItem
├── AuditLog
├── GoalGenerationLog
└── AIItemCreationSession
```

Shared capability:

```text
TrackingState
├── used by Routine
└── used by Goal
```

`Goal` خارج از درخت `Item` است.

---

# 2. Base identity و metadata

## 2.1 Item

فیلدهای مشترک پیشنهادی فعلی:

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

### نکته

`status` از Item حذف شده است؛ status بین همه‌ی subclassها مشترک نیست.

---

# 3. Schedulable

Task و Event رفتار زمانی/Description مشترک دارند.

```text
Schedulable extends Item
```

فیلدهای مفهومی:

```text
source: Source
start_at: DateTime/AllDayDate representation
end_at: DateTime | null
priority: Priority
description: RichDescription
```

Task در application layer می‌تواند `start_at` را با نام `due_at` نمایش دهد.

## 3.1 Parent relation

Hierarchy باید مستقیم queryable باشد.

مدل target فعلی برای ساختار single-parent:

```text
parent_id: UUID | null -> Schedulable
```

اما:

- Task: حداکثر یک structural parent.
- Event: چند reference مجاز است.
- `OPEN`: multi-parent ساختاری Event هنوز قطعی نشده.

اگر Event multi-parent واقعی لازم شود، `parent_id` به‌تنهایی کافی نیست و relation table لازم خواهد شد.

## 3.2 Index expectation

حداقل expectation مفهومی:

```text
INDEX(parent_id)
```

و بسته به query patterns:

```text
INDEX(column_id, parent_id)
```

schema نهایی بعداً تعیین می‌شود.

---

# 4. Task

```text
Task extends Schedulable
```

## 4.1 Fields

```text
due_at: alias/domain-name of Schedulable.start_at
end_at: DateTime | null
deadline_at: DateTime | null
grace_period_days: Integer >= 0
dependencies: TaskDependencySet
status: TaskStatus
```

## 4.2 TaskStatus

```text
Todo
Overdue
Missed
Done
Won't_Do
Skipped
```

## 4.3 State rules

```text
now < due_at
    => Todo

due_at passed && deadline not passed
    => Overdue

deadline passed && grace > 0 && grace boundary not passed
    => Missed

deadline passed && grace == 0
    => Skipped directly

deadline + grace passed
    => Skipped
```

`Skipped` system-controlled است.

## 4.4 Dependency

```text
TaskDependencySet
- blocked_by_ids: List<UUID(Task)>
```

Cycle validation در design/test specification باید اضافه شود.

---

# 5. Event

```text
Event extends Schedulable
```

Fields:

```text
start_at
end_at | null
location: Location | null
status: EventStatus
```

EventStatus:

```text
Not_Arrived
Ongoing
Finished
```

Event می‌تواند sub-event داشته باشد و هر sub-event اطلاعات مستقل خود را نگه دارد.

Event می‌تواند در Descriptionهای متعدد reference شود.

---

# 6. Source

Ownership از Source جدا است.

```text
Source
- platform: SourcePlatform
- external_account: String | null
- external_id: String | null
```

SourcePlatform examples:

```text
Manual
Google_Calendar
Email
Notion
TickTick
Other
```

`owner_user_id` و `created_by_user_id` برای identity داخلی استفاده می‌شوند.

---

# 7. Priority

```text
Priority
- Urgent_Important
- Important
- Urgent
- None
```

Priority روی Task/Event برای organization، scoring و ranking استفاده می‌شود.

Priority سند/Feature دیگر بخشی از specification نیست.

---

# 8. Description

## 8.1 RichDescription

```text
RichDescription
- content_blocks: Ordered List<ContentBlock>
```

## 8.2 ContentBlock capabilityها

انواع لازم:

```text
TextBlock
AttachmentBlock
LocationBlock
ItemReferenceBlock
```

Text capability:

```text
Bold
Italic
Underline
Strikethrough
Heading
Highlight
Bullets
Numbers
Indent
Separator
Code
Quote
link/phone/id recognition
```

## 8.3 Identity

برای comment/reorder/sync، ContentBlock باید identity پایدار داشته باشد.

حداقل concept:

```text
block_id: UUID
block_type
data
position/order metadata
```

schema دقیق OPEN است.

## 8.4 Item reference semantics

`ItemReferenceBlock` می‌تواند Task/Event را نمایش دهد.

backend باید بداند آیا reference در آن context نماینده‌ی:

- structural child relation
- normal reference

است.

این تفاوت لازم نیست به دو control مجزا در UI تبدیل شود.

---

# 9. Comment Model

حداقل نیاز مفهومی:

```text
Comment
- id
- author_user_id
- target_item_id
- target_block_id | null
- body
- created_at
- updated_at
```

اگر `target_block_id = null` باشد comment متعلق به کل Task/Event است.

اگر block مشخص باشد، comment باید هم در context block و هم در thread کلی دیده شود.

permission model نهایی با Group/ACL design تکمیل می‌شود.

---

# 10. Routine

```text
Routine extends Item
uses TrackingState
```

Routine از Schedulable ارث نمی‌برد.

## 10.1 Fields

```text
start_date: Date | null
end_date: Date | null
target_goal: RoutineTarget
recurrence_rule: RoutineRecurrence
reminders: ReminderConfig
tags: relation<Tag>
tracking_state: TrackingState
```

Routine **status ندارد**.

## 10.2 RoutineTarget

```text
RoutineTarget
- type: Achieve_All | Partial
```

Partial:

```text
metric:
  period: Daily | Weekly | Monthly | Yearly
  fix_amount: Number
  is_incremental: Boolean
  increment_amount: Number | null
  unit: Count | Cup | Liter | Minute | Hour | Meter | Kilometer | Page | Step | Custom
```

## 10.3 Incremental target

فرمول retained فعلی:

```text
current_target ≈ fix_amount + qualifying_completions * increment_amount
```

جزئیات دقیق اینکه کدام completion در افزایش target مؤثر است و reset پس از inactivity هنوز نیاز به formalization دارد.

---

# 11. TrackingState

`Trackable` به‌جای الزام به inheritance دیتابیسی، به‌عنوان shared capability/state دیده می‌شود.

```text
TrackingState
- current_streak: Integer
- best_streak: Integer
- total_completions: Integer
- ai_quote: String | null
- illustration_url: String | null
```

Used by:

```text
Routine
Goal
```

در implementation می‌تواند composition، embedded object یا table اشتراکی باشد؛ تصمیم storage باز است.

---

# 12. RoutineCompletion

Source of truth نتیجه‌ی یک Routine در یک روز.

```text
RoutineCompletion
- id: UUID
- routine_id: UUID -> Routine
- occurrence_date: Date
- status: RoutineCompletionStatus
- amount: Number | null
- note: Text | null
- created_at: DateTime
- updated_at: DateTime
- version: Integer
```

Status:

```text
Done
Won't_Do
```

Constraint:

```text
UNIQUE(routine_id, occurrence_date)
```

`completed_at` از مدل business حذف شده است.

Audit timestamps از `created_at`/`updated_at` و AuditLog قابل بازیابی‌اند.

## 12.1 Reset behavior

Reset:

```text
DELETE current RoutineCompletion row
KEEP AuditLog entry
```

## 12.2 Unscheduled date

`occurrence_date` لازم نیست حتماً scheduled date باشد.

User می‌تواند manually یک unscheduled date را Done کند.

---

# 13. Recurrence Model

یک Recurrence Object مشترک با capability restrictions.

## 13.1 Calendar

```text
Jalali
Gregorian
```

تمام month/year/day calculations باید نسبت به calendar انتخاب‌شده انجام شوند؛ `last_day` نیز باید در همان calendar resolve شود.

## 13.2 Task/Event supported granularity

```text
Minute interval
Hour interval
Day interval
Week recurrence
Month recurrence
Year recurrence
Advanced combined expression
```

## 13.3 Routine supported granularity

```text
Day
Week
Month
Year
```

Routine occurrence به زمان دقیق داخل روز نیاز ندارد.

## 13.4 Recurrence categories retained

```text
Constant
Dynamic/Interval
Advanced
```

Constant:

```text
Daily
Weekly
Monthly
Yearly
```

Dynamic/Interval:

```text
every x minutes
every x hours
every x days
every x weeks on selected weekdays
every x months on selected days / last_day
every x years on selected month/day
```

Advanced:

```text
combined minutes + hours + days expression
```

نمونه config نهایی هنوز OPEN است.

---

# 14. Routine Streak Semantics

## 14.1 Fixed-day

Streak sequence از completionهای معتبر تشکیل می‌شود، ولی missed scheduled occurrence sequence را می‌شکند.

Extra unscheduled completion:

- valid completion است.
- missed occurrence قبلی را جبران نمی‌کند.
- می‌تواند sequence جدید را شروع/ادامه دهد.

## 14.2 Frequency-based

برای `N times per period`، completion در هر روز period قابل قبول است تا quota پر شود.

مدل exact streak برای عبور بین periodها OPEN است.

---

# 15. Folder / List / Column

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

`Tab` و `Section` alias مفهومی قدیمی Column هستند و نباید entity جدید بسازند.

هر List یک Column پیش‌فرض برای Itemهای بدون Column explicit دارد. نام legacy آن `not_sectioned` است؛ نام فنی لزوماً در UI نمایش داده نمی‌شود.

Relation واقعی Item به List/Column باید در schema نهایی مشخص شود.

---

# 16. Tag

```text
Tag
- id: UUID
- title: String
- source: User | AI
- goal_id: UUID | null -> Goal
- archive_status: Active | Archived   // عمدتاً برای AI tags
- created_at
- updated_at
```

Relation Item-Tag many-to-many است.

Goal-Tag one-to-many فعلی است.

---

# 17. Goal

```text
Goal
- id
- created_at
- updated_at
- version
- title
- description | optional/current design
- tracking_state: TrackingState
- archive_status
- list_id
- column_id | null
- tags
```

ArchiveStatus:

```text
Active
Dormant
Archived
```

Lifecycle semantics:

- `Dormant`: Goal فعلاً Item فعال معنادار مرتبط با progress خود (Task/Event/Routine) ندارد؛ از Daily Ring selection خارج می‌شود و streak آن freeze می‌شود، نه reset.
- `Archived`: Goal تاریخی/superseded است و به‌صورت خودکار re-activate نمی‌شود.

## 17.1 Streak definition

```text
current_streak
= consecutive Dotick Days where Goal DailyRing was completed

total_completions
= count of all completed Goal days
```

---

# 18. GoalGenerationLog

Append-only.

```text
GoalGenerationLog
- id
- goal_id
- event_type:
    Initial_Generation
    Weekly_Review
    Reactivation_Check
- ai_model_used
- changed
- previous_title | null
- new_title | null
- previous_description | null
- new_description | null
- user_rating | null
- created_at
```

User rating فقط وقتی تغییر واقعی رخ داده relevant است.

---

# 19. DailyRing

یک snapshot از انتخاب یک Goal برای یک Dotick Day.

```text
DailyRing
- id: UUID
- user_id: UUID
- goal_id: UUID
- effective_date: Date
- target_value / target_score: Number
- progress_percent: Number [0..100]
- is_completed: Boolean
- final_score: Number | null
- is_finalized: Boolean
- selection_reason_metadata: JSON/Object | optional
- algorithm_version: String | null
- created_at
- finalized_at | null
```

Constraint مفهومی:

```text
UNIQUE(user_id, effective_date, goal_id)
```

و business rule:

```text
count(active rings per day) = min(3, eligible_active_goals)
```

اگر eligible goals >= 3، count دقیقاً 3 است.

---

# 20. DailyRingItem

Snapshot عضویت Item در Ring همان روز.

```text
DailyRingItem
- id
- daily_ring_id
- item_id
- item_type: Task | Event | RoutineOccurrence
- base_score
- priority_weight
- urgency_weight
- timing_weight
- difficulty_estimate
- expected_effort
- progress_contribution_rule
- snapshot_payload | optional
```

هدف snapshot:

- تاریخ گذشته با تغییر فیلدهای امروز بازنویسی نشود.
- تحلیل score همان روز قابل بازسازی باشد.

## 20.1 Credit rule

Completion فقط Ringی را جلو می‌برد که Item در `DailyRingItem` آن روز عضو باشد.

---

# 20.1 Daily target / Norm

Daily Ring target manually set by user نیست. سیستم آن را بر اساس recent performance و capacity تعیین می‌کند.

این state می‌تواند derived باشد یا snapshot metadata داشته باشد؛ schema نهایی OPEN است.

رفتار:

```text
Repeated misses -> temporary target reduction
Recovery -> gradual return
Repeated success -> gradual target increase
New data -> updated norm
```

# 21. Goal Progress و Score

## 21.1 Progress

```text
progress_percent: 0..100
```

UI هرگز >100 نشان نمی‌دهد.

## 21.2 Completion flag

```text
is_completed = progress_percent >= 100
```

## 21.3 Final score

```text
final_score >= 0
```

می‌تواند بالاتر از 100/baseline باشد.

Bonusهای early completion و اهمیت بالا در score اثر دارند.

Bonus until day finalization hidden است.

فرمول دقیق OPEN.

---

# 22. UserPreferences / Dotick Day

```text
UserPreferences
- user_id
- timezone
- day_boundary_offset_minutes | null
- ...
```

اگر `day_boundary_offset_minutes` null باشد:

- default ambiguity window = 60 minutes.
- completionهای 00:00 تا 01:00 با سؤال Today/Yesterday attribution می‌گیرند.

اگر explicit باشد، attribution خودکار است.

## 22.1 Credited date

برای completion/scoring باید مفهوم effective/credited date وجود داشته باشد، حتی اگر timestamp واقعی بعد از midnight باشد.

محل دقیق ذخیره‌ی credited date بسته به type completion در design نهایی تعیین می‌شود.

---

# 23. Day Finalization

Domain event مفهومی:

```text
DailyBoundaryReached(user, effective_date)
```

Responsibilities:

```text
Finalize previous DailyRings
Compute final_score
Reveal bonus
Finalize Goal streak state
Generate next DailyRings
```

در default unset mode، boundary فعلی 01:00 local است.

---

# 24. Statistics / Derived Data

Raw/source entities:

```text
Task/Event state changes
RoutineCompletion
DailyRing / DailyRingItem
AuditLog
```

Derived entities/cacheها می‌توانند شامل:

```text
WeeklyStats
MonthlyStats
RecentBehaviorFeatures
LifetimeAggregates
```

Update strategy:

```text
Affected window only
Increment/decrement simple counters
Local streak recomputation
Async refresh expensive behavior features
```

Full-history recomputation برای هر edit ممنوع/نامطلوب است مگر در maintenance jobs.

---

# 25. AuditLog

Generic conceptual model:

```text
AuditLog
- id
- actor_user_id
- entity_type
- entity_id
- action
- previous_value / diff
- new_value / diff
- occurred_at
- source/device metadata | optional
```

اهداف:

- history
- reset trace
- undo support
- sync troubleshooting

Append-only ترجیحی است.

---

# 26. AIItemCreationSession

```text
AIItemCreationSession
- id
- user_id
- source_type: Text | Voice | Email | ...
- original_input
- normalized_transcript | null
- ai_proposal_payload
- user_final_payload | null
- field_level_changes | null
- model_version
- accepted: Boolean | null
- created_at
- finalized_at | null
```

این entity برای:

- review flow
- debugging
- evaluation
- personalization آینده

مفید است.

Item واقعی فقط پس از confirm ساخته می‌شود.

---

# 27. ReminderConfig

مفهوم فعلی:

```text
ReminderConfig
- reminders: List<ReminderRule>
```

```text
ReminderRule
- trigger_before_minutes
- is_persistent
```

AI می‌تواند draft این rules را پیشنهاد دهد.

---

# 28. Location

Location باید بتواند حداقل این شکل‌ها را پوشش دهد:

```text
coordinates
human-readable address
place identifier
virtual meeting link
```

representation دقیق در design بعدی.

---

# 29. Group / Role / Assignment

Conceptual entities:

```text
Group
GroupMembership
SystemRole
TaskAssignment
```

Current scope:

- User can belong to multiple groups.
- Membership has a system-defined role.
- Task can be assigned to multiple members.
- CustomRole entity در current version لازم نیست.

Future enterprise:

- Custom roles
- richer permissions
- org hierarchy
- multi-tenancy

---

# 30. Sync Metadata

Entities قابل sync حداقل نیاز دارند:

```text
version
updated_at / field timestamps strategy
soft-delete where relevant
```

Baseline conflict strategy retained:

```text
Field-level Last-Write-Wins
```

اگر per-field timestamps لازم شوند، storage detail در Sync Design مشخص خواهد شد.

---

# 31. Class hierarchy vs Database inheritance

این Domain Model نباید با Class Table Inheritance قبلی یکی فرض شود.

تصمیم فعلی:

- inheritance بالا **مفهومی** است.
- اینکه PostgreSQL tableهای `items`, `schedulables`, `tracking_states` داشته باشد یا composition/denormalization بهتری استفاده شود هنوز OPEN است.
- هدف schema نهایی: query ساده، integrity بالا، migration قابل کنترل و performance مناسب.

---

# 32. Known constraints و validationهای لازم در طراحی بعدی

مواردی که باید formal validation شوند:

- Task title non-empty.
- Event title non-empty.
- Routine title non-empty.
- parent relation cycle ممنوع.
- dependency cycle policy.
- due/end/deadline ordering.
- recurrence validity within Routine start/end date.
- RoutineCompletion unique per day.
- DailyRing max/exact count rule.
- archived/dormant Goal selection rules.
- AI draft validation قبل از confirm.
- group data isolation.
- timezone/day-boundary consistency.

---

# 33. Open domain decisions

1. Event multi-parent structural relation یا single-parent + multi-reference.
2. storage schema ContentBlock.
3. exact generic relation model child/reference.
4. DailyRing scoring formula.
5. difficulty/effort representation.
6. global user streak entity.
7. frequency-routine streak formal model.
8. incremental Routine inactivity reset.
9. exact ownership of Folder/List/Column در group contexts.
10. storage inheritance strategy.
11. exact field-level sync metadata.

