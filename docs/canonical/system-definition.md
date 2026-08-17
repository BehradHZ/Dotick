# Dotick — System Definition Specification

> **وضعیت سند:** Canonical Working Specification  
> **هدف:** ثبت دقیق فهم فعلی از محصول، رفتار سیستم، قواعد دامنه، محدودیت‌ها و تصمیم‌های نهایی‌شده؛ Formal SRS و Design Documents از این منبع مشتق می‌شوند.
> **منابع پایه:** `docs/reference/software-requirements-specification.md` و `docs/reference/class-fields.md` قبلی + تصمیم‌های جدید این گفت‌وگو.  
> **قاعده‌ی حاکم:** هرجا این سند با نسخه‌های قبلی تعارض دارد، این سند مرجع فعلی است. مواردی که هنوز نهایی نشده‌اند صریحاً با `OPEN` علامت‌گذاری شده‌اند.

---

## 0. جایگاه این سند و اسناد قبلی

نسخه‌های اولیه‌ی `docs/reference/software-requirements-specification.md` و `docs/reference/class-fields.md` برای شکل‌دادن دامنه و جمع‌آوری ایده‌ها مفید بوده‌اند، اما چند نقش را هم‌زمان مخلوط می‌کردند: requirement، domain model، design proposal، implementation note و تصمیم‌های هنوز باز. طبق DR-052، این دو فایل اکنون می‌توانند برای حذف تناقض‌های فعال **reconcile** شوند، اما همچنان **canonical نیستند**.

در وضعیت فعلی:

1. `docs/reference/software-requirements-specification.md` اکنون **Formal SRS Baseline v2.0** است؛ requirement رسمی را نگه می‌دارد ولی در تعارض رفتاری پایین‌تر از منابع canonical است.
2. `docs/reference/class-fields.md` یک **derived field reference** است و physical database schema یا storage-inheritance decision نیست.
3. این سند، تعریف فعلی «سیستم چیست و چه رفتاری دارد» را نگه می‌دارد.
4. فایل `docs/canonical/domain-model.md` مدل مفهومی و فیلدهای فعلی را جداگانه نگه می‌دارد.
5. فایل `docs/canonical/decision-register.md` تصمیم‌های تثبیت‌شده، superseded و موارد باز را ثبت می‌کند.
6. سایر اسناد مهندسی مثل ERD، API Contract و specهای تخصصی طبق Roadmap و در Increment مالک خود ساخته/تکمیل می‌شوند.

---

# 1. چشم‌انداز محصول

Dotick یک سیستم مدیریت کار، رویداد و روتین برای استفاده‌ی جدی روزمره است که علاوه بر قابلیت‌های کلاسیک مدیریت کار، یک لایه‌ی انگیزشی و تحلیلی دارد.

اهداف اصلی محصول:

- مدیریت روزانه‌ی Task، Event و Routine.
- امکان برنامه‌ریزی پروژه‌محور و روزانه‌محور در کنار هم.
- استفاده‌ی شخصی واقعی توسط توسعه‌دهنده در فاز اول.
- تمرین کامل مهندسی نرم‌افزار از تحلیل تا استقرار.
- ساخت معماری‌ای که در آینده بتواند به نسخه‌ی تیمی/سازمانی و محصول تجاری گسترش یابد.
- ارائه‌ی انگیزش بصری و measurable progress بدون تبدیل شدن به یک بازی فانتزی مستقل.
- استفاده از AI به‌عنوان **پیشنهاددهنده و تحلیل‌گر**، نه به‌عنوان مرجع نهایی تصمیم کاربر.

فلسفه‌ی گیمیفیکیشن با رویکرد «هر حرکت کوچکی کافی است» یکسان نیست. برای اینکه یک Goal واقعاً complete شود، کاربر باید **مقدار معناداری از کار مرتبط با آن هدف** را پیش ببرد.

## 1.1 کلاس‌های کاربری شناخته‌شده

- **کاربر شخصی:** کاربر اصلی فاز فعلی و استفاده‌ی روزانه‌ی جدی.
- **اعضای گروه دوستانه/تیمی:** کاربران دارای Task/Group مشترک.
- **کاربر سازمانی:** فاز آینده؛ نیازمند access control و multi-tenancy کامل‌تر.
- **همکار تحلیل داده/مدل:** فاز آینده؛ نیازمند domain و analytics documentation روشن.

---

# 2. اصول طراحی محصول

## 2.1 سادگی تجربه‌ی کاربر

پیچیدگی مدل داده نباید الزاماً در UI دیده شود. اگر backend برای صحت و performance به دو نوع relation یا metadata نیاز دارد، تا زمانی که برای کاربر ارزش مستقیم ندارد، UI نباید دو دکمه یا دو workflow جدا ایجاد کند.

نمونه‌ی مهم:

- یک Task/Event می‌تواند داخل Description دیده شود.
- backend می‌تواند بداند این نمایش «رابطه‌ی child» است یا صرفاً reference.
- کاربر لزوماً نباید دو کنترل جداگانه‌ی پیچیده ببیند.

## 2.2 Source of Truth در برابر Derived Data

داده‌هایی مثل Completion، Task status، Relation و Daily Ring snapshot باید source of truth مشخص داشته باشند. آمار، streak aggregate، behavior features و dashboard metrics می‌توانند داده‌ی مشتق‌شده باشند و به‌صورت selective recalculation به‌روزرسانی شوند.

## 2.3 Snapshot برای رفتار روزانه

Daily Ringها و آیتم‌های انتخاب‌شده‌ی هر روز باید snapshot شوند؛ تغییر priority یا فیلدهای یک Task در روزهای بعد نباید معنای تاریخی Ring قبلی را بی‌دلیل تغییر دهد.

## 2.4 AI پیشنهاد می‌دهد؛ کاربر نهایی می‌کند

برای ایجاد Item با AI، مدل draft تولید می‌کند. قبل از ایجاد رکورد واقعی، کاربر تمام جزئیات را در یک Review/Popup می‌بیند و می‌تواند تغییر دهد. ایجاد نهایی فقط پس از تأیید کاربر انجام می‌شود، مگر در آینده automationهای trusted به‌طور جداگانه تعریف شوند.

