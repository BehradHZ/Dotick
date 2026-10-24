# Dotick — Business & Market Analysis

> **Document Status:** Working Business Analysis  
> **Document Type:** Business / Market Analysis — non-canonical for product behavior  
> **Research Baseline:** 2026-08-22  
> **Relationship to Canonical Documents:** Product behavior, scope, and domain semantics remain authoritative in the canonical `System Definition`, `Decision Register`, and `Domain Model`. This document records market-facing analysis and positioning and must not silently redefine product behavior.

---

# 0. Document Purpose & Scope

## 0.1 Purpose

این سند تحلیل بازار و جایگاه‌گذاری محصول Dotick را در سطح کسب‌وکار ثبت می‌کند. هدف آن تفکیک روشن «مسئله و رفتار محصول» از «تحلیل رقبا و استدلال بازار» است تا System Definition فقط تعریف کند Dotick چه مسئله‌ای را حل می‌کند و چه رفتاری دارد، در حالی که این سند توضیح می‌دهد محصولات مقایسه‌ای چگونه خود را عرضه می‌کنند، چه بخش‌هایی از نیاز کاربر را پوشش می‌دهند و Dotick باید بر چه تمایزی تکیه کند.

## 0.2 Current Coverage

در نسخه‌ی فعلی، این سند روی بخش `Market / Product Positioning` از Business Track تمرکز دارد و شامل موارد زیر است:

- تعریف مسئله‌ی بازار از دید کاربر؛
- تحلیل رقبا و محصولات مقایسه‌ای شناخته‌شده؛
- شناسایی هم‌پوشانی‌ها و نواحی تمایز؛
- تعریف positioning اولیه‌ی Dotick؛
- ثبت محدودیت‌های تحلیل و مواردی که هنوز نیازمند اعتبارسنجی بازار هستند.

قیمت‌گذاری، مدل درآمد، licensing، packaging تجاری و SLA در این نسخه نهایی نشده‌اند و باید در مراحل بعدی Business Track تکمیل شوند.

## 0.3 Evidence Rule

ادعا درباره‌ی قابلیت‌های رقبا باید بر مبنای منبع عمومی قابل‌ردگیری ثبت شود. نبود یک قابلیت در منابع بررسی‌شده، به‌تنهایی اثبات نمی‌کند که آن محصول آن قابلیت را ندارد؛ در چنین مواردی این سند از عبارت‌هایی مانند «در منابع رسمی بررسی‌شده تثبیت نشد» استفاده می‌کند و از ادعای مطلق پرهیز می‌کند.

---

# 1. Market Problem

کاربر هدف Dotick برای مدیریت روزمره صرفاً با یک فهرست کار یا یک تقویم مواجه نیست؛ او ممکن است هم‌زمان به مدیریت Task، Event و Routine، برنامه‌ریزی تکرارشونده، مشاهده‌ی پیشرفت، حفظ انگیزه و همکاری محدود با دیگران نیاز داشته باشد. بازار ابزارهای productivity این نیازها را با رویکردهای متفاوت پوشش می‌دهد و برخی محصولات چند مورد از آن‌ها را نیز در یک محصول گرد آورده‌اند؛ بنابراین مسئله‌ی بازار Dotick نباید به‌صورت «نبود هرگونه محصول یکپارچه» تعریف شود. مسئله‌ی قابل‌دفاع‌تر، نیاز به مدلی است که این رفتارها را در یک تجربه‌ی حرفه‌ای و منسجم، با semantics روشن برای کارهای روزانه، روتین‌ها، اهداف و همکاری، و با لایه‌ی انگیزشی غیرغالب بر تجربه‌ی اصلی، کنار هم قرار دهد.

---

# 2. Competitive Analysis

## 2.1 Analysis Basis

تحلیل فعلی سه محصولی را پوشش می‌دهد که در اسناد اولیه‌ی Dotick به‌عنوان نقاط مقایسه مطرح شده‌اند:

- TickTick
- Habitica
- Google Calendar

این فهرست یک market landscape کامل نیست و برای تصمیم‌های تجاری نهایی باید بعداً با محصولات دیگری که بخش‌های مشابه بازار را پوشش می‌دهند تکمیل شود.

## 2.2 TickTick

### Product Emphasis

