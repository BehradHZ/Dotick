# Dotick — Decision Register

> این سند تغییرات و تصمیم‌های تثبیت‌شده‌ی تحلیل فعلی را ثبت می‌کند تا در بازنویسی SRS/Domain/Design چیزی گم نشود.

Statusها:

- `CONFIRMED`: در گفت‌وگوی فعلی نهایی شده.
- `RETAINED`: از اسناد قبلی آمده و فعلاً contradicted نشده.
- `OPEN`: هنوز تصمیم نهایی ندارد.
- `SUPERSEDED`: تصمیم قدیمی که دیگر نباید مبنا باشد.

---

## DR-001 — اسناد قبلی canonical نیستند

**Status:** CONFIRMED

`docs/reference/software-requirements-specification.md` و `docs/reference/class-fields.md` اولیه‌اند و ممکن است بعداً کامل بازنویسی یا جایگزین شوند. بخش authority این تصمیم همچنان برقرار است؛ بند عدم-overwrite طبق DR-052 supersede شده است.

تصمیم:

- اصل اولیه این بود که overwrite نشوند و به‌عنوان Legacy/Source Material نگهداری شوند. **این بخش عملیاتی بعداً توسط DR-052 supersede شد:** برای رفع تناقض فعال، این فایل‌ها می‌توانند reconcile شوند، اما همچنان canonical نیستند.
- `docs/canonical/system-definition.md` و `docs/canonical/domain-model.md` منبع کاری جدید باشند.

---

## DR-002 — Feature Priority حذف شود

**Status:** CONFIRMED

ترتیب پیاده‌سازی در Roadmap/Incrementها مشخص می‌شود.

Priority فیلد Task/Event باقی می‌ماند؛ بحث فقط priority featureهای SRS است.

---

## DR-003 — Folder/List/Column terminology

**Status:** CONFIRMED

```text
Folder > List > Column
```

Tab و Section همان Column هستند و entity جدا نیستند.

---

## DR-004 — Routine status ندارد

**Status:** CONFIRMED

`status` از Item مشترک حذف می‌شود.

Task و Event status خودشان را دارند.

Routine نتیجه‌ی روزانه را در RoutineCompletion نگه می‌دارد.

---

## DR-005 — RoutineCompletion روز را با occurrence_date مشخص می‌کند

**Status:** CONFIRMED

تصمیم قبلی merge کردن date و completed_at کنار گذاشته شد.

مدل جدید:

```text
occurrence_date
status
amount
note
created_at
updated_at
version
```

`completed_at` business field حذف می‌شود.

---

## DR-006 — RoutineCompletion فقط یک row جاری در هر روز

**Status:** CONFIRMED

```text
UNIQUE(routine_id, occurrence_date)
```

Partial amount همان row update می‌شود.

---

## DR-007 — Reset RoutineCompletion

**Status:** CONFIRMED

Reset باعث حذف row جاری آن روز می‌شود.

AuditLog history را حفظ می‌کند.

Won't_Do با Reset یکسان نیست و باید row باقی بماند.

---

## DR-008 — historical routine edit آزاد است

**Status:** CONFIRMED

User می‌تواند هر روز گذشته را تغییر دهد.

آمار مرتبط باید اصلاح شود ولی full-history recomputation لازم نیست.

---

## DR-009 — Scheduled routine day محدودیت انجام نیست

**Status:** CONFIRMED

Recurrence تعیین می‌کند چه روزهایی Routine در نمای روزانه پیشنهاد شود.

User می‌تواند از صفحه‌ی Routine روی روز unscheduled نیز completion ثبت کند.

---

## DR-010 — extra routine completion missed day را جایگزین نمی‌کند

**Status:** CONFIRMED

برای fixed-day routine:

- missed scheduled day streak را می‌شکند.
- completion روز دیگر valid است و sequence جدید می‌سازد.
- جای occurrence از دست‌رفته را پر نمی‌کند.

برای `N times per period` semantics متفاوت است.

---

## DR-011 — Recurrence capability بر اساس entity

**Status:** CONFIRMED

```text
Task: minute/hour/day/week/month/year/advanced
Event: minute/hour/day/week/month/year/advanced
Routine: day/week/month/year
```

Recurrence engine/model می‌تواند shared باشد.

---

## DR-012 — Task lifecycle

**Status:** CONFIRMED

```text
Todo -> Overdue -> Missed -> Skipped
```

براساس due/deadline/grace.

Done و Won't_Do مسیرهای user-driven هستند.

---

## DR-013 — grace=0 مستقیماً Skipped

