# Dotick Requirements Traceability Matrix

**Document type:** Requirements Traceability Matrix

**Version:** 1.0

**Baseline date:** 2026-08-17

**Status:** Increment 0 Traceability Baseline

**Scope:** Personal V1

> این سند مسیر `Canonical Source -> Formal Requirement -> Planned Increment` را ثبت می‌کند. Traceability منبع رفتار یا تصمیم جدید نیست. اگر behavior تغییر کند، ابتدا منبع canonical و Formal SRS اصلاح می‌شوند و سپس این ماتریس update می‌شود.

# 1. Purpose and authority

این baseline مطابق Increment 0 در Roadmap ایجاد شده است. منابع authority به ترتیب زیرند:

```text
Confirmed Decision Register entry
        ->
System Definition
        ->
Domain Model
        ->
Formal SRS
        ->
traceability-matrix.md
```

`project-docs/02-requirements/traceability-matrix.md` فقط رابطه بین artifactها را ثبت می‌کند و نمی‌تواند یک `OPEN` decision را ببندد یا requirement جدید بسازد.

# 2. Source key

| Code | Document | Role |
|---|---|---|
| `DR` | `project-docs/decision-register.md` | confirmed, retained, open and superseded decisions |
| `SD` | `project-docs/02-requirements/system-definition.md` | current product behavior and scope |
| `DM` | `project-docs/03-design/domain-model.md` | conceptual entities, relations and constraints |
| `SRS` | `project-docs/02-requirements/srs.md` | formal testable requirements |
| `RM` | `project-docs/01-planning/increment-roadmap.md` | increment ownership, decision gates and document lifecycle only |

# 3. Increment key

| Code | Increment |
|---|---|
| `I0` | Formal Specification + Engineering Baseline |
| `I1` | Identity + Folder/List/Column + Basic Task MVP |
| `I2` | Complete Schedulable Domain: Task + Event + Hierarchy + Description + Comments |
| `I3` | Routine + RoutineCompletion + TrackingState |
| `I4` | Recurrence Engine + Routine Streak Semantics + Reminders + Time Semantics |
| `I5` | Product Navigation, Views, Responsive UI & Themes |
| `I6` | Offline-first Sync + History + Undo + Selective Recovery |
| `I7` | Groups + System Roles + Assignment + Realtime |
| `I8` | AI-Assisted Item Creation: Text + Voice Draft/Review |
| `I9` | Goal + AI Tagging + Semantic Discovery + Goal Lifecycle |
| `I10` | Daily Rings + Dotick Day + Scoring + Norm + Statistics |
| `I11` | Personal V1 Production Readiness & Deployment |

# 4. Baseline coverage summary

- Formal SRS normative requirements traced: **257**.
- Every normative requirement has at least one canonical source mapping.
- Every normative requirement has a planned owning Increment or a staged multi-Increment ownership.
- Formal SRS decision records traced: **25**؛ از این تعداد **24** مورد باز و `OPEN-021` با DR-054 resolved است.
- Analysis، test-case، implementation و release linkها تا ایجاد artifact واقعی ثبت نمی‌شوند. Design baselineهای موجود در §5.1 trace شده‌اند.

## 4.1 Planned ownership counts

این جدول تعداد requirementها را بر اساس label فعلی ownership نشان می‌دهد. Requirementهای cross-Increment یک بار و با همان label ترکیبی شمرده شده‌اند.

| Planned ownership | Requirement count |
|---|---:|
| `I0` | 4 |
| `I0 baseline + I1 implementation` | 4 |
| `I0 baseline + I7 implementation` | 1 |
| `I1` | 23 |
| `I1 + I2` | 1 |
| `I1-I3` | 1 |
| `I2` | 47 |
| `I2 + I4` | 1 |
| `I2-I3` | 1 |
| `I3` | 24 |
| `I3 + I5` | 1 |
| `I3 + I6` | 1 |
| `I4` | 23 |
| `I5` | 12 |
| `I6` | 9 |
| `I7` | 9 |
| `I7 + I11 validation` | 1 |
| `I8` | 14 |
| `I8 + I11 validation` | 1 |
| `I9` | 26 |
| `I10` | 52 |
| `I11` | 1 |

# 5. Detailed requirement traceability

`Verification` از Formal SRS گرفته شده است. ستون `Planned Increment` محل اصلی طراحی/پیاده‌سازی requirement را طبق Roadmap نشان می‌دهد. در requirementهای چندمرحله‌ای، ownership ترکیبی ثبت شده است.