منابع رسمی TickTick آن را یک ابزار productivity گسترده معرفی می‌کنند که Task Management، Calendar Views، Habit Tracker، reminderهای پیشرفته، List/Kanban/Timeline، Eisenhower Matrix، statistics، collaboration و sync چندپلتفرمی را در یک محصول ارائه می‌دهد. همچنین در نسخه‌ی فعلی، قابلیت‌های AI از جمله Voice Capture برای استخراج اطلاعاتی مانند تاریخ و priority از ورودی صوتی نیز در معرفی رسمی محصول دیده می‌شود.

### Competitive Significance for Dotick

TickTick نزدیک‌ترین مقایسه در میان سه محصول بررسی‌شده به ایده‌ی «productivity suite یکپارچه» است. در نتیجه، Dotick نباید تمایز خود را صرفاً بر ادعای «داشتن Task + Calendar + Habit + Collaboration در یک برنامه» بنا کند؛ این ترکیب به‌تنهایی تمایز پایداری ایجاد نمی‌کند.

تمایز قابل‌بررسی برای Dotick باید بیشتر بر کیفیت مدل و رفتار محصول متمرکز باشد: تفکیک روشن Task، Event و Routine؛ semantics دقیق recurrence و history؛ Goal و Daily Ring به‌عنوان لایه‌ی روزانه‌ی پیشرفت؛ Dotick Day؛ و گیمیفیکیشنی که هدف آن افزایش انگیزه در یک ابزار حرفه‌ای است، نه صرفاً افزودن featureهای جانبی به یک task manager. این موارد positioning هدف Dotick هستند و برتری واقعی آن‌ها نسبت به TickTick هنوز نیازمند validation محصول و کاربر است.

## 2.3 Habitica

### Product Emphasis

Habitica یک habit-building و productivity app با مدل گیمیفیکیشن صریح و RPGمحور است. منابع رسمی آن Habits، Dailies و To Do's را به‌عنوان انواع اصلی task معرفی می‌کنند و reward/punishment، Gold، Experience، Health، Avatar، equipment، pets، quests و party interaction را بخش مرکزی تجربه می‌دانند. Habitica همچنین قابلیت‌های اجتماعی و Group Plan با shared task board، نقش‌ها و assignment را ارائه می‌دهد.

### Competitive Significance for Dotick

Habitica نشان می‌دهد که گیمیفیکیشن می‌تواند هسته‌ی انگیزشی یک سیستم productivity باشد، اما سبک محصول آن عمداً بازی‌محور است. Dotick در positioning فعلی مسیر متفاوتی دارد: گیمیفیکیشن باید در خدمت برنامه‌ریزی و پیشرفت باشد، نه اینکه هویت بصری و مفهومی اصلی محصول را به یک RPG تبدیل کند.

بنابراین تفاوت موردنظر Dotick نسبت به Habitica در «وجود یا عدم وجود Gamification» نیست، بلکه در نوع Gamification و نسبت آن با ابزار حرفه‌ای است: Daily Ring، Goal progress، streak و performance feedback باید تجربه‌ی انگیزشی ایجاد کنند، در حالی که مدل اصلی محصول همچنان یک سیستم مدیریت کار و برنامه‌ریزی باقی می‌ماند.

## 2.4 Google Calendar

### Product Emphasis

Google Calendar یک محصول calendar و scheduling محور است. منابع رسمی آن بر event scheduling، appointment booking، shared calendars، availability، Google Meet، integration با Gmail و Google Tasks و قابلیت‌های productivity مانند Time Insights تمرکز دارند. Taskهایی که تاریخ و زمان دارند نیز می‌توانند در Calendar نمایش داده شوند و Calendar قابلیت اشتراک‌گذاری و permissionهای مختلف برای تقویم‌ها را فراهم می‌کند.

### Competitive Significance for Dotick

Google Calendar مرجع مهمی برای مسئله‌ی زمان‌بندی، مشاهده‌ی برنامه‌ی مشترک و هماهنگی میان افراد است. با این حال، positioning فعلی Dotick فراتر از calendar-centric planning است و Task، Event، Routine، Goal، progress و motivation را در یک مدل واحد دنبال می‌کند.

در منابع رسمی بررسی‌شده، Habit Tracking یا Gamification به‌عنوان هسته‌ی Google Calendar معرفی نشده‌اند؛ بنابراین Dotick می‌تواند از Google Calendar به‌عنوان benchmark برای clarity و collaboration زمانی استفاده کند، بدون آنکه خود را صرفاً به‌عنوان یک calendar replacement تعریف کند.

---

# 3. Comparative Summary

