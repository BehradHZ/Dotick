# Dotick Software Requirements Specification

**Document type:** Formal Software Requirements Specification

**Version:** 2.0

**Baseline date:** 2026-08-17

**Status:** Formal SRS Baseline

**Scope:** Personal V1

> این سند baseline رسمی نیازمندی‌های Dotick برای Personal V1 است. این نسخه جایگزین نقش `reconciled derived reference` نسخه 1.7 می‌شود. جزئیات طراحی فیزیکی، تصمیم‌های هنوز `OPEN` و قابلیت‌های Enterprise/Future تا زمان بسته شدن در منبع canonical مربوطه، requirement قطعی این سند نیستند.

## تاریخچه بازنگری

| نسخه | تاریخ | وضعیت | توضیح |
|---|---|---|---|
| 1.0 تا 1.7 | تاریخی | Non-canonical / Derived | نسخه‌های پیش از Formal SRS. این نسخه‌ها برای تاریخچه مفیدند، اما رفتار جاری را تعیین نمی‌کنند. |
| 2.0 | 2026-08-17 | Formal Baseline | بازنویسی از منابع canonical مطابق Increment 0 در Roadmap و جداسازی requirementهای قطعی از design proposal و تصمیم‌های `OPEN`. |

# 1. مقدمه

## 1.1 هدف سند

این سند نیازمندی‌های عملکردی، غیرعملکردی و محدودیت‌های محصول Dotick را برای Personal V1 تعریف می‌کند. متن requirementها باید برای تحلیل، طراحی، تست، پیاده‌سازی و traceability قابل استفاده باشد.

این SRS پاسخ می‌دهد که سیستم چه رفتاری باید داشته باشد. این سند schema نهایی PostgreSQL، ORM mapping، endpointهای دقیق API، طراحی UI، الگوریتم نهایی scoring یا سایر جزئیات implementation را تعیین نمی‌کند، مگر آنکه یک محدودیت فنی به صورت canonical تثبیت شده باشد.

## 1.2 مرجع و ترتیب authority

در صورت تعارض، ترتیب authority پروژه برای تفسیر این SRS چنین است:

```text
Confirmed Decision Register entry
        ↓
System Definition
        ↓
Domain Model
        ↓
Formal SRS
        ↓
Reconciled non-canonical references
```

منابع این baseline:

- `project-docs/decision-register.md`
- `project-docs/02-requirements/system-definition.md`
- `project-docs/03-design/domain-model.md`
- `project-docs/01-planning/increment-roadmap.md` فقط برای scope، lifecycle سند و Decision Gateهای Incrementها

`project-docs/reference/class-fields.md` منبع requirement یا schema فیزیکی نیست و فقط یک derived field reference است.

## 1.3 قواعد normative

در این سند:

- عبارت `باید` یک requirement الزام‌آور در scope فعلی است.
- عبارت `نباید` یک ممنوعیت الزام‌آور است.
- عبارت `Future` یا `Enterprise` خارج از Personal V1 است.
- عبارت `OPEN` requirement قطعی نیست و تا زمان ثبت تصمیم canonical نباید در implementation به صورت ضمنی بسته شود.
- شناسه‌های requirement پایدارند. اصلاح نگارشی یا شفاف‌سازی نباید شناسه را تغییر دهد. تغییر معنایی باید در traceability و Decision Register قابل ردگیری باشد.
- Feature Priority در این سند وجود ندارد. ترتیب پیاده‌سازی فقط در Roadmap تعیین می‌شود.

## 1.4 روش verification

ستون `Verification` روش اصلی اثبات requirement را مشخص می‌کند:

- `Test`: تست خودکار یا acceptance/system test.
- `Inspection`: بررسی artifact، UI، contract یا configuration.
- `Analysis`: تحلیل محاسباتی، review مدل یا ارزیابی تخصصی.
- `Test + Inspection`: ترکیب تست رفتاری و بررسی artifact.

روش دقیق تست و test caseها در Test Strategy و specificationهای Increment مربوطه تعریف می‌شوند.

## 1.5 دامنه محصول

Dotick یک سیستم مدیریت Task، Event و Routine برای استفاده روزمره است. محصول علاوه بر مدیریت کار، Goal، Daily Ring، Dotick Day، آمار و قابلیت‌های AI-assisted را برای ایجاد Item و تحلیل معنایی ارائه می‌کند.

Personal V1 شامل استفاده شخصی، collaboration با Group و System-defined Role، offline sync، AI-assisted item creation، Goal discovery و Daily Rings است. Enterprise multi-tenancy، Custom Role، Enterprise SSO، automationهای trusted و integrationهای پیشرفته در scope فعلی نیستند.

## 1.6 کلاس‌های کاربری

- کاربر شخصی، کاربر اصلی Personal V1 است.
- عضو Group می‌تواند در داده‌های اشتراکی مطابق نقش سیستمی خود مشارکت کند.
- کاربر سازمانی و نقش‌های مدیریتی پیشرفته در scope Enterprise قرار دارند.
- همکار تحلیل داده یا مدل، در صورت اضافه شدن در آینده، به مستندات analytics و domain نیاز خواهد داشت.

# 2. توصیف کلی سیستم

## 2.1 مدل مفهومی سطح بالا

Dotick سه نوع Item user-facing دارد:

```text
Item
├── Schedulable
│   ├── Task
│   └── Event
└── Routine
```

`Goal` خارج از Item hierarchy است. `TrackingState` یک capability مشترک برای Routine و Goal است و به تنهایی الزام به inheritance دیتابیسی ایجاد نمی‌کند.

## 2.2 سازمان‌دهی اطلاعات

ساختار canonical سازمان‌دهی داده چنین است:

```text
Folder
└── List
    └── Column
```

`Tab` و `Section` نام‌های legacy برای Column هستند و entity مستقل محسوب نمی‌شوند.

## 2.3 اصول رفتاری سیستم

سیستم باید source of truth هر داده عملیاتی را از aggregate و derived data جدا نگه دارد. Daily Ring و عضویت Itemهای آن باید snapshot تاریخی باشند. پیچیدگی relation یا metadata در backend نباید بدون نیاز محصول به workflow پیچیده در UI تبدیل شود. AI در جریان ایجاد Item پیشنهاد می‌دهد و کاربر نتیجه نهایی را قبل از ایجاد رکورد واقعی تایید می‌کند.

# 3. نیازمندی‌های عملکردی

## 3.1 سازمان‌دهی، Inbox و navigation

مبنای canonical: System Definition بخش 3، DR-003 و Domain Model بخش 15.

| ID | Requirement | Verification |
|---|---|---|
| SRS-ORG-001 | سیستم باید ساختار سازمانی `Folder > List > Column` را پشتیبانی کند. | Test |
| SRS-ORG-002 | سیستم باید یک محل پیش‌فرض با مفهوم `Inbox` برای Itemهایی داشته باشد که کاربر هنگام ایجاد، محل مشخصی برای آن‌ها انتخاب نکرده است. | Test |
| SRS-ORG-003 | هر List باید یک Column پیش‌فرض برای Itemهای بدون Column صریح داشته باشد. | Test |
| SRS-ORG-004 | اگر Column پیش‌فرض تنها Column یک List باشد، سیستم نباید کاربر را مجبور به مشاهده نام فنی legacy آن، یعنی `not_sectioned`، کند. | Test + Inspection |
| SRS-ORG-005 | سیستم نباید `Tab` یا `Section` را به عنوان entity مستقل از Column مدل کند. | Inspection |
| SRS-ORG-006 | سیستم باید دسترسی به Folderها، Listها و ورودی روزانه یا Today را در navigation اصلی فراهم کند. | Test + Inspection |

## 3.2 Item، identity، ownership و source

مبنای canonical: System Definition بخش‌های 4 و 5، DR-014 و DR-015، Domain Model بخش‌های 2 و 6.