---

# 3. سازمان‌دهی اطلاعات در UI

ساختار سازمانی اصلی:

```text
Folder
└── List
    └── Column
```

اصطلاحات قدیمی `Tab` و `Section` در مدل فعلی به همان **Column** اشاره می‌کنند و entity جدا نیستند.

## 3.1 Viewها

داده‌ی یکسان می‌تواند با presentationهای مختلف دیده شود؛ تغییر View نباید داده‌ی زیرین را تغییر دهد.

Viewهای شناخته‌شده:

- List
- Kanban
- Timeline
- Calendar
- Routine page
- Eisenhower / Priority Matrix

نمای اصلی برنامه باید بتواند Folderها، Listها و فیلترهای روزانه را در دسترس قرار دهد.

## 3.2 Inbox

یک List/Location پیش‌فرض برای آیتم‌هایی که کاربر محل مشخصی برای آن‌ها انتخاب نکرده لازم است. نام فعلی این مفهوم `Inbox` است.

هر List باید یک Column پیش‌فرض برای Itemهای بدون Column صریح داشته باشد. نام legacy این مفهوم `not_sectioned` بوده است. اگر تنها Column همان Column پیش‌فرض باشد، لازم نیست نام فنی آن در UI به user نمایش داده شود.

---

# 4. مدل سطح‌بالای Itemها

سه نوع اصلی user-facing content:

- Task
- Event
- Routine

Task و Event زمان‌بندی نقطه‌ای/بازه‌ای مشابهی دارند و در مفهوم `Schedulable` مشترک‌اند.

Routine مدل متفاوتی دارد و یک «تعریف تکرارشونده» است؛ نتیجه‌ی هر روز در رکورد جداگانه‌ی RoutineCompletion ثبت می‌شود.

مدل مفهومی فعلی:

```text
Item
├── Schedulable
│   ├── Task
│   └── Event
└── Routine

Tracking capability
├── Routine
└── Goal
```

`Goal` یک Item نیست.

`Trackable` در این مرحله **capability/shared state** است، نه الزاماً یک superclass یا table دیتابیسی.

---

# 5. Ownership، Creator و Source

مالکیت و منبع ایجاد از هم جدا هستند.

برای Itemهایی که نیاز دارند:

- `owner_user_id`: کاربری که Item متعلق به اوست.
- `created_by_user_id`: کاربری که Item را ایجاد کرده است.

`source` فقط provenance را بیان می‌کند، نه ownership.

نمونه‌ی source:

```text
platform: Manual | Google_Calendar | Email | Notion | TickTick | ...
external_account: optional
external_id: optional
```

مثلاً ممکن است Item متعلق به Bahram باشد ولی از Google Calendar خاصی import شده باشد، یا فرد دیگری در گروه آن را برای Bahram ساخته باشد.

---

# 6. Task

## 6.1 رفتار اصلی

Task یک Schedulable است و می‌تواند نقطه‌ای، all-day یا بازه‌ای باشد. اگر جزء ساعت تعیین نشده باشد، Item به‌صورت all-day تفسیر می‌شود. اگر `end_at` وجود نداشته باشد `due_at` یک لحظه/موعد واحد است؛ اگر `end_at` وجود داشته باشد `due_at` شروع duration است.

فیلدهای زمانی مفهومی:

- `due_at`: لحظه‌ی due یا شروع بازه.
- `end_at`: در صورت وجود، Task duration دارد.
- `deadline_at`: deadline جدا از due.
- `grace_period_days`: فاصله‌ی deadline تا auto-skip.

## 6.2 State machine

رفتار قطعی‌شده:

```text
قبل از due_at                     => Todo
عبور از due_at                    => Overdue
عبور از deadline_at               => Missed
عبور از deadline + grace_period   => Skipped
```

Statusهای دستی/نتیجه‌ای:

- Done
- Won't_Do

`Skipped` مستقیماً توسط کاربر انتخاب نمی‌شود.

### grace_period_days = 0

تصمیم نهایی:

اگر `grace_period_days = 0` باشد، Task در زمان عبور از deadline **مستقیماً به Skipped می‌رود** و وارد state قابل مشاهده‌ی `Missed` نمی‌شود.

## 6.3 Dependency

Task می‌تواند توسط Taskهای دیگر blocked شود.

مفهوم فعلی:

```text
dependencies.blocked_by_ids
```

## 6.4 Priority

Priority همچنان یک property خود Task/Event است و در ranking و Ring scoring استفاده می‌شود.

مقادیر فعلی:

- Urgent_Important
- Important
- Urgent
- None

اما **Feature Priority در سند نیازمندی‌ها حذف می‌شود** و ترتیب ساخت featureها در Roadmap/Incrementها مشخص خواهد شد.

---

# 7. Event

Event یک Schedulable با زمان شروع/پایان، location و description مستقل است. اگر زمان دقیق وجود نداشته باشد می‌تواند all-day باشد. `location` باید بتواند آدرس قابل بازکردن در navigation، مختصات یا virtual meeting link را نمایش دهد.

Statusهای فعلی:

- Not_Arrived
- Ongoing
- Finished

Event می‌تواند sub-event داشته باشد.

نمونه:

```text
نمایشگاه اصلی
├── افتتاحیه غرفه A — زمان/لوکیشن/توضیح مستقل
├── افتتاحیه غرفه B — زمان/لوکیشن/توضیح مستقل
├── افتتاحیه غرفه C
└── ...
```

همچنین یک Event می‌تواند در Descriptionهای دیگر **ذکر/نمایش** شود.

### OPEN — multiplicity ساختاری Event

قطعی است که Event می‌تواند چند جا reference شود. هنوز باید در Design نهایی مشخص شود آیا Event از نظر **parent ساختاری** فقط یک parent دارد یا می‌تواند چند parent ساختاری داشته باشد. برای سادگی، مدل یک parent ساختاری + چند reference گزینه‌ی ترجیحی فعلی است، اما این تصمیم هنوز نهایی نشده است.

