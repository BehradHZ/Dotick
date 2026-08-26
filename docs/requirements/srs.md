# Dotick Software Requirements Specification

**Document type:** Formal Software Requirements Specification

**Version:** 2.8

**Baseline date:** 2026-08-26

**Status:** Formal SRS Baseline

**Scope:** Personal V1

> این سند baseline رسمی نیازمندی‌های Dotick برای Personal V1 است. این نسخه جایگزین نقش `reconciled derived reference` نسخه 1.7 می‌شود. جزئیات طراحی فیزیکی و جزئیات implementation/tuning که عمداً به artifactهای تخصصی واگذار شده‌اند requirement رفتاری جدید ایجاد نمی‌کنند؛ قابلیت‌های Enterprise/Future نیز خارج از acceptance این baseline هستند.

## تاریخچه بازنگری

| نسخه | تاریخ | وضعیت | توضیح |
|---|---|---|---|
| 1.0 تا 1.7 | تاریخی | Non-canonical / Derived | نسخه‌های پیش از Formal SRS. این نسخه‌ها برای تاریخچه مفیدند، اما رفتار جاری را تعیین نمی‌کنند. |
| 2.0 | 2026-08-17 | Formal Baseline | بازنویسی از منابع canonical مطابق Increment 0 در Roadmap و جداسازی requirementهای قطعی از design proposal و تصمیم‌های `OPEN`. |
| 2.1 | 2026-08-25 | Reconciled Baseline | همگام‌سازی external-system boundaries، Google-only external authentication، email/phone discovery، AI execution/BYOK fallback، global AI control و notification delivery با Decision Register/System Definition. |
| 2.2 | 2026-08-26 | Quality & Client Baseline | تکمیل Quality Expectations، privacy-safe contact discovery، at-rest protection/admin audit، backup/export/account deletion، PWA Current Scope، حذف self-hosting requirement و English UI/Persian content support. |
| 2.3 | 2026-08-26 | Assumptions & Dependencies Baseline | تکمیل Assumptions/Dependencies، verification اجباری email/phone، notification-permission boundary، device-local Attachment cache، Voice-only AI creation، BYOK responsibility و clock-skew resilience. |
| 2.4 | 2026-08-26 | Future Scope Baseline | تفکیک Planned Future از صرفاً Out-of-Scope، Profile Picture بدون Public Profile، commercial-model boundary، controlled integrations/public-API boundary و accessibility به‌عنوان Future quality direction. |
| 2.5 | 2026-08-26 | Current-Scope Unspecified Details Baseline | حذف Product/Domain OPENهای stale، محدودکردن فهرست جزئیات عمداً نامشخص به Current Scope و همگام‌سازی handoff به Design/Tuning با DR-144 و Decision Register جاری. |
| 2.6 | 2026-08-26 | Terminology Baseline | تکمیل Glossary canonical، تفکیک اصطلاحات Dotick-specific/domain/legacy و اصلاح ارجاع‌های stale به شماره‌بخش‌های جاری System Definition. |
| 2.7 | 2026-08-26 | Consistency Reconciliation Baseline | همگام‌سازی Historical Statistics با immutable finalized windows، تثبیت Event single-parent، formalization History/Sync/Time guardrailها، external-AI acknowledgement، PWA/native alarm boundary و اصلاح traceability با Decision Register ادغام‌شده. |
| 2.8 | 2026-08-26 | SRS Coverage & Reference Integrity Baseline | formalization رفتارهای قطعی Task/Hierarchy که در SRS جا افتاده بودند، تثبیت Global Streak requirement، حذف/اصلاح referenceهای stale یا نامرتبط و همگام‌سازی traceability با System Definition و Decision Register جاری. |

# 1. مقدمه

## 1.1 هدف سند

این سند نیازمندی‌های عملکردی، غیرعملکردی و محدودیت‌های محصول Dotick را برای Personal V1 تعریف می‌کند. متن requirementها باید برای تحلیل، طراحی، تست، پیاده‌سازی و traceability قابل استفاده باشد.

این SRS پاسخ می‌دهد که سیستم چه رفتاری باید داشته باشد. این سند schema نهایی PostgreSQL، ORM mapping، endpointهای دقیق API، طراحی UI، الگوریتم نهایی scoring یا سایر جزئیات implementation را تعیین نمی‌کند، مگر آنکه یک محدودیت فنی به صورت canonical تثبیت شده باشد.

## 1.2 مرجع و ترتیب authority

در صورت تعارض درباره‌ی رفتار یا Scope، ترتیب authority پروژه چنین است:

```text
System Definition
        ↓
Decision Register
        ↓
Formal SRS
        ↓
Domain Model / Design
        ↓
Roadmap / reconciled non-canonical references
```

این SRS باید requirementهای قابل تست را از رفتار canonical بالاتر استخراج کند و حق ندارد برای رفع ابهام، behavior جدیدی را مستقل از System Definition/Decision Register ایجاد کند.

منابع این baseline:

- `project-docs/02-requirements/system-definition.md`
- `project-docs/decision-register.md`
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

مبنای canonical: System Definition بخش 6.1، DR-001 و DR-096، Domain Model بخش 15.

| ID | Requirement | Verification |
|---|---|---|
| SRS-ORG-001 | سیستم باید ساختار سازمانی `Folder > List > Column` را پشتیبانی کند. | Test |
| SRS-ORG-002 | سیستم باید یک محل پیش‌فرض با مفهوم `Inbox` برای Task/Eventهایی داشته باشد که کاربر هنگام ایجاد، محل مشخصی برای آن‌ها انتخاب نکرده است. Routine از Folder/List/Column placement استفاده نمی‌کند. | Test |
| SRS-ORG-003 | هر List باید یک Column پیش‌فرض برای Task/Eventهای بدون Column صریح داشته باشد. | Test |
| SRS-ORG-004 | اگر Column پیش‌فرض تنها Column یک List باشد، سیستم نباید کاربر را مجبور به مشاهده نام فنی legacy آن، یعنی `not_sectioned`، کند. | Test + Inspection |
| SRS-ORG-005 | سیستم نباید `Tab` یا `Section` را به عنوان entity مستقل از Column مدل کند. | Inspection |
| SRS-ORG-006 | سیستم باید دسترسی به Folderها، Listها و ورودی روزانه یا Today را در navigation اصلی فراهم کند. | Test + Inspection |

## 3.2 Item، identity، ownership و source

مبنای canonical: System Definition بخش‌های 6 و 7.1، DR-012، DR-013 و DR-111، Domain Model بخش‌های 2 و 6.

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

مبنای canonical: System Definition بخش 6.2، DR-010، DR-011، DR-080، DR-081 و DR-097، Domain Model بخش 4.

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
| SRS-TASK-017 | ایجاد یا ویرایش `blocked_by` نباید cycle در dependency graph ایجاد کند و action cycle-ساز باید با diagnostic قابل فهم رد شود. | Test |
| SRS-TASK-018 | اگر `end_at` و `deadline_at` وجود دارند، ترتیب معتبر باید `due_at <= end_at <= deadline_at` باشد؛ بدون `end_at` نیز باید `due_at <= deadline_at` برقرار باشد. | Test |
| SRS-TASK-019 | فقط `Done` شدن blocker باید dependency را satisfy کند؛ `Won't_Do`، `Skipped` یا stateهای دیگر نباید blocker را به‌صورت ضمنی resolve کنند. | Test |
| SRS-TASK-020 | Task باید بتواند بدون date، بدون time و بدون all-day date ایجاد، ذخیره، بازیابی و ویرایش شود و تا زمان تعیین schedule به‌صورت unscheduled باقی بماند. | Test |
| SRS-TASK-021 | اگر Task دارای `deadline_at` باشد و User مقدار `grace_period_days` را صریح تعیین نکند، مقدار پیش‌فرض grace باید `0` باشد. | Test |
| SRS-TASK-022 | صرفاً بازکردن، مشاهده یا ویرایش یک Task قدیمی نباید به‌تنهایی status آن را بر اساس زمان جاری دوباره محاسبه یا تغییر دهد؛ transition زمانی فقط از رفتار صریح lifecycle و state changeهای تعریف‌شده ناشی می‌شود. | Regression Test |
| SRS-TASK-023 | User باید بتواند Taskای را که سیستم قبلاً به `Skipped` منتقل کرده است، با action صریح به یک state مجاز دیگر منتقل کند؛ این قابلیت نباید `Skipped` را به یک state قابل انتخاب مستقیم عادی تبدیل کند. | Test |
| SRS-TASK-024 | حذف یک blocker باید dependency relation مربوط به همان blocker را حذف کند و Task وابسته دیگر نباید آن blocker حذف‌شده را require کند. | Test |
| SRS-TASK-025 | dependency و structural hierarchy باید مستقل باشند؛ ایجاد Parent/Subtask relation نباید به‌صورت ضمنی `blocked_by` ایجاد کند و ایجاد dependency نیز نباید structural parent ایجاد کند. | Test |
| SRS-TASK-026 | Task دارای blocker فعال نباید بتواند `Done` شود تا زمانی که همه blockerهای فعال آن `Done` شده باشند. | Test |
| SRS-TASK-027 | به‌صورت پیش‌فرض، وقتی همه structural childهای یک Task `Done` شوند، Parent باید `Done` شود. | Test |
| SRS-TASK-028 | User باید بتواند auto-completion رفتار `all structural children Done -> Parent Done` را از Preferences غیرفعال کند. | Test + Inspection |
| SRS-TASK-029 | وقتی User یک Parent Task را مستقیماً `Done` می‌کند، همه structural descendantهای آن Parent باید `Done` شوند. | Test |
| SRS-TASK-030 | stateهای time-driven یک Parent Task نباید به structural child/descendantهای آن cascade شوند. | Test |
| SRS-TASK-031 | به‌صورت پیش‌فرض، `Won't_Do` کردن Parent Task نباید state structural descendantهای آن را تغییر دهد. | Test |
| SRS-TASK-032 | User باید بتواند Preference اختیاری‌ای فعال کند که در آن `Won't_Do` کردن Parent Task به structural descendantهای آن نیز cascade شود. | Test + Inspection |

## 3.4 Event

مبنای canonical: System Definition بخش 6.3، DR-015، DR-098 و DR-115، Domain Model بخش 5.

