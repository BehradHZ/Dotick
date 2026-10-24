# قراردادهای API

> وضعیت: Increment 1 در حال اجرا

قرارداد اجرایی فعلی Identity در [`openapi.json`](openapi.json) ثبت شده است. این فایل با `openapi-spec-validator` در test suite اعتبارسنجی می‌شود و تغییر endpoint منتشرشده بدون تغییر هم‌زمان قرارداد و test مجاز نیست.

قواعد ثابت فعلی:

- prefix نسخه‌دار محصول `/api/v1` است؛
- payload و response از JSON استفاده می‌کنند؛
- field ناشناخته در input پذیرفته نمی‌شود؛
- خطا envelope پایدار `{"error":{"code":...,"details":...}}` دارد؛
- endpoint خصوصی از JWT Bearer و session فعال استفاده می‌کند؛
- lookup خصوصی همیشه با actor فعلی scope می‌شود؛
- `204` body ندارد و عملیات request/resend ضد account-disclosure پاسخ `202 accepted` یکسان دارد.

قرارداد I0 checkpoint در [`foundation-api.md`](foundation-api.md) مستقل و local/test-only است. قرارداد Folder/List/Column/Task هم‌زمان با نخستین vertical slice آن‌ها به OpenAPI افزوده می‌شود؛ idempotency و optimistic-version conflict باید پیش از انتشار endpoint mutation همان slice نهایی شوند.