| Requirement ID | SRS section | Canonical source(s) | Planned Increment | Verification | Requirement |
|---|---|---|---|---|---|
| `SRS-ORG-001` | 3.1 سازمان‌دهی، Inbox و navigation | SD §3; DR-003; DM §15 | `I1` | Test | سیستم باید ساختار سازمانی `Folder > List > Column` را پشتیبانی کند. |
| `SRS-ORG-002` | 3.1 سازمان‌دهی، Inbox و navigation | SD §3; DR-003; DM §15 | `I1` | Test | سیستم باید یک محل پیش‌فرض با مفهوم `Inbox` برای Itemهایی داشته باشد که کاربر هنگام ایجاد، محل مشخصی برای آن‌ها انتخاب نکرده است. |
| `SRS-ORG-003` | 3.1 سازمان‌دهی، Inbox و navigation | SD §3; DR-003; DM §15 | `I1` | Test | هر List باید یک Column پیش‌فرض برای Itemهای بدون Column صریح داشته باشد. |
| `SRS-ORG-004` | 3.1 سازمان‌دهی، Inbox و navigation | SD §3; DR-003; DM §15 | `I1` | Test + Inspection | اگر Column پیش‌فرض تنها Column یک List باشد، سیستم نباید کاربر را مجبور به مشاهده نام فنی legacy آن، یعنی `not_sectioned`، کند. |
| `SRS-ORG-005` | 3.1 سازمان‌دهی، Inbox و navigation | SD §3; DR-003; DM §15 | `I1` | Inspection | سیستم نباید `Tab` یا `Section` را به عنوان entity مستقل از Column مدل کند. |
| `SRS-ORG-006` | 3.1 سازمان‌دهی، Inbox و navigation | SD §3; DR-003; DM §15 | `I5` | Test + Inspection | سیستم باید دسترسی به Folderها، Listها و ورودی روزانه یا Today را در navigation اصلی فراهم کند. |
| `SRS-ITEM-001` | 3.2 Item، identity، ownership و source | SD §§4-5; DR-014; DR-015; DM §§2, 6 | `I1-I3` | Test | سیستم باید Task، Event و Routine را به عنوان سه نوع اصلی محتوای user-facing پشتیبانی کند. |
| `SRS-ITEM-002` | 3.2 Item، identity، ownership و source | SD §§4-5; DR-014; DR-015; DM §§2, 6 | `I1` | Test | هر Item باید یک شناسه پایدار داشته باشد و زمان ایجاد و آخرین ویرایش آن قابل ثبت باشد. |
| `SRS-ITEM-003` | 3.2 Item، identity، ownership و source | SD §§4-5; DR-014; DR-015; DM §§2, 6 | `I1` | Test | هر Item باید title غیرخالی داشته باشد. |
| `SRS-ITEM-004` | 3.2 Item، identity، ownership و source | SD §§4-5; DR-014; DR-015; DM §§2, 6 | `I1` | Test | سیستم باید soft-delete را برای Itemهایی که `is_trashed` دارند پشتیبانی کند. |
| `SRS-ITEM-005` | 3.2 Item، identity، ownership و source | SD §§4-5; DR-014; DR-015; DM §§2, 6 | `I1` | Test + Inspection | سیستم باید version metadata لازم برای Itemهای sync‌شونده را نگه دارد. |
| `SRS-ITEM-006` | 3.2 Item، identity، ownership و source | SD §§4-5; DR-014; DR-015; DM §§2, 6 | `I1` | Test | سیستم باید `owner_user_id` و `created_by_user_id` را به صورت دو مفهوم مستقل نگه دارد. |
| `SRS-ITEM-007` | 3.2 Item، identity، ownership و source | SD §§4-5; DR-014; DR-015; DM §§2, 6 | `I1` | Test | سیستم باید provenance را از ownership جدا نگه دارد. `Source` نباید مبنای تشخیص مالک داخلی باشد. |
| `SRS-ITEM-008` | 3.2 Item، identity، ownership و source | SD §§4-5; DR-014; DR-015; DM §§2, 6 | `I1` | Test | در Task/Event، Source باید حداقل platform و در صورت وجود external account و external id را قابل ثبت کند. |
| `SRS-ITEM-009` | 3.2 Item، identity، ownership و source | SD §§4-5; DR-014; DR-015; DM §§2, 6 | `I2-I3` | Test + Inspection | `status` نباید یک property مشترک برای همه Itemها باشد. Task و Event status مستقل دارند و Routine status ندارد. |
| `SRS-ITEM-010` | 3.2 Item، identity، ownership و source | SD §§4-5; DR-014; DR-015; DM §§2, 6 | `I2 + I4` | Test | سیستم باید Tag، recurrence و reminder را به عنوان capabilityهای قابل اتصال به Item، مطابق محدودیت هر نوع Item، پشتیبانی کند. |
| `SRS-TASK-001` | 3.3 Task | SD §6; DR-012; DR-013; DM §4 | `I1` | Test | سیستم باید ایجاد، بازیابی، ویرایش و soft-delete Task را پشتیبانی کند. |
| `SRS-TASK-002` | 3.3 Task | SD §6; DR-012; DR-013; DM §4 | `I2` | Test | Task باید بتواند بدون زمان دقیق به صورت all-day تعریف شود. |
| `SRS-TASK-003` | 3.3 Task | SD §6; DR-012; DR-013; DM §4 | `I2` | Test | اگر `end_at` وجود نداشته باشد، `due_at` باید یک due moment واحد را بیان کند. |
| `SRS-TASK-004` | 3.3 Task | SD §6; DR-012; DR-013; DM §4 | `I2` | Test | اگر `end_at` وجود داشته باشد، `due_at` باید شروع duration Task باشد. |
| `SRS-TASK-005` | 3.3 Task | SD §6; DR-012; DR-013; DM §4 | `I2` | Test | Task باید بتواند `deadline_at` مستقل از `due_at` داشته باشد. |
| `SRS-TASK-006` | 3.3 Task | SD §6; DR-012; DR-013; DM §4 | `I2` | Test | وقتی deadline وجود دارد، Task باید `grace_period_days` با مقدار غیرمنفی داشته باشد. |
| `SRS-TASK-007` | 3.3 Task | SD §6; DR-012; DR-013; DM §4 | `I2` | Test | سیستم باید statusهای `Todo`, `Overdue`, `Missed`, `Done`, `Won't_Do` و `Skipped` را برای Task پشتیبانی کند. |
| `SRS-TASK-008` | 3.3 Task | SD §6; DR-012; DR-013; DM §4 | `I2` | Test | قبل از عبور از due، Task باید در حالت `Todo` باشد مگر اینکه کاربر آن را به یک نتیجه user-driven منتقل کرده باشد. |
| `SRS-TASK-009` | 3.3 Task | SD §6; DR-012; DR-013; DM §4 | `I2` | Test | پس از عبور از due و پیش از deadline، یا وقتی deadline وجود ندارد، Task انجام‌نشده باید `Overdue` شود. |
| `SRS-TASK-010` | 3.3 Task | SD §6; DR-012; DR-013; DM §4 | `I2` | Test | پس از عبور از deadline و در صورتی که grace بزرگ‌تر از صفر باشد، Task انجام‌نشده باید تا پایان grace در حالت `Missed` قرار گیرد. |
| `SRS-TASK-011` | 3.3 Task | SD §6; DR-012; DR-013; DM §4 | `I2` | Test | اگر `grace_period_days = 0` باشد، Task انجام‌نشده باید هنگام عبور از deadline مستقیما `Skipped` شود و state قابل مشاهده `Missed` نداشته باشد. |
| `SRS-TASK-012` | 3.3 Task | SD §6; DR-012; DR-013; DM §4 | `I2` | Test | پس از عبور از `deadline + grace period`، Task انجام‌نشده باید `Skipped` شود. |
| `SRS-TASK-013` | 3.3 Task | SD §6; DR-012; DR-013; DM §4 | `I2` | Test | `Skipped` باید system-controlled باشد و کاربر نباید آن را مستقیما انتخاب کند. |
| `SRS-TASK-014` | 3.3 Task | SD §6; DR-012; DR-013; DM §4 | `I1 + I2` | Test | کاربر باید بتواند Task را به صورت دستی `Done` یا `Won't_Do` کند. |
| `SRS-TASK-015` | 3.3 Task | SD §6; DR-012; DR-013; DM §4 | `I2` | Test | Task باید بتواند با `blocked_by` به Taskهای دیگر وابسته باشد. |
| `SRS-TASK-016` | 3.3 Task | SD §6; DR-012; DR-013; DM §4 | `I2` | Test | Task باید priorityهای `Urgent_Important`, `Important`, `Urgent` و `None` را پشتیبانی کند. |
| `SRS-EVENT-001` | 3.4 Event | SD §7; DR-018; DM §5 | `I2` | Test | سیستم باید ایجاد، بازیابی، ویرایش و soft-delete Event را پشتیبانی کند. |
| `SRS-EVENT-002` | 3.4 Event | SD §7; DR-018; DM §5 | `I2` | Test | Event باید start time یا all-day date داشته باشد و بتواند end time اختیاری داشته باشد. |
| `SRS-EVENT-003` | 3.4 Event | SD §7; DR-018; DM §5 | `I2` | Test | Event باید location اختیاری داشته باشد. |
| `SRS-EVENT-004` | 3.4 Event | SD §7; DR-018; DM §5 | `I2` | Test | Location باید بتواند حداقل coordinates، human-readable address، place identifier یا virtual meeting link را نمایندگی کند. |
| `SRS-EVENT-005` | 3.4 Event | SD §7; DR-018; DM §5 | `I2` | Test | سیستم باید statusهای `Not_Arrived`, `Ongoing` و `Finished` را برای Event پشتیبانی کند. |
| `SRS-EVENT-006` | 3.4 Event | SD §7; DR-018; DM §5 | `I2` | Test | Event باید بتواند sub-event ساختاری داشته باشد و هر sub-event اطلاعات مستقل خود را نگه دارد. |
| `SRS-EVENT-007` | 3.4 Event | SD §7; DR-018; DM §5 | `I2` | Test | یک Event باید بتواند در چند RichDescription به صورت reference نمایش داده شود. |
| `SRS-EVENT-008` | 3.4 Event | SD §7; DR-018; DM §5 | `I2` | Test | Event باید priorityهای `Urgent_Important`, `Important`, `Urgent` و `None` را پشتیبانی کند. |
| `SRS-HIER-001` | 3.5 hierarchy ساختاری و reference | SD §8; DR-016..DR-019; DM §3 | `I2` | Test + Analysis | hierarchy ساختاری Task و Event باید از طریق relation مستقیم قابل query باشد و بازیابی آن نباید به parse کامل RichDescription وابسته باشد. |
| `SRS-HIER-002` | 3.5 hierarchy ساختاری و reference | SD §8; DR-016..DR-019; DM §3 | `I2` | Inspection | relation ساختاری باید برای query و index شدن قابل طراحی باشد. |
| `SRS-HIER-003` | 3.5 hierarchy ساختاری و reference | SD §8; DR-016..DR-019; DM §3 | `I2` | Test | یک Task نباید بیش از یک structural parent داشته باشد. |
| `SRS-HIER-004` | 3.5 hierarchy ساختاری و reference | SD §8; DR-016..DR-019; DM §3 | `I2` | Test | سیستم باید cycle در parent relation ساختاری را رد کند. |
| `SRS-HIER-005` | 3.5 hierarchy ساختاری و reference | SD §8; DR-016..DR-019; DM §3 | `I2` | Test | backend باید structural child را از normal reference تشخیص دهد. |
| `SRS-HIER-006` | 3.5 hierarchy ساختاری و reference | SD §8; DR-016..DR-019; DM §3 | `I2` | Inspection + Test | frontend نباید صرفا به دلیل تفاوت داخلی child و reference مجبور به ارائه دو workflow پیچیده و مستقل شود. |
| `SRS-DESC-001` | 3.6 RichDescription و ContentBlock | SD §9; DR-020; DR-021; DM §8 | `I2` | Test + Inspection | Description در Task و Event باید block-based باشد. |
| `SRS-DESC-002` | 3.6 RichDescription و ContentBlock | SD §9; DR-020; DR-021; DM §8 | `I2` | Test | RichDescription باید TextBlock را با قابلیت Bold، Italic، Underline، Strikethrough، Heading، Highlight، Bullets، Numbers، Indent، Separator، Code، Quote و تشخیص link/phone/id پشتیبانی کند. |
| `SRS-DESC-003` | 3.6 RichDescription و ContentBlock | SD §9; DR-020; DR-021; DM §8 | `I2` | Test | RichDescription باید Attachment، Location و Item reference برای Task/Event را پشتیبانی کند. |
| `SRS-DESC-004` | 3.6 RichDescription و ContentBlock | SD §9; DR-020; DR-021; DM §8 | `I2` | Test | هر ContentBlock باید identity پایدار داشته باشد تا comment، reorder، edit و sync بتوانند همان block را شناسایی کنند. |
| `SRS-DESC-005` | 3.6 RichDescription و ContentBlock | SD §9; DR-020; DR-021; DM §8 | `I2` | Test | تغییر ترتیب blockها نباید identity آن‌ها را از بین ببرد. |
| `SRS-COMMENT-001` | 3.7 Comment | SD §9.1; DM §9 | `I2` | Test | هر Task و Event باید comment thread مربوط به کل Item داشته باشد. |
| `SRS-COMMENT-002` | 3.7 Comment | SD §9.1; DM §9 | `I2` | Test | کاربر مجاز باید بتواند comment را به یک ContentBlock مشخص متصل کند. |
| `SRS-COMMENT-003` | 3.7 Comment | SD §9.1; DM §9 | `I2` | Test | comment متصل به block باید هم در context همان block و هم در thread کلی Item قابل مشاهده باشد. |
| `SRS-COMMENT-004` | 3.7 Comment | SD §9.1; DM §9 | `I2` | Test | سیستم باید author و زمان ایجاد و ویرایش comment را قابل نگهداری کند. |
| `SRS-ROUTINE-001` | 3.8 Routine | SD §10; DR-004..DR-010; DR-022; DM §§10-12 | `I3` | Test | هر Routine باید یک definition واحد باشد و سیستم نباید برای هر روز یک Routine جدید بسازد. |
| `SRS-ROUTINE-002` | 3.8 Routine | SD §10; DR-004..DR-010; DR-022; DM §§10-12 | `I3` | Test + Inspection | Routine نباید Schedulable باشد و نباید status مستقل داشته باشد. |
| `SRS-ROUTINE-003` | 3.8 Routine | SD §10; DR-004..DR-010; DR-022; DM §§10-12 | `I3` | Test | Routine باید `start_date` اختیاری داشته باشد و در صورت نبود آن، اعتبار Routine از تاریخ ایجاد شروع شود. |
| `SRS-ROUTINE-004` | 3.8 Routine | SD §10; DR-004..DR-010; DR-022; DM §§10-12 | `I3` | Test | Routine باید `end_date` اختیاری داشته باشد و در صورت نبود آن، تعریف Routine از نظر validity window بدون پایان باشد. |
| `SRS-ROUTINE-005` | 3.8 Routine | SD §10; DR-004..DR-010; DR-022; DM §§10-12 | `I3` | Test | `end_date` باید تولید occurrenceهای scheduled آینده را پس از آن تاریخ متوقف کند و به تنهایی نباید archive state جدا ایجاد کند. |
| `SRS-ROUTINE-006` | 3.8 Routine | SD §10; DR-004..DR-010; DR-022; DM §§10-12 | `I3` | Test | outcome یک Routine در یک روز باید در `RoutineCompletion` ثبت شود، نه در status خود Routine. |
| `SRS-ROUTINE-007` | 3.8 Routine | SD §10; DR-004..DR-010; DR-022; DM §§10-12 | `I3` | Test | `RoutineCompletion.status` باید `Done` یا `Won't_Do` باشد. |
| `SRS-ROUTINE-008` | 3.8 Routine | SD §10; DR-004..DR-010; DR-022; DM §§10-12 | `I3` | Test | `occurrence_date` باید تاریخ business مربوط به یک RoutineCompletion را مشخص کند. |
| `SRS-ROUTINE-009` | 3.8 Routine | SD §10; DR-004..DR-010; DR-022; DM §§10-12 | `I3` | Test | برای هر زوج `(routine_id, occurrence_date)` فقط یک RoutineCompletion جاری مجاز است. |
| `SRS-ROUTINE-010` | 3.8 Routine | SD §10; DR-004..DR-010; DR-022; DM §§10-12 | `I3` | Test | نبود RoutineCompletion برای یک روز نباید به صورت `Done` یا `Won't_Do` تفسیر شود. |
| `SRS-ROUTINE-011` | 3.8 Routine | SD §10; DR-004..DR-010; DR-022; DM §§10-12 | `I3` | Test | در targetهای Partial، تغییر amount همان روز باید همان RoutineCompletion جاری را update کند. |
| `SRS-ROUTINE-012` | 3.8 Routine | SD §10; DR-004..DR-010; DR-022; DM §§10-12 | `I3` | Test | Reset یک RoutineCompletion باید row جاری همان Routine و occurrence_date را حذف کند. |
| `SRS-ROUTINE-013` | 3.8 Routine | SD §10; DR-004..DR-010; DR-022; DM §§10-12 | `I3` | Test | Reset نباید history مربوط به آن تغییر را از AuditLog حذف کند. |
| `SRS-ROUTINE-014` | 3.8 Routine | SD §10; DR-004..DR-010; DR-022; DM §§10-12 | `I3` | Test | `Won't_Do` باید یک outcome صریح و ماندگار باشد و نباید معادل Reset تلقی شود. |
| `SRS-ROUTINE-015` | 3.8 Routine | SD §10; DR-004..DR-010; DR-022; DM §§10-12 | `I3` | Test | کاربر باید بتواند RoutineCompletion روزهای گذشته را ویرایش کند. |
| `SRS-ROUTINE-016` | 3.8 Routine | SD §10; DR-004..DR-010; DR-022; DM §§10-12 | `I3` | Test | کاربر باید بتواند برای یک روز unscheduled نیز RoutineCompletion معتبر ثبت کند. |
| `SRS-ROUTINE-017` | 3.8 Routine | SD §10; DR-004..DR-010; DR-022; DM §§10-12 | `I4` | Test | recurrence یک Routine باید تعیین کند Routine در چه روزهایی به صورت scheduled پیشنهاد شود، اما نباید ثبت completion در روز دیگر را ممنوع کند. |
| `SRS-ROUTINE-018` | 3.8 Routine | SD §10; DR-004..DR-010; DR-022; DM §§10-12 | `I5` | Test + Inspection | صفحه روزانه Routineها باید scheduled Routineهای روز انتخاب‌شده را به عنوان پیشنهاد اصلی نمایش دهد. |
| `SRS-ROUTINE-019` | 3.8 Routine | SD §10; DR-004..DR-010; DR-022; DM §§10-12 | `I3 + I5` | Test | اگر Routine در یک روز unscheduled به صورت دستی complete شده باشد، completion ثبت‌شده باید در history یا context مربوط به آن روز قابل مشاهده باشد. |
| `SRS-ROUTINE-020` | 3.8 Routine | SD §10; DR-004..DR-010; DR-022; DM §§10-12 | `I5` | Test + Inspection | صفحه اختصاصی Routine باید امکان مشاهده تقویم Routine و ثبت completion دستی در روز unscheduled را فراهم کند. |
| `SRS-ROUTINE-021` | 3.8 Routine | SD §10; DR-004..DR-010; DR-022; DM §§10-12 | `I3` | Test | Routine target باید حداقل `Achieve_All` و `Partial` را پشتیبانی کند. |
| `SRS-ROUTINE-022` | 3.8 Routine | SD §10; DR-004..DR-010; DR-022; DM §§10-12 | `I3` | Test | target نوع `Partial` باید periodهای `Daily`, `Weekly`, `Monthly`, `Yearly`، مقدار پایه، unit و حالت incremental اختیاری را پشتیبانی کند. |
| `SRS-ROUTINE-023` | 3.8 Routine | SD §10; DR-004..DR-010; DR-022; DM §§10-12 | `I3` | Test | unitهای Partial باید حداقل `Count`, `Cup`, `Liter`, `Minute`, `Hour`, `Meter`, `Kilometer`, `Page`, `Step` و `Custom` را پوشش دهند. |
| `SRS-ROUTINE-024` | 3.8 Routine | SD §10; DR-004..DR-010; DR-022; DM §§10-12 | `I3` | Test | TrackingState Routine باید حداقل current streak، best streak و total completions را قابل نگهداری کند. |
| `SRS-ROUTINE-025` | 3.8 Routine | SD §10; DR-004..DR-010; DR-022; DM §§10-12 | `I3` | Test | RoutineCompletion باید شناسه پایدار، `created_at`, `updated_at` و `version` داشته باشد. |
| `SRS-ROUTINE-026` | 3.8 Routine | SD §10; DR-004..DR-010; DR-022; DM §§10-12 | `I3` | Test | RoutineCompletion باید `amount` و `note` اختیاری را پشتیبانی کند. |
| `SRS-ROUTINE-027` | 3.8 Routine | SD §10; DR-004..DR-010; DR-022; DM §§10-12 | `I3` | Test + Inspection | سیستم نباید `completed_at` را به عنوان business identity روز RoutineCompletion استفاده کند؛ `occurrence_date` باید این نقش را داشته باشد. |
| `SRS-ROUTINE-028` | 3.8 Routine | SD §10; DR-004..DR-010; DR-022; DM §§10-12 | `I4` | Test | occurrenceهای scheduled Routine نباید خارج از validity window تعریف‌شده با `start_date` و `end_date` تولید شوند. |
| `SRS-RSTREAK-001` | 3.9 Routine streak | SD §11.2; DR-010; DM §14 | `I4` | Test | در Routine با occurrenceهای fixed-day، completion معتبر scheduled باید در sequence streak قابل شمارش باشد. |
| `SRS-RSTREAK-002` | 3.9 Routine streak | SD §11.2; DR-010; DM §14 | `I4` | Test | missed scheduled occurrence باید sequence streak fixed-day را قطع کند. |
| `SRS-RSTREAK-003` | 3.9 Routine streak | SD §11.2; DR-010; DM §14 | `I4` | Test | completion در روز unscheduled باید completion معتبر باشد، اما نباید missed occurrence قبلی را ترمیم یا جایگزین کند. |
| `SRS-RSTREAK-004` | 3.9 Routine streak | SD §11.2; DR-010; DM §14 | `I4` | Test | completion معتبر پس از break باید بتواند sequence جدید streak را شروع یا ادامه دهد. |
| `SRS-RSTREAK-005` | 3.9 Routine streak | SD §11.2; DR-010; DM §14 | `I4` | Test | Routine از نوع frequency-based باید بتواند quota به شکل `N times per period` داشته باشد و completionهای روزهای مختلف همان period را تا رسیدن به quota بپذیرد. |
| `SRS-RSTREAK-006` | 3.9 Routine streak | SD §11.2; DR-010; DM §14 | `I4` | Test | در Routine از نوع frequency-based، تکمیل quota نباید به fixed weekdayهای از پیش تعیین‌شده وابسته باشد، مگر خود تعریف Routine چنین محدودیتی داشته باشد. |
| `SRS-REC-001` | 3.10 Recurrence | SD §11.1; DR-011; DM §13 | `I4` | Test | سیستم باید recurrence را بر اساس calendar انتخاب‌شده از میان `Jalali` و `Gregorian` محاسبه کند. |
| `SRS-REC-002` | 3.10 Recurrence | SD §11.1; DR-011; DM §13 | `I4` | Test | Task و Event باید recurrence در granularityهای minute، hour، day، week، month و year را پشتیبانی کنند. |
| `SRS-REC-003` | 3.10 Recurrence | SD §11.1; DR-011; DM §13 | `I4` | Test | Task و Event باید advanced combined expression مبتنی بر day/hour/minute را پشتیبانی کنند. |
| `SRS-REC-004` | 3.10 Recurrence | SD §11.1; DR-011; DM §13 | `I4` | Test | Routine باید recurrence روزمحور در granularityهای day، week، month و year را پشتیبانی کند. |
| `SRS-REC-005` | 3.10 Recurrence | SD §11.1; DR-011; DM §13 | `I4` | Test | Routine نباید recurrence دقیقه‌ای، ساعتی یا advanced day/hour/minute داشته باشد. |
| `SRS-REC-006` | 3.10 Recurrence | SD §11.1; DR-011; DM §13 | `I4` | Test | سیستم باید recurrenceهای Constant شامل Daily، Weekly، Monthly و Yearly را پشتیبانی کند. |
| `SRS-REC-007` | 3.10 Recurrence | SD §11.1; DR-011; DM §13 | `I4` | Test | سیستم باید interval recurrence برای هر `x` دقیقه، ساعت، روز، هفته، ماه یا سال را در entityهایی که آن granularity را مجاز می‌دانند پشتیبانی کند. |
| `SRS-REC-008` | 3.10 Recurrence | SD §11.1; DR-011; DM §13 | `I4` | Test | week recurrence باید weekdayهای انتخابی را پشتیبانی کند. |
| `SRS-REC-009` | 3.10 Recurrence | SD §11.1; DR-011; DM §13 | `I4` | Test | month recurrence باید dayهای انتخابی و `last_day` را پشتیبانی کند. |
| `SRS-REC-010` | 3.10 Recurrence | SD §11.1; DR-011; DM §13 | `I4` | Test | year recurrence باید month/day انتخابی را پشتیبانی کند. |
| `SRS-REC-011` | 3.10 Recurrence | SD §11.1; DR-011; DM §13 | `I4` | Test | `last_day` و سایر محاسبات day/month/year باید در همان calendar انتخاب‌شده resolve شوند. |
| `SRS-REC-012` | 3.10 Recurrence | SD §11.1; DR-011; DM §13 | `I4` | Test | validation recurrence باید capability matrix هر entity را enforce کند. |
| `SRS-REM-001` | 3.11 Reminder | SD §12; DM §27 | `I4` | Test | Task، Event و Routine باید بتوانند چند reminder داشته باشند. |
| `SRS-REM-002` | 3.11 Reminder | SD §12; DM §27 | `I4` | Test | هر reminder باید بتواند trigger-before را بیان کند. |
| `SRS-REM-003` | 3.11 Reminder | SD §12; DM §27 | `I4` | Test + Inspection | domain باید intent مربوط به persistent یا alarm-like reminder را مستقل از محدودیت platform نمایندگی کند. |
| `SRS-REM-004` | 3.11 Reminder | SD §12; DM §27 | `I8` | Test | در جریان AI-assisted creation، reminderهای پیشنهادی باید قبل از ایجاد Item قابل مشاهده و ویرایش باشند. |
| `SRS-AUTH-001` | 3.12 Authentication و session | SD §23; DR-050 | `I1` | Test | سیستم باید authentication با email و password را پشتیبانی کند. |
| `SRS-AUTH-002` | 3.12 Authentication و session | SD §23; DR-050 | `I1` | Test + Inspection | سیستم نباید password را به صورت plaintext ذخیره کند و باید از password hashing امن استفاده کند. |
| `SRS-AUTH-003` | 3.12 Authentication و session | SD §23; DR-050 | `I1` | Test | سیستم باید Google OAuth را برای authentication پشتیبانی کند. |
| `SRS-AUTH-004` | 3.12 Authentication و session | SD §23; DR-050 | `I1` | Test | سیستم باید session کاربر را با JWT پشتیبانی کند. |
| `SRS-AUTH-005` | 3.12 Authentication و session | SD §23; DR-050 | `I1` | Test | اگر Google OAuth در دسترس نباشد، مسیر email/password باید برای login قابل استفاده باقی بماند. |
| `SRS-AUTH-006` | 3.12 Authentication و session | SD §23; DR-050 | `I1` | Test | سیستم باید Passkey را برای authentication پشتیبانی کند. |
| `SRS-VIEW-001` | 3.13 Viewها و presentation | SD §§3.1, 28; RM I5 | `I5` | Test | سیستم باید داده یکسان را بدون تغییر domain data در presentationهای مختلف نمایش دهد. |
| `SRS-VIEW-002` | 3.13 Viewها و presentation | SD §§3.1, 28; RM I5 | `I5` | Test + Inspection | صفحه List باید حداقل Viewهای `List`, `Kanban` و `Timeline` را پشتیبانی کند. |
| `SRS-VIEW-003` | 3.13 Viewها و presentation | SD §§3.1, 28; RM I5 | `I5` | Test + Inspection | سیستم باید View یا صفحه مستقل `Calendar` را ارائه کند. |
| `SRS-VIEW-004` | 3.13 Viewها و presentation | SD §§3.1, 28; RM I5 | `I5` | Test + Inspection | سیستم باید صفحه مستقل Routine را ارائه کند. |
| `SRS-VIEW-005` | 3.13 Viewها و presentation | SD §§3.1, 28; RM I5 | `I5` | Test + Inspection | سیستم باید View یا صفحه `Eisenhower / Priority Matrix` را بر پایه priority ارائه کند. |
| `SRS-VIEW-006` | 3.13 Viewها و presentation | SD §§3.1, 28; RM I5 | `I5` | Test + Inspection | رابط کاربری Personal V1 باید responsive و mobile-first باشد. |
| `SRS-VIEW-007` | 3.13 Viewها و presentation | SD §§3.1, 28; RM I5 | `I5` | Inspection | سیستم باید امکان ارائه themeهای `Minimal customizable`, `Liquid Glass`, `Material 3 Expressive inspired` و `Dot-matrix` را در presentation layer داشته باشد. |
| `SRS-SYNC-001` | 3.14 Offline use و sync | SD §22; DR-049; DM §30 | `I6` | Test | سیستم باید core flowهای پشتیبانی‌شده را بدون اتصال اینترنت قابل استفاده نگه دارد. |
| `SRS-SYNC-002` | 3.14 Offline use و sync | SD §22; DR-049; DM §30 | `I6` | Test | تغییرات local پشتیبانی‌شده باید تا زمان reconnect حفظ شوند. |
| `SRS-SYNC-003` | 3.14 Offline use و sync | SD §22; DR-049; DM §30 | `I6` | Test | پس از reconnect، سیستم باید تغییرات local را با server همگام کند. |
| `SRS-SYNC-004` | 3.14 Offline use و sync | SD §22; DR-049; DM §30 | `I6` | Test | conflict resolution baseline باید در سطح field اعمال شود، نه فقط در سطح record کامل. |
| `SRS-SYNC-005` | 3.14 Offline use و sync | SD §22; DR-049; DM §30 | `I6` | Test | اگر یک field در چند replica تغییر کرده باشد، baseline conflict policy باید Field-level Last-Write-Wins بر مبنای metadata زمانی تعریف‌شده باشد. |
| `SRS-SYNC-006` | 3.14 Offline use و sync | SD §22; DR-049; DM §30 | `I6` | Test + Inspection | entityهای sync‌شونده باید version و metadata زمانی کافی برای sync policy داشته باشند. |
| `SRS-SYNC-007` | 3.14 Offline use و sync | SD §22; DR-049; DM §30 | `I6` | Test | sync نباید AuditLog و history لازم برای بررسی conflict و recovery را از بین ببرد. |
| `SRS-AUDIT-001` | 3.15 Audit، history و Undo | SD §21; DM §25 | `I2` | Test | سیستم باید history قابل استفاده‌ای از تغییرات مهم نگه دارد. |
| `SRS-AUDIT-002` | 3.15 Audit، history و Undo | SD §21; DM §25 | `I2` | Test | Audit history باید actor، entity، action، زمان رخداد و previous/new value یا diff لازم را قابل ثبت کند. |
| `SRS-AUDIT-003` | 3.15 Audit، history و Undo | SD §21; DM §25 | `I3` | Test | حذف state جاری در flowهایی مانند RoutineCompletion Reset نباید history آن تغییر را حذف کند. |
| `SRS-AUDIT-004` | 3.15 Audit، history و Undo | SD §21; DM §25 | `I6` | Test + Inspection | history باید بتواند برای مشاهده تغییرات، troubleshooting sync و Undo/restore در flowهایی که محصول اجازه می‌دهد استفاده شود. |
| `SRS-AUDIT-005` | 3.15 Audit، history و Undo | SD §21; DM §25 | `I2` | Inspection | AuditLog نباید سیستم را ملزم به full event sourcing کند. |
| `SRS-GROUP-001` | 3.16 Group، Role و Assignment | SD §24; DR-024; DM §29 | `I7` | Test | یک User باید بتواند هم‌زمان عضو چند Group باشد. |
| `SRS-GROUP-002` | 3.16 Group، Role و Assignment | SD §24; DR-024; DM §29 | `I7` | Test | هر GroupMembership در Personal V1 باید یک System-defined Role داشته باشد. |
| `SRS-GROUP-003` | 3.16 Group، Role و Assignment | SD §24; DR-024; DM §29 | `I7` | Inspection | Custom Role نباید بخشی از role model فعلی Personal V1 باشد. |
| `SRS-GROUP-004` | 3.16 Group، Role و Assignment | SD §24; DR-024; DM §29 | `I7` | Test | سیستم باید assignment یک Task به چند عضو Group را پشتیبانی کند. |
| `SRS-GROUP-005` | 3.16 Group، Role و Assignment | SD §24; DR-024; DM §29 | `I7` | Security Test | داده Groupها باید از Groupهای دیگر و از userهای غیرمجاز ایزوله باشد. |
| `SRS-GROUP-006` | 3.16 Group، Role و Assignment | SD §24; DR-024; DM §29 | `I7` | Test | زمان یک Task/Event اشتراکی باید یک instant مطلق قابل تبدیل داشته باشد و برای هر عضو بر اساس timezone او نمایش داده شود. |
| `SRS-GROUP-007` | 3.16 Group، Role و Assignment | SD §24; DR-024; DM §29 | `I7` | Integration Test | live update و notificationهای Group باید بتوانند از کانال WebSocket سبک استفاده کنند، در حالی که REST مرجع عملیات CRUD باقی می‌ماند. |
| `SRS-TAG-001` | 3.17 Tag | SD §14; DR-047; DM §16 | `I2` | Test + Inspection | Tag باید entity مستقل باشد. |
| `SRS-TAG-002` | 3.17 Tag | SD §14; DR-047; DM §16 | `I2` | Test | Tag باید source از نوع `User` یا `AI` داشته باشد. |
| `SRS-TAG-003` | 3.17 Tag | SD §14; DR-047; DM §16 | `I2` | Test | یک Item باید بتواند چند Tag داشته باشد و یک Tag باید بتواند به چند Item متصل شود. |
| `SRS-TAG-004` | 3.17 Tag | SD §14; DR-047; DM §16 | `I9` | Test | یک Goal باید بتواند چند Tag داشته باشد. |
| `SRS-TAG-005` | 3.17 Tag | SD §14; DR-047; DM §16 | `I9` | Test | Tag ساخته‌شده توسط user نباید صرفا به دلیل semantic cleanup به صورت خودکار archive شود. |
| `SRS-TAG-006` | 3.17 Tag | SD §14; DR-047; DM §16 | `I9` | Test | AI tag باید در semantic review قابلیت merge یا archive شدن داشته باشد. |
| `SRS-TAG-007` | 3.17 Tag | SD §14; DR-047; DM §16 | `I9` | Test | سیستم باید بتواند ارتباط معنایی Goal با Itemها را از طریق Tagهای مرتبط برقرار کند. |
| `SRS-TAG-008` | 3.17 Tag | SD §14; DR-047; DM §16 | `I2` | Test | هر Tag باید شناسه پایدار و title داشته باشد. |
| `SRS-GOAL-001` | 3.18 Goal و lifecycle | SD §13; DR-023; DR-025; DR-027; DR-028; DR-047; DM §17 | `I9` | Test + Inspection | Goal باید entity مستقل و خارج از Item hierarchy باشد. |
| `SRS-GOAL-002` | 3.18 Goal و lifecycle | SD §13; DR-023; DR-025; DR-027; DR-028; DR-047; DM §17 | `I9` | Test | تعداد Goalهای قابل نگهداری برای user نباید سقف ثابت محصولی داشته باشد. |
| `SRS-GOAL-003` | 3.18 Goal و lifecycle | SD §13; DR-023; DR-025; DR-027; DR-028; DR-047; DM §17 | `I9` | Test | Goal باید lifecycle stateهای `Active`, `Dormant` و `Archived` را پشتیبانی کند. |
| `SRS-GOAL-004` | 3.18 Goal و lifecycle | SD §13; DR-023; DR-025; DR-027; DR-028; DR-047; DM §17 | `I9` | Test | Goal باید بتواند به List و در صورت نیاز Column مرتبط شود. |
| `SRS-GOAL-005` | 3.18 Goal و lifecycle | SD §13; DR-023; DR-025; DR-027; DR-028; DR-047; DM §17 | `I9` | Test | وقتی Goal فعلا Item فعال و معنادار مرتبط با progress ندارد، lifecycle آن باید بتواند وارد حالت `Dormant` شود. |
| `SRS-GOAL-006` | 3.18 Goal و lifecycle | SD §13; DR-023; DR-025; DR-027; DR-028; DR-047; DM §17 | `I9` | Test | Goal در حالت `Dormant` نباید برای Daily Ring eligibility در نظر گرفته شود. |
| `SRS-GOAL-007` | 3.18 Goal و lifecycle | SD §13; DR-023; DR-025; DR-027; DR-028; DR-047; DM §17 | `I9` | Test | ورود Goal به `Dormant` نباید current streak آن را reset کند و streak باید freeze شود. |
| `SRS-GOAL-008` | 3.18 Goal و lifecycle | SD §13; DR-023; DR-025; DR-027; DR-028; DR-047; DM §17 | `I9` | Test | Goal `Dormant` باید در recheck بتواند دوباره Active شود، مشروط به قواعد similarity که در Decision Gate مربوطه نهایی می‌شوند. |
| `SRS-GOAL-009` | 3.18 Goal و lifecycle | SD §13; DR-023; DR-025; DR-027; DR-028; DR-047; DM §17 | `I9` | Test | Goal `Archived` نباید به صورت خودکار reactivate شود. |
| `SRS-GOAL-010` | 3.18 Goal و lifecycle | SD §13; DR-023; DR-025; DR-027; DR-028; DR-047; DM §17 | `I10` | Test | `Goal.current_streak` باید تعداد Dotick Dayهای متوالی باشد که DailyRing همان Goal complete شده است. |
| `SRS-GOAL-011` | 3.18 Goal و lifecycle | SD §13; DR-023; DR-025; DR-027; DR-028; DR-047; DM §17 | `I10` | Test | `Goal.total_completions` باید تعداد کل Dotick Dayهایی باشد که Goal complete شده است. |
| `SRS-GOAL-012` | 3.18 Goal و lifecycle | SD §13; DR-023; DR-025; DR-027; DR-028; DR-047; DM §17 | `I10` | Test | فعالیتی که DailyRing را به completion threshold نمی‌رساند نباید به تنهایی Goal streak را حفظ کند. |
| `SRS-GOAL-013` | 3.18 Goal و lifecycle | SD §13; DR-023; DR-025; DR-027; DR-028; DR-047; DM §17 | `I10` | Test | سیستم باید قابلیت reminder سطح Goal را مستقل از reminderهای تک Item داشته باشد و trigger آن بتواند افت معنادار نسبت به Norm را در نظر بگیرد. |
| `SRS-GOAL-014` | 3.18 Goal و lifecycle | SD §13; DR-023; DR-025; DR-027; DR-028; DR-047; DM §17 | `I9` | Test | TrackingState Goal باید بتواند `best_streak` را در کنار current streak و total completions نگه دارد. |
| `SRS-GOAL-015` | 3.18 Goal و lifecycle | SD §13; DR-023; DR-025; DR-027; DR-028; DR-047; DM §17 | `I9` | Test | هر Goal باید شناسه پایدار و title داشته باشد و description آن می‌تواند اختیاری باشد. |
| `SRS-GDISC-001` | 3.19 AI Goal discovery و GoalGenerationLog | SD §15; DR-045..DR-048; DM §18 | `I9` | Test + Analysis | AI Goal discovery باید List، Column، محتوای واقعی Itemها و Tagهای موجود را به عنوان context بررسی کند. |
| `SRS-GDISC-002` | 3.19 AI Goal discovery و GoalGenerationLog | SD §15; DR-045..DR-048; DM §18 | `I9` | Test | نام List یا Column نباید تنها مبنای ایجاد Goal باشد. |
| `SRS-GDISC-003` | 3.19 AI Goal discovery و GoalGenerationLog | SD §15; DR-045..DR-048; DM §18 | `I9` | Test + Analysis | سیستم نباید برای grouping نامنسجم یا بدون semantic coherence به اجبار Goal ایجاد کند. |
| `SRS-GDISC-004` | 3.19 AI Goal discovery و GoalGenerationLog | SD §15; DR-045..DR-048; DM §18 | `I9` | Test + Analysis | initial semantic flow باید Tagهای user را در context قرار دهد تا duplicate یا Tagهای بسیار مشابه کاهش یابند. |
| `SRS-GDISC-005` | 3.19 AI Goal discovery و GoalGenerationLog | SD §15; DR-045..DR-048; DM §18 | `I9` | Test + Analysis | در current model، تعداد Goalهای استخراج‌شده از یک List نباید از تعداد Columnهای معنادار آن بیشتر شود، مگر اینکه یک تصمیم canonical بعدی این rule را تغییر دهد. |
| `SRS-GDISC-006` | 3.19 AI Goal discovery و GoalGenerationLog | SD §15; DR-045..DR-048; DM §18 | `I9` | Test | reactive review برای context جدید یا Dormant باید بتواند با baseline delay برابر 12 ساعت اجرا شود و فقط context متاثر را دوباره ارزیابی کند. |
| `SRS-GDISC-007` | 3.19 AI Goal discovery و GoalGenerationLog | SD §15; DR-045..DR-048; DM §18 | `I9` | Test | سیستم باید weekly global review برای merge Goalهای بسیار مشابه، cleanup یا archive AI tagها و semantic refresh داشته باشد. |
| `SRS-GDISC-008` | 3.19 AI Goal discovery و GoalGenerationLog | SD §15; DR-045..DR-048; DM §18 | `I9` | Test | هر Initial Generation، Weekly Review یا Reactivation Check مربوط به Goal باید در `GoalGenerationLog` قابل ثبت باشد. |
| `SRS-GDISC-009` | 3.19 AI Goal discovery و GoalGenerationLog | SD §15; DR-045..DR-048; DM §18 | `I9` | Test | GoalGenerationLog باید model/version استفاده‌شده، changed flag، previous/new title و description و زمان ایجاد را قابل نگهداری کند. |
| `SRS-GDISC-010` | 3.19 AI Goal discovery و GoalGenerationLog | SD §15; DR-045..DR-048; DM §18 | `I9` | Test | user rating در GoalGenerationLog باید فقط وقتی مرتبط باشد که تغییر واقعی AI رخ داده باشد. |
| `SRS-GDISC-011` | 3.19 AI Goal discovery و GoalGenerationLog | SD §15; DR-045..DR-048; DM §18 | `I9` | Test | GoalGenerationLog باید append-only باشد؛ review جدید باید entry جدید ایجاد کند و history قبلی را بازنویسی نکند. |
| `SRS-RING-001` | 3.20 Daily Ring selection و snapshot | SD §16; DR-026; DR-033; DR-034; DR-045; DR-046; DM §§19-20 | `I10` | Test | تعداد Daily Ring فعال هر Dotick Day باید `min(3, eligible_active_goals)` باشد. |
| `SRS-RING-002` | 3.20 Daily Ring selection و snapshot | SD §16; DR-026; DR-033; DR-034; DR-045; DR-046; DM §§19-20 | `I10` | Test | اگر حداقل سه Goal eligible وجود داشته باشد، سیستم باید دقیقا سه Daily Ring بسازد. |
| `SRS-RING-003` | 3.20 Daily Ring selection و snapshot | SD §16; DR-026; DR-033; DR-034; DR-045; DR-046; DM §§19-20 | `I10` | Test | اگر دو Goal eligible وجود داشته باشد، سیستم باید دو Ring و اگر یک Goal eligible وجود داشته باشد یک Ring بسازد. |
| `SRS-RING-004` | 3.20 Daily Ring selection و snapshot | SD §16; DR-026; DR-033; DR-034; DR-045; DR-046; DM §§19-20 | `I10` | Test | اگر Goal eligible وجود نداشته باشد، سیستم نباید Daily Ring فعال ایجاد کند. |
| `SRS-RING-005` | 3.20 Daily Ring selection و snapshot | SD §16; DR-026; DR-033; DR-034; DR-045; DR-046; DM §§19-20 | `I10` | Analysis + Test | selection باید ترکیب روز را balanced کند و نباید صرفا بزرگ‌ترین backlog را انتخاب کند. |
| `SRS-RING-006` | 3.20 Daily Ring selection و snapshot | SD §16; DR-026; DR-033; DR-034; DR-045; DR-046; DM §§19-20 | `I10` | Analysis + Inspection | selection باید حداقل due/timing، priority، neglect، weekday behavior، holiday context، streak momentum، workload، difficulty و recent user capacity را به عنوان signal قابل استفاده در نظر بگیرد. |
| `SRS-RING-007` | 3.20 Daily Ring selection و snapshot | SD §16; DR-026; DR-033; DR-034; DR-045; DR-046; DM §§19-20 | `I10` | Test | DailyRing باید user، goal، effective date، target، progress، completion state، final score، finalization state و algorithm/version metadata لازم را به صورت snapshot نگه دارد. |
| `SRS-RING-008` | 3.20 Daily Ring selection و snapshot | SD §16; DR-026; DR-033; DR-034; DR-045; DR-046; DM §§19-20 | `I10` | Test | تغییر عادی future fieldهای Item نباید معنای historical DailyRing را بازنویسی کند. |
| `SRS-RING-009` | 3.20 Daily Ring selection و snapshot | SD §16; DR-026; DR-033; DR-034; DR-045; DR-046; DM §§19-20 | `I10` | Test | DailyRingItem باید membership Itemهای انتخاب‌شده همان روز و featureهای scoring لازم برای بازسازی تصمیم آن روز را snapshot کند. |
| `SRS-RING-010` | 3.20 Daily Ring selection و snapshot | SD §16; DR-026; DR-033; DR-034; DR-045; DR-046; DM §§19-20 | `I10` | Test | Task، Event و Routine occurrence باید بتوانند در صورت eligibility عضو DailyRingItem شوند. |
| `SRS-RING-011` | 3.20 Daily Ring selection و snapshot | SD §16; DR-026; DR-033; DR-034; DR-045; DR-046; DM §§19-20 | `I10` | Test | completion یک Item فقط باید Ring همان credited day را جلو ببرد که Item در DailyRingItem آن Ring عضو بوده است. |
| `SRS-RING-012` | 3.20 Daily Ring selection و snapshot | SD §16; DR-026; DR-033; DR-034; DR-045; DR-046; DM §§19-20 | `I10` | Test | completion یک Item خارج از DailyRingItemهای credited day نباید progress هیچ Goal روزانه‌ای را افزایش دهد. |
| `SRS-SCORE-001` | 3.21 Progress، completion، performance score و Norm | SD §17; DR-029..DR-032; DM §21 | `I10` | Test | `progress_percent` DailyRing باید در بازه 0 تا 100 باقی بماند. |
| `SRS-SCORE-002` | 3.21 Progress، completion، performance score و Norm | SD §17; DR-029..DR-032; DM §21 | `I10` | Test + Inspection | UI نباید progress بزرگ‌تر از 100 نمایش دهد. |
| `SRS-SCORE-003` | 3.21 Progress، completion، performance score و Norm | SD §17; DR-029..DR-032; DM §21 | `I10` | Test | `is_completed` باید زمانی true شود که progress به completion threshold برابر 100 درصد برسد. |
| `SRS-SCORE-004` | 3.21 Progress، completion، performance score و Norm | SD §17; DR-029..DR-032; DM §21 | `I10` | Test | `final_score` باید از progress جدا باشد و بتواند از baseline یا 100 بالاتر برود. |
| `SRS-SCORE-005` | 3.21 Progress، completion، performance score و Norm | SD §17; DR-029..DR-032; DM §21 | `I10` | Test | bonusهای performance که ممکن است حس completion زودهنگام ایجاد کنند باید تا day finalization برای user مخفی بمانند. |
| `SRS-SCORE-006` | 3.21 Progress، completion، performance score و Norm | SD §17; DR-029..DR-032; DM §21 | `I10` | Test | final score و bonusهای مخفی باید در day finalization محاسبه یا reveal شوند. |
| `SRS-SCORE-007` | 3.21 Progress، completion، performance score و Norm | SD §17; DR-029..DR-032; DM §21 | `I10` | Test + Analysis | انجام زودتر یک Item مهم باید بتواند final performance score بیشتری نسبت به انجام دیرتر همان کار در شرایط قابل مقایسه ایجاد کند. |
| `SRS-SCORE-008` | 3.21 Progress، completion، performance score و Norm | SD §17; DR-029..DR-032; DM §21 | `I10` | Test + Analysis | در انتهای روز، انجام کارهای relevant باقی‌مانده باید همچنان بتواند progress واقعی را به completion نزدیک کند. |
| `SRS-SCORE-009` | 3.21 Progress، completion، performance score و Norm | SD §17; DR-029..DR-032; DM §21 | `I10` | Test | late-day recovery نباید progress را از 100 بالاتر ببرد و overachievement باید در final score منعکس شود. |
| `SRS-SCORE-010` | 3.21 Progress، completion، performance score و Norm | SD §17; DR-029..DR-032; DM §21 | `I10` | Test | target روزانه Ring نباید به صورت مستقیم توسط user تعیین شود. |
| `SRS-SCORE-011` | 3.21 Progress، completion، performance score و Norm | SD §17; DR-029..DR-032; DM §21 | `I10` | Test + Analysis | repeated misses باید بتواند target یا Norm را به صورت موقت کاهش دهد. |
| `SRS-SCORE-012` | 3.21 Progress، completion، performance score و Norm | SD §17; DR-029..DR-032; DM §21 | `I10` | Test + Analysis | recovery عملکرد باید بتواند target را به صورت تدریجی به سطح قبلی برگرداند. |
| `SRS-SCORE-013` | 3.21 Progress، completion، performance score و Norm | SD §17; DR-029..DR-032; DM §21 | `I10` | Test + Analysis | repeated success باید بتواند target را به صورت تدریجی افزایش دهد. |
| `SRS-SCORE-014` | 3.21 Progress، completion، performance score و Norm | SD §17; DR-029..DR-032; DM §21 | `I10` | Test + Analysis | داده جدید باید بتواند Norm را بر اساس رفتار واقعی user به‌روزرسانی کند. |
| `SRS-DAY-001` | 3.22 Dotick Day و credited date | SD §19; DR-035..DR-037; DM §§22-23 | `I10` | Test | سیستم باید `Dotick Day` را به عنوان روز منطقی مستقل از Calendar Day پشتیبانی کند. |
| `SRS-DAY-002` | 3.22 Dotick Day و credited date | SD §19; DR-035..DR-037; DM §§22-23 | `I10` | Test | UserPreferences باید timezone کاربر را برای محاسبات زمانی و نمایش محلی نگه دارد. |
| `SRS-DAY-003` | 3.22 Dotick Day و credited date | SD §19; DR-035..DR-037; DM §§22-23 | `I10` | Test | user باید بتواند day boundary صریح تنظیم کند. |
| `SRS-DAY-004` | 3.22 Dotick Day و credited date | SD §19; DR-035..DR-037; DM §§22-23 | `I10` | Test | اگر user day boundary صریح تنظیم نکرده باشد، ambiguity window پیش‌فرض باید 60 دقیقه پس از midnight local باشد. |
| `SRS-DAY-005` | 3.22 Dotick Day و credited date | SD §19; DR-035..DR-037; DM §§22-23 | `I10` | Test | در حالت پیش‌فرض، completion ثبت‌شده در ambiguity window باید امکان attribution به Today یا Yesterday را به user بدهد. |
| `SRS-DAY-006` | 3.22 Dotick Day و credited date | SD §19; DR-035..DR-037; DM §§22-23 | `I10` | Test | اگر day boundary صریح تنظیم شده باشد، completion پیش از آن boundary باید به Dotick Day قبلی attribution شود. |
| `SRS-DAY-007` | 3.22 Dotick Day و credited date | SD §19; DR-035..DR-037; DM §§22-23 | `I10` | Test | completionهایی که در scoring استفاده می‌شوند باید credited/effective date داشته باشند که در صورت نیاز از raw timestamp مستقل باشد. |
| `SRS-DAY-008` | 3.22 Dotick Day و credited date | SD §19; DR-035..DR-037; DM §§22-23 | `I10` | Test | در day boundary، سیستم باید DailyRingهای روز قبلی را finalize کند. |
| `SRS-DAY-009` | 3.22 Dotick Day و credited date | SD §19; DR-035..DR-037; DM §§22-23 | `I10` | Test | finalization باید completion state و final score DailyRing را تثبیت و bonus مربوطه را reveal کند. |
| `SRS-DAY-010` | 3.22 Dotick Day و credited date | SD §19; DR-035..DR-037; DM §§22-23 | `I10` | Test | finalization باید Goal streak state مربوط به روز بسته‌شده را update کند. |
| `SRS-DAY-011` | 3.22 Dotick Day و credited date | SD §19; DR-035..DR-037; DM §§22-23 | `I10` | Test | پس از بسته شدن روز قبلی، سیستم باید DailyRingهای روز جدید را تولید کند. |
| `SRS-DAY-012` | 3.22 Dotick Day و credited date | SD §19; DR-035..DR-037; DM §§22-23 | `I10` | Test | پس از finalization، historical Ring باید snapshot تاریخی باقی بماند و تغییر عادی Item نباید آن را خودکار باز کند. |
| `SRS-STAT-001` | 3.23 Statistics و historical correction | SD §20; DR-038; DM §24 | `I10` | Test | تغییر historical RoutineCompletion باید آمار متاثر را اصلاح کند. |
| `SRS-STAT-002` | 3.23 Statistics و historical correction | SD §20; DR-038; DM §24 | `I10` | Test + Analysis | سیستم نباید به صورت پیش‌فرض برای هر historical edit کل history را از ابتدا recompute کند. |
| `SRS-STAT-003` | 3.23 Statistics و historical correction | SD §20; DR-038; DM §24 | `I10` | Test + Analysis | recomputation باید به windowها و metricهای متاثر محدود شود، مگر maintenance job یا recovery صریح نیاز دیگری داشته باشد. |
| `SRS-STAT-004` | 3.23 Statistics و historical correction | SD §20; DR-038; DM §24 | `I10` | Test | simple lifetime counterها باید در صورت امکان با increment/decrement اصلاح شوند. |
| `SRS-STAT-005` | 3.23 Statistics و historical correction | SD §20; DR-038; DM §24 | `I10` | Test | streakهایی که historical edit روی آن‌ها اثر دارد باید در محدوده لازم دوباره محاسبه شوند. |
| `SRS-STAT-006` | 3.23 Statistics و historical correction | SD §20; DR-038; DM §24 | `I10` | Test + Inspection | raw completion و state-change data باید source of truth آمار باشند، نه dashboard aggregate. |
| `SRS-STAT-007` | 3.23 Statistics و historical correction | SD §20; DR-038; DM §24 | `I10` | Test + Analysis | behavior featureهای پرهزینه باید بتوانند مستقل از core write path refresh شوند. |
| `SRS-AIITEM-001` | 3.24 AI-assisted Item creation | SD §25; DR-039..DR-043; DM §26 | `I8` | Test | سیستم باید AI-assisted Item creation را حداقل از Text و Voice پشتیبانی کند. |
| `SRS-AIITEM-002` | 3.24 AI-assisted Item creation | SD §25; DR-039..DR-043; DM §26 | `I8` | Inspection + Test | در contextهایی که user Item ایجاد می‌کند، UI باید در صورت عملی بودن ورودی voice را در کنار create input در دسترس قرار دهد. |
| `SRS-AIITEM-003` | 3.24 AI-assisted Item creation | SD §25; DR-039..DR-043; DM §26 | `I8` | Test | Voice input باید پیش از AI analysis به transcript قابل پردازش تبدیل شود. |
| `SRS-AIITEM-004` | 3.24 AI-assisted Item creation | SD §25; DR-039..DR-043; DM §26 | `I8` | Test + Evaluation | AI باید در صورت قابل استنتاج بودن بتواند Task یا Event بودن ورودی، title، date/time، location، description، Folder، List، Column و reminder را پیشنهاد دهد. |
| `SRS-AIITEM-005` | 3.24 AI-assisted Item creation | SD §25; DR-039..DR-043; DM §26 | `I8` | Test | AI output باید به عنوان Draft/Proposal نمایش داده شود و user باید بتواند تمام جزئیات پیشنهادی را قبل از ایجاد Item ویرایش کند. |
| `SRS-AIITEM-006` | 3.24 AI-assisted Item creation | SD §25; DR-039..DR-043; DM §26 | `I8` | Test | سیستم نباید صرفا بر اساس AI inference و پیش از Confirm user رکورد نهایی Item ایجاد کند. |
| `SRS-AIITEM-007` | 3.24 AI-assisted Item creation | SD §25; DR-039..DR-043; DM §26 | `I8` | Test | پس از Confirm، سیستم باید Item واقعی را از payload نهایی تاییدشده ایجاد کند. |
| `SRS-AIITEM-008` | 3.24 AI-assisted Item creation | SD §25; DR-039..DR-043; DM §26 | `I8` | Test | سیستم باید بتواند یک AIItemCreationSession شامل source type، original input، transcript در صورت وجود، AI proposal، user final payload، model version، accepted state و timestamps را نگه دارد. |
| `SRS-AIITEM-009` | 3.24 AI-assisted Item creation | SD §25; DR-039..DR-043; DM §26 | `I8` | Test | سیستم باید بتواند field-level change بین AI proposal و user final payload را برای evaluation و future personalization نگه دارد. |
| `SRS-AIITEM-010` | 3.24 AI-assisted Item creation | SD §25; DR-039..DR-043; DM §26 | `I8` | Test | draft/session باید بتواند provenance field را حداقل میان explicit user input، AI inferred، user-preference inferred و external source تفکیک کند. |
| `SRS-AIITEM-011` | 3.24 AI-assisted Item creation | SD §25; DR-039..DR-043; DM §26 | `I8` | Failure Test | failure سرویس AI یا STT نباید manual Item creation و core task management را از کار بیندازد. |
| `SRS-AIITEM-012` | 3.24 AI-assisted Item creation | SD §25; DR-039..DR-043; DM §26 | `I8` | Test | payload نهایی AI-assisted creation باید پیش از ایجاد Item واقعی همان validationهای domain مربوط به Task/Event را پاس کند. |
| `SRS-IF-001` | 4.1 API و ارتباط client/server | SD §27; RM I0 | `I0 baseline + I1 implementation` | Inspection | frontend و backend باید به عنوان بخش‌های جدا با contract ارتباطی مشخص توسعه‌پذیر باشند. |
| `SRS-IF-002` | 4.1 API و ارتباط client/server | SD §27; RM I0 | `I0 baseline + I1 implementation` | Integration Test | عملیات CRUD اصلی باید از REST استفاده کنند. |
| `SRS-IF-003` | 4.1 API و ارتباط client/server | SD §27; RM I0 | `I0 baseline + I1 implementation` | Contract Test | فرمت تبادل اصلی REST باید JSON باشد. |
| `SRS-IF-004` | 4.1 API و ارتباط client/server | SD §27; RM I0 | `I0 baseline + I7 implementation` | Integration Test + Inspection | WebSocket باید برای notification و live update سبک استفاده شود و نباید جایگزین CRUD authority مبتنی بر REST شود. |
| `SRS-IF-005` | 4.1 API و ارتباط client/server | SD §27; RM I0 | `I0 baseline + I1 implementation` | Security Test + Inspection | ارتباط client/server باید از HTTPS استفاده کند. در local development فقط Deployment Design می‌تواند برای محیطی که HTTPS عملا قابل اعمال نیست exception صریح تعریف کند. |
| `SRS-CON-001` | 4.2 storage و platform constraints | SD §27; RM I0 | `I0` | Inspection + Integration Test | persistence اصلی server-side باید از PostgreSQL استفاده کند. |
| `SRS-CON-002` | 4.2 storage و platform constraints | DM §31; DR-054 | `I0` | Architecture Inspection | hierarchy مفهومی Domain Model نباید به تنهایی implementation را به Class Table Inheritance متعهد کند. |
| `SRS-CON-003` | 4.2 storage و platform constraints | DM §31; SD §27 | `I0` | Architecture Review + Test | storage strategy باید query simplicity، integrity، migration safety و performance لازم برای behaviorهای این SRS را حفظ کند. |
| `SRS-CON-004` | 4.2 storage و platform constraints | SD §27 | `I0` | Deployment Test | Personal V1 باید بتواند روی server local-hosted اجرا شود. |
| `SRS-NFR-SEC-001` | 5.1 امنیت | SD §§23, 29; DR-050 | `I1` | Security Test + Inspection | password plaintext نباید در persistence یا logهای عادی ذخیره شود. |
| `SRS-NFR-SEC-002` | 5.1 امنیت | SD §§23, 29; DR-050 | `I1` | Security Inspection | password credential باید با الگوریتم hashing امن مانند Argon2، bcrypt یا معادل امن پروژه محافظت شود. |
| `SRS-NFR-SEC-003` | 5.1 امنیت | SD §29 | `I1` | Security Test | requestها و queryهای user-private باید دسترسی user دیگر به داده خصوصی را در حالت عادی رد کنند. |
| `SRS-NFR-SEC-004` | 5.1 امنیت | SD §§24, 29; DR-024 | `I7` | Security Test | queryها و authorization مربوط به Group باید cross-group data leakage را رد کنند. |
| `SRS-NFR-SEC-005` | 5.1 امنیت | SD §§24, 29; RM I7 | `I7` | Security Test | WebSocket و سایر live channelها باید همان authorization لازم برای داده قابل مشاهده را رعایت کنند. |
| `SRS-NFR-REL-001` | 5.2 قابلیت اطمینان و حفاظت از داده | SD §§25, 27; RM I8 | `I8 + I11 validation` | Failure Test | failure سرویس خارجی AI نباید core manual task management را unavailable کند. |
| `SRS-NFR-REL-002` | 5.2 قابلیت اطمینان و حفاظت از داده | SD §§20-21; DR-007, DR-038 | `I3 + I6` | Test | Reset و historical edit باید history لازم برای recovery و بررسی خطا را حفظ کنند. |
| `SRS-NFR-REL-003` | 5.2 قابلیت اطمینان و حفاظت از داده | SD §22; DR-049 | `I6` | Sync Test | sync conflict resolution نباید تغییر fieldهای مستقل را صرفا به دلیل conflict در field دیگر از بین ببرد. |
| `SRS-NFR-REL-004` | 5.2 قابلیت اطمینان و حفاظت از داده | SD §§2.3, 16.4, 19.4; DR-034 | `I10` | Regression Test | historical DailyRing snapshot نباید با تغییرات عادی آینده به صورت ناخواسته بازنویسی شود. |
| `SRS-NFR-PERF-001` | 5.3 کارایی | SD §8; DR-016 | `I2` | Performance Test + Analysis | بازیابی hierarchy child/parent باید بدون parse کامل RichDescription انجام شود. |
| `SRS-NFR-PERF-002` | 5.3 کارایی | SD §8; DR-016 | `I2` | Data Design Inspection + Performance Test | design hierarchy باید امکان index-supported query را فراهم کند. |
| `SRS-NFR-PERF-003` | 5.3 کارایی | SD §28.1 | `I11` | Performance Test | baseline local deployment باید در Performance Test Plan برای حدود 30 user هم‌زمان ارزیابی شود. این عدد test target است و SLA محسوب نمی‌شود. |
| `SRS-NFR-PERF-004` | 5.3 کارایی | SD §28.1 | `I7 + I11 validation` | Performance Test | live update گروهی باید در Performance Test Plan با threshold مناسب برای تجربه تقریبا real-time ارزیابی شود. |
| `SRS-NFR-PERF-005` | 5.3 کارایی | SD §20; DR-038 | `I10` | Performance Test + Analysis | historical edit نباید به صورت پیش‌فرض full-history recomputation synchronous را به core user action تحمیل کند. |
| `SRS-NFR-UX-001` | 5.4 usability و presentation | SD §§3.1, 28; RM I5 | `I5` | Usability Test + Inspection | UI باید در اندازه‌های رایج mobile و layoutهای responsive قابل استفاده باقی بماند. |
| `SRS-NFR-UX-002` | 5.4 usability و presentation | SD §§2.1, 8.3; DR-019 | `I2` | UX Inspection | پیچیدگی داخلی child/reference، sync metadata یا storage inheritance نباید بدون requirement صریح به controlهای پیچیده اضافی در UI نشت کند. |
| `SRS-NFR-UX-003` | 5.4 usability و presentation | SD §25; DR-042 | `I8` | Usability Test | AI proposal باید قبل از Confirm برای user قابل بازبینی و اصلاح باشد. |
| `SRS-NFR-UX-004` | 5.4 usability و presentation | SD §17.1; DR-029 | `I10` | UI Test | progress Daily Ring باید برای user حداکثر 100 درصد نمایش داده شود، حتی اگر final performance بالاتر از baseline باشد. |
| `SRS-NFR-MAINT-001` | 5.5 maintainability و change isolation | SD §§5, 27; DR-014, DR-015 | `I1` | Architecture Review + Test | failure یا تغییر یک integration خارجی نباید مدل ownership داخلی را به Source وابسته کند. |
| `SRS-NFR-MAINT-002` | 5.5 maintainability و change isolation | SD §3.1 | `I5` | Regression Test | تغییر View نباید domain data را تغییر دهد. |