| ID | Requirement | Verification |
|---|---|---|
| SRS-ITEM-001 | سیستم باید Task، Event و Routine را به عنوان سه نوع اصلی محتوای user-facing پشتیبانی کند. | Test |
| SRS-ITEM-002 | هر Item باید یک شناسه پایدار داشته باشد و زمان ایجاد و آخرین ویرایش آن قابل ثبت باشد. | Test |
| SRS-ITEM-003 | هر Item باید title غیرخالی داشته باشد. | Test |
| SRS-ITEM-004 | سیستم باید soft-delete را برای Itemهایی که `is_trashed` دارند پشتیبانی کند. | Test |
| SRS-ITEM-005 | سیستم باید version metadata لازم برای Itemهای sync‌شونده را نگه دارد. | Test + Inspection |
| SRS-ITEM-006 | سیستم باید `owner_user_id` و `created_by_user_id` را به صورت دو مفهوم مستقل نگه دارد. | Test |
| SRS-ITEM-007 | سیستم باید provenance را از ownership جدا نگه دارد. `Source` نباید مبنای تشخیص مالک داخلی باشد. | Test |
| SRS-ITEM-008 | در Task/Event، Source باید حداقل platform و در صورت وجود external account و external id را قابل ثبت کند. | Test |
| SRS-ITEM-009 | `status` نباید یک property مشترک برای همه Itemها باشد. Task و Event status مستقل دارند و Routine status ندارد. | Test + Inspection |
| SRS-ITEM-010 | سیستم باید Tag، recurrence و reminder را به عنوان capabilityهای قابل اتصال به Item، مطابق محدودیت هر نوع Item، پشتیبانی کند. | Test |

## 3.3 Task

مبنای canonical: System Definition بخش 6، DR-012 و DR-013، Domain Model بخش 4.

| ID | Requirement | Verification |
|---|---|---|
| SRS-TASK-001 | سیستم باید ایجاد، بازیابی، ویرایش و soft-delete Task را پشتیبانی کند. | Test |
| SRS-TASK-002 | Task باید بتواند بدون زمان دقیق به صورت all-day تعریف شود. | Test |
| SRS-TASK-003 | اگر `end_at` وجود نداشته باشد، `due_at` باید یک due moment واحد را بیان کند. | Test |
| SRS-TASK-004 | اگر `end_at` وجود داشته باشد، `due_at` باید شروع duration Task باشد. | Test |
| SRS-TASK-005 | Task باید بتواند `deadline_at` مستقل از `due_at` داشته باشد. | Test |
| SRS-TASK-006 | وقتی deadline وجود دارد، Task باید `grace_period_days` با مقدار غیرمنفی داشته باشد. | Test |
| SRS-TASK-007 | سیستم باید statusهای `Todo`, `Overdue`, `Missed`, `Done`, `Won't_Do` و `Skipped` را برای Task پشتیبانی کند. | Test |
| SRS-TASK-008 | قبل از عبور از due، Task باید در حالت `Todo` باشد مگر اینکه کاربر آن را به یک نتیجه user-driven منتقل کرده باشد. | Test |
| SRS-TASK-009 | پس از عبور از due و پیش از deadline، یا وقتی deadline وجود ندارد، Task انجام‌نشده باید `Overdue` شود. | Test |
| SRS-TASK-010 | پس از عبور از deadline و در صورتی که grace بزرگ‌تر از صفر باشد، Task انجام‌نشده باید تا پایان grace در حالت `Missed` قرار گیرد. | Test |
| SRS-TASK-011 | اگر `grace_period_days = 0` باشد، Task انجام‌نشده باید هنگام عبور از deadline مستقیما `Skipped` شود و state قابل مشاهده `Missed` نداشته باشد. | Test |
| SRS-TASK-012 | پس از عبور از `deadline + grace period`، Task انجام‌نشده باید `Skipped` شود. | Test |
| SRS-TASK-013 | `Skipped` باید system-controlled باشد و کاربر نباید آن را مستقیما انتخاب کند. | Test |
| SRS-TASK-014 | کاربر باید بتواند Task را به صورت دستی `Done` یا `Won't_Do` کند. | Test |
| SRS-TASK-015 | Task باید بتواند با `blocked_by` به Taskهای دیگر وابسته باشد. | Test |
| SRS-TASK-016 | Task باید priorityهای `Urgent_Important`, `Important`, `Urgent` و `None` را پشتیبانی کند. | Test |

## 3.4 Event

مبنای canonical: System Definition بخش 7، DR-018، Domain Model بخش 5.

| ID | Requirement | Verification |
|---|---|---|
| SRS-EVENT-001 | سیستم باید ایجاد، بازیابی، ویرایش و soft-delete Event را پشتیبانی کند. | Test |
| SRS-EVENT-002 | Event باید start time یا all-day date داشته باشد و بتواند end time اختیاری داشته باشد. | Test |
| SRS-EVENT-003 | Event باید location اختیاری داشته باشد. | Test |
| SRS-EVENT-004 | Location باید بتواند حداقل coordinates، human-readable address، place identifier یا virtual meeting link را نمایندگی کند. | Test |
| SRS-EVENT-005 | سیستم باید statusهای `Not_Arrived`, `Ongoing` و `Finished` را برای Event پشتیبانی کند. | Test |
| SRS-EVENT-006 | Event باید بتواند sub-event ساختاری داشته باشد و هر sub-event اطلاعات مستقل خود را نگه دارد. | Test |
| SRS-EVENT-007 | یک Event باید بتواند در چند RichDescription به صورت reference نمایش داده شود. | Test |
| SRS-EVENT-008 | Event باید priorityهای `Urgent_Important`, `Important`, `Urgent` و `None` را پشتیبانی کند. | Test |

## 3.5 hierarchy ساختاری و reference

مبنای canonical: System Definition بخش 8، DR-016 تا DR-019، Domain Model بخش 3.

| ID | Requirement | Verification |
|---|---|---|
| SRS-HIER-001 | hierarchy ساختاری Task و Event باید از طریق relation مستقیم قابل query باشد و بازیابی آن نباید به parse کامل RichDescription وابسته باشد. | Test + Analysis |
| SRS-HIER-002 | relation ساختاری باید برای query و index شدن قابل طراحی باشد. | Inspection |
| SRS-HIER-003 | یک Task نباید بیش از یک structural parent داشته باشد. | Test |
| SRS-HIER-004 | سیستم باید cycle در parent relation ساختاری را رد کند. | Test |
| SRS-HIER-005 | backend باید structural child را از normal reference تشخیص دهد. | Test |
| SRS-HIER-006 | frontend نباید صرفا به دلیل تفاوت داخلی child و reference مجبور به ارائه دو workflow پیچیده و مستقل شود. | Inspection + Test |

## 3.6 RichDescription و ContentBlock

مبنای canonical: System Definition بخش 9، DR-020 و DR-021، Domain Model بخش 8.

| ID | Requirement | Verification |
|---|---|---|
| SRS-DESC-001 | Description در Task و Event باید block-based باشد. | Test + Inspection |
| SRS-DESC-002 | RichDescription باید TextBlock را با قابلیت Bold، Italic، Underline، Strikethrough، Heading، Highlight، Bullets، Numbers، Indent، Separator، Code، Quote و تشخیص link/phone/id پشتیبانی کند. | Test |
| SRS-DESC-003 | RichDescription باید Attachment، Location و Item reference برای Task/Event را پشتیبانی کند. | Test |
| SRS-DESC-004 | هر ContentBlock باید identity پایدار داشته باشد تا comment، reorder، edit و sync بتوانند همان block را شناسایی کنند. | Test |
| SRS-DESC-005 | تغییر ترتیب blockها نباید identity آن‌ها را از بین ببرد. | Test |

## 3.7 Comment

مبنای canonical: System Definition بخش 9.1 و Domain Model بخش 9.