**Status:** CONFIRMED

اگر grace_period_days صفر باشد، Task هنگام عبور deadline مستقیماً Skipped می‌شود و Missed قابل مشاهده ندارد.

---

## DR-014 — ownership و source جدا هستند

**Status:** CONFIRMED

اضافه شود:

```text
owner_user_id
created_by_user_id
```

Source فقط provenance است.

---

## DR-015 — Source پیشنهادی

**Status:** CONFIRMED IN CONCEPT

```text
platform
external_account
external_id
```

Source نباید برای تعیین مالک داخلی استفاده شود.

---

## DR-016 — hierarchy مستقیم queryable است

**Status:** CONFIRMED

List UI باید بدون parse Description بتواند children را بگیرد.

parent/child relation باید indexable و queryable باشد.

---

## DR-017 — Task یک parent ساختاری دارد

**Status:** CONFIRMED

Task فقط زیر یک Item/Schedulable ساختاری قرار می‌گیرد.

می‌تواند به‌صورت reference در contextهای دیگری دیده شود فقط اگر UI/Domain بعداً اجازه دهد؛ structural parent واحد است.

---

## DR-018 — Event چند جا قابل ذکر است

**Status:** CONFIRMED

Event می‌تواند در چند Description reference شود.

**OPEN:** آیا چند structural parent هم مجاز است یا فقط یک parent واقعی + references متعدد.

---

## DR-019 — Child و Reference در UI نباید سیستم را پیچیده کنند

**Status:** CONFIRMED

Backend می‌تواند semantics را جدا نگه دارد ولی لازم نیست دو دکمه/دو workflow آشکار برای user ایجاد شود.

---

## DR-020 — Description capability است، schema نهایی نیست

**Status:** CONFIRMED

لیست text/attachment/location/task/event در Class_Fields قبلی فقط capabilities بودند.

ContentBlock model بعداً کامل طراحی می‌شود.

---

## DR-021 — ContentBlock identity لازم است

**Status:** CONFIRMED IN DESIGN DIRECTION

برای block comment، reorder و sync، block identity پایدار لازم خواهد بود.

field/schema exact هنوز OPEN است.

---

## DR-022 — Trackable inheritance نهایی نیست

**Status:** CONFIRMED

Trackable به‌عنوان capability/shared state بین Routine و Goal دیده می‌شود.

پیشنهاد فعلی:

```text
TrackingState
```

با composition؛ نه الزاماً table/class inheritance.

---

## DR-023 — Goal Item نیست

**Status:** CONFIRMED

Goal خارج از Item hierarchy است.

Routine Item است ولی Tracking capability نیز دارد.

---

## DR-024 — System Roles فقط در نسخه فعلی

**Status:** CONFIRMED

Custom Roles به فاز Enterprise منتقل شد.

تناقض قبلی SRS درباره custom role current scope superseded است.

---

## DR-025 — تعداد Goal محدود نیست

**Status:** CONFIRMED

User می‌تواند هر تعداد Goal شناسایی‌شده داشته باشد.

---

## DR-026 — Daily Ring count

**Status:** CONFIRMED

```text
eligible goals >= 3 => exactly 3 rings
eligible goals = 2 => 2 rings
eligible goals = 1 => 1 ring
```

عبارت قدیمی «3 تا 4 ring» superseded است.

---

## DR-027 — Goal.current_streak

**Status:** CONFIRMED

تعداد روزهای متوالی که Goal کامل شده است.

Activity کوچک کافی نیست؛ completion threshold باید کامل شود.

---

## DR-028 — Goal.total_completions

**Status:** CONFIRMED

تعداد کل روزهای کامل‌شدن Goal، بدون نیاز به توالی.

---

## DR-029 — progress و performance جدا هستند

**Status:** CONFIRMED

```text
progress_percent: 0..100
is_completed: Boolean
final_score: can exceed baseline
```

progress UI از 100 بالاتر نمی‌رود.

---

## DR-030 — Bonus تا پایان روز مخفی است

**Status:** CONFIRMED

User در طول روز نباید به دلیل early bonus احساس کند Goal را زودتر از حد کافی تمام کرده.

Bonus/final score بعد از daily finalization reveal می‌شود.

---

## DR-031 — Early completion reward

**Status:** CONFIRMED

انجام زودتر Item مهم باید final performance score بالاتری بدهد.

---

## DR-032 — Late-day recovery

**Status:** CONFIRMED IN PRODUCT BEHAVIOR