| ID | Requirement | Verification |
|---|---|---|
| SRS-EVENT-001 | سیستم باید ایجاد، بازیابی، ویرایش و soft-delete Event را پشتیبانی کند. | Test |
| SRS-EVENT-002 | Event باید بتواند بدون start time و بدون all-day date ایجاد، ذخیره، بازیابی و ویرایش شود و تا زمان تعیین schedule معتبر به‌صورت unscheduled باقی بماند. | Test |
| SRS-EVENT-003 | Event باید location اختیاری داشته باشد. | Test |
| SRS-EVENT-004 | Location باید بتواند حداقل coordinates، human-readable address، place identifier یا virtual meeting link را نمایندگی کند. | Test |
| SRS-EVENT-005 | سیستم باید statusهای `Not_Arrived`, `Ongoing` و `Finished` را برای Event پشتیبانی کند. | Test |
| SRS-EVENT-006 | Event باید بتواند sub-event ساختاری داشته باشد و هر sub-event اطلاعات مستقل خود را نگه دارد. | Test |
| SRS-EVENT-007 | یک Event باید بتواند در چند RichDescription به صورت reference نمایش داده شود. | Test |
| SRS-EVENT-008 | Event باید priorityهای `Urgent_Important`, `Important`, `Urgent` و `None` را پشتیبانی کند. | Test |
| SRS-EVENT-009 | Event زمان‌بندی‌شده باید status را به‌صورت time-driven تعیین کند و User نباید `Not_Arrived`، `Ongoing` یا `Finished` را به‌عنوان state دستی عادی انتخاب کند. | Test |
| SRS-EVENT-010 | overlap زمانی Eventها یا سایر Itemهای زمانی باید مجاز باشد؛ سیستم می‌تواند هشدار دهد اما نباید صرف overlap creation/move را رد کند. | Test |
| SRS-EVENT-011 | اگر Event زمان‌بندی‌شده `end_at` صریح نداشته باشد، lifecycle باید پایان Calendar Day مربوط به start date را به‌عنوان پایان آن occurrence در نظر بگیرد. | Test |
| SRS-EVENT-012 | Event بدون schedule نباید status زمانی `Not_Arrived`، `Ongoing` یا `Finished` بگیرد؛ این statusها فقط پس از وجود start schedule معتبر محاسبه می‌شوند. | Test |
| SRS-EVENT-013 | افزودن یا تکمیل schedule یک Event موجود باید همان identity پایدار Event را حفظ کند و نباید به ایجاد Event جایگزین نیاز داشته باشد. | Test |

## 3.5 hierarchy ساختاری و reference

مبنای canonical: System Definition بخش‌های 6.4، 7.3 و 7.4، DR-014، DR-015، DR-017، DR-099، DR-113 و DR-114، Domain Model بخش 3.

| ID | Requirement | Verification |
|---|---|---|
| SRS-HIER-001 | hierarchy ساختاری Task و Event باید از طریق relation مستقیم قابل query باشد و بازیابی آن نباید به parse کامل RichDescription وابسته باشد. | Test + Analysis |
| SRS-HIER-002 | relation ساختاری باید برای query و index شدن قابل طراحی باشد. | Inspection |
| SRS-HIER-003 | هر Task و هر Event باید حداکثر یک structural parent داشته باشد. | Test |
| SRS-HIER-004 | سیستم باید cycle در parent relation ساختاری را رد کند. | Test |
| SRS-HIER-005 | backend باید structural child را از normal reference تشخیص دهد. | Test |
| SRS-HIER-006 | frontend نباید صرفا به دلیل تفاوت داخلی child و reference مجبور به ارائه دو workflow پیچیده و مستقل شود. | Inspection + Test |
| SRS-HIER-007 | relationهای structural `Task→Task`، `Task→Event`، `Event→Task` و `Event→Event` باید از نظر domain قابل پشتیبانی باشند. | Test |
| SRS-HIER-008 | structural child در زمان ایجاد باید placement سازگار با Parent داشته باشد و move کردن Parent باید descendantهای structural را طبق rule canonical همراه کند. | Test |
| SRS-HIER-009 | move مستقل child به placement ناسازگار با Parent باید relation structural را بشکند و identity child را حفظ کند. | Test |
| SRS-HIER-010 | حذف Parent باید descendantهای structural را وارد همان delete flow کند؛ حذف صرف relation parent/child نباید هیچ‌کدام از Itemها را حذف کند. | Test |
| SRS-HIER-011 | Reference نباید structural parent ایجاد کند و یک Item باید بتواند در چند context مجاز reference شود. | Test |
| SRS-HIER-012 | اگر actor permission معتبر برای حذف structural Parent داشته باشد، همان permission باید برای اجرای intrinsic delete cascade روی structural descendantها کافی باشد و نباید برای هر descendant permission حذف جداگانه require شود. | Security Test |
| SRS-HIER-013 | اگر actor permission معتبر برای `Done` کردن Parent Task داشته باشد، همان permission باید برای intrinsic `Done` cascade روی descendantها کافی باشد؛ در صورت فعال‌بودن Preference مربوط، همین rule برای `Won't_Do` cascade نیز برقرار است. | Security Test |
| SRS-HIER-014 | permission ناشی از intrinsic delete/completion cascade نباید general یا persistent permission جدیدی روی descendantها برای actor ایجاد کند. | Security Test |
| SRS-HIER-015 | move کردن structural Parent فقط زمانی باید کل descendantهای متاثر را جابه‌جا کند که actor برای هر Resourceای که placement آن تغییر می‌کند move authority لازم را داشته باشد؛ permission روی Parent به‌تنهایی برای move cascade کافی نیست. | Security Test + Test |
| SRS-HIER-016 | پیش از اجرای destructive cascade روی چند Resource، سیستم باید scope اثر را به شکل قابل فهم به User نشان دهد و confirmation صریح او را دریافت کند. | Test + Inspection |
| SRS-HIER-017 | هر consequence چند-Resourceای که برای حفظ consistency باید یکجا اعمال شود، باید کاملاً موفق شود یا اصلاً اعمال نشود؛ failure در authorization، validation یا domain constraint نباید partial state باقی بگذارد. | Atomicity Test |

## 3.6 RichDescription و ContentBlock

مبنای canonical: System Definition بخش 6.5، DR-018 و DR-019، Domain Model بخش 8.

| ID | Requirement | Verification |
|---|---|---|
| SRS-DESC-001 | Description در Task و Event باید block-based باشد. | Test + Inspection |
| SRS-DESC-002 | RichDescription باید TextBlock را با قابلیت Bold، Italic، Underline، Strikethrough، Heading، Highlight، Bullets، Numbers، Indent، Separator، Code، Quote و تشخیص link/phone/id پشتیبانی کند. | Test |
| SRS-DESC-003 | RichDescription باید Attachment، Location و Item reference برای Task/Event را پشتیبانی کند. | Test |
| SRS-DESC-004 | هر ContentBlock باید identity پایدار داشته باشد تا comment، reorder، edit و sync بتوانند همان block را شناسایی کنند. | Test |
| SRS-DESC-005 | تغییر ترتیب blockها نباید identity آن‌ها را از بین ببرد. | Test |

## 3.7 Comment

مبنای canonical: System Definition بخش 6.5 و DR-100، Domain Model بخش 9.

| ID | Requirement | Verification |
|---|---|---|
| SRS-COMMENT-001 | هر Task و Event باید comment thread مربوط به کل Item داشته باشد. | Test |
| SRS-COMMENT-002 | کاربر مجاز باید بتواند comment را به یک ContentBlock مشخص متصل کند. | Test |
| SRS-COMMENT-003 | comment متصل به block باید هم در context همان block و هم در thread کلی Item قابل مشاهده باشد. | Test |
| SRS-COMMENT-004 | سیستم باید author و زمان ایجاد و ویرایش comment را قابل نگهداری کند. | Test |
| SRS-COMMENT-005 | Routine shared باید برای collaborator مجاز comment روی خود Routine و، در context پشتیبانی‌شده، روی اجرای یک `occurrence_date` مشخص را پشتیبانی کند. | Test |
| SRS-COMMENT-006 | note شخصی روزانه Owner روی Routine باید از `RoutineCompletion.note` استفاده کند و Comment collaboration جایگزین آن نباشد. | Test + Inspection |

## 3.8 Routine

مبنای canonical: System Definition بخش 6.6، DR-002 تا DR-008، DR-083 و DR-101، Domain Model بخش‌های 10 تا 12.

| ID | Requirement | Verification |
|---|---|---|
| SRS-ROUTINE-001 | هر Routine باید یک definition واحد باشد و سیستم نباید برای هر روز یک Routine جدید بسازد. | Test |
| SRS-ROUTINE-002 | Routine نباید Schedulable باشد و نباید status مستقل داشته باشد. | Test + Inspection |
| SRS-ROUTINE-003 | Routine باید `start_date` اختیاری داشته باشد و در صورت نبود آن، اعتبار Routine از تاریخ ایجاد شروع شود. | Test |
| SRS-ROUTINE-004 | Routine باید `end_date` اختیاری داشته باشد و در صورت نبود آن، تعریف Routine از نظر validity window بدون پایان باشد. | Test |
| SRS-ROUTINE-005 | `end_date` باید تولید occurrenceهای scheduled آینده را پس از آن تاریخ متوقف کند و به تنهایی نباید archive state جدا ایجاد کند. | Test |
| SRS-ROUTINE-006 | outcome یک Routine در یک روز باید در `RoutineCompletion` ثبت شود، نه در status خود Routine. | Test |
| SRS-ROUTINE-007 | `RoutineCompletion.status` باید `In_Progress`, `Done` یا `Won't_Do` باشد. | Test |
| SRS-ROUTINE-008 | `occurrence_date` باید تاریخ business مربوط به یک RoutineCompletion را مشخص کند. | Test |
| SRS-ROUTINE-009 | برای هر زوج `(routine_id, occurrence_date)` فقط یک RoutineCompletion جاری مجاز است. | Test |
| SRS-ROUTINE-010 | نبود RoutineCompletion برای یک روز باید به معنی نبود progress/outcome ثبت‌شده باشد و نباید با `In_Progress`, `Done` یا `Won't_Do` یکسان تلقی شود. | Test |
| SRS-ROUTINE-011 | در targetهای Partial، تغییر amount همان روز باید همان RoutineCompletion جاری را update کند؛ مقدار کمتر از target باید `In_Progress` باشد و رسیدن amount به target یا عبور از آن باید status را به‌صورت خودکار `Done` کند. | Test |
| SRS-ROUTINE-029 | `amount` RoutineCompletion نباید روی target cap شود و باید مقدار واقعی انجام‌شده، از جمله over-target، را قابل ثبت نگه دارد. | Test |
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

مبنای canonical: System Definition بخش 6.6، DR-008 و DR-095، Domain Model بخش 14.

