# پایش و ثبت رویدادها

> وضعیت: baseline محدود Increment 0 پیاده‌سازی شده؛ راهبرد کامل عملیاتی نیازمند تدوین است.

در Increment 0، application/API logها به‌صورت JSON ثبت می‌شوند. هر request یک request ID تولیدشده
توسط سرور دارد و رکورد request فقط فیلدهای allowlistشده‌ی `timestamp`، `level`، `service`، `event`،
`request_id`، `method`، route نرمال‌شده، `status` و `duration_ms` را می‌پذیرد. formatter متن آزاد
پیام و هر فیلد خارج از allowlist را حذف می‌کند؛ بنابراین header، cookie، credential، token، body،
payload، exception message، secret key، DSN و environment object وارد خروجی ساخت‌یافته نمی‌شوند.

این baseline تعریف metrics، traces، dashboard، alert، retention، مالک سیگنال‌ها، آستانه‌ها و runbookها
را کامل نمی‌کند. این موارد باید پیش از production operation با مالک و سیاست نگهداری مشخص تدوین شوند.