در انتهای روز انجام کارهای باقی‌مانده باید user را راحت‌تر به completion واقعی نزدیک کند تا انگیزه‌ی تمام‌کردن حفظ شود.

progress هرگز >100 نیست.

فرمول exact OPEN است.

---

## DR-033 — Item فقط Ring همان روز را جلو می‌برد

**Status:** CONFIRMED

اگر Item در DailyRingItemهای credited day نباشد، انجام آن هیچ Goal روزانه‌ای را جلو نمی‌برد.

---

## DR-034 — Daily Ring snapshot تاریخی است

**Status:** CONFIRMED

Task ممکن است روزهای مختلف دوباره وارد/خارج selection شود.

معنای Ring تاریخی با تغییر عادی future fields نباید بازنویسی شود.

---

## DR-035 — Dotick Day از Calendar Day جداست

**Status:** CONFIRMED

Day boundary user-configurable است.

---

## DR-036 — Default day ambiguity window

**Status:** CONFIRMED

اگر user boundary صریح نداشته باشد:

- default = 1 hour after midnight.
- completion داخل window با سؤال Today/Yesterday attribution می‌گیرد.

---

## DR-037 — New Rings after boundary

**Status:** CONFIRMED

بعد از بسته‌شدن previous Dotick Day:

- score finalize
- bonus reveal
- streak finalize
- Ringهای روز جدید generate

---

## DR-038 — Selective statistics recomputation

**Status:** CONFIRMED

تغییر historical data فقط metric/windowهای affected را update می‌کند.

Full recomputation default نیست.

---

## DR-039 — AI item creation عمومی‌تر از Speech-to-Task است

**Status:** CONFIRMED

Feature باید Text/Voice و در آینده Email/External sources را به یک draft creation pipeline وصل کند.

---

## DR-040 — Voice input کنار create box

**Status:** CONFIRMED

هرجایی که user Item می‌سازد، microphone می‌تواند input voice ارائه کند.

---

## DR-041 — AI باید فیلدها را infer کند

**Status:** CONFIRMED

حداقل:

- Task/Event type
- title
- time/date
- location
- description
- Folder/List/Column
- reminders
- سایر fieldهای قابل استنتاج

---

## DR-042 — AI draft نیاز به review دارد

**Status:** CONFIRMED

AI proposal در popup/review نمایش داده می‌شود.

User می‌تواند همه‌ی جزئیات را تغییر دهد.

Item واقعی فقط بعد از Confirm ساخته می‌شود.

---

## DR-043 — AI correction learning

**Status:** CONFIRMED AS FUTURE CAPABILITY

سیستم در آینده باید بتواند proposal و user final payload را مقایسه کند تا preference user را یاد بگیرد.

مثال: reminder preference برای restaurant/social events.

---

## DR-044 — Email/Integration vision

**Status:** CONFIRMED

سیستم در آینده به Email و منابع دیگر وصل می‌شود تا creation/automation ممکن شود.

---

## DR-045 — Goal selection quality

**Status:** CONFIRMED IN INTENT

سه Goal روز باید balanced باشند، مثلاً:

- current/important work
- neglected area
- growth/learning

این سه category hard-coded نیستند؛ quality target هستند.

---

## DR-046 — Goal selection inputs

**Status:** RETAINED + EXTENDED

معیارها:

- due/timing
- priority
- neglect
- weekday behavior
- holiday context
- streak momentum
- workload
- difficulty
- recent user capacity

فرمول exact OPEN.

---

## DR-047 — Goal/Tag lifecycle

**Status:** RETAINED

Goal مستقل، Tag مستقل، Goal Active/Dormant/Archived و AI tag lifecycle از مدل قبلی حفظ می‌شوند.

---

## DR-048 — GoalGenerationLog

**Status:** RETAINED

AI model/version/change history append-only حفظ می‌شود.

---

## DR-049 — Offline sync

**Status:** RETAINED

Field-level sync و Last-Write-Wins baseline فعلی باقی می‌ماند تا Sync Design formalize شود.

---

## DR-050 — Authentication

**Status:** RETAINED

Email/password، Google OAuth، JWT، Passkey.

Enterprise SSO future.

---

## DR-051 — Global daily streak

**Status:** OPEN / RETAINED FROM LEGACY

SRS قبلی global streak را با complete شدن حداقل یک Ring تعریف کرده بود.

Latest discussion فقط Goal streak را دقیق کرد.

Global streak باید دوباره تأیید یا حذف شود.

---

## DR-052 — Reconciliation of legacy reference documents

**Status:** CONFIRMED

