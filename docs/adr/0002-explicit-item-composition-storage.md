# ADR-0002 — Explicit composition for Item persistence

> **Status:** Accepted
> **Date:** 2026-08-17
> **Decision:** DR-054

# Context

Domain Model، Item و capabilityهای مشترک را به‌صورت مفهومی بیان می‌کند، اما SRS صریحاً مانع تبدیل مکانیکی این hierarchy به ORM inheritance می‌شود. schema باید identity مشترک، ownership isolation، queryهای cross-item و constraintهای subtype را حفظ کند.

# Decision

- `items` table identity و metadata واقعاً مشترک را نگه می‌دارد.
- subtype tableها با primary-key/foreign-key یک‌به‌یک به `items` متصل‌اند.
- ORM inheritance استفاده نمی‌شود؛ create/update/delete هر aggregate با service و transaction صریح انجام می‌شود.
- capabilityهای optional در component/relation tableهای مستقل و Incremental ذخیره می‌شوند.
- discriminator `items.kind` با presence subtype row در یک transaction هماهنگ می‌شود و invariant آن با service tests و database checks قابل اعمال محافظت می‌شود.

# Consequences

مزایا:

- UUID، owner، title، trash و version برای همه‌ی Itemها یک محل قطعی دارند.
- reference به هر Item یک foreign key عادی دارد.
- subtypeها columnهای nullable نامرتبط دریافت نمی‌کنند.
- افزودن capability یا subtype migration مستقل و قابل فهم دارد.

هزینه‌ها:

- query subtype یک join نیاز دارد.
- database به تنهایی نمی‌تواند همه‌ی حالت‌های discriminator/subtype را با یک constraint ساده تضمین کند؛ transaction service و integrity tests لازم‌اند.
- bulk list query باید projection کنترل‌شده داشته باشد تا N+1 ایجاد نشود.

# Rejected alternatives

- single wide table: nullable column و constraint شرطی زیاد ایجاد می‌کند.
- Django multi-table model inheritance: domain inheritance را به ORM coupling تبدیل می‌کند و transaction/query behavior را پنهان می‌سازد.
- table مستقل بدون `items`: identity/reference/query مشترک را پیچیده می‌کند.
