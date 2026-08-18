# Dotick

Dotick در مرحله‌ی بازطراحی مبتنی بر سند قرار دارد. پیاده‌سازی آزمایشی قبلی از شاخه‌ی اصلی حذف شده است تا توسعه‌ی بعدی بر پایه‌ی نیازمندی‌ها و تصمیم‌های جدید آغاز شود.

در حال حاضر این مخزن **کد قابل اجرا، dependency یا CI فعال ندارد**، اما Formal SRS، Traceability و baselineهای معماری/داده/امنیت/تست/استقرار Increment 0 ایجاد شده‌اند. مرحله‌ی جاری، scaffold و Walking Skeleton است.

## اسناد پروژه

نقطه‌ی شروع مستندات، [`project-docs/00-README.md`](project-docs/00-README.md) است.

در صورت تعارض میان اسناد، ترتیب اعتبار فعلی چنین است:

1. [`project-docs/decision-register.md`](project-docs/decision-register.md)
2. [`project-docs/02-requirements/system-definition.md`](project-docs/02-requirements/system-definition.md)
3. [`project-docs/03-design/domain-model.md`](project-docs/03-design/domain-model.md)
4. [`project-docs/02-requirements/srs.md`](project-docs/02-requirements/srs.md)
5. [`project-docs/reference/class-fields.md`](project-docs/reference/class-fields.md)

برنامه و ترتیب توسعه در [`project-docs/01-planning/increment-roadmap.md`](project-docs/01-planning/increment-roadmap.md) ثبت می‌شود.

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