| ID | Requirement | Verification |
|---|---|---|
| SRS-RSTREAK-001 | در Routine با occurrenceهای fixed-day، completion معتبر scheduled باید در sequence streak قابل شمارش باشد. | Test |
| SRS-RSTREAK-002 | missed scheduled occurrence باید sequence streak fixed-day را قطع کند. | Test |
| SRS-RSTREAK-003 | completion در روز unscheduled باید completion معتبر باشد، اما نباید missed occurrence قبلی را ترمیم یا جایگزین کند. | Test |
| SRS-RSTREAK-004 | completion معتبر پس از break باید بتواند sequence جدید streak را شروع یا ادامه دهد. | Test |
| SRS-RSTREAK-005 | Routine از نوع frequency-based باید بتواند quota به شکل `N times per period` داشته باشد و completionهای روزهای مختلف همان period را تا رسیدن به quota بپذیرد. | Test |
| SRS-RSTREAK-006 | در Routine از نوع frequency-based، تکمیل quota نباید به fixed weekdayهای از پیش تعیین‌شده وابسته باشد، مگر خود تعریف Routine چنین محدودیتی داشته باشد. | Test |

## 3.10 Recurrence

مبنای canonical: System Definition بخش 6.7، DR-009، DR-082 و DR-102، Domain Model بخش 13.

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
| SRS-REC-013 | edit یک occurrence calendar-anchored نباید به‌صورت ضمنی pattern سایر occurrenceها را تغییر دهد. | Test |
| SRS-REC-014 | در recurrence فاصله‌ای/زنجیره‌ای، هنگام move یک occurrence باید User بتواند میان تغییر فقط همان occurrence و حفظ interval با shift کردن occurrenceهای آینده انتخاب کند. | Test |
| SRS-REC-015 | حذف occurrence تکرارشونده باید حداقل انتخاب «فقط همین occurrence» و «پایان recurrence برای occurrenceهای آینده» را پشتیبانی کند. | Test |
| SRS-REC-016 | تغییر recurrence rule نباید occurrenceهای تاریخی گذشته را بازنویسی کند. | Test |

## 3.11 Reminder

مبنای canonical: System Definition بخش 6.8، DR-066 و DR-103، Domain Model بخش 27.

| ID | Requirement | Verification |
|---|---|---|
| SRS-REM-001 | Task، Event و Routine باید بتوانند چند reminder داشته باشند. | Test |
| SRS-REM-002 | هر reminder باید بتواند trigger-before را بیان کند. | Test |
| SRS-REM-003 | domain باید intent مربوط به persistent یا alarm-like reminder را مستقل از محدودیت platform نمایندگی کند. | Test + Inspection |
| SRS-REM-004 | در جریان AI-assisted creation، reminderهای پیشنهادی باید قبل از ایجاد Item قابل مشاهده و ویرایش باشند. | Test |
| SRS-REM-005 | persistent/alarm-like باید به‌عنوان domain intent قابل ثبت بماند، حتی اگر Current-Scope PWA روی یک browser/OS نتواند full native alarm behavior را کامل اجرا کند. | Test + Inspection |
| SRS-REM-006 | نبود native full-screen/ringing integration در PWA نباید acceptance کل Reminder را fail کند؛ client باید capability واقعی platform را به‌صورت best-effort/degraded ارائه کند و تکمیل native alarm behavior می‌تواند به native-client Future Scope واگذار شود. | Platform Test + Inspection |

## 3.12 Authentication و session

مبنای canonical: System Definition بخش‌های 3.1، 6.13 و 9.1، DR-048، DR-061، DR-128 و DR-140.

| ID | Requirement | Verification |
|---|---|---|
| SRS-AUTH-001 | سیستم باید authentication با email و password را پشتیبانی کند. | Test |
| SRS-AUTH-002 | سیستم نباید password را به صورت plaintext ذخیره کند و باید از password hashing امن استفاده کند. | Test + Inspection |
| SRS-AUTH-003 | سیستم باید Google OAuth را برای authentication پشتیبانی کند. | Test |
| SRS-AUTH-004 | سیستم باید session کاربر را با JWT پشتیبانی کند. | Test |
| SRS-AUTH-005 | اگر Google OAuth در دسترس نباشد، email/password باید به‌عنوان authentication method مستقل پلتفرم قابل استفاده باقی بماند؛ این requirement تضمین نمی‌کند Accountی که فقط Google دارد بدون configure کردن fallback بتواند login جدید انجام دهد. | Test |
| SRS-AUTH-006 | سیستم باید Passkey را برای authentication پشتیبانی کند. | Test |
| SRS-AUTH-007 | در Current Scope، Google باید تنها external authentication provider پشتیبانی‌شده باشد. | Test + Inspection |
| SRS-AUTH-008 | Email/password authentication باید email verification داشته باشد و User باید بتواند password reset را از طریق email انجام دهد. | Test |
| SRS-AUTH-009 | استفاده از Google نباید به configure کردن password یا Passkey مستقل به‌عنوان prerequisite اجباری وابسته باشد. | Test |
| SRS-AUTH-010 | سیستم باید امکان افزودن authentication fallback مستقل برای Account استفاده‌کننده از Google را فراهم کند و UI باید افزودن آن را به User توصیه کند. | Test + Inspection |
| SRS-AUTH-011 | Current Scope نباید User را به enrollment یا استفاده از TOTP/SMS-based second factor مستقل علاوه بر authentication baseline فعلی ملزم کند. | Inspection + Test |
| SRS-AUTH-012 | افزودن email یا phone به Account باید نیازمند verification موفق از طریق code ارسال‌شده به همان contact باشد. | Test + Security Test |
| SRS-AUTH-013 | email/phone تأییدنشده نباید به‌عنوان contact فعال Account ثبت شود یا برای discovery و flowهای وابسته به contact قابل استفاده باشد. | Test + Security Test |
| SRS-AUTH-014 | User باید بتواند یک Profile Picture اختیاری برای Account خود داشته باشد. | Test |
| SRS-AUTH-015 | Profile Picture باید بخشی از identity presentation Account باشد و نباید به‌تنهایی Public Profile، follower relation یا social-network surface ایجاد کند. | Test + Inspection |

## 3.13 Viewها و presentation

مبنای canonical: System Definition بخش‌های 1.4، 5.4.7، 6.1، 6.6 و 10.6، DR-066 و DR-133؛ Roadmap Increment 5 فقط برای scope presentation مربوط به View/Themeهای Current Scope.

| ID | Requirement | Verification |
|---|---|---|
| SRS-VIEW-001 | سیستم باید داده یکسان را بدون تغییر domain data در presentationهای مختلف نمایش دهد. | Test |
| SRS-VIEW-002 | صفحه List باید حداقل Viewهای `List`, `Kanban` و `Timeline` را پشتیبانی کند. | Test + Inspection |
| SRS-VIEW-003 | سیستم باید View یا صفحه مستقل `Calendar` را ارائه کند. | Test + Inspection |
| SRS-VIEW-004 | سیستم باید صفحه مستقل Routine را ارائه کند. | Test + Inspection |
| SRS-VIEW-005 | سیستم باید View یا صفحه `Eisenhower / Priority Matrix` را بر پایه priority ارائه کند. | Test + Inspection |
| SRS-VIEW-006 | رابط کاربری Personal V1 باید responsive و mobile-first باشد. | Test + Inspection |
| SRS-VIEW-007 | سیستم باید امکان ارائه themeهای `Minimal customizable`, `Liquid Glass`, `Material 3 Expressive inspired` و `Dot-matrix` را در presentation layer داشته باشد. | Inspection |
| SRS-VIEW-008 | client رسمی User-facing در Current Scope باید یک responsive installable PWA باشد که در browserهای پشتیبانی‌شده روی desktop و mobile قابل استفاده باشد. | Test + Inspection |
| SRS-VIEW-009 | PWA باید در platform/browserهای پشتیبانی‌کننده بتواند Notification/Pushهای Current Scope را دریافت و نمایش دهد. | Integration Test + Inspection |
| SRS-VIEW-010 | زبان interface/chrome محصول در Current Scope باید English باشد. | Inspection |
| SRS-VIEW-011 | fieldهای متنی user-generated باید بتوانند محتوای Persian و English را ذخیره و نمایش دهند و presentation باید typography/font مناسب زبان محتوای نمایش‌داده‌شده را اعمال کند. | Test + Inspection |

## 3.14 Offline use و sync

مبنای canonical: System Definition بخش‌های 6.15، 8.5 و 8.6، DR-047، DR-109 و DR-122، Domain Model بخش 30.

| ID | Requirement | Verification |
|---|---|---|
| SRS-SYNC-001 | سیستم باید core flowهای پشتیبانی‌شده را بدون اتصال اینترنت قابل استفاده نگه دارد. | Test |
| SRS-SYNC-002 | تغییرات local پشتیبانی‌شده باید تا زمان reconnect حفظ شوند. | Test |
| SRS-SYNC-003 | پس از reconnect، سیستم باید تغییرات local را با server همگام کند. | Test |
| SRS-SYNC-004 | conflict resolution baseline باید در سطح field اعمال شود، نه فقط در سطح record کامل. | Test |
| SRS-SYNC-005 | اگر یک field در چند replica تغییر کرده باشد، baseline conflict policy باید Field-level Last-Write-Wins بر مبنای metadata زمانی تعریف‌شده باشد. | Test |
| SRS-SYNC-006 | entityهای sync‌شونده باید version و metadata زمانی کافی برای sync policy داشته باشند. | Test + Inspection |
| SRS-SYNC-007 | sync نباید AuditLog و history لازم برای بررسی conflict و recovery را از بین ببرد. | Test |
| SRS-SYNC-008 | استفاده‌ی offline از local working set قبلاً مجازشده نباید صرفاً پس از یک `N-day` ثابت product-defined منقضی شود؛ revalidation برای operationهای server-dependent یا reconnect می‌تواند طبق Security Design اعمال شود. | Test + Security Inspection |
| SRS-SYNC-009 | اگر browser/platform persistent local storage کافی در اختیار PWA نگذارد، سیستم باید تا حد امکان online functionality را حفظ کند، Offline capability را مطابق ظرفیت واقعی degrade کند و limitation را به User نشان دهد. | Failure Test + Inspection |
| SRS-SYNC-010 | conflict resolution، history ordering و authorization acceptance نباید صرفاً بر raw local wall-clock device تکیه کنند؛ clock skew غیرعادی نباید به‌تنهایی باعث data loss یا winning write نادرست شود. | Sync Test + Analysis |

## 3.15 Audit، history و Undo

