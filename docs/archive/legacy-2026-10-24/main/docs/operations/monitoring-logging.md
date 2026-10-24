# پایش و ثبت رویدادها

> **وضعیت:** baseline مشاهده‌پذیری Increment 0 پیاده‌سازی شده و در Increment 1 حفظ/تست شده است؛ راهبرد کامل production monitoring هنوز متعلق به release/operations آینده است.
> **Reconciled:** 2026-09-16

در runtime فعلی، application/API logها به‌صورت JSON ساخت‌یافته ثبت می‌شوند. هر request یک request/correlation ID تولیدشده توسط سرور دارد و رکورد request فقط فیلدهای allowlistشده مانند `timestamp`، `level`، `service`، `event`، `request_id`، `method`، route نرمال‌شده، `status` و `duration_ms` را می‌پذیرد.

formatter و request logger نباید header، cookie، credential، password، access/refresh token، provider assertion، body/payload، secret key، DSN، environment object یا free-form exception message را وارد ordinary structured request log کنند. این invariant در test suite و hosted CI پوشش داده می‌شود.

`/health` برای liveness process و `/ready` برای readiness وابستگی ضروری PostgreSQL استفاده می‌شوند؛ availability سرویس‌های خارجی هویت/تحویل، readiness هستهٔ Task دستی را تعیین نمی‌کند.

Hosted CI run `35057831342` روی audited implementation HEAD `7302ca3b18a79af35058828102bb62e845a56645` قبل از reconciliation اسناد با موفقیت اجرا شد و تست‌های backend/security، production settings، container smoke و persistence را در کنار سایر gateها پوشش داد.

این baseline هنوز موارد زیر را به‌عنوان production operations کامل نمی‌کند:

- metrics و distributed traces؛
- dashboard و alert policy؛
- retention و log shipping؛
- signal ownership و escalation؛
- production runbookها و SLO/SLA؛
- provider-specific operational telemetry؛
- backup/restore alerting و rehearsal evidence.

این موارد باید پیش از production operation با owner، retention و escalation policy مشخص شوند. ثبت رخداد business/audit history نیز با request logging یکی نیست و در Incrementهای مالک Audit/History پیاده می‌شود.

برای وضعیت کامل implementation و release gateها، [Increment 1 readiness](../tracking/increment-1-readiness.md) و [development commit audit](../tracking/development-commit-audit.md) را ببینید.