---

# 8. Hierarchy و Sub-itemها

## 8.1 نیاز UI

در List ساده، کاربر باید بدون باز کردن Description بتواند ساختار childها را ببیند؛ مثل:

```text
Task اصلی
    Subtask 1
        Subtask 1.1
    Subtask 2
```

پس query کردن hierarchy **نباید نیازمند parse کل RichText/Description باشد**.

## 8.2 Relation مستقیم

وجود relation مستقیم parent/child در storage ضروری است.

برای Task تصمیم فعلی:

- Task فقط زیر یک item ساختاری قرار می‌گیرد.
- parent relation باید مستقیم و indexable باشد.

Task/Event هر دو می‌توانند داخل Description نمایش داده شوند، ولی UI نمایش Description جایگزین relation queryable نیست.

## 8.3 Child در برابر Reference

سیستم داخلی باید بتواند تفاوت این دو مفهوم را بفهمد:

1. **Child relation**: hierarchy واقعی.
2. **Reference**: فقط نمایش/لینک به Item در Description دیگر.

اما این تفکیک **نباید الزاماً به دو دکمه یا workflow کاربری جدا تبدیل شود**. هدف، ساده نگه‌داشتن UI است.

### قاعده‌ی طراحی

در backend metadata یا relation مناسب نگهداری می‌شود؛ frontend می‌تواند از یک interaction واحد برای insert/mention استفاده کند و context تعیین کند که relation ساختاری است یا reference.

---

# 9. Description و Content Blocks

Description فعلی هنوز schema نهایی ندارد. مواردی که تاکنون نوشته شده‌اند **capabilityهای مورد پشتیبانی** هستند، نه فهرست نهایی فیلدها.

Description باید block-based باشد و حداقل بتواند این انواع content را پشتیبانی کند:

- Text
  - Bold
  - Italic
  - Underline
  - Strikethrough
  - Heading
  - Highlight
  - Bullets/Numbers
  - Indent
  - Separator
  - Code
  - Quote
  - link/phone/id recognition
- Attachment
- Location
- Task/Event embedded reference

برای پشتیبانی پایدار از comment روی block، reorder و edit، هر ContentBlock در مدل نهایی باید identity پایدار داشته باشد؛ schema دقیق بعداً طراحی می‌شود.

## 9.1 Comments

نیاز فعلی حفظ می‌شود:

- Task/Event یک comment thread مستقل دارند.
- کاربران مجاز می‌توانند روی یک block خاص comment بگذارند.
- block comment باید هم کنار block و هم در نمای کلی commentها قابل مشاهده باشد.

---

# 10. Routine

## 10.1 Routine یک تعریف واحد است

Routine به‌ازای هر روز یک row مستقل در جدول Routine ندارد.

یک Routine شامل تعریف کلی است:

- title
- validity window
- recurrence
- target definition
- tags
- reminders
- tracking state

نتیجه‌ی هر روز در `RoutineCompletion` ذخیره می‌شود.

## 10.2 Validity Window

- `start_date`: شروع اعتبار تعریف Routine؛ در صورت خالی بودن از created date استفاده می‌شود.
- `end_date`: پایان اعتبار؛ در صورت خالی بودن، Routine ادامه‌دار است.

این فیلدها زمان اجرای روزانه نیستند؛ فقط محدوده‌ای هستند که recurrence در آن معتبر است.

## 10.3 Routine status ندارد

Routine خود `status` ندارد.

Outcome روزانه در `RoutineCompletion.status` ذخیره می‌شود.

Statusهای فعلی RoutineCompletion:

- Done
- Won't_Do

نبود رکورد برای یک روز یعنی هیچ outcome ثبت‌شده‌ای برای آن روز وجود ندارد.

## 10.4 RoutineCompletion

مفهوم اصلی روز با `occurrence_date` ذخیره می‌شود.

`completed_at` به‌عنوان business field فعلاً لازم نیست.

اطلاعات زمان ثبت/ویرایش از `created_at`، `updated_at` و AuditLog در دسترس خواهد بود.

مدل مفهومی:

```text
RoutineCompletion
- id
- routine_id
- occurrence_date
- status
- amount
- note
- created_at
- updated_at
- version
```

Constraint مطلوب:

```text
UNIQUE(routine_id, occurrence_date)
```

در هر روز حداکثر یک وضعیت جاری برای یک Routine وجود دارد.

## 10.5 Reset

اگر user completion یک روز را Reset کند:

- رکورد RoutineCompletion جاری آن روز حذف می‌شود.
- AuditLog تغییر را حفظ می‌کند.

این رفتار در روز scheduled و unscheduled قابل استفاده است.

`Won't_Do` با Reset فرق دارد؛ Won't_Do یک تصمیم صریح است و رکورد باید باقی بماند.

## 10.6 روزهای مجاز و غیرمجاز

Recurrence تعیین می‌کند Routine در چه روزهایی **پیشنهاد/نمایش داده شود**؛ این recurrence محدودیت مطلق برای انجام Routine نیست.

### صفحه‌ی اصلی Routineها

صفحه‌ی اصلی Routine روزهای همین هفته را نشان می‌دهد.

وقتی user یک روز را انتخاب می‌کند:

- فقط Routineهایی که برای آن روز scheduled هستند به‌صورت پیشنهاد اصلی نمایش داده می‌شوند.
- اگر user در همان هفته یک Routine را در روز unscheduled دستی انجام داده باشد، completion انجام‌شده‌ی آن روز نیز در نمای مربوطه قابل مشاهده است.

### صفحه‌ی اختصاصی یک Routine

تقویم کامل Routine نمایش داده می‌شود.

User می‌تواند در روزی که recurrence آن Routine را schedule نکرده نیز یک completion ثبت کند.

این completion معتبر است و در آمار Routine اثر دارد.

اگر Reset شود، row حذف می‌شود ولی AuditLog باقی می‌ماند.

## 10.7 Target Goal روتین

مدل قبلی حفظ می‌شود مگر بعداً بازطراحی شود:

- Achieve_All
- Partial

Partial می‌تواند metric داشته باشد:

- period
- fix_amount
- unit
- is_incremental
- increment_amount

برای incremental routine، target جاری جداگانه ذخیره نمی‌شود و از state قبلی مشتق می‌شود.

### OPEN

رفتار reset شدن target incremental پس از inactivity طولانی هنوز نهایی نشده است.

---

# 11. Routine Recurrence و Streak

## 11.1 Recurrence capability

تمام recurrenceها باید نسبت به یکی از دو calendar system محاسبه شوند:

- Jalali
- Gregorian

Task:

- minute
- hour
- day
- week
- month
- year
- advanced

Event:

- minute
- hour
- day
- week
- month
- year
- advanced

Routine:

- day
- week
- month
- year

Routine day-level است و minute/hour recurrence ندارد.

### Recurrence modes retained

**Constant:** Daily / Weekly / Monthly / Yearly.

**Interval/Dynamic:**

- هر `x` دقیقه
- هر `x` ساعت
- هر `x` روز
- هر `x` هفته روی weekdayهای انتخابی
- هر `x` ماه روی dayهای انتخابی یا `last_day`
- هر `x` سال روی ماه/روز انتخابی

**Advanced:** ترکیب هم‌زمان day/hour/minute، مثل «هر 2 روز و 4 ساعت و 30 دقیقه».

برای Routine فقط subset روزمحور این engine مجاز است.

## 11.2 Fixed-Day Routine

برای Routineهایی که occurrenceهای مشخص دارند، streak بر اساس sequence فرصت‌های scheduled و completionهای واقعی محاسبه می‌شود.

مثال:

```text
Routine: Monday / Wednesday / Friday
Monday     Done
Wednesday  Done
Friday     Done
=> streak = 3
```

اگر یک scheduled occurrence از دست برود:

```text
Monday     missed
=> streak breaks
Tuesday    manual extra Done
=> streak = 1
Wednesday  scheduled Done
=> streak = 2
```

انجام یک روز غیرمجاز **جای occurrence از دست‌رفته را پر نمی‌کند**، ولی خودش یک completion معتبر است و می‌تواند sequence جدیدی بسازد.

## 11.3 Frequency Routine

اگر تعریف Routine از نوع «N بار در یک period» باشد، semantics با fixed-day فرق می‌کند.

مثلاً:

```text
3 times per week
```

انجام Monday، Tuesday و Saturday می‌تواند requirement هفته را کامل کند و نیازی به روزهای ثابت ندارد.

جزئیات دقیق streak در frequency-based routines باید هنگام طراحی recurrence model نهایی formalize شود.

---

# 12. Reminders

Task/Event/Routine می‌توانند reminder داشته باشند.

capability فعلی:

- چند reminder برای یک Item
- trigger-before
- persistent/alarm-like notification در صورت پشتیبانی platform

AI می‌تواند reminder مناسب پیشنهاد کند، ولی پیشنهاد باید قبل از ثبت Item در Review UI قابل مشاهده و اصلاح باشد.

---

# 13. Goal

Goal یک entity مستقل است، نه فقط یک string/tag.

Goal نشان‌دهنده‌ی یک مسیر یا objective معنایی در کارهای user است.

نمونه:

- موفقیت دانشگاهی
- فعالیت هنری و فرهنگی
- یادگیری مهارت
- سلامت

Goal توسط سیستم بر اساس List/Column و محتوای واقعی Itemها شناسایی می‌شود.

## 13.1 Goal lifecycle

وضعیت‌های فعلی:

- Active
- Dormant
- Archived

### Dormant

وقتی Goal فعلاً آیتم فعال معناداری ندارد:

- از Daily Ring selection خارج می‌شود.
- streak آن reset نمی‌شود؛ freeze می‌شود.
- در صورت ورود محتوای جدید می‌تواند دوباره بررسی و reactivated شود.

### Archived

Goal تاریخی حفظ می‌شود ولی به‌صورت خودکار Active نمی‌شود.

## 13.2 Goal tracking

تعریف نهایی‌شده:

- `Goal.current_streak`: تعداد روزهای متوالی که Goal آن روز **واقعاً کامل شده است**.
- `Goal.total_completions`: تعداد کل روزهایی که Goal کامل شده است، بدون شرط توالی.

یک فعالیت کوچک به‌تنهایی streak را حفظ نمی‌کند. Goal زمانی complete است که progress آن روز به threshold کامل برسد.

## 13.3 Goal-level reminder

سیستم می‌تواند مستقل از reminderهای تک‌تک Task/Routine، بر اساس افت عملکرد user نسبت به Norm یک Goal، reminder انگیزشی برای همان Goal ارسال کند. زمان‌بندی و frequency دقیق این reminder در Gamification Specification تعیین می‌شود.

---

# 14. Tag و ارتباط Goal

Tag یک entity مستقل است.

Sourceهای فعلی:

- User
- AI

رابطه‌ی Goal به Itemها از طریق Tag می‌تواند برقرار شود.

Tagهای user-created به‌صورت خودکار حذف/آرشیو نمی‌شوند.

Tagهای AI می‌توانند در بازبینی‌های معنایی merge/archive شوند.

یک Goal می‌تواند چند Tag داشته باشد.

---

# 15. AI Goal Discovery

رفتارهای قبلی حفظ می‌شوند مگر اینکه در تحلیل بعدی تغییر کنند:

## 15.1 Initial warm-up

بعد از دوره‌ی warm-up اولیه، سیستم مجموعه‌ی Listها، Columnها و Itemهای مرتبط را برای semantic analysis بررسی می‌کند.

AI باید از محتوای واقعی استفاده کند، نه صرفاً نام List/Column. نام List/Column می‌تواند signal و پیشنهاد title باشد، ولی معیار یگانه نیست.

واحد شناسایی Goal می‌تواند List یا Column coherent باشد. در کوچک‌ترین حالت، هر Goal از یک Column منسجم به‌دست می‌آید. تعداد Goalهای قابل استخراج از یک List نمی‌تواند بیش از تعداد Columnهای معنادار آن باشد، مگر Domain Review بعدی این قاعده را تغییر دهد.