برای جلوگیری از تناقض فعال بین فایل‌های پروژه، `docs/reference/software-requirements-specification.md` و `docs/reference/class-fields.md` می‌توانند در passهای consistency به‌روزرسانی شوند تا با تصمیم‌های canonical فعلی تضاد مستقیم نداشته باشند.

این تصمیم فقط بخش «overwrite نشوند» از DR-001 را supersede می‌کند؛ ترتیب authority تغییر نمی‌کند:

```text
Confirmed Decision Register entry
        ↓
System Definition
        ↓
Domain Model
        ↓
Derived SRS / reference documents
        ↓
Historical legacy wording
```

بنابراین:

- `docs/reference/software-requirements-specification.md` در 2026-08-17 به Formal SRS Baseline v2.0 تبدیل شد؛ همچنان پایین‌تر از منابع canonical قرار دارد.
- `docs/reference/class-fields.md` یک **derived field reference** است، نه physical database schema و نه منبع تصمیم معماری.
- تصمیم‌های `OPEN` نباید برای یکدست‌کردن اسناد به‌صورت ضمنی بسته شوند؛ wording قدیمی باید به `OPEN` یا wording خنثی تبدیل شود.
- متن تاریخی مهم می‌تواند در revision history باقی بماند، ولی requirement/field جاری نباید تصمیم superseded را به‌عنوان رفتار فعلی بیان کند.

---

## DR-053 — Increment 0 technology and architecture baseline

**Status:** CONFIRMED

برای Walking Skeleton و Personal V1، baseline فنی زیر انتخاب شد:

- معماری backend یک **modular monolith** با boundaryهای صریح domain/application/interface/infrastructure است.
- backend با Python 3.14، Django 5.2 LTS و Django REST Framework ساخته می‌شود؛ dependency management با `uv` و lockfile است.
- frontend یک application مستقل TypeScript بر پایه Expo SDK 57، React Native و React Native for Web است؛ Node.js 24 LTS و npm workspace baseline ابزار آن هستند.
- persistence اصلی PostgreSQL است.
- HTTP/JSON/REST مسیر authoritative برای command و query است؛ WebSocket فقط notification و invalidation سبک را حمل می‌کند.
- dependencyها در زمان scaffold با lockfile ثبت می‌شوند و فقط نسخه‌های پشتیبانی‌شده انتخاب می‌شوند.
- Redis، worker queue، Channels و سرویس‌های AI تا Increment مالکشان dependency اجباری نیستند.

این انتخاب با سابقه‌ی پروژه هم‌راستاست، اما دلیل اعتبار آن اسناد canonical و baseline مهندسی فعلی است، نه کد archiveشده.

جزئیات و trade-offها در `docs/adr/0001-modular-monolith-and-technology-stack.md` ثبت شده‌اند.

---

## DR-054 — Explicit composition for Item persistence

**Status:** CONFIRMED

OPEN مربوط به storage inheritance برای baseline Personal V1 به این شکل بسته شد:

- table پایه‌ی `items` فقط identity، ownership و metadata واقعاً مشترک را نگه می‌دارد.
- هر subtype در table صریح یک‌به‌یک خود نگه‌داری می‌شود؛ برای مثال `tasks.item_id` هم primary key و هم foreign key به `items.id` است.
- implementation به ORM/model inheritance متکی نیست؛ relationها و transaction boundaryها صریح‌اند.
- capabilityهایی مانند Source، recurrence، reminder و tracking به‌صورت component/relation مستقل و فقط هنگام نیاز Increment اضافه می‌شوند.
- denormalization پیش‌فرض نیست و فقط پس از اندازه‌گیری، با migration و ADR جدا مجاز است.

این تصمیم query مشترک Item و integrity نوع را حفظ می‌کند، بدون آنکه Domain inheritance را مکانیکی به Class Table Inheritance تبدیل کند. جزئیات در `docs/DATA_DESIGN.md` و `docs/adr/0002-explicit-item-composition-storage.md` آمده‌اند.

# Decision backlog and resolution status

1. Event multi-parent structural support.
2. Description/ContentBlock exact schema.
3. backend relation schema child/reference.
4. exact scoring formula.
5. difficulty/effort model.
6. global daily streak.
7. frequency routine streak formalization.
8. incremental routine inactivity reset.
9. AI Goal warm-up duration.
10. Goal similarity thresholds.
11. exact Goal selection algorithm.
12. ~~database inheritance/storage strategy~~ — resolved by DR-054 for the Personal V1 baseline.
13. API endpoint design.
14. sync metadata design.
15. trusted automation confirmation policy.

