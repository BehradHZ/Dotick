# Dotick Data Design Baseline

> **Status:** Increment 0 baseline; Increment 1 physical scope defined
> **Date:** 2026-08-17
> **Decision source:** DR-054 / ADR-0002
> **Database:** PostgreSQL

# 1. Scope

این سند storage strategy را می‌بندد و schema لازم برای Walking Skeleton و Increment 1 را مشخص می‌کند. entityهای Incrementهای بعدی فقط زمانی وارد physical design می‌شوند که behavior و decision gate آن‌ها آماده باشد.

# 2. Design rules

- UUID شناسه‌ی عمومی entityها است.
- نام table و column به `snake_case` است.
- timestampهای لحظه‌ای `timestamptz` و به UTC ذخیره می‌شوند.
- business date مانند `occurrence_date` در آینده از نوع `date` است.
- foreign key، unique و check constraint هرجا invariant قابل بیان باشد در database ثبت می‌شود.
- تمام queryهای private باید owner/scope را در predicate داشته باشند.
- migration منتشرشده immutable است؛ تغییر بعدی migration جدید می‌سازد.
- JSONB جای relation queryable یا constraint اصلی را نمی‌گیرد.
- enumهای پرتحول با check constraint/text یا lookup کنترل‌شده طراحی می‌شوند؛ انتخاب دقیق در migration مالک ثبت می‌شود.

# 3. Item persistence strategy

```text
items
  id PK
  kind
  owner_user_id
  created_by_user_id
  title
  is_trashed
  version
  created_at
  updated_at
       |
       +-- 1:1 tasks
       +-- 1:1 events       (I2)
       +-- 1:1 routines     (I3)
```

این مدل composition صریح است، نه Django model inheritance. ایجاد یا حذف base/subtype باید در یک transaction انجام شود.

Invariantها:

- هر `items.kind = 'task'` دقیقاً یک row در `tasks` دارد.
- subtype row بدون Item متناظر وجود ندارد.
- تغییر kind در Personal V1 مجاز نیست.
- status در `items` قرار نمی‌گیرد.

# 4. Increment 1 schema

## 4.1 Users and preferences

### `users`

custom Django user model باید پیش از اولین migration ساخته شود.

| Column | Type | Constraint / note |
|---|---|---|
| `id` | uuid | PK |
| `email` | varchar | normalized, case-insensitive uniqueness strategy |
| `password` | varchar | Django encoded hash; never plaintext |
| `is_active` | boolean | not null |
| `is_staff` | boolean | not null |
| `date_joined` | timestamptz | not null |

framework-required fields/tables در migration واقعی تکمیل می‌شوند؛ contract محصول نباید به نام داخلی آن‌ها وابسته شود.

### `user_preferences`

| Column | Type | Constraint / note |
|---|---|---|
| `user_id` | uuid | PK, FK users, cascade |
| `timezone` | varchar | valid IANA timezone identifier |
| `day_boundary_offset_minutes` | integer nullable | behavior در I10؛ storage می‌تواند دیرتر اضافه شود |
| `created_at` | timestamptz | not null |
| `updated_at` | timestamptz | not null |

## 4.2 Organization hierarchy

### `folders`

| Column | Type | Constraint / note |
|---|---|---|
| `id` | uuid | PK |
| `owner_user_id` | uuid | FK users, not null |
| `title` | varchar | trimmed, non-empty |
| `position` | integer | non-negative |
| `created_at` / `updated_at` | timestamptz | not null |

### `lists`

| Column | Type | Constraint / note |
|---|---|---|
| `id` | uuid | PK |
| `folder_id` | uuid | FK folders, not null |
| `title` | varchar | trimmed, non-empty |
| `position` | integer | non-negative |
| `created_at` / `updated_at` | timestamptz | not null |

### `columns`

| Column | Type | Constraint / note |
|---|---|---|
| `id` | uuid | PK |
| `list_id` | uuid | FK lists, not null |
| `title` | varchar | trimmed, non-empty |
| `position` | integer | non-negative |
| `is_default` | boolean | not null, default false |
| `created_at` / `updated_at` | timestamptz | not null |

یک partial unique constraint باید حداکثر یک default Column در هر List را تضمین کند. ساخت List و default Column در یک transaction انجام می‌شود تا قاعده‌ی «دقیقاً یک default» در write path حفظ شود.

Personal V1 ownership از chain زیر derive می‌شود:

```text
column -> list -> folder -> owner_user_id
```

Group scope تا Increment 7 به این tableها اضافه نمی‌شود؛ migration آن Increment ownership model را بازنگری می‌کند.

## 4.3 Items and placement

### `items`