مبنای canonical: System Definition بخش‌های 6.12، 8.3 و 8.4، DR-036، DR-072 و DR-118، Domain Model بخش 25.

| ID | Requirement | Verification |
|---|---|---|
| SRS-AUDIT-001 | سیستم باید history قابل استفاده‌ای از تغییرات مهم نگه دارد. | Test |
| SRS-AUDIT-002 | Audit history باید actor، entity، action، زمان رخداد و previous/new value یا diff لازم را قابل ثبت کند. | Test |
| SRS-AUDIT-003 | حذف state جاری در flowهایی مانند RoutineCompletion Reset نباید history آن تغییر را حذف کند. | Test |
| SRS-AUDIT-004 | history باید بتواند برای مشاهده تغییرات، troubleshooting sync و Undo/restore در flowهایی که محصول اجازه می‌دهد استفاده شود. | Test + Inspection |
| SRS-AUDIT-005 | AuditLog نباید سیستم را ملزم به full event sourcing کند. | Inspection |
| SRS-AUDIT-006 | User مجاز باید بتواند versionهای معنادار قبلی Resource را مشاهده و در flowهای پشتیبانی‌شده checkout/restore کند. | Test |
| SRS-AUDIT-007 | ادامه‌ی edit از یک historical version باید branch جدید ایجاد کند و branch قبلی را حفظ کند. | Test |
| SRS-AUDIT-008 | checkout/restore باید history event جدید ایجاد کند و نباید history یا branch قبلی را بازنویسی/حذف کند. | Test |
| SRS-AUDIT-009 | user-visible History، Audit evidence و Sync operation/version metadata باید stable identity و ordering semantics سازگار داشته باشند و نباید برای یک change/conflict interpretation متناقض ایجاد کنند. | Architecture Inspection + Sync Test |

## 3.16 Sharing، Group، Role و Assignment

مبنای canonical: System Definition بخش‌های 3.1 تا 3.4، 6.14، 7.1، 7.3، 7.4 و 10.1؛ DR-054، DR-055، DR-056، DR-057، DR-060، DR-061، DR-062، DR-063، DR-093، DR-108، DR-109، DR-111، DR-113، DR-114، DR-115 و DR-140؛ Domain Model بخش 29.

| ID | Requirement | Verification |
|---|---|---|
| SRS-SHARE-001 | سیستم باید Direct Sharing یک Resource را بدون الزام به GroupMembership پشتیبانی کند. | Test |
| SRS-SHARE-002 | Resourceهای قابل اشتراک در Personal V1 باید حداقل `Folder`، `List` و `Item` را پوشش دهند؛ `Item` در این requirement شامل `Task`، `Event` و `Routine` است. | Test |
| SRS-SHARE-003 | اشتراک‌گذاری یک Resource نباید به‌تنهایی ownership آن Resource را منتقل کند. | Test |
| SRS-SHARE-004 | مالک یا actor دارای permission لازم باید بتواند یک Share مستقیم را revoke کند، بدون اینکه این عمل به GroupMembership وابسته باشد. | Test |
| SRS-SHARE-005 | هنگام اشتراک‌گذاری Item، سیستم باید بتواند visibility اطلاعات را در قالب field groupهای معنادار در سطح محصول/domain محدود کند. | Test + Inspection |
| SRS-SHARE-006 | سیستم نباید arbitrary database/ORM fieldها یا metadata داخلی مانند sync، audit، authorization و versioning را صرفاً به دلیل وجود در persistence به عنوان field قابل اشتراک به user ارائه کند. | Inspection + Security Test |
| SRS-SHARE-007 | Direct Sharing باید از Access Profileهای از پیش تعریف‌شده برای بیان سطح دسترسی user-facing پشتیبانی کند. | Test |
| SRS-SHARE-008 | GroupMembership در Personal V1 باید از `System-defined Role` استفاده کند و `Custom Role` نباید بخشی از current role model باشد. | Test + Inspection |
| SRS-SHARE-009 | authorization باید بتواند operationهای مجاز را مستقل از نام Role/Profile و بر مبنای permission capabilityهای مؤثر ارزیابی کند. | Test + Architecture Inspection |
| SRS-SHARE-010 | capabilityهای collaboration باید بتوانند متناسب با Resource شامل view، comment، edit، move، claim، assign، manage sharing و سایر capabilityهای از پیش تعریف‌شده باشند. | Test |
| SRS-SHARE-011 | سیستم باید بتواند interaction سبک `Nudge` یا encouragement را، در صورت داشتن permission مربوطه، مستقل از Comment پشتیبانی کند. | Test |
| SRS-SHARE-012 | دسترسی Shareشده روی Folder باید بتواند به Listها و Itemهای داخل آن، و دسترسی Shareشده روی List باید بتواند به Itemهای داخل آن، به صورت inherited اعمال شود. | Test |
| SRS-SHARE-013 | Personal V1 نباید برای هر descendant یک container مشترک به explicit-deny exception پیچیده نیاز داشته باشد. | Inspection + Test |
| SRS-SHARE-014 | یک User باید بتواند هم‌زمان عضو چند Group باشد. | Test |
| SRS-SHARE-015 | Group باید بتواند به عنوان context پایدار collaboration چندنفره روی Resourceهای مشترک استفاده شود. | Test |
| SRS-SHARE-016 | سیستم باید assignment یک Task به چند عضو واجد دسترسی را پشتیبانی کند. | Test |
| SRS-SHARE-017 | سیستم باید claim کردن Task را برای actor دارای permission مربوطه پشتیبانی کند. | Test |
| SRS-SHARE-018 | Assignment و Authorization باید مستقل باشند؛ assigned یا claimed شدن Task نباید به‌تنهایی permission دسترسی به آن Task ایجاد کند. | Security Test |
| SRS-SHARE-019 | actor فقط زمانی باید بتواند روی Resource مشترک operation انجام دهد که از Direct Share، inherited access یا Group access معتبر permission لازم را داشته باشد. | Security Test |
| SRS-SHARE-020 | comment و live update روی Resource مشترک باید همان effective authorization مربوط به Resource را رعایت کنند. | Security Test + Integration Test |
| SRS-SHARE-021 | داده Resourceهای shareنشده یا خارج از permission مؤثر actor باید از userها و Groupهای غیرمجاز ایزوله بماند. | Security Test |
| SRS-SHARE-022 | زمان یک Task/Event مشترک باید یک instant مطلق قابل تبدیل داشته باشد و برای هر user بر اساس timezone او نمایش داده شود. | Test |
| SRS-SHARE-023 | live update و notificationهای collaboration باید بتوانند از کانال WebSocket سبک استفاده کنند، در حالی که REST مرجع عملیات CRUD باقی می‌ماند. | Integration Test |
| SRS-SHARE-024 | discovery مقصد برای Direct Sharing و Group invitation باید بتواند username/handle، name/display name، email و phone را به‌عنوان ورودی شناسایی User پشتیبانی کند. | Test |
| SRS-SHARE-025 | پیدا شدن User از طریق email یا phone نباید به‌خودی‌خود Share grant، access یا GroupMembership ایجاد کند. | Security Test |
| SRS-SHARE-026 | invitation باید تنها پس از authentication/registration معتبر recipient و تکمیل acceptance flow مربوط به access یا Membership فعال تبدیل شود. | Test + Security Test |
| SRS-SHARE-027 | lookup مقصد با email یا phone باید exact یا normalized-exact match باشد و partial contact-identifier search نباید behavior عادی discovery باشد. | Security Test + Test |
| SRS-SHARE-028 | نتیجه‌ی discovery از طریق email/phone نباید contact identifier خصوصی User مقصد را صرفاً به دلیل match شدن reveal کند؛ فقط identity لازم برای ادامه‌ی collaboration flow باید نمایش داده شود. | Security Test + Inspection |
| SRS-SHARE-029 | در contextهای معتبر نمایش هویت مانند collaboration discovery، Share/Group request، Group member list، Comment و Assignment، سیستم باید بتواند Profile Picture User را همراه identity presentation او نمایش دهد، بدون ایجاد public-discovery surface مستقل. | Test + Inspection |
| SRS-SHARE-030 | Folder/Resourceای که مستقیماً در Group context ساخته می‌شود باید Group-owned باشد و خروج creator نباید ownership یا بقای آن را از بین ببرد. | Test |
| SRS-SHARE-031 | Resource شخصی واردشده به Group context باید owner اصلی خود را حفظ کند و در عین حال تا زمان حضور در Group context از authorization همان Group تبعیت کند. | Test + Security Test |
| SRS-SHARE-032 | فقط owner شخصی باید بتواند personal Resource خود را از Group context detach کند، مگر تصمیم canonical دیگری authority صریح بدهد. | Security Test |
| SRS-SHARE-033 | Group-owned Resource نباید با Direct Share به actor خارج از Group، Group authorization boundary را دور بزند. | Security Test |

## 3.17 Tag

مبنای canonical: System Definition بخش 6.9، DR-045 و DR-104، Domain Model بخش 16.

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

مبنای canonical: System Definition بخش 6.9، DR-021، DR-023، DR-025، DR-026، DR-045 و DR-089، Domain Model بخش 17.

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

مبنای canonical: System Definition بخش‌های 5.4.3، 6.9 و 8.9؛ DR-045، DR-046، DR-073، DR-085، DR-086، DR-104 و DR-123؛ Domain Model بخش 18. Cadenceهای reactive/weekly موجود در این بخش با Roadmap Increment 9 trace می‌شوند.

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

## 3.20 Daily Ring selection، Daily Action و snapshot

مبنای canonical: System Definition بخش 6.10، DR-024، DR-031، DR-043، DR-044، DR-049 و DR-094، Domain Model بخش‌های 19 و 20.

