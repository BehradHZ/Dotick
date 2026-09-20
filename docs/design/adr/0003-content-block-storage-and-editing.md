# ADR-0003 — ContentBlock storage and editing

> **Status:** Accepted
> **Date:** 2026-09-21
> **Scope:** Increment 2 ContentBlock Design Gate

# Context

RichDescription به blockهای مرتب، identity پایدار، comment target و reference به Item نیاز دارد. schema باید reorder/edit را بدون تغییر identity پشتیبانی کند و برای sync آینده قابل گسترش باشد، اما Increment 2 نباید sync engine یا CRDT را زودتر پیاده کند.

# Decision

- هر `Item` صفر یا چند `ContentBlock` دارد؛ entity جداگانه‌ی `RichDescription` ذخیره نمی‌شود.
- هر block دارای UUID پایدار، `item_id`، `block_type`، `position` غیرمنفی، `data` از نوع JSON object، `version` مثبت و timestamp است.
- `(item_id, position)` یکتا و ترتیب canonical است. reorder در transaction انجام می‌شود و UUID block را تغییر نمی‌دهد.
- typeهای Increment 2 دقیقاً `text`، `attachment`، `location` و `item_reference` هستند. type و field ناشناخته رد می‌شود.
- payloadهای canonical:
  - `text`: `text`، `style` از `paragraph|heading|bullet|number|code|quote|separator`، `indent` غیرمنفی و `marks` مرتب؛ هر mark دارای `type`، `start` و `end` و فقط برای `link|phone|identifier` دارای `value` است.
  - `attachment`: `attachment_id`، `name` و `media_type`؛ blob lifecycle مستقل از block است.
  - `location`: مختصات latitude/longitude به‌صورت pair و/یا `address`، `place_id`، `meeting_url`؛ حداقل یک locator لازم است.
  - `item_reference`: payload خالی و `referenced_item_id` به‌صورت foreign key؛ title snapshot authoritative ذخیره نمی‌شود.
- `referenced_item_id` فقط برای `item_reference` مجاز/الزامی است. reference، structural relation نیست و هر Item می‌تواند در چند block مجاز reference شود.
- edit با optimistic concurrency روی `version` کل block انجام می‌شود. conflict granularity در Increment 2 یک block کامل است.
- comment روی block به UUID آن متصل می‌شود. حذف block، comment جاری آن را cascade می‌کند؛ AuditLog history را مستقل نگه می‌دارد.
- validation محدودیت اندازه و shape در API/application layer انجام می‌شود؛ database constraintهای relational، type/reference consistency و position را محافظت می‌کنند.

# Consequences

مزایا:

- identity و ordering برای comment، reorder و sync بعدی پایدار است.
- Item reference از hierarchy جدا و مستقیم queryable است.
- JSON payload انعطاف type-specific می‌دهد، در حالی که discriminator و validation contract آن را محدود نگه می‌دارد.

هزینه‌ها:

- database به‌تنهایی همه‌ی shapeهای JSON و mark rangeها را validate نمی‌کند.
- reorder چند block نیازمند transaction و locking هماهنگ است.
- merge همزمان داخل یک text block تا Increment 6 در سطح block conflict می‌دهد.

# Rejected alternatives

- یک HTML/Markdown blob: block identity و block-level comment/reorder را از بین می‌برد.
- table جدا برای هر block type: ordering و mutation را پیچیده و Increment 2 را بیش‌ازحد گسترده می‌کند.
- CRDT در Increment 2: قبل از sync architecture هزینه و semantics تثبیت‌نشده ایجاد می‌کند.