## 5.1 Increment 0 engineering artifact trace

| Requirement(s) | Engineering artifact | Current evidence |
|---|---|---|
| `SRS-IF-001..004` | `project-docs/03-design/architecture.md`; ADR-0001 | client/server boundary، REST authority و WebSocket scope تعریف شده‌اند؛ implementation verification در Increment مالک باقی می‌ماند. |
| `SRS-IF-005` | `project-docs/03-design/security-design.md`; `project-docs/06-operations/release-deployment.md` | TLS baseline و loopback-only development exception تعریف شده‌اند. |
| `SRS-CON-001..003` | `project-docs/03-design/data-model.md`; ADR-0002; DR-054 | PostgreSQL و explicit-composition storage baseline تعریف و review شده‌اند. |
| `SRS-CON-004` | `project-docs/06-operations/release-deployment.md` | local-hosted Compose topology و clean-clone verification تعریف شده‌اند؛ deployment test پس از scaffold انجام می‌شود. |
| Increment 0 verification process | `project-docs/05-quality/test-strategy.md` | gateهای migration، integration، contract و Walking Skeleton تعریف شده‌اند. |
| Increment risks | `project-docs/01-planning/risk-log.md` | riskهای architecture، isolation، reproducibility و recovery ثبت شده‌اند. |