| ID | Requirement | Verification |
|---|---|---|
| SRS-RING-001 | تعداد Daily Ring فعال هر Dotick Day باید `min(3, eligible_active_goals)` باشد. | Test |
| SRS-RING-002 | اگر حداقل سه Goal eligible وجود داشته باشد، سیستم باید دقیقا سه Daily Ring بسازد. | Test |
| SRS-RING-003 | اگر دو Goal eligible وجود داشته باشد، سیستم باید دو Ring و اگر یک Goal eligible وجود داشته باشد یک Ring بسازد. | Test |
| SRS-RING-004 | اگر Goal eligible وجود نداشته باشد، سیستم نباید Daily Ring فعال ایجاد کند. | Test |
| SRS-RING-005 | selection باید ترکیب روز را balanced کند و نباید صرفا بزرگ‌ترین backlog را انتخاب کند. | Analysis + Test |
| SRS-RING-006 | selection و plan generation باید حداقل due/timing، priority، neglect، weekday behavior، holiday context، streak momentum، workload، difficulty/effort و recent user capacity را به عنوان signal قابل استفاده در نظر بگیرد. | Analysis + Inspection |
| SRS-RING-007 | DailyRing باید user، goal، effective date، progress، completion state، final score، finalization state و algorithm/version metadata لازم را به صورت snapshot قابل بازسازی نگه دارد. | Test |
| SRS-RING-008 | تغییر عادی future fieldهای Item نباید معنای historical finalized DailyRing را بازنویسی کند. | Test |
| SRS-RING-009 | هر DailyRing باید بتواند Daily Actionهای روز را در یک یا چند RingGroup سازمان‌دهی کند. | Test |
| SRS-RING-010 | هر DailyAction باید به Original Item مرتبط باشد و بتواند completion کامل Item یا یک بخش معنادار و قابل‌اندازه‌گیری از آن را برای همان Dotick Day نمایندگی کند. | Test + Analysis |
| SRS-RING-011 | اگر DailyAction فقط بخشی از Original Item را نمایندگی کند، complete شدن Action نباید Original Item را به‌صورت کامل Done کند مگر requirement کامل Item نیز واقعاً برآورده شده باشد. | Test |
| SRS-RING-012 | RingGroup باید بتواند ruleهایی مانند all-members، minimum-count، minimum-credit، one-of-many و credit-cap را برای مشارکت در completion Ring بیان کند. | Test |
| SRS-RING-013 | RingGroup باید بتواند سهم مشخصی از progress کل Ring داشته باشد و بتواند به‌عنوان hard requirement تعریف شود. | Test |
| SRS-RING-014 | completion Ring باید از ruleهای deterministic RingGroup/DailyAction به‌دست آید و با وجود استفاده از AI برای estimation یا decomposition، قابل بازسازی باشد. | Test + Analysis |
| SRS-RING-015 | plan اولیه Ring باید در آغاز Dotick Day تولید شود، اما current Ring باید در همان روز بتواند از طریق replan کنترل‌شده به تغییرات معنادار واکنش نشان دهد. | Test |
| SRS-RING-016 | Item جدیدی که در طول Dotick Day ایجاد می‌شود باید بتواند در صورت relevance و feasibility به DailyAction یک Ring فعال تبدیل شود، بدون اینکه Goalهای روز از ابتدا reselect شوند. | Test + Analysis |
| SRS-RING-017 | replan نباید Ringی را که قبلا Complete شده دوباره ناقص کند. | Test |
| SRS-RING-018 | حذف Original Item در طول روز باید DailyAction وابسته را از current Ring حذف کند و در صورت نیاز plan همان Ring را replan کند. | Test |
| SRS-RING-019 | پس از finalization، relationship میان DailyRing، RingGroup، DailyAction و Original Item باید historical snapshot باشد و تغییرات آینده‌ی Item نباید آن را بازنویسی کند. | Test |
| SRS-RING-020 | اگر در یک Dotick Day هیچ Ringی به علت نبود Goal eligible ساخته نشود، Global Streak نباید افزایش یا reset شود و باید ثابت بماند. | Test |
| SRS-RING-021 | در هر Dotick Day قابل ارزیابی، complete شدن حداقل یک Daily Ring باید Global Streak را یک واحد افزایش دهد؛ اگر Ring معتبر وجود داشته باشد ولی هیچ Ringی complete نشود، Global Streak باید به `0` reset شود و complete شدن همه Ringها شرط ادامه streak نیست. | Test |

## 3.21 Progress، completion، performance score و Norm

مبنای canonical: System Definition بخش 6.10.6، DR-027، DR-028، DR-029، DR-030 و DR-070، Domain Model بخش 21.

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

مبنای canonical: System Definition بخش‌های 6.11، 8.1 و 8.2، DR-033، DR-035 و DR-115، Domain Model بخش‌های 22 و 23.

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
| SRS-DAY-013 | پروژه باید Time Semantics specification مستقلی داشته باشد که real instant، Calendar Day، Dotick Day، `occurrence_date`، credited/effective date، all-day interval، Account/device timezone، timezone change، DST، Jalali/Gregorian recurrence، leap/invalid dates و finalization boundary را به‌صورت یکپارچه تحلیل کند. | Analysis + Inspection |
| SRS-DAY-014 | برای ترکیب‌های زمانی فوق باید test vector و test case جامع شامل boundary، DST، timezone change، calendar edge، recurrence و day-attribution ساخته و در Incrementهای owning اجرا شود. | Test + Inspection |

## 3.23 Statistics و historical correction

مبنای canonical: System Definition بخش‌های 6.12، 7.2 و 8.3، DR-036 و DR-072، Domain Model بخش 24.

| ID | Requirement | Verification |
|---|---|---|
| SRS-STAT-001 | تغییر historical domain data مانند RoutineCompletion باید source/domain state و History را اصلاح کند؛ اثر آن بر derived statistics باید به open/finalized بودن window وابسته باشد. | Test |
| SRS-STAT-002 | سیستم نباید به صورت پیش‌فرض برای هر historical edit کل history را از ابتدا recompute کند. | Test + Analysis |
| SRS-STAT-003 | اگر statistical window هنوز open باشد، recomputation باید فقط به metric/windowهای متاثر محدود شود؛ maintenance/recovery صریح می‌تواند رفتار گسترده‌تری داشته باشد. | Test + Analysis |
| SRS-STAT-004 | simple counterهای مربوط به window/aggregate باز باید در صورت امکان با increment/decrement یا recomputation محدود اصلاح شوند. | Test |
| SRS-STAT-005 | streak یا derived state باز که historical edit روی آن اثر دارد باید فقط در محدوده لازم دوباره محاسبه شود. | Test |
| SRS-STAT-006 | raw completion و state-change data باید source of truth domain/derived state باز باشند، نه dashboard aggregate. | Test + Inspection |
| SRS-STAT-007 | behavior featureهای پرهزینه باید بتوانند مستقل از core write path refresh شوند. | Test + Analysis |
| SRS-STAT-008 | پس از finalize شدن day/week/month/year statistical window، نتیجه finalized آن نباید با historical Item edit بعدی بازنویسی شود. | Regression Test |
| SRS-STAT-009 | historical edit بعد از finalization باید در History/Audit قابل مشاهده بماند، حتی اگر نتیجه‌ی window بسته‌شده عمداً تغییر نکند. | Test |
| SRS-STAT-010 | long-lived aggregateای که از periodهای finalized تغذیه می‌شود باید contribution بسته‌شده را از outcome finalized همان period بگیرد تا edit آینده آن period را silently تغییر ندهد. | Test + Analysis |

## 3.24 AI-assisted Item creation

مبنای canonical: System Definition بخش 6.16، DR-037، DR-041 و DR-042، Domain Model مربوط به AI-assisted creation.

| ID | Requirement | Verification |
|---|---|---|
| SRS-AIITEM-001 | AI-assisted Item creation در Current Scope باید Voice را به‌عنوان user input modality پشتیبانی کند؛ typed Text باید از manual creation عادی استفاده کند و نباید Current-Scope AI-assisted input محسوب شود. | Test + Inspection |
| SRS-AIITEM-002 | در contextهای مناسب ایجاد Item، UI باید Voice AI creation را در کنار manual create flow در دسترس قرار دهد. | Inspection + Test |
| SRS-AIITEM-003 | Voice input باید پیش از AI analysis به transcript قابل پردازش تبدیل شود. | Test |
| SRS-AIITEM-004 | AI باید در صورت قابل استنتاج بودن بتواند نوع ورودی را از میان Task، Event و Routine و همچنین fieldهای معتبر مانند title، date/time، recurrence، location، description، Folder/List/Column، reminder، priority، deadline/grace و Tag پیشنهاد دهد. | Test + Evaluation |
| SRS-AIITEM-005 | AI output باید به عنوان Draft/Proposal نمایش داده شود و user باید بتواند تمام جزئیات پیشنهادی را قبل از ایجاد Item ویرایش کند. | Test |
| SRS-AIITEM-006 | سیستم نباید صرفا بر اساس AI inference و پیش از Confirm user رکورد نهایی Item ایجاد کند. | Test |
| SRS-AIITEM-007 | پس از Confirm، سیستم باید Item واقعی را از payload نهایی تاییدشده ایجاد کند. | Test |
| SRS-AIITEM-008 | سیستم باید بتواند برای proposal تأییدشده/موردنیاز یک AIItemCreationSession شامل source type، original input، transcript، AI proposal، user final payload، model version، accepted state و timestamps را نگه دارد؛ source type مستقیم User در Current Scope باید Voice باشد. | Test |
| SRS-AIITEM-009 | سیستم باید بتواند field-level change بین AI proposal و user final payload را برای evaluation و future personalization نگه دارد. | Test |
| SRS-AIITEM-010 | draft/session باید بتواند provenance field را حداقل میان explicit user input، AI inferred، user-preference inferred و external source تفکیک کند. | Test |
| SRS-AIITEM-011 | failure سرویس AI یا STT نباید manual Item creation و core task management را از کار بیندازد. | Failure Test |
| SRS-AIITEM-012 | payload نهایی AI-assisted creation باید پیش از ایجاد Item واقعی همان validationهای domain مربوط به Task/Event/Routine را، متناسب با type نهایی proposal، پاس کند. | Test |
| SRS-AIITEM-013 | Voice AI creation باید به microphone capability/permission وابسته باشد و در نبود permission باید به User اعلام شود که دسترسی microphone لازم است. | Permission Test + Inspection |
| SRS-AIITEM-014 | نبود microphone permission نباید به typed-text AI fallback منجر شود؛ manual Item creation باید مستقل از microphone و AI قابل استفاده باقی بماند. | Test + Inspection |
| SRS-AIITEM-015 | Cancel/Reject کردن proposal نباید Item واقعی ایجاد کند و session رد/لغوشده در Current Scope نباید صرفاً برای future learning به‌صورت دائمی نگه‌داری شود؛ retention مجاز باید با System Definition و Privacy Design سازگار باشد. | Test + Privacy Inspection |

## 3.25 AI provider execution، BYOK و AI controls

مبنای canonical: System Definition بخش‌های 5.4.3، 6.16 و 9.2، DR-068، DR-126 و DR-128.

