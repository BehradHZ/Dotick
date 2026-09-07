# Dotick Documentation

این پوشه نقطهٔ ورود و منبع سازمان‌یافتهٔ مستندات پروژهٔ Dotick است. هر سند باید در پوشه‌ای نگهداری شود که با نقش آن در چرخهٔ عمر محصول هم‌خوان است.

## مسیر پیشنهادی مطالعه

1. [`planning/vision-and-charter.md`](planning/vision-and-charter.md)
2. [`planning/scope-statement.md`](planning/scope-statement.md)
3. [`requirements/system-definition.md`](requirements/system-definition.md)
4. [`decision-register.md`](decision-register.md)
5. [`requirements/srs.md`](requirements/srs.md)
6. [`design/domain-model.md`](design/domain-model.md)
7. [`planning/increment-roadmap.md`](planning/increment-roadmap.md)

## ساختار مستندات

- [`planning/`](planning/) — چشم‌انداز، محدوده، نقشهٔ راه و ریسک‌ها
- [`requirements/`](requirements/) — تعریف سیستم، نیازمندی‌ها و ردیابی آن‌ها
- [`design/`](design/) — طراحی دامنه، معماری، داده، API، امنیت و تجربهٔ کاربری
- [`development/`](development/) — راه‌اندازی و رویه‌های محیط توسعه
- [`quality/`](quality/) — راهبرد و شواهد کیفیت و آزمون
- [`operations/`](operations/) — استقرار، مشاهده‌پذیری، بازیابی و عملیات امنیت
- [`tracking/`](tracking/) — تاریخچهٔ تغییرات و مرور Incrementها
- [`reference/`](reference/) — اسناد مرجع مشتق‌شده یا قدیمی که منبع نهایی تصمیم نیستند

تصمیم‌های تثبیت‌شده و باز در [`decision-register.md`](decision-register.md) ثبت می‌شوند و تصمیم‌های معماری تفصیلی در [`design/adr/`](design/adr/) قرار می‌گیرند.

نام فایل‌ها و پوشه‌ها از قرارداد `lowercase-kebab-case` پیروی می‌کند؛ نام‌های قراردادی مانند `README.md` و `CHANGELOG.md` استثنا هستند.

Current implementation: [I0 verification](tracking/increment-0-foundation-review.md) and the in-progress I1 [Authentication Design](design/authentication-design.md) / [OpenAPI contract](design/openapi.json). Remaining I1 scope: [readiness and acceptance plan](tracking/increment-1-readiness.md).