اگر یک Column/مجموعه واقعاً coherent نباشد، نباید به زور Goal تولید شود.

فرآیند initial tagging retained از مدل قبلی:

1. پس از warm-up، Listها/Columnها و Itemهایشان به مدل داده می‌شوند.
2. AI مجموعه‌ی Tagهای اولیه را پیشنهاد می‌کند و Tagهای دستی user نیز برای جلوگیری از duplicate/similar tag در context قرار می‌گیرند.
3. مدل Itemها را دوباره بررسی و Tagهای مناسب را assign می‌کند.
4. Goalها بر اساس clustering/semantic structure و Tagهای نتیجه ساخته یا مرتبط می‌شوند.

## 15.2 Reactive review

برای محتوای جدید یا Goal Dormant، بررسی هدف می‌تواند با تأخیر کنترل‌شده انجام شود تا داده‌ی کافی جمع شود و ایجاد Task به AI وابسته نشود.

مقدار فعلی retained از سند قبلی: 12 ساعت.

## 15.3 Weekly review

یک بازبینی سراسری کم‌تکرار برای:

- merge هدف‌های بسیار مشابه
- archive/cleanup AI tags
- به‌روزرسانی کلی semantic model

مقدار فعلی retained: weekly.

## 15.4 GoalGenerationLog

هر تغییر واقعی AI روی title/description یک Goal باید قابل ردگیری باشد.

Log append-only فعلی شامل:

- goal_id
- event_type
- ai_model_used
- changed
- previous/new title
- previous/new description
- user_rating در صورت تغییر واقعی
- created_at

---

# 16. Daily Rings

Daily Ring نمای روزانه‌ی Goal است؛ خود Goal محدود به یک روز نیست.

## 16.1 تعداد Goalها و Ringها

تعداد Goalهای user محدودیت ثابت ندارد.

اگر تعداد Goalهای active و eligible حداقل 3 باشد:

- **دقیقاً 3 Daily Ring** انتخاب می‌شود.

اگر تعداد Goalهای active و eligible کمتر از 3 باشد:

- به اندازه‌ی Goalهای موجود Ring ساخته می‌شود.

مثال:

```text
1 Goal  => 1 Ring
2 Goals => 2 Rings
8 Goals => exactly 3 Rings
```

## 16.2 کیفیت ترکیب سه Goal

سیستم باید ترکیب روز را balanced کند.

نمونه‌ی desired outcome، بدون hard-code الزاماً ثابت:

- یک Goal مرتبط با کارهای جاری/ضروری امروز
- یک Goal از حوزه‌ای که مدتی neglected بوده
- یک Goal رشد/learning یا کارهای با urgency پایین‌تر ولی ارزش بلندمدت

این دسته‌ها guideline کیفیت هستند، نه سه enum اجباری.

## 16.3 معیارهای انتخاب Goal

انتخاب باید حداقل این اطلاعات را در نظر بگیرد:

- due/زمان نزدیک Itemها
- priority
- مدت زمان از آخرین فعالیت معنادار Goal
- weekday behavior
- تعطیلات/تقویم کاربر
- streak momentum
- workload همان روز
- difficulty/effort تخمینی
- عملکرد و ظرفیت واقعی user در روزهای اخیر
- پرهیز از انتخاب Goal صرفاً به دلیل backlog زیاد

وزن‌ها باید در آینده قابلیت یادگیری از رفتار user را داشته باشند.

### Baseline scoring signals retained

در اسناد قبلی یک baseline اولیه برای priority وجود داشت:

- Urgent_Important ≈ 2.0
- Important ≈ 1.5
- Urgent ≈ 1.2
- None ≈ 1.0
- Routine که priority ندارد، priority weight آن 1 است.

این اعداد **فرمول نهایی نیستند**؛ چون مدل جدید difficulty، user capacity، early completion و progress/final-score separation را نیز در نظر می‌گیرد. این مقادیر صرفاً baseline retained برای تست و مقایسه در طراحی scoring هستند.

Timeliness نیز باید نسبت به due/duration/deadline اثر داشته باشد؛ exact coefficient و نحوه‌ی ترکیب با early bonus هنوز OPEN است.

## 16.4 DailyRing snapshot

برای هر Ring روزانه باید snapshotی از تصمیم همان روز وجود داشته باشد.

مفهوم پیشنهادی:

```text
DailyRing
- user_id
- effective_date
- goal_id
- target_score / target definition
- progress_percent
- is_completed
- final_score
- is_finalized
- algorithm/model version metadata
```

و اعضای روزانه:

```text
DailyRingItem
- daily_ring_id
- item reference
- item type
- snapshot weights/features
```

جزئیات schema در Domain Model آمده است.

---

# 17. Progress، Completion و Performance Score

سه مفهوم باید جدا باشند:

## 17.1 progress_percent

- چیزی است که user در طول روز می‌بیند.
- بین 0 تا 100 است.
- هرگز بالاتر از 100 نمایش داده نمی‌شود.

## 17.2 is_completed

Boolean است و نشان می‌دهد user به مقدار کافی برای کامل شدن Goal رسیده یا نه.

```text
is_completed = progress_percent >= 100
```

این flag مبنای Goal streak/completion است.

## 17.3 final/performance score

امتیاز واقعی عملکرد می‌تواند بالاتر از baseline باشد.

موارد مؤثر:

- اهمیت Item
- urgency/priority
- زمان انجام نسبت به زمان مطلوب
- early completion
- difficulty/effort
- completion quality

بنابراین ممکن است:

```text
progress_percent = 100
final_score = 137
```

## 17.4 Bonus visibility

امتیاز اضافه/Bonus نباید در طول روز باعث شود user زود احساس کند «کار کافی انجام داده».

در طول روز user عمدتاً progress باقی‌مانده را می‌بیند.

بعد از بسته‌شدن روز:

- score نهایی finalize می‌شود.
- bonusها reveal می‌شوند.

## 17.5 Early vs late completion

هدف رفتاری سیستم:

- انجام زودتر Item مهم باید reward بیشتری داشته باشد.
- در ساعات پایانی روز، انجام Itemهای باقی‌مانده همچنان باید user را واقع‌بینانه به 100% نزدیک کند تا انگیزه‌ی تمام‌کردن کارها حفظ شود.
- recovery/late-day behavior نباید باعث شود progress نمایش‌داده‌شده از 100 بالاتر برود.
- overachievement در final score قابل ثبت است، نه در progress bar.

فرمول دقیق هنوز `OPEN` است.

## 17.6 Dynamic daily capacity / Norm

Target روزانه‌ی Ring توسط user به‌صورت دستی تعیین نمی‌شود. سیستم آن را بر اساس ظرفیت و رفتار اخیر تنظیم می‌کند. رفتار retained و تأییدشده‌ی کلی:

- شکست‌های پیاپی می‌توانند target را موقتاً کاهش دهند.
- بازگشت عملکرد باعث recovery تدریجی target می‌شود.
- موفقیت‌های پیاپی می‌توانند target را به‌تدریج سخت‌تر کنند.
- با داده‌های جدید، یک norm جدید حول عملکرد واقعی user شکل می‌گیرد.

thresholdهای دقیق و windowها OPEN هستند.

---

# 18. Itemهای مؤثر بر Ring

Task، Event و Routine occurrence می‌توانند در scoring یک Goal روزانه اثر داشته باشند، به شرطی که برای Daily Ring همان روز انتخاب/عضو شده باشند.

قاعده‌ی مهم:

> اگر یک Item در Daily Ringهای آن روز عضو نباشد، انجام آن هیچ Goal روزانه‌ای را جلو نمی‌برد.

یک Task ممکن است امروز در Daily Ring باشد، انجام نشود، فردا دوباره انتخاب شود، پس‌فردا انتخاب نشود و چند روز بعد دوباره برگردد.

هر زمان انجام شود، فقط به **روز credited/effective همان completion** و Ring همان روز تعلق می‌گیرد.

---

# 19. Dotick Day و Day Boundary

روز منطقی سیستم الزاماً در 00:00 تمام نمی‌شود.

مفهوم رسمی لازم است:

```text
Calendar Day != Dotick Day
```

تنظیم user:

```text
day_boundary / daily_rollover_offset
```

## 19.1 حالت پیش‌فرض

اگر user مقدار صریح تعیین نکرده باشد:

- ambiguity window پیش‌فرض = 1 ساعت بعد از midnight.
- اگر user در این window یک Task/Item را complete کند، سیستم می‌پرسد:
  - برای امروز انجام شد؟
  - یا برای دیروز؟

completion یک `credited/effective date` پیدا می‌کند.

## 19.2 حالت تنظیم‌شده

اگر user مثلاً day boundary را 02:00 تعیین کند:

- completionهای قبل از 02:00 خودکار به Dotick Day قبلی attribution می‌شوند.
- در 02:00 روز قبلی finalize و روز جدید فعال می‌شود.

## 19.3 Finalization و Ring generation

در زمان Day Boundary:

1. روز قبلی بسته می‌شود.
2. progress نهایی می‌شود.
3. is_completed تثبیت می‌شود.
4. final score و bonus محاسبه/reveal می‌شود.
5. streakهای مرتبط finalize می‌شوند.
6. Daily Ringهای روز جدید ساخته می‌شوند.

در حالت default unset، این نقطه فعلاً 1 ساعت بعد از midnight است.

## 19.4 Late credit

تا قبل از boundary user می‌تواند completion را به روز قبل نسبت دهد.

بعد از finalization، Daily Ring قدیمی snapshot تاریخی محسوب می‌شود و تغییر عادی Item نباید آن را دوباره باز کند.

---

# 20. Statistics و تغییرات تاریخی

کاربر می‌تواند RoutineCompletion روزهای گذشته را آزادانه تغییر دهد.

این تغییر باید آمار مرتبط را اصلاح کند، اما نباید کل تاریخ سیستم را هر بار از صفر محاسبه کند.

اصل طراحی:

> Selective invalidation / selective recomputation.

نمونه‌ی metric/windowها:

- TodayStats
- CurrentWeekStats
- MonthlyStats
- RecentBehaviorStats
- LifetimeStats

اگر داده‌ی پنج هفته‌ی قبل تغییر کند:

- آمار امروز لزوماً تغییر نمی‌کند.
- آمار هفته‌ی مربوطه در صورت نگهداری update می‌شود.
- lifetime aggregate می‌تواند increment/decrement شود.
- metricهایی مثل streak فقط در محدوده‌ی تحت تأثیر دوباره محاسبه می‌شوند.

Behavior/ML features می‌توانند asynchronous refresh شوند.

Source of truth همیشه completion/raw events هستند، نه dashboard aggregate.

---

# 21. Audit Log و Undo

سیستم باید تاریخچه‌ی کامل و قابل استفاده‌ای از تغییرات مهم داشته باشد.

اهداف:

- مشاهده‌ی history
- امکان Undo/restore در جاهای لازم
- حفظ تغییرات حتی وقتی row جاری حذف می‌شود، مانند Reset یک RoutineCompletion
- کمک به sync conflict investigation

این Audit/History لزوماً به معنی event sourcing کامل نیست.

---

# 22. Offline Sync

نیاز فعلی حفظ می‌شود:

- app بدون اینترنت باید تا حد امکان قابل استفاده باشد.
- تغییرات local ذخیره شوند.
- بعد از اتصال sync انجام شود.
- واحد conflict resolution در مدل قبلی field-level بوده است.
- Last-Write-Wins در سطح field بر اساس timestamp، baseline فعلی است.
- version metadata برای entityهای sync‌شونده استفاده می‌شود.

جزئیات معماری sync و conflict metadata بعداً در Design Stage formalize می‌شود.

---

# 23. Authentication و User Access

قابلیت‌های فعلی:

- Email/password
- password hashing امن
- Google OAuth
- JWT session
- Passkey

اگر Google OAuth unavailable باشد، email/password باید مسیر جایگزین باشد.

Enterprise SSO در فاز آینده است؛ انتخاب SAML/OIDC هنوز نهایی نشده.