| ID | Requirement | Verification |
|---|---|---|
| SRS-AIEXEC-001 | در حالت service-managed، سیستم باید provider/model مورد استفاده برای AI را طبق policy سرویس انتخاب کند و نباید انتخاب provider/model را به‌عنوان control عادی User ارائه کند. | Test + Inspection |
| SRS-AIEXEC-002 | سیستم باید به User اجازه دهد برای provider پشتیبانی‌شده credential/API شخصی configure کند و personal-credential mode را فعال کند. | Test |
| SRS-AIEXEC-003 | User باید بتواند personal-credential mode را غیرفعال کرده و به service-managed AI پیش‌فرض برگردد. | Test |
| SRS-AIEXEC-004 | اگر credential شخصی برای یک request قابل استفاده نباشد، سیستم باید بتواند request را از طریق service-managed AI ادامه دهد. | Failure Test |
| SRS-AIEXEC-005 | در fallback از credential شخصی به service-managed AI، سیستم باید بدون نیاز به popup جداگانه یک indication قابل مشاهده و non-blocking ارائه کند که credential شخصی استفاده نشده و سرویس Dotick به‌کار رفته است. | Test + Inspection |
| SRS-AIEXEC-006 | سیستم ملزم نیست exact provider/model service-managed را به User نمایش دهد. | Inspection |
| SRS-AIEXEC-007 | داده‌ای که actor طبق effective authorization و field visibility حق مشاهده‌ی آن را دارد، از جمله داده‌ی Shareشده، باید بتواند در capability مجاز به‌عنوان AI context استفاده شود؛ AI نباید field/Resource خارج از access مؤثر actor را به provider ارسال کند. | Security Test |
| SRS-AIEXEC-008 | سیستم باید یک control سراسری برای غیرفعال‌کردن external AI processing در اختیار User قرار دهد. | Test + Inspection |
| SRS-AIEXEC-009 | با غیرفعال‌شدن external AI processing، AI-assisted Item Creation، Goal Discovery/AI Tag processing و Daily Ring capabilityهای وابسته به AI باید unavailable شوند، در حالی که core Task/Event/Routine management، organization، collaboration و behaviorهای مستقل از AI قابل استفاده باقی بمانند. | Test + Failure Test |
| SRS-AIEXEC-010 | SRS نباید implementation Voice transcription را به external STT provider خاصی مقید کند؛ transcription می‌تواند local، platform-provided یا external باشد، مشروط بر حفظ semantics و validation یکسان downstream. | Inspection + Test |
| SRS-AIEXEC-011 | در personal-credential mode، اعتبار credential، quota، billing و provider-account limits باید مسئولیت User محسوب شوند و سیستم نباید availability یا cost آن account خارجی را تضمین کند. | Inspection + Failure Test |

## 3.26 Notification delivery and cross-device interaction

مبنای canonical: System Definition بخش‌های 6.8، 8.7 و 9.4، DR-103، DR-121، DR-128 و DR-135.

| ID | Requirement | Verification |
|---|---|---|
| SRS-NOTIF-001 | Notification/push delivery از طریق OS یا push infrastructure پشتیبانی‌شده باید بخشی از Current Scope باشد. | Integration Test + Inspection |
| SRS-NOTIF-002 | Dotick باید trigger، recipient، content، category و interaction state Notification را تعیین کند و external delivery infrastructure نباید source of truth این semantics باشد. | Test + Architecture Inspection |
| SRS-NOTIF-003 | User باید بتواند categoryهای اصلی Notification مانند reminders/alarms، comments/mentions، Group/Sharing/invitations، Nudge/collaboration و gamification/motivational را مستقل configure یا disable کند. | Test |
| SRS-NOTIF-004 | سیستم باید برای workflow/collaboration notificationهایی که نیازمند review/action داخل application هستند Notification Center داخلی ارائه کند. | Test + Inspection |
| SRS-NOTIF-005 | interaction نهایی با Notification روی یک device باید state مربوط را بین deviceها sync کند و از delivery مجدد همان notification اولیه روی deviceهای دیگر جلوگیری کند. | Integration Test |
| SRS-NOTIF-006 | Snooze/remind-later نباید acknowledgement نهایی محسوب شود و باید trigger جدیدی ایجاد کند که دوباره روی deviceهای واجد شرایط قابل delivery باشد. | Test |
| SRS-NOTIF-007 | ندادن یا revoke شدن browser/OS notification permission نباید underlying Reminder/Notification domain state یا سایر capabilityهای Dotick را غیرفعال کند؛ فقط external presentation/delivery باید unavailable شود. | Permission Test + Failure Test |
| SRS-NOTIF-008 | Reminderها و alarmهای معمولی که به علت نبود permission تحویل نشده‌اند نباید برای جبران در Notification Center داخلی جمع شوند. | Test + Inspection |
| SRS-NOTIF-009 | Notification Center داخلی باید برای workflow/app-level messages مانند Share/Group invitation و requestهای نیازمند action و updateهای system/product استفاده شود، نه به‌عنوان reminder history. | Test + Inspection |



## 3.27 Attachment local cache

مبنای canonical: System Definition بخش‌های 6.15 و 11.2، DR-136.

| ID | Requirement | Verification |
|---|---|---|
| SRS-CACHE-001 | Attachment metadata باید بتواند در local working set باقی بماند حتی اگر binary همان Attachment روی device ذخیره نشده باشد. | Test |
| SRS-CACHE-002 | Attachmentی که از همان device upload/selected شده است باید تا زمانی که local copy آن موجود است بدون download مجدد قابل بازشدن باشد. | Offline Test |
| SRS-CACHE-003 | روی device دیگر، binary Attachment باید در صورت نبود local copy هنگام نیاز download شود، مگر اینکه auto-download policy آن device فایل را قبلاً دریافت کرده باشد. | Multi-device Test |
| SRS-CACHE-004 | هر device باید Attachment cache مستقل با default سراسری قابل تنظیم داشته باشد. | Test + Inspection |
| SRS-CACHE-005 | User باید بتواند حداقل automatic download، retention duration شامل keep-indefinitely و maximum local cache size را برای cache همان device تنظیم کند. | Test + Inspection |
| SRS-CACHE-006 | User باید بتواند cache policy را برای Folder یا List مشخص override کند و policy خاص‌تر باید بر default بالادستی اولویت داشته باشد. | Test |
| SRS-CACHE-007 | eviction/cleanup cache باید فقط local binary را حذف کند و نباید server-side Attachment، metadata یا relation آن با Item را حذف کند. | Data Integrity Test |
| SRS-CACHE-008 | Attachment evictشده باید هنگام connectivity دوباره قابل download باشد. | Integration Test |
| SRS-CACHE-009 | نبود local Attachment binary در حالت Offline نباید سایر داده‌های local Resource را غیرقابل استفاده کند. | Offline Test |

## 3.28 Data export و Account deletion

مبنای canonical: System Definition بخش 10.2، DR-131.

| ID | Requirement | Verification |
|---|---|---|
| SRS-DATA-001 | User باید بتواند به‌صورت دستی export قابل حمل و machine-readable از داده‌های متعلق به Account خود درخواست کند. | Test + Inspection |
| SRS-DATA-002 | export نباید core user-owned domain data را به‌صورت silent حذف کند؛ format و packaging دقیق، از جمله نحوه‌ی inclusion Attachment، در Design مربوط تعیین می‌شود. | Test + Inspection |
| SRS-DATA-003 | Current Scope نباید scheduled export، automatic third-party backup destination یا import/restore از export را به‌عنوان capability اجباری require کند. | Inspection |
| SRS-DATA-004 | User باید بتواند Account deletion را درخواست کند و deletion باید وارد recovery window سی‌روزه شود. | Test |
| SRS-DATA-005 | User باید در recovery window بتواند deletion را cancel و Account را recover کند. | Test |
| SRS-DATA-006 | پس از پایان recovery window، Account و personal operational data متعلق به User باید از active persistence به‌صورت permanent حذف شوند. | Test + Data Inspection |
| SRS-DATA-007 | Group-owned Resource یا داده‌ای که ownership آن متعلق به actor/entity دیگری است نباید صرفاً به دلیل حذف Account creator حذف شود. | Test |
| SRS-DATA-008 | history/audit ضروری برای integrity داده‌ی سایر Userها باید بتواند پس از Account deletion با minimal identity یا anonymization لازم باقی بماند. | Test + Security Inspection |

# 4. نیازمندی‌های رابط خارجی و محدودیت‌های فنی

## 4.1 API و ارتباط client/server

مبنای canonical: System Definition بخش‌های 4.1 و 10.6، Roadmap Increment 0 برای engineering baseline.

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
| SRS-CON-004 | Current Scope نباید supported self-hosting برای arbitrary end user را به‌عنوان product capability الزام کند؛ source availability یا development/local execution به‌تنهایی self-host deployment contract ایجاد نمی‌کند. | Architecture + Deployment Inspection |

## 4.3 External service responsibility boundaries

مبنای canonical: System Definition بخش 9، DR-048، DR-061، DR-065، DR-121، DR-128 و DR-135.

| ID | Requirement | Verification |
|---|---|---|
| SRS-EXT-001 | Google identity provider باید فقط identity assertion لازم برای external authentication را فراهم کند؛ Account state، authorization و application data باید تحت authority Dotick باقی بمانند. | Integration Test + Security Inspection |
| SRS-EXT-002 | در email verification و password reset، Dotick باید token/state validity و Account transition را کنترل کند؛ external email delivery provider در صورت استفاده فقط مسئول transport پیام است. | Security Test + Integration Test |
| SRS-EXT-003 | invitation delivery از طریق email یا در صورت پشتیبانی phone/SMS نباید authorization ایجاد کند؛ recipient matching، acceptance و access/Membership transition باید توسط Dotick کنترل شوند. | Security Test |
| SRS-EXT-006 | external email/SMS delivery provider در contact verification فقط باید code را transport کند؛ challenge validity و فعال‌شدن contact باید تحت authority Dotick باقی بمانند. | Security Test + Integration Test |
| SRS-EXT-004 | OS/push notification infrastructure باید فقط نقش delivery/display داشته باشد و نباید authorization یا notification semantics را تعیین کند. | Integration Test + Security Test |
| SRS-EXT-005 | Current Scope نباید import/sync/automation مستقیم با Google Calendar، Notion، TickTick یا سایر productivity systemهای مشابه را به‌عنوان dependency لازم داشته باشد. | Inspection + Integration Test |

# 5. نیازمندی‌های غیرعملکردی

## 5.1 امنیت

مبنای canonical: System Definition بخش 10.1 و requirements امنیتی مرتبط با Authentication/Group، DR-061، DR-126 و DR-130.

