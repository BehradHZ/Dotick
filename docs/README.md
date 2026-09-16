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
- [`tracking/`](tracking/) — تاریخچهٔ تغییرات، audit پیاده‌سازی و مرور Incrementها
- [`reference/`](reference/) — اسناد مرجع مشتق‌شده یا قدیمی که منبع نهایی تصمیم نیستند

تصمیم‌های تثبیت‌شده و باز در [`decision-register.md`](decision-register.md) ثبت می‌شوند و تصمیم‌های معماری تفصیلی در [`design/adr/`](design/adr/) قرار می‌گیرند.

نام فایل‌ها و پوشه‌ها از قرارداد `lowercase-kebab-case` پیروی می‌کند؛ نام‌های قراردادی مانند `README.md` و `CHANGELOG.md` استثنا هستند.

## Current implementation evidence

- [Increment 0 verification](tracking/increment-0-foundation-review.md) — formally closed foundation checkpoint.
- [Increment 1 readiness](tracking/increment-1-readiness.md) — current implemented boundary, acceptance evidence and remaining formal release gates.
- [Increment 1 backend review](tracking/increment-1-backend-review.md) — historical backend checkpoint plus 2026-09-16 reconciliation.
- [Increment 1 client review](tracking/increment-1-client-review.md) — minimal product-client checkpoint plus hosted-evidence reconciliation.
- [Development commit audit](tracking/development-commit-audit.md) — complete post-reset audit boundary covering the 148 implementation commits from the documentation-only baseline through audited HEAD `7302ca3`.
- [API contract](design/openapi.json) and [API contract rules](design/api-contracts.md) — executable published I1 backend contract.
- [Security design](design/security-design.md) — current I1 API/origin/identity/migration hardening.
- [Test strategy](quality/test-strategy.md) — current hosted verification and migration-history policy.

The 2026-09-16 commit-history reconciliation found no implementation change that requires redefining canonical product behavior. System Definition, Decision Register and SRS remain above implementation evidence in authority; implementation/tracking documents were updated instead of turning code accidents into requirements.

Current hosted CI is green for the audited I1 implementation. Formal I1 closure still requires configured target-environment email, Google, real WebAuthn authenticator and phone-delivery smoke, deployment-edge enforcement for declared identity-ceremony rate limits, and the formal Increment 1 release record/publication.