| ID | Requirement | Verification |
|---|---|---|
| SRS-COMMENT-001 | هر Task و Event باید comment thread مربوط به کل Item داشته باشد. | Test |
| SRS-COMMENT-002 | کاربر مجاز باید بتواند comment را به یک ContentBlock مشخص متصل کند. | Test |
| SRS-COMMENT-003 | comment متصل به block باید هم در context همان block و هم در thread کلی Item قابل مشاهده باشد. | Test |
| SRS-COMMENT-004 | سیستم باید author و زمان ایجاد و ویرایش comment را قابل نگهداری کند. | Test |

## 3.8 Routine

مبنای canonical: System Definition بخش 10، DR-004 تا DR-010 و DR-022، Domain Model بخش‌های 10 تا 12.

| ID | Requirement | Verification |
|---|---|---|
| SRS-ROUTINE-001 | هر Routine باید یک definition واحد باشد و سیستم نباید برای هر روز یک Routine جدید بسازد. | Test |
| SRS-ROUTINE-002 | Routine نباید Schedulable باشد و نباید status مستقل داشته باشد. | Test + Inspection |
| SRS-ROUTINE-003 | Routine باید `start_date` اختیاری داشته باشد و در صورت نبود آن، اعتبار Routine از تاریخ ایجاد شروع شود. | Test |
| SRS-ROUTINE-004 | Routine باید `end_date` اختیاری داشته باشد و در صورت نبود آن، تعریف Routine از نظر validity window بدون پایان باشد. | Test |
| SRS-ROUTINE-005 | `end_date` باید تولید occurrenceهای scheduled آینده را پس از آن تاریخ متوقف کند و به تنهایی نباید archive state جدا ایجاد کند. | Test |
| SRS-ROUTINE-006 | outcome یک Routine در یک روز باید در `RoutineCompletion` ثبت شود، نه در status خود Routine. | Test |
| SRS-ROUTINE-007 | `RoutineCompletion.status` باید `Done` یا `Won't_Do` باشد. | Test |
| SRS-ROUTINE-008 | `occurrence_date` باید تاریخ business مربوط به یک RoutineCompletion را مشخص کند. | Test |
| SRS-ROUTINE-009 | برای هر زوج `(routine_id, occurrence_date)` فقط یک RoutineCompletion جاری مجاز است. | Test |
| SRS-ROUTINE-010 | نبود RoutineCompletion برای یک روز نباید به صورت `Done` یا `Won't_Do` تفسیر شود. | Test |
| SRS-ROUTINE-011 | در targetهای Partial، تغییر amount همان روز باید همان RoutineCompletion جاری را update کند. | Test |
| SRS-ROUTINE-012 | Reset یک RoutineCompletion باید row جاری همان Routine و occurrence_date را حذف کند. | Test |
| SRS-ROUTINE-013 | Reset نباید history مربوط به آن تغییر را از AuditLog حذف کند. | Test |
| SRS-ROUTINE-014 | `Won't_Do` باید یک outcome صریح و ماندگار باشد و نباید معادل Reset تلقی شود. | Test |
| SRS-ROUTINE-015 | کاربر باید بتواند RoutineCompletion روزهای گذشته را ویرایش کند. | Test |
| SRS-ROUTINE-016 | کاربر باید بتواند برای یک روز unscheduled نیز RoutineCompletion معتبر ثبت کند. | Test |
| SRS-ROUTINE-017 | recurrence یک Routine باید تعیین کند Routine در چه روزهایی به صورت scheduled پیشنهاد شود، اما نباید ثبت completion در روز دیگر را ممنوع کند. | Test |
| SRS-ROUTINE-018 | صفحه روزانه Routineها باید scheduled Routineهای روز انتخاب‌شده را به عنوان پیشنهاد اصلی نمایش دهد. | Test + Inspection |
| SRS-ROUTINE-019 | اگر Routine در یک روز unscheduled به صورت دستی complete شده باشد، completion ثبت‌شده باید در history یا context مربوط به آن روز قابل مشاهده باشد. | Test |
| SRS-ROUTINE-020 | صفحه اختصاصی Routine باید امکان مشاهده تقویم Routine و ثبت completion دستی در روز unscheduled را فراهم کند. | Test + Inspection |
| SRS-ROUTINE-021 | Routine target باید حداقل `Achieve_All` و `Partial` را پشتیبانی کند. | Test |
| SRS-ROUTINE-022 | target نوع `Partial` باید periodهای `Daily`, `Weekly`, `Monthly`, `Yearly`، مقدار پایه، unit و حالت incremental اختیاری را پشتیبانی کند. | Test |
| SRS-ROUTINE-023 | unitهای Partial باید حداقل `Count`, `Cup`, `Liter`, `Minute`, `Hour`, `Meter`, `Kilometer`, `Page`, `Step` و `Custom` را پوشش دهند. | Test |
| SRS-ROUTINE-024 | TrackingState Routine باید حداقل current streak، best streak و total completions را قابل نگهداری کند. | Test |
| SRS-ROUTINE-025 | RoutineCompletion باید شناسه پایدار، `created_at`, `updated_at` و `version` داشته باشد. | Test |
| SRS-ROUTINE-026 | RoutineCompletion باید `amount` و `note` اختیاری را پشتیبانی کند. | Test |
| SRS-ROUTINE-027 | سیستم نباید `completed_at` را به عنوان business identity روز RoutineCompletion استفاده کند؛ `occurrence_date` باید این نقش را داشته باشد. | Test + Inspection |
| SRS-ROUTINE-028 | occurrenceهای scheduled Routine نباید خارج از validity window تعریف‌شده با `start_date` و `end_date` تولید شوند. | Test |

## 3.9 Routine streak

مبنای canonical: System Definition بخش 11.2، DR-010 و Domain Model بخش 14.

| ID | Requirement | Verification |
|---|---|---|
| SRS-RSTREAK-001 | در Routine با occurrenceهای fixed-day، completion معتبر scheduled باید در sequence streak قابل شمارش باشد. | Test |
| SRS-RSTREAK-002 | missed scheduled occurrence باید sequence streak fixed-day را قطع کند. | Test |
| SRS-RSTREAK-003 | completion در روز unscheduled باید completion معتبر باشد، اما نباید missed occurrence قبلی را ترمیم یا جایگزین کند. | Test |
| SRS-RSTREAK-004 | completion معتبر پس از break باید بتواند sequence جدید streak را شروع یا ادامه دهد. | Test |
| SRS-RSTREAK-005 | Routine از نوع frequency-based باید بتواند quota به شکل `N times per period` داشته باشد و completionهای روزهای مختلف همان period را تا رسیدن به quota بپذیرد. | Test |
| SRS-RSTREAK-006 | در Routine از نوع frequency-based، تکمیل quota نباید به fixed weekdayهای از پیش تعیین‌شده وابسته باشد، مگر خود تعریف Routine چنین محدودیتی داشته باشد. | Test |

## 3.10 Recurrence

مبنای canonical: System Definition بخش 11.1، DR-011 و Domain Model بخش 13.

| ID | Requirement | Verification |
|---|---|---|
| SRS-REC-001 | سیستم باید recurrence را بر اساس calendar انتخاب‌شده از میان `Jalali` و `Gregorian` محاسبه کند. | Test |
| SRS-REC-002 | Task و Event باید recurrence در granularityهای minute، hour، day، week، month و year را پشتیبانی کنند. | Test |
| SRS-REC-003 | Task و Event باید advanced combined expression مبتنی بر day/hour/minute را پشتیبانی کنند. | Test |
| SRS-REC-004 | Routine باید recurrence روزمحور در granularityهای day، week، month و year را پشتیبانی کند. | Test |
| SRS-REC-005 | Routine نباید recurrence دقیقه‌ای، ساعتی یا advanced day/hour/minute داشته باشد. | Test |
| SRS-REC-006 | سیستم باید recurrenceهای Constant شامل Daily، Weekly، Monthly و Yearly را پشتیبانی کند. | Test |
| SRS-REC-007 | سیستم باید interval recurrence برای هر `x` دقیقه، ساعت، روز، هفته، ماه یا سال را در entityهایی که آن granularity را مجاز می‌دانند پشتیبانی کند. | Test |
| SRS-REC-008 | week recurrence باید weekdayهای انتخابی را پشتیبانی کند. | Test |
| SRS-REC-009 | month recurrence باید dayهای انتخابی و `last_day` را پشتیبانی کند. | Test |
| SRS-REC-010 | year recurrence باید month/day انتخابی را پشتیبانی کند. | Test |
| SRS-REC-011 | `last_day` و سایر محاسبات day/month/year باید در همان calendar انتخاب‌شده resolve شوند. | Test |
| SRS-REC-012 | validation recurrence باید capability matrix هر entity را enforce کند. | Test |

