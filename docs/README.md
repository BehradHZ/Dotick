# Dotick Documentation

این پوشه نقطهٔ ورود و منبع سازمان‌یافتهٔ مستندات پروژهٔ Dotick است. هر سند باید در پوشه‌ای نگهداری شود که با نقش آن در چرخهٔ عمر محصول هم‌خوان است.

## مسیر پیشنهادی مطالعه

- **قواعد Agent و فرایند توسعه:** [`../AGENTS.md`](../AGENTS.md) → [`development/engineering-process.md`](development/engineering-process.md) (مرجع اصلی SDLC، Vertical Slice و Definition of Done).
- **معنای محصول:** [`requirements/system-definition.md`](requirements/system-definition.md) → [`decision-register.md`](decision-register.md) → [`requirements/srs.md`](requirements/srs.md)، تا زمانی که بازنگری محصول جانشین مصوب آن‌ها را تعیین کند.
- **طراحی:** [`design/domain-model.md`](design/domain-model.md)، [`design/architecture.md`](design/architecture.md) و اسناد تخصصی مرتبط.
- **تحویل و کیفیت:** [`planning/increment-roadmap.md`](planning/increment-roadmap.md) → [`quality/test-strategy.md`](quality/test-strategy.md).
- [`planning/vision-and-charter.md`](planning/vision-and-charter.md) و [`planning/scope-statement.md`](planning/scope-statement.md) هنوز نیازمند بازنگری و تکمیل‌اند؛ Placeholderها تصمیم مصوب محصول نیستند.

## ساختار مستندات

- [`planning/`](planning/) — چشم‌انداز، محدوده، نقشهٔ راه و ریسک‌ها
- [`requirements/`](requirements/) — تعریف سیستم، نیازمندی‌ها و ردیابی آن‌ها
- [`design/`](design/) — طراحی دامنه، معماری، داده، API، امنیت و تجربهٔ کاربری
- [`development/`](development/) — فرایند مهندسی مصوب، راه‌اندازی و رویه‌های محیط توسعه
- [`quality/`](quality/) — راهبرد و شواهد کیفیت و آزمون
- [`operations/`](operations/) — استقرار، مشاهده‌پذیری، بازیابی و عملیات امنیت
- [`tracking/`](tracking/) — تاریخچهٔ تغییرات، audit پیاده‌سازی و مرور Incrementها
- [`reference/`](reference/) — اسناد مرجع مشتق‌شده یا قدیمی که منبع نهایی تصمیم نیستند
- [`licensing.md`](licensing.md) — مدل AGPL-3.0، مرز self-hosting/support و سیاست هویت/برند Dotick

تصمیم‌های تثبیت‌شده و باز در [`decision-register.md`](decision-register.md) ثبت می‌شوند و تصمیم‌های معماری تفصیلی در [`design/adr/`](design/adr/) قرار می‌گیرند.

نام فایل‌ها و پوشه‌ها از قرارداد `lowercase-kebab-case` پیروی می‌کند؛ نام‌های قراردادی مانند `README.md` و `CHANGELOG.md` استثنا هستند.

## Historical implementation evidence (I0/I1)

- [Increment 0 verification](tracking/increment-0-foundation-review.md) — formally closed foundation checkpoint.
- [Increment 1 readiness](tracking/increment-1-readiness.md) — current implemented boundary, acceptance evidence and remaining formal release gates.
- [Increment 1 backend review](tracking/increment-1-backend-review.md) — current implemented backend boundary and remaining external evidence.
- [Increment 1 client review](tracking/increment-1-client-review.md) — current web/Android product-client boundary and deliberate UI limits.
- [Development commit audit](tracking/development-commit-audit.md) — historical post-reset implementation audit.
- [API contract](design/openapi.json) and [API contract rules](design/api-contracts.md) — executable published I1 backend contract.
- [Security design](design/security-design.md) — current I1 API/origin/identity/migration hardening.
- [Test strategy](quality/test-strategy.md) — verification gates, historical hosted evidence and migration-history policy.

System Definition, Decision Register and SRS remain above implementation evidence in authority; implementation/tracking documents must describe the checked-in behavior without turning code accidents into requirements.

Increment 1 was closed and released as `v0.2.0` under the previous process. These records describe that historical release, not requirements or mandatory gates for the rebuild. The existing CI and security/data-integrity checks remain in place until a separately verified, risk-based change is approved. Optional external email/SMS and live-provider/device/edge checks were previously deferred to deployment.