| ID | Requirement | Verification |
|---|---|---|
| SRS-NFR-SEC-001 | password plaintext نباید در persistence یا logهای عادی ذخیره شود. | Security Test + Inspection |
| SRS-NFR-SEC-002 | password credential باید با الگوریتم hashing امن مانند Argon2، bcrypt یا معادل امن پروژه محافظت شود. | Security Inspection |
| SRS-NFR-SEC-003 | requestها و queryهای user-private باید دسترسی user دیگر به داده خصوصی را در حالت عادی رد کنند. | Security Test |
| SRS-NFR-SEC-004 | queryها و authorization مربوط به Group باید cross-group data leakage را رد کنند. | Security Test |
| SRS-NFR-SEC-005 | WebSocket و سایر live channelها باید همان authorization لازم برای داده قابل مشاهده را رعایت کنند. | Security Test |
| SRS-NFR-SEC-006 | AI context construction باید effective authorization و field visibility actor را enforce کند؛ shared بودن Resource نباید باعث ارسال fieldهای غیرقابل مشاهده به external AI provider شود. | Security Test |
| SRS-NFR-SEC-010 | پیش از فعال‌شدن/اولین استفاده از external AI processing، سیستم باید به User اعلام کند و acceptance او را ثبت/قابل اثبات کند که context مجاز ــ شامل shared data در محدوده effective visibility ــ می‌تواند برای پردازش به third-party AI infrastructure ارسال شود و provider-side risk خارج از boundary کنترل مستقیم Dotick وجود دارد. | Security Test + Inspection |
| SRS-NFR-SEC-011 | Privacy/Terms release مربوط باید provider-side processing/retention/training و allocation مسئولیت third-party data processing را صریح formalize کند؛ System/SRS نباید این موضوع حقوقی را با assumption ضمنی جایگزین کند. | Legal/Privacy Gate Inspection |
| SRS-NFR-SEC-007 | server-side user data، operational backup و local replica باید از protection/encryption-at-rest مناسب محیط خود استفاده کنند؛ algorithm و key-management دقیق در Security Design تعیین می‌شود. | Security Inspection + Test |
| SRS-NFR-SEC-008 | operationهای state-changing Platform Administrator باید audit شوند. | Security Test |
| SRS-NFR-SEC-009 | دسترسی Platform Administrator به User-private data نیز باید در administrative audit قابل trace باشد. | Security Test + Inspection |

## 5.2 قابلیت اطمینان و حفاظت از داده

| ID | Requirement | Verification |
|---|---|---|
| SRS-NFR-REL-001 | failure سرویس خارجی AI نباید core manual task management را unavailable کند. | Failure Test |
| SRS-NFR-REL-002 | Reset و historical edit باید history لازم برای recovery و بررسی خطا را حفظ کنند. | Test |
| SRS-NFR-REL-003 | sync conflict resolution نباید تغییر fieldهای مستقل را صرفا به دلیل conflict در field دیگر از بین ببرد. | Sync Test |
| SRS-NFR-REL-004 | historical DailyRing snapshot نباید با تغییرات عادی آینده به صورت ناخواسته بازنویسی شود. | Regression Test |
| SRS-NFR-REL-005 | server-side user data باید backup/recovery مناسب برای disaster یا infrastructure failure داشته باشد؛ RPO/RTO، frequency و retention دقیق در Operations/Security Design تعیین می‌شوند. | Recovery Test + Inspection |
| SRS-NFR-REL-006 | multi-Resource operationی که consequence کامل آن قابل اعمال نیست نباید partial state را به‌عنوان outcome موفق باقی بگذارد. | Transaction/Integration Test |
| SRS-NFR-REL-007 | permanent Account deletion نباید خارج از recovery/backup policy کنترل‌شده باعث بازگشت silent داده‌ی حذف‌شده به active product state شود. | Recovery Test + Security Inspection |
| SRS-NFR-REL-008 | foundational entity/version/delete/order design در Incrementهای اولیه باید با Offline/Sync، branching History/Audit و authorization-revocation semantics شناخته‌شده‌ی Incrementهای بعدی سازگار باشد؛ defer شدن implementation نباید incompatibility بنیادی ایجاد کند. | Architecture/Data Design Inspection |

## 5.3 کارایی

| ID | Requirement | Verification |
|---|---|---|
| SRS-NFR-PERF-001 | بازیابی hierarchy child/parent باید بدون parse کامل RichDescription انجام شود. | Performance Test + Analysis |
| SRS-NFR-PERF-002 | design hierarchy باید امکان index-supported query را فراهم کند. | Data Design Inspection + Performance Test |
| SRS-NFR-PERF-003 | baseline local deployment باید در Performance Test Plan برای حدود 30 user هم‌زمان ارزیابی شود. این عدد test target است و SLA محسوب نمی‌شود. | Performance Test |
| SRS-NFR-PERF-004 | live update گروهی باید در Performance Test Plan با threshold مناسب برای تجربه تقریبا real-time ارزیابی شود. | Performance Test |
| SRS-NFR-PERF-005 | historical edit نباید به صورت پیش‌فرض full-history recomputation synchronous را به core user action تحمیل کند. | Performance Test + Analysis |
| SRS-NFR-PERF-006 | core local interactionها مانند navigation، Item open/edit و state change نباید در جایی که semantics اجازه می‌دهد به network request یا heavy computation غیرضروری synchronous وابسته باشند. | Performance Test + Analysis |
| SRS-NFR-PERF-007 | AI inference، semantic analysis، large sync و expensive statistics/recomputation باید در صورت امکان بدون تغییر semantics از synchronous interaction path defer یا جدا شوند. | Performance Test + Architecture Inspection |

## 5.4 usability و presentation

| ID | Requirement | Verification |
|---|---|---|
| SRS-NFR-UX-001 | UI باید در اندازه‌های رایج mobile و layoutهای responsive قابل استفاده باقی بماند. | Usability Test + Inspection |
| SRS-NFR-UX-002 | پیچیدگی داخلی child/reference، sync metadata یا storage inheritance نباید بدون requirement صریح به controlهای پیچیده اضافی در UI نشت کند. | UX Inspection |
| SRS-NFR-UX-003 | AI proposal باید قبل از Confirm برای user قابل بازبینی و اصلاح باشد. | Usability Test |
| SRS-NFR-UX-004 | progress Daily Ring باید برای user حداکثر 100 درصد نمایش داده شود، حتی اگر final performance بالاتر از baseline باشد. | UI Test |
| SRS-NFR-UX-005 | نمایش Persian user-generated content نباید به English-only UI language وابسته باشد و باید typography/font مناسب محتوای Persian را پشتیبانی کند. | UI Test + Inspection |

## 5.5 maintainability و change isolation

| ID | Requirement | Verification |
|---|---|---|
| SRS-NFR-MAINT-001 | failure یا تغییر یک integration خارجی نباید مدل ownership داخلی را به Source وابسته کند. | Architecture Review + Test |
| SRS-NFR-MAINT-002 | تغییر View نباید domain data را تغییر دهد. | Regression Test |
| SRS-NFR-MAINT-003 | limitation یک browser/PWA platform نباید semantics مشترک status، ownership، schedule، completion یا authorization را تغییر دهد؛ unsupported capability باید در presentation/delivery degrade شود. | Architecture Review + Cross-platform Test |

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
16. Task می‌تواند کاملاً unscheduled باشد و نبود date/time مانع وجود آن نیست.
17. blocked Task تا Done شدن همه blockerهای فعال نمی‌تواند Done شود و dependency از hierarchy مستقل است.
18. completion cascade Task طبق Preferences و قواعد Parent/descendant تعریف‌شده در بخش 3.3 اعمال می‌شود.
19. delete/completion cascade و move cascade باید authorization semantics متفاوت و atomicity چند-Resource را رعایت کنند.
20. Global Streak در Dotick Day قابل ارزیابی با complete شدن حداقل یک Ring ادامه پیدا می‌کند و complete شدن همه Ringها لازم نیست.

# 7. جزئیات عمداً نامشخص و non-normative در Current Scope

در baseline فعلی هیچ Product/Domain decision بازی برای Personal V1 باقی نمانده است. موارد این بخش requirement رفتاری جدید ایجاد نمی‌کنند؛ behavior آن‌ها در بخش‌های normative یا منابع canonical مشخص شده و فقط implementation، representation یا tuning دقیق به artifact مالک واگذار شده است.

موارد Enterprise/Future در این بخش فهرست نمی‌شوند.

| Detail ID | موضوع عمداً نامشخص | محل formalization |
|---|---|---|
| UNSPEC-001 | schema، serialization، ordering و edit-storage دقیق RichDescription/ContentBlock | Increment 2 Design |
| UNSPEC-002 | schema/indexing دقیق structural child، dependency و reference | Increment 2 Data/API Design |
| UNSPEC-003 | recurrence config serialization و occurrence persistence/identity | Increment 4 Recurrence/Data Design |
| UNSPEC-004 | sync metadata، clock/device strategy، idempotency و conflict representation | Increment 6 Sync Design |
| UNSPEC-005 | endpointها، payloadها و API versioning دقیق | به تفکیک Increment/API Contract |
| UNSPEC-006 | representation فیزیکی RingGroup/DailyAction و replan concurrency | Increment 10 Design |
| UNSPEC-007 | فرمول و coefficientهای دقیق Ring progress/final score/early bonus/late recovery | Increment 10 Scoring Specification |
| UNSPEC-008 | الگوریتم و وزن‌های دقیق Goal selection و learning parameters | Increment 10 Algorithm Specification |
| UNSPEC-009 | representation/estimation دقیق difficulty/effort | Increment 10 Algorithm/AI Specification |
| UNSPEC-010 | thresholdها/windowها و نرخ تغییر Adaptive Norm | Increment 10 Tuning Specification |
| UNSPEC-011 | inactivity threshold و decay curve incremental Routine | Increment 3/10 Routine/Tuning Specification |
| UNSPEC-012 | مدت دقیق AI Goal warm-up | Increment 9 AI/Goal Specification |
| UNSPEC-013 | thresholdهای عددی/model-specific Goal similarity | Increment 9 AI/Goal Specification |
| UNSPEC-014 | timing/frequency/cooldown/copy رفتار motivational/scolding | Increment 10 Gamification Specification |
| UNSPEC-015 | frequency/rate-limit دقیق Goal-level motivational reminder | Increment 10 Gamification/Notification Specification |
| UNSPEC-016 | verification-code format/expiry/retry/rate-limit، anti-abuse و normalization تماس | Authentication/Security Design |
| UNSPEC-017 | Attachment cache accounting، eviction ordering، quota و platform storage implementation | Offline/Storage Design |
| UNSPEC-018 | encryption-at-rest algorithms، key management و storage-protection mechanism | Security Design |
| UNSPEC-019 | backup frequency/retention/RPO/RTO و restore procedure | Operations/Security Design |
| UNSPEC-020 | manual data-export format و Attachment packaging | Data/Export Design |
| UNSPEC-021 | session hardening، account linking و credential recovery mechanics | Authentication Design |
| UNSPEC-022 | service-managed AI routing/retry/timeout، BYOK credential storage و STT/provider implementation | AI/Security Design |
| UNSPEC-023 | PWA service-worker/install/offline-storage implementation و supported browser/version matrix | Client/PWA Design |
| UNSPEC-024 | Notification transport/provider/device-registration/retry implementation | Notification Design |
| UNSPEC-025 | prompt templateها، model-specific parameters و AI evaluation/tuning جزئی | AI Specification |
| UNSPEC-026 | representation/storage دقیق Time Semantics و test-vector catalog، با حفظ behavior canonical | `TIME_SEMANTICS_SPEC.md` / Recurrence & Time Design |