---

# 24. Group و Sharing

یک user می‌تواند عضو چند Group باشد.

Task می‌تواند به چند عضو assign شود.

داده‌ی Groupها باید از هم ایزوله باشد.

برای Task/Event مشترک، زمان ذخیره‌شده باید یک instant مطلق قابل تبدیل (baseline: UTC) داشته باشد و برای هر عضو بر اساس timezone محلی نمایش داده شود.

## 24.1 Roles

تصمیم نهایی فعلی:

- نسخه‌ی فعلی فقط **System-defined Roles** دارد.
- Custom Roles به فاز Enterprise منتقل شده است.

## 24.2 Future enterprise access

کنترل دسترسی مدیریتی، hierarchy سازمانی، multi-tenancy کامل و permissionهای پیچیده‌تر در فاز سازمانی formalize می‌شوند.

---

# 25. AI-Assisted Item Creation

این feature محدود به Speech-to-Task نیست؛ یک pipeline عمومی برای ایجاد Item با کمک AI است.

## 25.1 نقاط ورود

هرجایی که user بتواند Item جدید اضافه کند، کنار ورودی متنی می‌تواند گزینه‌ی microphone/voice داشته باشد.

در آینده input sourceهای دیگری نیز قابل اتصال‌اند، مانند Email.

## 25.2 Voice flow

مثال user:

> «یادم بنداز چهارشنبه هفته دیگه ساعت ۸ شب با علی قرار دارم توی رستوران روما»

سیستم باید بتواند تحلیل کند:

- Task یا Event بودن درخواست
- title مناسب
- description احتمالی
- زمان/تاریخ
- location
- Folder/List/Column مناسب
- reminderهای مناسب
- سایر فیلدهای قابل استنتاج

## 25.3 Proposal نه Create مستقیم

Flow:

```text
Text / Voice
    ↓
Speech-to-Text (در صورت voice)
    ↓
Intent + Entity Analysis
    ↓
AI Item Draft / Proposal
    ↓
Review Popup
    ↓
User Edit
    ↓
Confirm
    ↓
Create Real Item
```

قبل از Confirm هیچ Item نهایی نباید صرفاً به دلیل AI inference ساخته شود.

## 25.4 Field provenance در AI draft

برای learning آینده مفید است که سیستم بتواند بداند هر field چگونه تولید شده:

- Explicit user input
- AI inferred
- User preference inferred
- External source

این metadata در draft/session مهم‌تر از Item نهایی است.

## 25.5 Learning from corrections

در مراحل بعدی، سیستم باید بتواند تفاوت بین AI proposal و user final payload را تحلیل کند.

مثال:

AI برای dinner event همیشه reminderهای:

- 1 day before
- 2 hours before

پیشنهاد می‌دهد، ولی user چند بار آن‌ها را به:

- 3 days before
- 4 hours before

تغییر می‌دهد.

سیستم می‌تواند preference شخصی user را یاد بگیرد و دفعات بعد پیشنهاد نزدیک‌تری ارائه دهد.

Session مفهومی پیشنهادی:

```text
AIItemCreationSession
- original_input
- source_type
- ai_proposal
- user_final_payload
- field_level_changes
- model_version
- accepted/rejected
- timestamps
```

---

# 26. Integrations و Automation

Vision فعلی شامل اتصال به سرویس‌های دیگر است.

نمونه‌ها:

- Email → AI analysis → Task/Event draft
- Google Calendar import/sync
- سایر task/calendar sources

اصل معماری مطلوب:

```text
External Source
    ↓
Normalized Input / Intent
    ↓
Analysis / Mapping
    ↓
Draft or Automated Action
    ↓
Item Model
```

سطح confirmation برای automationهای آینده هنوز OPEN است.

---

# 27. Technical Constraints Retained از اسناد قبلی

این موارد فعلاً به‌عنوان baseline فنی حفظ می‌شوند، ولی در Design Docs نهایی دوباره validate خواهند شد:

- PostgreSQL
- frontend/backend جدا
- REST برای CRUD
- JSON
- HTTPS حتی در development تا حد عملی
- WebSocket سبک برای notification/live update، نه جایگزین REST
- Docker از یک مرحله‌ی مناسب توسعه
- React Native / responsive mobile-first برای فاز اولیه
- امکان بررسی native Android/iOS بعداً
- server فعلی می‌تواند local-hosted باشد
- AI external service نباید failure آن core task management را از کار بیندازد

---

# 28. UI / Presentation Retained

تم‌های مطرح‌شده در اسناد قبلی، تا زمانی که حذف نشده‌اند، جزء vision هستند:

- Minimal customizable
- Liquid Glass style
- Material 3 Expressive inspired
- Dot-matrix style

جزئیات visual design در UI Design Specification جداگانه خواهد آمد.

---


# 28.1 Performance baseline retained

هدف تقریبی legacy برای نمونه‌ی local، پشتیبانی از حدود 30 user هم‌زمان بدون افت محسوس بوده است. این عدد SLA یا load-test guarantee نیست و باید در Performance Test Plan بعدی validate شود.

WebSocket notification/live updates باید latency کافی برای تجربه‌ی تقریباً real-time در Groupها داشته باشند.

# 28.2 User documentation

در فاز شخصی، راهنمای کاربر رسمی/آموزش تعاملی الزامی نیست. در فاز سازمانی، user/admin documentation و onboarding رسمی لازم خواهد شد.

# 29. امنیت و کیفیت

Baselineهای حفظ‌شده:

- password plaintext ممنوع
- bcrypt/argon2 یا معادل امن
- HTTPS
- user/group query isolation
- audit/history برای کاهش ریسک data loss
- test-driven development به‌عنوان رویکرد توسعه‌ی مدنظر
- regression test پس از bug fix
- Git/SCM از ابتدای پروژه
- مستندسازی تصمیم‌های فنی

الزامات privacy سازمانی مانند GDPR در فاز enterprise formalize می‌شوند.

---


# 29.1 Safety / operational risk baseline