# 6. OPEN decision traceability

این recordها requirement قطعی نیستند. جدول نشان می‌دهد هر تصمیم روی چه requirementهایی اثر دارد و در کدام Decision Gate باید formalize شود؛ record resolved برای حفظ history باقی می‌ماند.

| Open ID | Topic | Affected requirement(s) | Canonical/open source | Decision Gate |
|---|---|---|---|---|
| OPEN-001 | Event structural multi-parent vs single parent + multi-reference | SRS-EVENT-006, SRS-EVENT-007, SRS-HIER-* | DR-018 / SRS §7 | I2 |
| OPEN-002 | Exact RichDescription/ContentBlock schema | SRS-DESC-001..005, SRS-COMMENT-002..003 | DR-020, DR-021 / SRS §7 | I2 |
| OPEN-003 | Backend schema for structural child vs normal reference | SRS-HIER-001..006, SRS-DESC-003 | DR-016..019 / SRS §7 | I2 |
| OPEN-004 | Exact Task dependency-cycle policy | SRS-TASK-015 | DM §4.4, §32 / SRS §7 | I2 |
| OPEN-005 | Exact due/end/deadline ordering validation | SRS-TASK-002..012 | DM §32 / SRS §7 | I2 |
| OPEN-006 | Definition of qualifying completions for incremental Routine | SRS-ROUTINE-021..023 | DR open item 8 / DM §10.3 / SRS §7 | I3/I4 |
| OPEN-007 | Incremental Routine inactivity reset | SRS-ROUTINE-021..023 | DR open item 8 / SRS §7 | I3/I10 gate |
| OPEN-008 | Full frequency-based Routine streak semantics | SRS-RSTREAK-005..006 | DR open item 7 / DM §14.2 / SRS §7 | I4 |
| OPEN-009 | Final recurrence config schema and occurrence identity | SRS-REC-* | DM §13 / SRS §7 | I4 |
| OPEN-010 | Exact sync metadata, clock strategy and conflict granularity | SRS-SYNC-* | DR open item 14 / DM §30 / SRS §7 | I6 |
| OPEN-011 | Folder/List/Column ownership in Group context | SRS-ORG-*, SRS-GROUP-* | DM open item 9 / SRS §7 | I7 |
| OPEN-012 | Initial AI Goal warm-up duration | SRS-GDISC-* | DR open item 9 / SRS §7 | I9 |
| OPEN-013 | Goal similarity thresholds | SRS-GOAL-008..009, SRS-GDISC-* | DR open item 10 / SRS §7 | I9 |
| OPEN-014 | Exact Goal selection algorithm and learning weights | SRS-RING-005..006 | DR open item 11 / SRS §7 | I10 |
| OPEN-015 | Exact Ring progress/final-score/bonus/recovery formula | SRS-SCORE-* | DR open item 4 / SRS §7 | I10 |
| OPEN-016 | Difficulty/effort representation | SRS-RING-006, SRS-SCORE-* | DR open item 5 / SRS §7 | I10 |
| OPEN-017 | Adaptive Norm thresholds and windows | SRS-SCORE-010..014 | SRS §7; SD §17.6 | I10 |
| OPEN-018 | Global daily streak and related motivational behavior | No normative SRS requirement yet | DR-051 / SRS §7 | I10 |
| OPEN-019 | RoutineOccurrence representation in DailyRingItem | SRS-RING-009..010 | DM §20 / SRS §7 | I10 |
| OPEN-020 | Goal-level reminder frequency/rate limit | SRS-GOAL-013 | SD §13.3 / SRS §7 | I10 |
| OPEN-021 | Physical storage inheritance/composition/denormalization strategy | SRS-CON-002..003 | RESOLVED by DR-054 / DM §31 / ADR-0002 | I0 baseline complete; revisit only by measured need |
| OPEN-022 | Exact API endpoints and versioning contract | SRS-IF-001..004 | DR open item 13 / SRS §7 | Per increment |
| OPEN-023 | Trusted automation confirmation policy | Future only | DR open item 15 / SRS §7 | Future Integration |
| OPEN-024 | Enterprise SSO protocol | Future only | SD §23 / SRS §7 | Enterprise |
| OPEN-025 | Enterprise privacy/compliance requirements | Future only | SD §29.2 / SRS §7 | Enterprise |