## 3.11 Reminder

مبنای canonical: System Definition بخش 12 و Domain Model بخش 27.

| ID | Requirement | Verification |
|---|---|---|
| SRS-REM-001 | Task، Event و Routine باید بتوانند چند reminder داشته باشند. | Test |
| SRS-REM-002 | هر reminder باید بتواند trigger-before را بیان کند. | Test |
| SRS-REM-003 | domain باید intent مربوط به persistent یا alarm-like reminder را مستقل از محدودیت platform نمایندگی کند. | Test + Inspection |
| SRS-REM-004 | در جریان AI-assisted creation، reminderهای پیشنهادی باید قبل از ایجاد Item قابل مشاهده و ویرایش باشند. | Test |

## 3.12 Authentication و session

مبنای canonical: System Definition بخش 23، DR-050.

| ID | Requirement | Verification |
|---|---|---|
| SRS-AUTH-001 | سیستم باید authentication با email و password را پشتیبانی کند. | Test |
| SRS-AUTH-002 | سیستم نباید password را به صورت plaintext ذخیره کند و باید از password hashing امن استفاده کند. | Test + Inspection |
| SRS-AUTH-003 | سیستم باید Google OAuth را برای authentication پشتیبانی کند. | Test |
| SRS-AUTH-004 | سیستم باید session کاربر را با JWT پشتیبانی کند. | Test |
| SRS-AUTH-005 | اگر Google OAuth در دسترس نباشد، مسیر email/password باید برای login قابل استفاده باقی بماند. | Test |
| SRS-AUTH-006 | سیستم باید Passkey را برای authentication پشتیبانی کند. | Test |

## 3.13 Viewها و presentation

مبنای canonical: System Definition بخش‌های 3.1 و 28، Roadmap Increment 5 برای scope presentation.

| ID | Requirement | Verification |
|---|---|---|
| SRS-VIEW-001 | سیستم باید داده یکسان را بدون تغییر domain data در presentationهای مختلف نمایش دهد. | Test |
| SRS-VIEW-002 | صفحه List باید حداقل Viewهای `List`, `Kanban` و `Timeline` را پشتیبانی کند. | Test + Inspection |
| SRS-VIEW-003 | سیستم باید View یا صفحه مستقل `Calendar` را ارائه کند. | Test + Inspection |
| SRS-VIEW-004 | سیستم باید صفحه مستقل Routine را ارائه کند. | Test + Inspection |
| SRS-VIEW-005 | سیستم باید View یا صفحه `Eisenhower / Priority Matrix` را بر پایه priority ارائه کند. | Test + Inspection |
| SRS-VIEW-006 | رابط کاربری Personal V1 باید responsive و mobile-first باشد. | Test + Inspection |
| SRS-VIEW-007 | سیستم باید امکان ارائه themeهای `Minimal customizable`, `Liquid Glass`, `Material 3 Expressive inspired` و `Dot-matrix` را در presentation layer داشته باشد. | Inspection |

## 3.14 Offline use و sync

مبنای canonical: System Definition بخش 22، DR-049، Domain Model بخش 30.

| ID | Requirement | Verification |
|---|---|---|
| SRS-SYNC-001 | سیستم باید core flowهای پشتیبانی‌شده را بدون اتصال اینترنت قابل استفاده نگه دارد. | Test |
| SRS-SYNC-002 | تغییرات local پشتیبانی‌شده باید تا زمان reconnect حفظ شوند. | Test |
| SRS-SYNC-003 | پس از reconnect، سیستم باید تغییرات local را با server همگام کند. | Test |
| SRS-SYNC-004 | conflict resolution baseline باید در سطح field اعمال شود، نه فقط در سطح record کامل. | Test |
| SRS-SYNC-005 | اگر یک field در چند replica تغییر کرده باشد، baseline conflict policy باید Field-level Last-Write-Wins بر مبنای metadata زمانی تعریف‌شده باشد. | Test |
| SRS-SYNC-006 | entityهای sync‌شونده باید version و metadata زمانی کافی برای sync policy داشته باشند. | Test + Inspection |
| SRS-SYNC-007 | sync نباید AuditLog و history لازم برای بررسی conflict و recovery را از بین ببرد. | Test |

## 3.15 Audit، history و Undo

مبنای canonical: System Definition بخش 21، Domain Model بخش 25.

| ID | Requirement | Verification |
|---|---|---|
| SRS-AUDIT-001 | سیستم باید history قابل استفاده‌ای از تغییرات مهم نگه دارد. | Test |
| SRS-AUDIT-002 | Audit history باید actor، entity، action، زمان رخداد و previous/new value یا diff لازم را قابل ثبت کند. | Test |
| SRS-AUDIT-003 | حذف state جاری در flowهایی مانند RoutineCompletion Reset نباید history آن تغییر را حذف کند. | Test |
| SRS-AUDIT-004 | history باید بتواند برای مشاهده تغییرات، troubleshooting sync و Undo/restore در flowهایی که محصول اجازه می‌دهد استفاده شود. | Test + Inspection |
| SRS-AUDIT-005 | AuditLog نباید سیستم را ملزم به full event sourcing کند. | Inspection |

## 3.16 Group، Role و Assignment

مبنای canonical: System Definition بخش 24، DR-024، Domain Model بخش 29.

| ID | Requirement | Verification |
|---|---|---|
| SRS-GROUP-001 | یک User باید بتواند هم‌زمان عضو چند Group باشد. | Test |
| SRS-GROUP-002 | هر GroupMembership در Personal V1 باید یک System-defined Role داشته باشد. | Test |
| SRS-GROUP-003 | Custom Role نباید بخشی از role model فعلی Personal V1 باشد. | Inspection |
| SRS-GROUP-004 | سیستم باید assignment یک Task به چند عضو Group را پشتیبانی کند. | Test |
| SRS-GROUP-005 | داده Groupها باید از Groupهای دیگر و از userهای غیرمجاز ایزوله باشد. | Security Test |
| SRS-GROUP-006 | زمان یک Task/Event اشتراکی باید یک instant مطلق قابل تبدیل داشته باشد و برای هر عضو بر اساس timezone او نمایش داده شود. | Test |
| SRS-GROUP-007 | live update و notificationهای Group باید بتوانند از کانال WebSocket سبک استفاده کنند، در حالی که REST مرجع عملیات CRUD باقی می‌ماند. | Integration Test |

## 3.17 Tag

مبنای canonical: System Definition بخش 14، DR-047، Domain Model بخش 16.

| ID | Requirement | Verification |
|---|---|---|
| SRS-TAG-001 | Tag باید entity مستقل باشد. | Test + Inspection |
| SRS-TAG-002 | Tag باید source از نوع `User` یا `AI` داشته باشد. | Test |
| SRS-TAG-003 | یک Item باید بتواند چند Tag داشته باشد و یک Tag باید بتواند به چند Item متصل شود. | Test |
| SRS-TAG-004 | یک Goal باید بتواند چند Tag داشته باشد. | Test |
| SRS-TAG-005 | Tag ساخته‌شده توسط user نباید صرفا به دلیل semantic cleanup به صورت خودکار archive شود. | Test |
| SRS-TAG-006 | AI tag باید در semantic review قابلیت merge یا archive شدن داشته باشد. | Test |
| SRS-TAG-007 | سیستم باید بتواند ارتباط معنایی Goal با Itemها را از طریق Tagهای مرتبط برقرار کند. | Test |
| SRS-TAG-008 | هر Tag باید شناسه پایدار و title داشته باشد. | Test |