| Column | Type | Constraint / note |
|---|---|---|
| `id` | uuid | PK |
| `kind` | varchar | initial allowed value `task`; later expanded by migration |
| `owner_user_id` | uuid | FK users, not null |
| `created_by_user_id` | uuid | FK users, not null |
| `column_id` | uuid | FK columns, not null; Inbox/default placement is explicit |
| `title` | varchar | trimmed, non-empty |
| `is_trashed` | boolean | not null, default false |
| `version` | bigint | not null, positive, incremented on mutation |
| `created_at` / `updated_at` | timestamptz | not null |

در I1، List از `column_id -> list_id` قابل استخراج است و duplication آن در Item انجام نمی‌شود. انتقال Item فقط column را عوض می‌کند و service باید ownership chain مقصد را validate کند.

### `tasks`

I1 فقط lifecycle پایه را پیاده می‌کند.

| Column | Type | Constraint / note |
|---|---|---|
| `item_id` | uuid | PK, FK items, cascade |
| `status` | varchar | `todo`, `done`, `wont_do` در I1؛ stateهای زمانی در I2 |

فیلدهای scheduling، priority، dependency و hierarchy در migration Increment 2 افزوده می‌شوند، نه به صورت columnهای unused در I1.

## 4.4 Source

### `item_sources`

| Column | Type | Constraint / note |
|---|---|---|
| `item_id` | uuid | PK, FK items, cascade |
| `platform` | varchar | not null; `manual` value allowed |
| `external_account_id` | varchar nullable | provider-scoped identifier; not internal owner |
| `external_id` | varchar nullable | provider-scoped object identifier |

اگر `external_id` وجود دارد، uniqueness باید حداقل روی `(platform, external_account_id, external_id)` با null semantics صریح اعمال شود. Source هیچ foreign key یا derivationی برای `owner_user_id` فراهم نمی‌کند.

# 5. Index baseline

حداقل indexهای Increment 1:

- `folders(owner_user_id, position)`
- `lists(folder_id, position)`
- `columns(list_id, position)`
- partial unique روی `columns(list_id) WHERE is_default`
- `items(owner_user_id, is_trashed, updated_at desc)`
- `items(column_id, is_trashed, updated_at desc)`
- `items(owner_user_id, kind, is_trashed)`
- unique source identity فقط برای rowهای external واجد identity کامل

هر index اضافی باید از query یا execution plan واقعی ناشی شود. indexهای آینده صرفاً از روی Domain Model ایجاد نمی‌شوند.

# 6. Delete and history behavior

- Item user-facing با `is_trashed` soft-delete می‌شود.
- hard delete عمومی API در Personal V1 تعریف نشده است.
- حذف Folder/List/Column تا تعریف flow انتقال/حذف children نباید با cascade کور پیاده شود.
- AuditLog در I2 اضافه می‌شود؛ تا آن زمان API منتشرشده نباید وعده‌ی undo/history بدهد.
- auth/session cleanup و retention عملیاتی جدا از business soft-delete است.

# 7. Concurrency

- `version` برای optimistic concurrency foundation نگه‌داری می‌شود.
- mutation باید version را atomically افزایش دهد.
- contract دقیق conflict response در Increment 1 API design تعریف می‌شود.
- transactionهای ایجاد List/default Column و Item/subtype atomic هستند.
- `select_for_update` فقط برای invariantهای واقعاً concurrent به کار می‌رود؛ lock سراسری ممنوع است.

# 8. Migration policy

هر migration باید:

1. forward migration معتبر داشته باشد؛
2. روی database خالی اجرا شود؛
3. در صورت data migration، idempotency/rollback strategy مستند داشته باشد؛
4. constraint و index را با نام پایدار بسازد؛
5. با version code همان commit سازگار باشد؛
6. برای عملیات پرریسک backup/restore note داشته باشد.

# 9. Verification for Increment 0/1

| Requirement | Design evidence | Required verification |
|---|---|---|
| SRS-CON-001 | PostgreSQL-only server persistence | integration test against PostgreSQL |
| SRS-CON-002 | explicit composition, no ORM inheritance | architecture inspection |
| SRS-CON-003 | constraints, indexes, transaction rules | migration + query/integrity tests |
| SRS-CON-004 | Compose/local-hosted topology | deployment smoke test |
| SRS-ITEM-002..009 | `items`, `tasks`, `item_sources` | model/service/API tests in I1 |
| SRS-ORG-001..005 | folder/list/column schema | constraint and acceptance tests in I1 |

# 10. Deferred physical design

- Event, Routine and TrackingState tables.
- hierarchy child/reference relation.
- ContentBlock storage.
- recurrence/reminder schema.
- Group ownership.
- sync field clocks.
- audit/history schema.
- DailyRing/scoring snapshots.

این موارد با Decision Gate مالکشان طراحی می‌شوند و نباید از این baseline استنباط فیزیکی شوند.