محصول در فاز فعلی ریسک مستقیم فیزیکی/مالی تعریف‌شده‌ای ندارد. ریسک عملیاتی مهم، از دست رفتن/overwrite داده در sync و editهای تاریخی است؛ AuditLog، versioning و sync policy برای کاهش این ریسک الزامی‌اند.

# 29.2 Business / Future Scope retained

موارد خارج از scope فعلی ولی در vision:

- مدل قیمت‌گذاری و license برای نسخه‌ی تجاری هنوز OPEN است.
- SLA/support رسمی برای فاز سازمانی هنوز OPEN است.
- native Android (Kotlin) و iOS (Swift) بعد از تثبیت تجربه‌ی اولیه قابل ارزیابی‌اند.
- Enterprise multi-tenancy، reporting مدیریتی و access control پیشرفته در سند جداگانه تعریف خواهند شد.
- Google Calendar sync و AI integrations پیشرفته‌تر future capability هستند.

# 30. Global / User Streak

`Goal.current_streak` و Routine streak در این سند تعریف شده‌اند.

در SRS قبلی یک **global daily streak** نیز وجود داشت که با کامل شدن حداقل یک Ring در روز افزایش می‌یافت.

### RETAINED BUT NEEDS REVALIDATION

این global streak هنوز صریحاً در گفت‌وگوی جدید حذف نشده، ولی رفتار دقیق آن در کنار Goal streakها دوباره تأیید نشده است. بنابراین در این سند به‌عنوان requirement نهایی قطعی تلقی نمی‌شود و باید در مرحله‌ی Gamification Domain Review بسته شود.

همین وضعیت برای پیام‌های motivational/سرزنش‌گر هنگام شکستن streak نیز برقرار است.

---

# 31. موارد باز باقی‌مانده

موارد زیر عمداً نهایی نشده‌اند:

1. آیا Event می‌تواند چند **parent ساختاری** داشته باشد یا فقط چند reference و یک parent واقعی؟
2. schema دقیق Description/ContentBlock و relation metadata.
3. فرمول دقیق Ring progress، final score، early bonus و late-day recovery.
4. تعریف دقیق difficulty/effort estimation.
5. warm-up دقیق AI Goal discovery.
6. threshold similarity برای reactivation/merge Goal.
7. الگوریتم دقیق انتخاب سه Goal و نحوه‌ی learning weightها.
8. رفتار incremental Routine بعد از inactivity طولانی.
9. formal semantics کامل frequency-based routine streak.
10. final policy برای global user streak.
11. confirmation policy برای automationهای trusted آینده.
12. جزئیات endpointها، database indexes، ORM mapping و storage inheritance.
13. Enterprise SSO protocol.
14. معیارهای privacy/compliance نسخه‌ی سازمانی.

---

# 32. قواعد مهمی که نباید در بازنویسی اسناد بعدی گم شوند

- Routine خود status ندارد؛ RoutineCompletion دارد.
- `occurrence_date` business identity روز RoutineCompletion است؛ `completed_at` فعلاً حذف می‌شود.
- Reset completion row جاری را حذف می‌کند، AuditLog را نه.
- user می‌تواند historical routine completion را آزادانه تغییر دهد.
- unscheduled routine completion مجاز و معتبر است؛ schedule فقط discovery/presentation را کنترل می‌کند.
- missed scheduled day با extra completion روز دیگر جایگزین نمی‌شود مگر Routine از نوع frequency-per-period باشد.
- Task با grace=0 مستقیم از deadline به Skipped می‌رود.
- ownership از source جداست: owner و creator identity جدا دارند.
- hierarchy باید مستقیم queryable باشد؛ parse Description برای ساخت List tree قابل قبول نیست.
- Description capabilityها هنوز schema نهایی نیستند.
- Folder > List > Column terminology مبناست.
- Feature priority از specification حذف می‌شود؛ roadmap ترتیب توسعه را مشخص می‌کند.
- Daily Rings حداکثر «سه تا در صورت داشتن حداقل سه Goal» نیست؛ **دقیقاً سه تا** هستند وقتی حداقل سه Goal active و eligible وجود دارد.
- Goal progress در UI از 100 بالاتر نمی‌رود.
- final performance score می‌تواند از baseline بالاتر رود.
- bonus تا finalization روز مخفی می‌ماند.
- Goal completion یک Boolean معنادار است؛ فعالیت کوچک الزاماً streak را حفظ نمی‌کند.
- Dotick Day می‌تواند بعد از midnight تمام شود.
- default ambiguity window فعلاً 1 ساعت است مگر user تنظیم صریح داشته باشد.
- Daily Rings جدید بعد از day boundary ساخته می‌شوند.
- Item فقط وقتی Daily Goal را جلو می‌برد که عضو Ring همان credited day باشد.
- AI-created item قبل از تأیید user فقط draft است.
- اصلاحات user روی AI proposal باید در آینده برای personalization قابل یادگیری باشند.
- آمار باید selective recomputation داشته باشد، نه full-history recalculation برای هر edit.

---

# 33. وضعیت خروجی‌های مهندسی

Formal SRS و Traceability baseline در Increment 0 ایجاد شده‌اند. خروجی‌های زیر طبق Roadmap ایجاد یا در Increment مالکشان تکمیل می‌شوند:

1. **Formal SRS** — ایجاد شده؛ فقط requirements قابل تست و scope.
2. **Traceability Matrix** — baseline ایجاد شده و در هر Increment تکمیل می‌شود.
3. **Domain Model / ERD** — مدل مفهومی موجود است؛ ERD فیزیکی با Increment 1 تکمیل می‌شود.
4. **Data Design Specification** — baseline PostgreSQL و storage strategy در Increment 0 ایجاد می‌شود.
5. **API Contract** — به تفکیک Increment.
6. **UI/UX Specification** — flowها، screens، description editor، hierarchy interaction.
7. **Gamification & Scoring Specification** — فرمول‌ها و lifecycle روزانه.
8. **Sync & Audit Specification**.
9. **AI/Integration Specification**.
10. **Roadmap / Increment Plan** — موجود است و با آموخته‌های هر Increment update می‌شود.