## 3.18 Goal و lifecycle

مبنای canonical: System Definition بخش 13، DR-023، DR-025، DR-027، DR-028 و DR-047، Domain Model بخش 17.

| ID | Requirement | Verification |
|---|---|---|
| SRS-GOAL-001 | Goal باید entity مستقل و خارج از Item hierarchy باشد. | Test + Inspection |
| SRS-GOAL-002 | تعداد Goalهای قابل نگهداری برای user نباید سقف ثابت محصولی داشته باشد. | Test |
| SRS-GOAL-003 | Goal باید lifecycle stateهای `Active`, `Dormant` و `Archived` را پشتیبانی کند. | Test |
| SRS-GOAL-004 | Goal باید بتواند به List و در صورت نیاز Column مرتبط شود. | Test |
| SRS-GOAL-005 | وقتی Goal فعلا Item فعال و معنادار مرتبط با progress ندارد، lifecycle آن باید بتواند وارد حالت `Dormant` شود. | Test |
| SRS-GOAL-006 | Goal در حالت `Dormant` نباید برای Daily Ring eligibility در نظر گرفته شود. | Test |
| SRS-GOAL-007 | ورود Goal به `Dormant` نباید current streak آن را reset کند و streak باید freeze شود. | Test |
| SRS-GOAL-008 | Goal `Dormant` باید در recheck بتواند دوباره Active شود، مشروط به قواعد similarity که در Decision Gate مربوطه نهایی می‌شوند. | Test |
| SRS-GOAL-009 | Goal `Archived` نباید به صورت خودکار reactivate شود. | Test |
| SRS-GOAL-010 | `Goal.current_streak` باید تعداد Dotick Dayهای متوالی باشد که DailyRing همان Goal complete شده است. | Test |
| SRS-GOAL-011 | `Goal.total_completions` باید تعداد کل Dotick Dayهایی باشد که Goal complete شده است. | Test |
| SRS-GOAL-012 | فعالیتی که DailyRing را به completion threshold نمی‌رساند نباید به تنهایی Goal streak را حفظ کند. | Test |
| SRS-GOAL-013 | سیستم باید قابلیت reminder سطح Goal را مستقل از reminderهای تک Item داشته باشد و trigger آن بتواند افت معنادار نسبت به Norm را در نظر بگیرد. | Test |
| SRS-GOAL-014 | TrackingState Goal باید بتواند `best_streak` را در کنار current streak و total completions نگه دارد. | Test |
| SRS-GOAL-015 | هر Goal باید شناسه پایدار و title داشته باشد و description آن می‌تواند اختیاری باشد. | Test |

## 3.19 AI Goal discovery و GoalGenerationLog

مبنای canonical: System Definition بخش 15، DR-045 تا DR-048، Domain Model بخش 18.

| ID | Requirement | Verification |
|---|---|---|
| SRS-GDISC-001 | AI Goal discovery باید List، Column، محتوای واقعی Itemها و Tagهای موجود را به عنوان context بررسی کند. | Test + Analysis |
| SRS-GDISC-002 | نام List یا Column نباید تنها مبنای ایجاد Goal باشد. | Test |
| SRS-GDISC-003 | سیستم نباید برای grouping نامنسجم یا بدون semantic coherence به اجبار Goal ایجاد کند. | Test + Analysis |
| SRS-GDISC-004 | initial semantic flow باید Tagهای user را در context قرار دهد تا duplicate یا Tagهای بسیار مشابه کاهش یابند. | Test + Analysis |
| SRS-GDISC-005 | در current model، تعداد Goalهای استخراج‌شده از یک List نباید از تعداد Columnهای معنادار آن بیشتر شود، مگر اینکه یک تصمیم canonical بعدی این rule را تغییر دهد. | Test + Analysis |
| SRS-GDISC-006 | reactive review برای context جدید یا Dormant باید بتواند با baseline delay برابر 12 ساعت اجرا شود و فقط context متاثر را دوباره ارزیابی کند. | Test |
| SRS-GDISC-007 | سیستم باید weekly global review برای merge Goalهای بسیار مشابه، cleanup یا archive AI tagها و semantic refresh داشته باشد. | Test |
| SRS-GDISC-008 | هر Initial Generation، Weekly Review یا Reactivation Check مربوط به Goal باید در `GoalGenerationLog` قابل ثبت باشد. | Test |
| SRS-GDISC-009 | GoalGenerationLog باید model/version استفاده‌شده، changed flag، previous/new title و description و زمان ایجاد را قابل نگهداری کند. | Test |
| SRS-GDISC-010 | user rating در GoalGenerationLog باید فقط وقتی مرتبط باشد که تغییر واقعی AI رخ داده باشد. | Test |
| SRS-GDISC-011 | GoalGenerationLog باید append-only باشد؛ review جدید باید entry جدید ایجاد کند و history قبلی را بازنویسی نکند. | Test |

## 3.20 Daily Ring selection و snapshot

مبنای canonical: System Definition بخش 16، DR-026، DR-033، DR-034، DR-045 و DR-046، Domain Model بخش‌های 19 و 20.

| ID | Requirement | Verification |
|---|---|---|
| SRS-RING-001 | تعداد Daily Ring فعال هر Dotick Day باید `min(3, eligible_active_goals)` باشد. | Test |
| SRS-RING-002 | اگر حداقل سه Goal eligible وجود داشته باشد، سیستم باید دقیقا سه Daily Ring بسازد. | Test |
| SRS-RING-003 | اگر دو Goal eligible وجود داشته باشد، سیستم باید دو Ring و اگر یک Goal eligible وجود داشته باشد یک Ring بسازد. | Test |
| SRS-RING-004 | اگر Goal eligible وجود نداشته باشد، سیستم نباید Daily Ring فعال ایجاد کند. | Test |
| SRS-RING-005 | selection باید ترکیب روز را balanced کند و نباید صرفا بزرگ‌ترین backlog را انتخاب کند. | Analysis + Test |
| SRS-RING-006 | selection باید حداقل due/timing، priority، neglect، weekday behavior، holiday context، streak momentum، workload، difficulty و recent user capacity را به عنوان signal قابل استفاده در نظر بگیرد. | Analysis + Inspection |
| SRS-RING-007 | DailyRing باید user، goal، effective date، target، progress، completion state، final score، finalization state و algorithm/version metadata لازم را به صورت snapshot نگه دارد. | Test |
| SRS-RING-008 | تغییر عادی future fieldهای Item نباید معنای historical DailyRing را بازنویسی کند. | Test |
| SRS-RING-009 | DailyRingItem باید membership Itemهای انتخاب‌شده همان روز و featureهای scoring لازم برای بازسازی تصمیم آن روز را snapshot کند. | Test |
| SRS-RING-010 | Task، Event و Routine occurrence باید بتوانند در صورت eligibility عضو DailyRingItem شوند. | Test |
| SRS-RING-011 | completion یک Item فقط باید Ring همان credited day را جلو ببرد که Item در DailyRingItem آن Ring عضو بوده است. | Test |
| SRS-RING-012 | completion یک Item خارج از DailyRingItemهای credited day نباید progress هیچ Goal روزانه‌ای را افزایش دهد. | Test |

## 3.21 Progress، completion، performance score و Norm

مبنای canonical: System Definition بخش 17، DR-029 تا DR-032، Domain Model بخش 21.