| Dimension | TickTick | Habitica | Google Calendar | Dotick — Intended Position |
|---|---|---|---|---|
| Primary product emphasis | Broad productivity / task management | Gamified habits and productivity | Calendar and scheduling | Integrated daily planning and progress system |
| Task management | Strong | Supported through To Do's / Dailies / Habits | Supported through Google Tasks integration | First-class Task domain |
| Event / calendar scheduling | Strong calendar views and integrations | Not established as a core capability in reviewed official materials | Core capability | First-class Event domain |
| Habit / routine tracking | Habit Tracker | Core Habits / Dailies model | Not established as a core capability in reviewed official materials | First-class Routine + dated completion history |
| Recurrence | Flexible recurring rules are publicly documented | Structured recurring Dailies are supported | Recurring calendar behavior is supported | Shared recurrence model with entity-specific semantics |
| Collaboration | Shared lists and task assignment | Parties and Group Plans with shared tasks | Shared calendars and scheduling collaboration | Small-group collaboration within the same domain model |
| Gamification | Productivity-first; achievement-oriented elements exist | Core RPG-style system | Not a core positioning element in reviewed materials | Professional, restrained motivational layer |
| AI-assisted capture | AI Voice Capture is publicly promoted | Not established in reviewed official materials | Gemini-assisted scheduling/event workflows exist in supported plans | Draft → Review → Confirm item creation |
| Long-term/daily goal model | Product has goals/habits, but Dotick-equivalent semantics are not established by reviewed sources | Goals are tied strongly to game/task mechanics | Not a core product model | Goal + Daily Ring + Dotick Day |

> **Interpretation:** این جدول برای تعیین «برنده‌ی مطلق» طراحی نشده است. هدف آن مشخص‌کردن محورهای هم‌پوشانی و نقاطی است که Dotick برای ایجاد تمایز باید در سطح تجربه و semantics، نه صرفاً تعداد featureها، بهتر یا متفاوت عمل کند.

---

# 4. Product Positioning

## 4.1 Positioning Statement

برای کاربران فردی و گروه‌های کوچک که برنامه‌ریزی روزانه‌ی آن‌ها ترکیبی از Task، Event، Routine و اهداف بلندمدت است، Dotick یک سیستم productivity یکپارچه است که برنامه‌ریزی ساختاریافته، recurrence، همکاری و پیگیری پیشرفت را با یک لایه‌ی انگیزشی حرفه‌ای در یک تجربه‌ی واحد ترکیب می‌کند. Dotick به‌جای تمرکز صرف بر فهرست وظایف، تقویم یا گیمیفیکیشن RPGمحور، تلاش می‌کند انگیزش و پیشرفت روزانه را به بخشی بومی از مدل برنامه‌ریزی تبدیل کند، بدون آنکه قابلیت‌های حرفه‌ای مدیریت کار تحت‌الشعاع عناصر بازی قرار گیرند.

## 4.2 Intended Differentiation

تمایز هدف Dotick در وضعیت فعلی باید بر مجموعه‌ی زیر استوار باشد:

1. **Unified domain semantics:** Task، Event و Routine مفاهیم مجزا و صریح‌اند، نه صرفاً variantهای سطح UI.
2. **Professional motivation layer:** Gamification باید progress را تقویت کند، اما ماهیت ابزار را به game تبدیل نکند.
3. **Goal-to-day bridge:** Goalهای بلندمدت از طریق Daily Ring و Dotick Day به کار روزانه متصل می‌شوند.
4. **Historical integrity:** completion، Daily Ring و history باید معنای تاریخی پایدار و قابل‌ردگیری داشته باشند.
5. **Integrated small-group collaboration:** collaboration باید بخشی از همان مدل برنامه‌ریزی باشد، نه workflow جدا از کار شخصی.
6. **AI with user control:** AI می‌تواند پیشنهاد و draft تولید کند، اما در current scope تصمیم نهایی ایجاد Item با کاربر است.

## 4.3 What Must Not Be Used as a Differentiation Claim

تا زمانی که تحقیق جامع‌تر انجام نشده، موارد زیر نباید به‌عنوان claim بازاری قطعی استفاده شوند:

- «هیچ محصول دیگری Task، Habit و Calendar را با هم ندارد.»
- «هیچ رقیبی collaboration و productivity را یکپارچه نکرده است.»
- «Dotick اولین محصولی است که از AI برای ساخت Task استفاده می‌کند.»
- «رقبا recurrence یا cross-platform support ندارند.»

