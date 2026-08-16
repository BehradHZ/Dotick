# Dotick

Dotick در مرحله‌ی بازطراحی مبتنی بر سند قرار دارد. پیاده‌سازی آزمایشی قبلی از شاخه‌ی اصلی حذف شده است تا توسعه‌ی بعدی بر پایه‌ی نیازمندی‌ها و تصمیم‌های جدید آغاز شود.

در حال حاضر این مخزن **کد قابل اجرا، dependency یا CI فعال ندارد**. اضافه‌کردن ساختار برنامه، ابزارهای توسعه و workflowهای CI باید هم‌زمان با شروع Increment اجرایی مرتبط انجام شود.

## اسناد پروژه

نقطه‌ی شروع مستندات، [`docs/README.md`](docs/README.md) است.

در صورت تعارض میان اسناد، ترتیب اعتبار فعلی چنین است:

1. [`docs/canonical/decision-register.md`](docs/canonical/decision-register.md)
2. [`docs/canonical/system-definition.md`](docs/canonical/system-definition.md)
3. [`docs/canonical/domain-model.md`](docs/canonical/domain-model.md)
4. [`docs/reference/software-requirements-specification.md`](docs/reference/software-requirements-specification.md)
5. [`docs/reference/class-fields.md`](docs/reference/class-fields.md)

برنامه و ترتیب توسعه در [`docs/planning/roadmap.md`](docs/planning/roadmap.md) ثبت می‌شود.

## وضعیت بازنشانی

- کد و تست‌های پیاده‌سازی آزمایشی قبلی بخشی از وضعیت فعال پروژه نیستند.
- workflowهای وابسته به فناوری نسخه‌ی قبلی حذف شده‌اند.
- پوشه‌ی محلی `archive/` صرفاً برای نگهداری نسخه‌های قبلی است و وارد Git نمی‌شود.
- پوشه‌ی محلی `resources/skills/` ابزار کمکی توسعه است و وارد Git نمی‌شود.

## شروع پیاده‌سازی جدید

پیش از اضافه‌کردن کد جدید:

1. موارد `OPEN` مؤثر بر Increment موردنظر را در Decision Register تعیین تکلیف کنید.
2. محدوده و معیارهای پذیرش Increment را از Roadmap استخراج کنید.
3. ساختار فنی و dependencyها را فقط برای همان Increment ایجاد کنید.
4. تست‌ها و CI را همراه با اولین برش اجرایی اضافه کنید تا با stack واقعی پروژه هم‌راستا باشند.