# 7. Traceability gap retained for review

Roadmap در Increment 4 یک behavior برای recurring Task دارد که تولید Task بعدی را time-based و مستقل از completion Task قبلی می‌داند. Formal SRS v2.0 این behavior را normative نکرده، چون Decision Register و System Definition فعلی آن را به صورت صریح تثبیت نکرده‌اند.

تا قبل از Increment 4 یکی از این دو کار باید انجام شود:

1. behavior در canonical source تایید شود و سپس Requirement جدید یا اصلاح‌شده با ID پایدار وارد SRS و این ماتریس شود؛ یا
2. اگر behavior مورد نظر نیست، Roadmap اصلاح شود.

این gap نباید با implementation ضمنی بسته شود.

# 8. Update rules for future increments

در هر Increment، این فایل بعد از ایجاد artifactهای واقعی update می‌شود. حداقل trace نهایی برای requirementهای همان Increment باید بتواند این مسیر را نشان دهد:

```text
Canonical Source
-> SRS Requirement
-> Analysis / Acceptance Criteria
-> Design / API / Data / UI / ADR
-> Automated or Manual Verification
-> Implementation
-> Increment Review / Release
```

قواعد update:

- requirement جدید فقط پس از ورود به Formal SRS به این ماتریس اضافه می‌شود.
- تغییر behavior ابتدا در Decision Register/System Definition و سپس SRS ثبت می‌شود.
- resolve شدن `OPEN` باید با تصمیم canonical ثبت شود؛ حذف صرف آن از این فایل کافی نیست.
- Test ID، ADR، API operation، migration، module یا release فقط وقتی ثبت می‌شود که artifact واقعی وجود داشته باشد.
- Requirement حذف‌شده از history پاک نمی‌شود؛ وضعیت آن باید به تصمیم superseding یا نسخه SRS مربوط trace شود.
- در پایان هر Increment، requirementهای owning Increment نباید بدون Verification artifact و نتیجه acceptance باقی بمانند.

# 9. Baseline status

این نسخه baseline اولیه Increment 0 است. در حال حاضر trace تا سطح `Canonical Source -> Formal Requirement -> Planned Increment -> Verification Method` کامل است. Trace به Analysis، Design، Test Case، Code و Release در Incrementهای مالک اضافه خواهد شد.