منابع رسمی فعلی حداقل برای TickTick نشان می‌دهند چند مورد از این قابلیت‌ها از قبل در یک محصول واحد وجود دارند.

---

# 5. Target User and Buyer Baseline

## 5.1 Current Target User

بر اساس Current Scope محصول، target user فعلی فردی است که برای مدیریت جدی زندگی شخصی خود به ترکیبی از task management، scheduling، routines و progress tracking نیاز دارد و ممکن است در گروه‌های کوچک غیرسازمانی نیز همکاری کند.

## 5.2 Future Organizational User

نسخه‌ی آینده می‌تواند برای تیم‌ها و سازمان‌هایی توسعه یابد که علاوه بر رفتارهای productivity فعلی، به hierarchy، custom authorization، tenant isolation، administration و reporting سازمانی نیاز دارند.

## 5.3 Buyer / User Distinction

در Personal Scope، user و تصمیم‌گیرنده‌ی خرید می‌توانند یک نفر باشند. در Enterprise Scope، buyer، administrator و end user ممکن است نقش‌های متفاوتی داشته باشند. این تفکیک هنوز به‌اندازه‌ی کافی تحلیل نشده و باید در Business Track آینده formalize شود.

---

# 6. Packaging, Pricing & Commercial Model

در وضعیت فعلی، packaging، pricing، licensing و مدل درآمدی Dotick نهایی نشده‌اند. هیچ نتیجه‌ای از تحلیل رقبا در این سند نباید به‌صورت ضمنی به یک مدل قیمت‌گذاری تبدیل شود.

مواردی که در مرحله‌ی بعد باید بررسی شوند:

- Personal / Free tier
- Subscription model
- Per-user vs per-organization pricing
- Enterprise contract
- Feature packaging
- Support and SLA model

---

# 7. Validation Gaps

پیش از استفاده‌ی تجاری از positioning این سند، موارد زیر باید با تحقیق تکمیلی یا بازخورد کاربر بررسی شوند:

- آیا کاربران واقعاً از جابه‌جایی میان ابزارهای productivity به‌اندازه‌ی کافی رنج می‌برند که migration به محصول جدید را توجیه کند؟
- آیا Goal + Daily Ring برای کاربران ارزش متمایز و قابل‌درک ایجاد می‌کند؟
- آیا «Gamification حرفه‌ای و restrained» مزیت مطلوب است یا برای بخشی از بازار ارزش کمی دارد؟
- TickTick و سایر productivity suites تا زمان عرضه‌ی Dotick چه قابلیت‌های دیگری اضافه می‌کنند؟
- کدام segment حاضر است برای یکپارچگی و مدل پیشرفت Dotick هزینه پرداخت کند؟
- آیا collaboration فعلی برای differentiation کافی است یا صرفاً feature پایه محسوب می‌شود؟

---

# 8. References

منابع زیر در تاریخ 2026-08-22 برای تحلیل قابلیت‌های محصولات مقایسه‌ای بررسی شده‌اند:

1. TickTick — Features  
   https://ticktick.com/features?language=en_US

2. TickTick — Product Home  
   https://ticktick.com/home

3. TickTick Help Center  
   https://help.ticktick.com/

4. Habitica — Gamify Your Life  
   https://habitica.com/static/home

5. Habitica — FAQ / Task Types / Group Plans  
   https://habitica.com/static/faq

6. Google Workspace — Google Calendar  
   https://workspace.google.com/products/calendar/

7. Google Calendar Help — Create & manage tasks in Google Calendar  
   https://support.google.com/calendar/answer/9901136

8. Google Calendar Help — Share your calendar  
   https://support.google.com/calendar/answer/37082

---

# Appendix A — Document Responsibility Boundary

```text
System Definition
= کاربر چه مسئله‌ای دارد؟
  Dotick چیست؟
  Scope و رفتار محصول چیست؟

BUSINESS.md
= بازار این مسئله چگونه است؟
  محصولات مقایسه‌ای چه قابلیت‌هایی دارند؟
  Dotick چگونه باید position شود؟
  چه claimهایی قابل‌دفاع یا نیازمند validation هستند؟

Formal SRS
= رفتار پذیرفته‌شده چگونه به requirementهای atomic و testable تبدیل می‌شود؟

Roadmap
= این قابلیت‌ها چه زمانی و با چه ترتیبی ساخته می‌شوند؟
```