| ID | Requirement | Verification |
|---|---|---|
| SRS-SCORE-001 | `progress_percent` DailyRing باید در بازه 0 تا 100 باقی بماند. | Test |
| SRS-SCORE-002 | UI نباید progress بزرگ‌تر از 100 نمایش دهد. | Test + Inspection |
| SRS-SCORE-003 | `is_completed` باید زمانی true شود که progress به completion threshold برابر 100 درصد برسد. | Test |
| SRS-SCORE-004 | `final_score` باید از progress جدا باشد و بتواند از baseline یا 100 بالاتر برود. | Test |
| SRS-SCORE-005 | bonusهای performance که ممکن است حس completion زودهنگام ایجاد کنند باید تا day finalization برای user مخفی بمانند. | Test |
| SRS-SCORE-006 | final score و bonusهای مخفی باید در day finalization محاسبه یا reveal شوند. | Test |
| SRS-SCORE-007 | انجام زودتر یک Item مهم باید بتواند final performance score بیشتری نسبت به انجام دیرتر همان کار در شرایط قابل مقایسه ایجاد کند. | Test + Analysis |
| SRS-SCORE-008 | در انتهای روز، انجام کارهای relevant باقی‌مانده باید همچنان بتواند progress واقعی را به completion نزدیک کند. | Test + Analysis |
| SRS-SCORE-009 | late-day recovery نباید progress را از 100 بالاتر ببرد و overachievement باید در final score منعکس شود. | Test |
| SRS-SCORE-010 | target روزانه Ring نباید به صورت مستقیم توسط user تعیین شود. | Test |
| SRS-SCORE-011 | repeated misses باید بتواند target یا Norm را به صورت موقت کاهش دهد. | Test + Analysis |
| SRS-SCORE-012 | recovery عملکرد باید بتواند target را به صورت تدریجی به سطح قبلی برگرداند. | Test + Analysis |
| SRS-SCORE-013 | repeated success باید بتواند target را به صورت تدریجی افزایش دهد. | Test + Analysis |
| SRS-SCORE-014 | داده جدید باید بتواند Norm را بر اساس رفتار واقعی user به‌روزرسانی کند. | Test + Analysis |

## 3.22 Dotick Day و credited date

مبنای canonical: System Definition بخش 19، DR-035 تا DR-037، Domain Model بخش‌های 22 و 23.

| ID | Requirement | Verification |
|---|---|---|
| SRS-DAY-001 | سیستم باید `Dotick Day` را به عنوان روز منطقی مستقل از Calendar Day پشتیبانی کند. | Test |
| SRS-DAY-002 | UserPreferences باید timezone کاربر را برای محاسبات زمانی و نمایش محلی نگه دارد. | Test |
| SRS-DAY-003 | user باید بتواند day boundary صریح تنظیم کند. | Test |
| SRS-DAY-004 | اگر user day boundary صریح تنظیم نکرده باشد، ambiguity window پیش‌فرض باید 60 دقیقه پس از midnight local باشد. | Test |
| SRS-DAY-005 | در حالت پیش‌فرض، completion ثبت‌شده در ambiguity window باید امکان attribution به Today یا Yesterday را به user بدهد. | Test |
| SRS-DAY-006 | اگر day boundary صریح تنظیم شده باشد، completion پیش از آن boundary باید به Dotick Day قبلی attribution شود. | Test |
| SRS-DAY-007 | completionهایی که در scoring استفاده می‌شوند باید credited/effective date داشته باشند که در صورت نیاز از raw timestamp مستقل باشد. | Test |
| SRS-DAY-008 | در day boundary، سیستم باید DailyRingهای روز قبلی را finalize کند. | Test |
| SRS-DAY-009 | finalization باید completion state و final score DailyRing را تثبیت و bonus مربوطه را reveal کند. | Test |
| SRS-DAY-010 | finalization باید Goal streak state مربوط به روز بسته‌شده را update کند. | Test |
| SRS-DAY-011 | پس از بسته شدن روز قبلی، سیستم باید DailyRingهای روز جدید را تولید کند. | Test |
| SRS-DAY-012 | پس از finalization، historical Ring باید snapshot تاریخی باقی بماند و تغییر عادی Item نباید آن را خودکار باز کند. | Test |

## 3.23 Statistics و historical correction

مبنای canonical: System Definition بخش 20، DR-038، Domain Model بخش 24.

| ID | Requirement | Verification |
|---|---|---|
| SRS-STAT-001 | تغییر historical RoutineCompletion باید آمار متاثر را اصلاح کند. | Test |
| SRS-STAT-002 | سیستم نباید به صورت پیش‌فرض برای هر historical edit کل history را از ابتدا recompute کند. | Test + Analysis |
| SRS-STAT-003 | recomputation باید به windowها و metricهای متاثر محدود شود، مگر maintenance job یا recovery صریح نیاز دیگری داشته باشد. | Test + Analysis |
| SRS-STAT-004 | simple lifetime counterها باید در صورت امکان با increment/decrement اصلاح شوند. | Test |
| SRS-STAT-005 | streakهایی که historical edit روی آن‌ها اثر دارد باید در محدوده لازم دوباره محاسبه شوند. | Test |
| SRS-STAT-006 | raw completion و state-change data باید source of truth آمار باشند، نه dashboard aggregate. | Test + Inspection |
| SRS-STAT-007 | behavior featureهای پرهزینه باید بتوانند مستقل از core write path refresh شوند. | Test + Analysis |

## 3.24 AI-assisted Item creation

مبنای canonical: System Definition بخش 25، DR-039 تا DR-043، Domain Model بخش 26.

| ID | Requirement | Verification |
|---|---|---|
| SRS-AIITEM-001 | سیستم باید AI-assisted Item creation را حداقل از Text و Voice پشتیبانی کند. | Test |
| SRS-AIITEM-002 | در contextهایی که user Item ایجاد می‌کند، UI باید در صورت عملی بودن ورودی voice را در کنار create input در دسترس قرار دهد. | Inspection + Test |
| SRS-AIITEM-003 | Voice input باید پیش از AI analysis به transcript قابل پردازش تبدیل شود. | Test |
| SRS-AIITEM-004 | AI باید در صورت قابل استنتاج بودن بتواند Task یا Event بودن ورودی، title، date/time، location، description، Folder، List، Column و reminder را پیشنهاد دهد. | Test + Evaluation |
| SRS-AIITEM-005 | AI output باید به عنوان Draft/Proposal نمایش داده شود و user باید بتواند تمام جزئیات پیشنهادی را قبل از ایجاد Item ویرایش کند. | Test |
| SRS-AIITEM-006 | سیستم نباید صرفا بر اساس AI inference و پیش از Confirm user رکورد نهایی Item ایجاد کند. | Test |
| SRS-AIITEM-007 | پس از Confirm، سیستم باید Item واقعی را از payload نهایی تاییدشده ایجاد کند. | Test |
| SRS-AIITEM-008 | سیستم باید بتواند یک AIItemCreationSession شامل source type، original input، transcript در صورت وجود، AI proposal، user final payload، model version، accepted state و timestamps را نگه دارد. | Test |
| SRS-AIITEM-009 | سیستم باید بتواند field-level change بین AI proposal و user final payload را برای evaluation و future personalization نگه دارد. | Test |
| SRS-AIITEM-010 | draft/session باید بتواند provenance field را حداقل میان explicit user input، AI inferred، user-preference inferred و external source تفکیک کند. | Test |
| SRS-AIITEM-011 | failure سرویس AI یا STT نباید manual Item creation و core task management را از کار بیندازد. | Failure Test |
| SRS-AIITEM-012 | payload نهایی AI-assisted creation باید پیش از ایجاد Item واقعی همان validationهای domain مربوط به Task/Event را پاس کند. | Test |

# 4. نیازمندی‌های رابط خارجی و محدودیت‌های فنی

## 4.1 API و ارتباط client/server

مبنای canonical: System Definition بخش 27 و Roadmap Increment 0 برای engineering baseline.

