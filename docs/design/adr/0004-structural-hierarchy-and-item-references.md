# ADR-0004 — Structural hierarchy and Item references

> **Status:** Accepted
> **Date:** 2026-09-21
> **Scope:** Increment 2 hierarchy/reference Design Gate

# Context

Task و Event هرکدام حداکثر یک structural parent دارند، اما می‌توانند از چند context reference شوند. backend باید این دو مفهوم را صریح جدا کند، cycle و ownership leak را نپذیرد و placement/cascade semantics را atomic اجرا کند.

# Decision

- structural relation با nullable self foreign key به نام `items.structural_parent_id` ذخیره می‌شود و index مستقیم دارد.
- یک column فقط یک parent می‌پذیرد؛ بنابراین single-parent invariant در schema ذاتی است.
- در Increment 2 فقط Task/Event می‌توانند parent یا child باشند. هر چهار ترکیب Task→Task، Task→Event، Event→Task و Event→Event معتبر است.
- parent و child باید owner یکسان داشته باشند. child هنگام اتصال، placement parent را می‌گیرد.
- cycle، self-parent و اتصال به Item حذف‌شده ممنوع است. mutation hierarchy زیر transaction و owner-scoped lock انجام می‌شود تا cycleهای concurrent ساخته نشوند.
- move parent همه‌ی descendantها را در همان transaction به Column مقصد می‌برد.
- move مستقل child به Column دیگر ابتدا structural relation آن را قطع می‌کند؛ identity child ثابت می‌ماند.
- حذف parent همه‌ی descendantها را atomic soft-delete می‌کند. اگر بیش از یک resource متاثر باشد، API confirmation صریح لازم دارد.
- reference فقط با `ContentBlock(type=item_reference, referenced_item_id=...)` ذخیره می‌شود، structural effect ندارد و multi-reference است.
- dependency Task relation مستقل از hierarchy باقی می‌ماند.
- تکمیل parent، descendantهای Task را Done می‌کند. Done شدن همه‌ی childهای فعال، parent Task را به‌طور پیش‌فرض Done می‌کند و preference می‌تواند آن را غیرفعال کند.
- Won't Do cascade فقط با preference صریح فعال است. stateهای زمانی Event و Task cascade نمی‌شوند.

# Consequences

مزایا:

- parent و child مستقیم و indexable query می‌شوند.
- cardinality structural parent مبهم نیست و reference workflow مستقل می‌ماند.
- placement، completion و delete cascade در application service قابل audit/test هستند.

هزینه‌ها:

- cycle prevention recursive به application transaction و concurrency test نیاز دارد.
- move/delete روی tree بزرگ چند row را lock و mutate می‌کند.
- cross-type hierarchy service باید subtype rules را بدون ORM inheritance enforce کند.

# Rejected alternatives

- generic relation table برای structural edge: cardinality یک را غیرضروری پنهان می‌کند.
- استفاده از ContentBlock برای structural child: lifecycle و cascade را با presentation/reference مخلوط می‌کند.
- materialized path در Increment 2: برای depth و queryهای فعلی پیچیدگی migration و write amplification اضافی دارد.