این جزئیات نباید بهانه‌ای برای تغییر behavior canonical باشند. اگر در Design مشخص شود یک موضوع واقعاً نیازمند تصمیم Product/Domain جدید است، آن موضوع باید به Decision Register بازگردد و تا زمان نهایی‌شدن، implementation نباید آن تصمیم را به‌صورت ضمنی ببندد.

## 7.1 مواردی که نباید دوباره به‌عنوان OPEN Product Question تلقی شوند

موضوعاتی مانند Event structural multiplicity، Task dependency cycle، ordering زمانی Task، recurring Task generation، frequency-based Routine streak، Group container ownership، global daily streak، Goal similarity behavior، Daily Ring difficulty ownership و recurring occurrence product semantics در Decision Register بسته شده‌اند. جزئیات implementation/tuning باقی‌مانده‌ی آن‌ها فقط در جدول بالا یا Design مالک قرار می‌گیرد.

## 7.2 مرز Current Scope

این inventory عمداً فقط به Personal V1 / Current Scope محدود است. جزئیات قابلیت‌های خارج از Current Scope در این بخش نگه‌داری نمی‌شوند و در صورت ورود آن capability به Scope باید در artifact مالک خود formalize شوند.

# 8. Future و خارج از scope Personal V1

موارد این بخش normative acceptance برای Personal V1 نیستند. این بخش عمداً میان `Planned Future Direction` و قابلیت‌هایی که صرفاً `Out of Scope / Unplanned` هستند تفاوت می‌گذارد.

## 8.1 Planned Future Direction

- Enterprise multi-tenancy و Organization/Tenant hierarchy.
- Custom Roles و authorization سازمانی پیشرفته.
- Enterprise SSO پس از انتخاب protocol مناسب.
- management reporting، organization administration و privacy/compliance specificationهای وابسته به Enterprise context.
- Google Calendar، Notion، TickTick و سایر calendar/productivity integrationها.
- Email و سایر external sourceها به‌عنوان ورودی automation/creation pipeline فراتر از delivery/invitation فعلی.
- external AI agent و voice-assistant integration؛ در صورت اضافه‌شدن باید user-authorized، resource/capability-scoped، revocable و auditable باشد.
- Trusted Automation بدون confirmation موردبه‌مورد، فقط تحت authority صریح، scoped، revocable و auditable؛ exact permission levels و UX در Future Design تعیین می‌شوند.
- personalization پیشرفته AI بر اساس correction history و signalهای رفتاری ثبت‌شده.
- accessibility support برای release mature/public، با specification آینده برای keyboard interaction، screen-reader semantics، scalable text، contrast و measurable conformance target.
- native Android/iOS، desktop-native clientها، OS/application widgetها و platform-specific capabilityهای عمیق‌تر؛ Current Scope روی installable PWA است. تکمیل full persistent/alarm-like integration با APIهای اختصاصی هر OS می‌تواند در همین native evolution انجام شود.

## 8.2 Explicitly Out of Scope and Not Currently Planned as Future Commitments

موارد زیر نه Current-Scope requirement هستند و نه صرفاً به دلیل نبودن در نسخه فعلی، وعده‌ی نسخه‌ی آینده محسوب می‌شوند. ورود هرکدام به Future Scope نیازمند تصمیم canonical جدید است:

- public social-network behavior شامل follower/following، public feed، standalone Public Profile و public discovery خارج از collaboration action مشخص؛ Profile Picture اختیاری Account از این مرز مستثنا است و فقط identity presentation است.
- supported self-hosting برای arbitrary end user و production deployment contract شخص ثالث.
- typed-text AI-assisted Item creation به‌عنوان input مستقیم User؛ typed User input در مدل فعلی manual creation است.
- general-purpose public developer API برای arbitrary third-party clients؛ integrationهای آینده در جهت فعلی از controlled permission-based surface استفاده می‌کنند.
- full UI localization به Persian یا سایر زبان‌ها؛ Current Scope UI انگلیسی است و Persian فقط در user-generated content/typography پشتیبانی می‌شود.
- TOTP/SMS-based additional independent 2FA.

Commercialization آینده ممکن است، اما مدل monetization هنوز انتخاب نشده است. Pricing، subscription، billing، payment، license enforcement و support contract تجاری تا زمان تصمیم Business/Product جداگانه نه requirement فعلی هستند و نه Future commitment مشخص.

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

این پیوست نسخه‌ی requirement-oriented واژه‌نامه است. در صورت تفاوت در wording، تعریف canonical در System Definition بخش 14 مرجع بالاتر است.

| اصطلاح | تعریف |
|---|---|
| Item | ریشه مفهومی Task، Event و Routine؛ Goal یک Item نیست. |
| Schedulable | capability مفهومی مشترک Task و Event برای رفتارهای زمان‌بندی‌شونده؛ الزام به inheritance فیزیکی ایجاد نمی‌کند. |
| Task | Item مربوط به کار قابل انجام با lifecycle، schedule/deadline و dependency مخصوص Task. |
| Event | Item مربوط به رویدادی که می‌تواند unscheduled، زمان‌دار یا all-day باشد؛ lifecycle time-driven آن فقط پس از داشتن start schedule معتبر اعمال می‌شود و Location آن اختیاری است. |
| Routine | definition تکرارشونده‌ای که outcome هر روز آن در RoutineCompletion ثبت می‌شود و status کلی روزانه ندارد. |
| RoutineCompletion | state جاری progress/outcome یک Routine برای occurrence_date مشخص. |
| Goal | objective معنایی مستقل از Item hierarchy که توسط Goal Discovery مدیریت می‌شود و مبنای Daily Ring است. |
| Tag | entity مستقل برای tagging/semantic association که می‌تواند User-created یا AI-created باشد. |
| TrackingState | capability/state مشترک Routine و Goal برای streak و completion aggregateهای مربوط. |
| Daily Ring | برنامه‌ی روزانه‌ی یک Goal برای یک Dotick Day که از RingGroup و DailyAction تشکیل می‌شود. |
| RingGroup | گروه DailyActionها با rule مشخص برای contribution/satisfaction در Daily Ring. |
| DailyAction | action snapshotشده‌ی روزانه که completion کامل یا بخش معناداری از Original Item را نمایندگی می‌کند. |
| Global Streak | streak روزانه‌ی User که با complete شدن حداقل یک Daily Ring در Dotick Day قابل ارزیابی ادامه پیدا می‌کند. |
| Dotick Day | روز منطقی سیستم که boundary آن می‌تواند با midnight متفاوت باشد. |
| Calendar Day | روز تقویمی در calendar/timezone مؤثر؛ الزاماً با Dotick Day یکسان نیست. |
| Credited / Effective Date | business dayای که completion/action برای scoring، streak یا day-based statistics به آن نسبت داده می‌شود. |
| Structural Child | relation hierarchy واقعی میان Task/Event که با Reference متفاوت است. |
| Reference | اشاره‌ی غیرساختاری به Item بدون ایجاد structural parent. |
| Dependency / Blocker | relation Task-to-Task که Done شدن Task وابسته را تا Done شدن blocker محدود می‌کند. |
| Direct Sharing | اعطای دسترسی Resource-specific بدون نیاز به GroupMembership. |
| Access Profile | preset از پیش تعریف‌شده‌ی permission capabilityها برای Direct Sharing. |
| Group | context پایدار collaboration با Membership، Role و Resourceهای مشترک. |
| System-defined Role | preset از پیش تعریف‌شده‌ی capabilityها برای GroupMembership در Current Scope. |
| Effective Access | permissionهای واقعی actor روی Resource پس از جمع‌بندی access pathهای معتبر. |
| Assignment | responsibility انجام Task؛ به‌تنهایی authorization ایجاد نمی‌کند. |
| Source | provenance داده، مستقل از owner، creator و authorization. |
| Finalized Artifact | derived historical business recordی که پس از finalization با edit بعدی source data بازنویسی نمی‌شود. |
| Historical Snapshot | representation تثبیت‌شده‌ی state/decision گذشته که تغییرات آینده source data آن را بازنویسی نمی‌کند. |
| Trash | lifecycle بازیابی‌پذیر حذف برای Resourceهای eligible با retention فعلی 30 روز. |
| Local Replica | نسخه‌ی local قابل‌تغییر state موردنیاز User برای Offline flow؛ صرفاً read-only cache نیست. |
| Reconciliation | همگراکردن local changes و server state پس از connectivity. |
| Field-level LWW | baseline conflict policy در سطح field؛ device clock به‌تنهایی authoritative نیست. |
| Service-managed AI | AI execution با provider/credential مدیریت‌شده توسط Dotick. |
| Personal AI Credential / BYOK | credential/API شخصی User برای provider پشتیبانی‌شده. |
| External AI Processing Control | setting سراسری برای غیرفعال‌کردن capabilityهای وابسته به external AI processing. |
| Attachment Cache | local binary cache device-specific برای Attachment؛ eviction آن server-side Attachment را حذف نمی‌کند. |
| Profile Picture | تصویر اختیاری identity User در contextهای معتبر؛ Public Profile ایجاد نمی‌کند. |
| `Tab` / `Section` | اصطلاحات legacy برای Column و نه entity مستقل. |
| `DailyRingItem` | representation legacy و superseded مدل flat Daily Ring؛ مدل فعلی RingGroup/DailyAction است. |
| `Speech-to-Task` | framing legacy؛ Current Scope از Voice AI-assisted creation برای Task/Event/Routine proposal استفاده می‌کند. |
| Formal SRS | baseline requirementهای رسمی و قابل verification؛ design/tuning detail عمداً واگذارشده به‌تنهایی requirement رفتاری جدید نیست. |

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