| ID | Requirement | Verification |
|---|---|---|
| SRS-IF-001 | frontend و backend باید به عنوان بخش‌های جدا با contract ارتباطی مشخص توسعه‌پذیر باشند. | Inspection |
| SRS-IF-002 | عملیات CRUD اصلی باید از REST استفاده کنند. | Integration Test |
| SRS-IF-003 | فرمت تبادل اصلی REST باید JSON باشد. | Contract Test |
| SRS-IF-004 | WebSocket باید برای notification و live update سبک استفاده شود و نباید جایگزین CRUD authority مبتنی بر REST شود. | Integration Test + Inspection |
| SRS-IF-005 | ارتباط client/server باید از HTTPS استفاده کند. در local development فقط Deployment Design می‌تواند برای محیطی که HTTPS عملا قابل اعمال نیست exception صریح تعریف کند. | Security Test + Inspection |

## 4.2 storage و platform constraints

| ID | Requirement | Verification |
|---|---|---|
| SRS-CON-001 | persistence اصلی server-side باید از PostgreSQL استفاده کند. | Inspection + Integration Test |
| SRS-CON-002 | hierarchy مفهومی Domain Model نباید به تنهایی implementation را به Class Table Inheritance متعهد کند. | Architecture Inspection |
| SRS-CON-003 | storage strategy باید query simplicity، integrity، migration safety و performance لازم برای behaviorهای این SRS را حفظ کند. | Architecture Review + Test |
| SRS-CON-004 | Personal V1 باید بتواند روی server local-hosted اجرا شود. | Deployment Test |

# 5. نیازمندی‌های غیرعملکردی

## 5.1 امنیت

مبنای canonical: System Definition بخش 29 و requirements امنیتی مرتبط با Authentication/Group.

| ID | Requirement | Verification |
|---|---|---|
| SRS-NFR-SEC-001 | password plaintext نباید در persistence یا logهای عادی ذخیره شود. | Security Test + Inspection |
| SRS-NFR-SEC-002 | password credential باید با الگوریتم hashing امن مانند Argon2، bcrypt یا معادل امن پروژه محافظت شود. | Security Inspection |
| SRS-NFR-SEC-003 | requestها و queryهای user-private باید دسترسی user دیگر به داده خصوصی را در حالت عادی رد کنند. | Security Test |
| SRS-NFR-SEC-004 | queryها و authorization مربوط به Group باید cross-group data leakage را رد کنند. | Security Test |
| SRS-NFR-SEC-005 | WebSocket و سایر live channelها باید همان authorization لازم برای داده قابل مشاهده را رعایت کنند. | Security Test |

## 5.2 قابلیت اطمینان و حفاظت از داده

| ID | Requirement | Verification |
|---|---|---|
| SRS-NFR-REL-001 | failure سرویس خارجی AI نباید core manual task management را unavailable کند. | Failure Test |
| SRS-NFR-REL-002 | Reset و historical edit باید history لازم برای recovery و بررسی خطا را حفظ کنند. | Test |
| SRS-NFR-REL-003 | sync conflict resolution نباید تغییر fieldهای مستقل را صرفا به دلیل conflict در field دیگر از بین ببرد. | Sync Test |
| SRS-NFR-REL-004 | historical DailyRing snapshot نباید با تغییرات عادی آینده به صورت ناخواسته بازنویسی شود. | Regression Test |

## 5.3 کارایی

| ID | Requirement | Verification |
|---|---|---|
| SRS-NFR-PERF-001 | بازیابی hierarchy child/parent باید بدون parse کامل RichDescription انجام شود. | Performance Test + Analysis |
| SRS-NFR-PERF-002 | design hierarchy باید امکان index-supported query را فراهم کند. | Data Design Inspection + Performance Test |
| SRS-NFR-PERF-003 | baseline local deployment باید در Performance Test Plan برای حدود 30 user هم‌زمان ارزیابی شود. این عدد test target است و SLA محسوب نمی‌شود. | Performance Test |
| SRS-NFR-PERF-004 | live update گروهی باید در Performance Test Plan با threshold مناسب برای تجربه تقریبا real-time ارزیابی شود. | Performance Test |
| SRS-NFR-PERF-005 | historical edit نباید به صورت پیش‌فرض full-history recomputation synchronous را به core user action تحمیل کند. | Performance Test + Analysis |

## 5.4 usability و presentation

| ID | Requirement | Verification |
|---|---|---|
| SRS-NFR-UX-001 | UI باید در اندازه‌های رایج mobile و layoutهای responsive قابل استفاده باقی بماند. | Usability Test + Inspection |
| SRS-NFR-UX-002 | پیچیدگی داخلی child/reference، sync metadata یا storage inheritance نباید بدون requirement صریح به controlهای پیچیده اضافی در UI نشت کند. | UX Inspection |
| SRS-NFR-UX-003 | AI proposal باید قبل از Confirm برای user قابل بازبینی و اصلاح باشد. | Usability Test |
| SRS-NFR-UX-004 | progress Daily Ring باید برای user حداکثر 100 درصد نمایش داده شود، حتی اگر final performance بالاتر از baseline باشد. | UI Test |

## 5.5 maintainability و change isolation

| ID | Requirement | Verification |
|---|---|---|
| SRS-NFR-MAINT-001 | failure یا تغییر یک integration خارجی نباید مدل ownership داخلی را به Source وابسته کند. | Architecture Review + Test |
| SRS-NFR-MAINT-002 | تغییر View نباید domain data را تغییر دهد. | Regression Test |

# 6. قواعد کسب‌وکار consolidated

این بخش requirement جدید ایجاد نمی‌کند و فقط قواعدی را که در بخش 3 normative شده‌اند یکجا خلاصه می‌کند:

1. Routine status ندارد و outcome روزانه در RoutineCompletion است.
2. `occurrence_date` هویت business روز RoutineCompletion است و `completed_at` business field لازم نیست.
3. Reset row جاری RoutineCompletion را حذف می‌کند، ولی AuditLog history را نگه می‌دارد.
4. completion روز unscheduled معتبر است، اما missed fixed-day occurrence را جبران نمی‌کند.
5. Task با grace صفر در deadline مستقیما `Skipped` می‌شود.
6. ownership از Source جداست.
7. hierarchy باید مستقیم queryable باشد.
8. Folder، List و Column terminology canonical است.
9. وقتی حداقل سه Goal eligible وجود دارد، تعداد Daily Ring دقیقا سه است.
10. progress از 100 بالاتر نمی‌رود، ولی final score می‌تواند بالاتر باشد.
11. bonus performance تا finalization روز مخفی می‌ماند.
12. یک Item فقط Ring همان credited day را جلو می‌برد که در snapshot آن عضو بوده است.
13. Dotick Day می‌تواند از Calendar Day متفاوت باشد.
14. AI-created Item تا قبل از Confirm فقط Draft است.
15. historical correction باید selective recomputation داشته باشد.

# 7. موارد OPEN و non-normative

موارد این بخش بخشی از behavior قطعی Personal V1 نیستند. implementation مربوط به هر مورد باید تا Decision Gate مالک آن از تصمیم ضمنی پرهیز کند.

| Open ID | موضوع | وضعیت فعلی | Decision Gate / محل formalization |
|---|---|---|---|
| OPEN-001 | Event structural multi-parent در برابر single parent + multi-reference | OPEN | Increment 2 |
| OPEN-002 | schema دقیق RichDescription/ContentBlock | OPEN | Increment 2 |
| OPEN-003 | schema backend برای structural child در برابر normal reference | OPEN | Increment 2 |
| OPEN-004 | dependency-cycle policy دقیق Task | نیازمند formal validation | Increment 2 design/test |
| OPEN-005 | ordering validation دقیق میان `due_at`, `end_at` و `deadline_at` | نیازمند formal validation | Increment 2 design/test |
| OPEN-006 | تعریف `qualifying_completions` برای incremental Routine | OPEN | Increment 3/4 |
| OPEN-007 | reset target incremental Routine پس از inactivity طولانی | OPEN | Increment 3/10 gate |
| OPEN-008 | semantics کامل streak برای frequency-based Routine | OPEN | Increment 4 |
| OPEN-009 | schema نهایی recurrence config و occurrence identity | OPEN | Increment 4 |
| OPEN-010 | sync metadata دقیق، clock strategy و conflict granularity | OPEN | Increment 6 |
| OPEN-011 | مالکیت Folder/List/Column در context Group | OPEN | Increment 7 |
| OPEN-012 | مدت warm-up اولیه AI Goal discovery | OPEN | Increment 9 |
| OPEN-013 | thresholdهای similarity برای reactivation/merge Goal | OPEN | Increment 9 |
| OPEN-014 | الگوریتم دقیق Goal selection و learning weights | OPEN | Increment 10 |
| OPEN-015 | فرمول دقیق Ring progress/final score/early bonus/late recovery | OPEN | Increment 10 |
| OPEN-016 | representation دقیق difficulty/effort | OPEN | Increment 10 |
| OPEN-017 | thresholdها و windowهای دقیق adaptive Norm | OPEN | Increment 10 |
| OPEN-018 | global daily streak و behavior motivational/scolding مرتبط | OPEN | Increment 10 |
| OPEN-019 | representation دقیق RoutineOccurrence در DailyRingItem | OPEN | Increment 10 |
| OPEN-020 | frequency/rate-limit دقیق Goal-level reminder | OPEN | Increment 10 |
| OPEN-021 | storage inheritance/composition/denormalization strategy | RESOLVED برای baseline Personal V1 با DR-054 و ADR-0002 | Increment 0 Data Design؛ بازنگری فقط با evidence و ADR جدید |
| OPEN-022 | endpointهای دقیق API و versioning contract | OPEN در سطح global | به تفکیک Increment |
| OPEN-023 | confirmation policy برای trusted automation | OPEN / Future | Future Integration |
| OPEN-024 | Enterprise SSO protocol | OPEN / Future | Enterprise |
| OPEN-025 | privacy/compliance requirementهای Enterprise | OPEN / Future | Enterprise |

## 7.1 مواردی که از baseline normative حذف شده‌اند

موارد زیر در referenceهای قدیمی یا جزئیات design دیده می‌شوند، اما در این Formal SRS به عنوان requirement قطعی تثبیت نشده‌اند:

- global daily streak با قاعده legacy `حداقل یک Ring complete شود` تا زمان تصمیم OPEN-018.
- فرمول یا coefficient ثابت برای scoring و priority weighting.
- schema JSON پیشنهادی recurrence به عنوان contract نهایی.
- Class Table Inheritance یا هر mapping فیزیکی مشخص برای Item/Schedulable/TrackingState.
- table یا cache پیشنهادی مشخص برای child/reference.
- endpoint، index یا ORM mapping مشخص قبل از Design Stage مالک.
- Custom Role در Personal V1.

## 7.2 نکته traceability درباره rule تولید Task تکرارشونده

Roadmap در Increment 4 یک rule با این مضمون دارد که تولید Task تکرارشونده time-based باشد و به completion Task قبلی وابسته نباشد. این behavior در Decision Register و System Definition فعلی به صورت صریح ثبت نشده است. چون Formal SRS باید از منابع canonical استخراج شود، این rule در baseline normative این نسخه وارد نشده است. پیش از implementation recurrence باید یا در منبع canonical تایید شود یا از Roadmap اصلاح شود.

# 8. Future و خارج از scope Personal V1

موارد این بخش vision محصول را حفظ می‌کنند، اما acceptance Personal V1 به آن‌ها وابسته نیست:

- Enterprise multi-tenancy و Organization hierarchy.
- Custom Roles و authorization سازمانی پیشرفته.
- Enterprise SSO پس از انتخاب protocol مناسب.
- management reporting و Enterprise administration.
- privacy/compliance specification سازمانی، از جمله تحلیل GDPR در صورت applicable بودن.
- Google Calendar import/sync.
- Email و external-source automation.
- trusted auto-create یا auto-action بدون review تا زمان تصمیم confirmation policy.
- personalization پیشرفته AI بر اساس correction history. Personal V1 فقط داده لازم برای این قابلیت آینده را نگه می‌دارد.
- native Android با Kotlin یا native iOS با Swift، اگر پس از ارزیابی تجربه اولیه توجیه شود.
- SLA، pricing، licensing و support contract تجاری.

# 9. موارد مهندسی که عمدا خارج از بدنه normative SRS هستند

Roadmap برای Increment 0 و Incrementهای بعدی artifactها و processهای مهندسی دیگری تعریف می‌کند. این موارد مهم‌اند، اما product requirement این SRS نیستند:

- TDD workflow و regression discipline.
- Git/SCM و code review process.
- CI pipeline، formatter و linter.
- Docker/dev reproducibility setup.
- migration tooling.
- `project-docs/03-design/architecture.md`, `project-docs/03-design/data-model.md`, `project-docs/03-design/api-contracts.md` یا OpenAPI، `project-docs/03-design/ui-ux/`, `project-docs/03-design/security-design.md`, `project-docs/05-quality/test-strategy.md`, `project-docs/06-operations/release-deployment.md` و specهای تخصصی.
- ADRها، migrationها، release noteها و Increment reviewها.

این artifactها باید requirementهای این SRS را بدون کپی مکانیکی Domain Model به schema فیزیکی پیاده‌پذیر و testable کنند.

# پیوست A. واژه‌نامه

| اصطلاح | تعریف |
|---|---|
| Item | ریشه مفهومی Task، Event و Routine. |
| Schedulable | capability مفهومی مشترک Task و Event برای زمان‌بندی، priority و Description. |
| Task | Item زمان‌پذیر با due/deadline/grace، dependency و lifecycle مخصوص Task. |
| Event | Item زمان‌پذیر با start/end، location و lifecycle مخصوص Event. |
| Routine | تعریف تکرارشونده روزمحور که outcome هر روز آن در RoutineCompletion ثبت می‌شود. |
| RoutineCompletion | state جاری outcome یک Routine برای occurrence_date مشخص. |
| Goal | objective معنایی مستقل از Item hierarchy که مبنای Daily Ring است. |
| TrackingState | capability مشترک Routine و Goal برای streak و completion aggregateهای مربوط. |
| DailyRing | snapshot روزانه یک Goal برای یک Dotick Day. |
| DailyRingItem | snapshot عضویت Itemهای موثر بر یک DailyRing در credited day. |
| Dotick Day | روز منطقی سیستم که boundary آن می‌تواند با midnight متفاوت باشد. |
| Credited / Effective Date | روزی که completion برای scoring و history به آن نسبت داده می‌شود. |
| Source | provenance یک Task/Event در مدل فعلی، مستقل از owner و creator. |
| Structural Child | relation hierarchy واقعی بین Itemها. |
| Reference | نمایش یا لینک به Item بدون الزام به relation hierarchy. |
| Field-level LWW | baseline conflict policy که آخرین write یک field را مستقل از fieldهای دیگر برنده می‌کند. |
| Formal SRS | baseline requirementهای قابل تست. design proposal و OPEN decision به تنهایی requirement قطعی نیستند. |

# پیوست B. معیار کیفیت requirementهای این baseline

هر requirement normative این سند باید این ویژگی‌ها را حفظ کند:

- یک behavior یا constraint مشخص را بیان کند.
- بدون نیاز به فرض design باز قابل فهم باشد.
- تا حد ممکن با Test، Inspection یا Analysis قابل verification باشد.
- با Decision Register، System Definition و Domain Model تضاد نداشته باشد.
- Feature Priority یا ترتیب implementation را در خود requirement وارد نکند.
- تصمیم `OPEN` را به صورت ضمنی نهایی نکند.

# پیوست C. وضعیت baseline

این سند با ایجاد version 2.0 وارد حالت Formal SRS Baseline می‌شود. تغییر behavior بعدی باید طبق lifecycle پروژه انجام شود: ابتدا تصمیم یا رفتار canonical در صورت نیاز اصلاح شود، سپس SRS و traceability به‌روزرسانی شوند. Design artifactها می‌توانند بدون تغییر SRS refine شوند، به شرطی که behavior و constraintهای normative این سند تغییر نکنند.
