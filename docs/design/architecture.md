# Dotick Architecture Baseline

> **Status:** Increment 0 baseline
> **Date:** 2026-08-17
> **Decision sources:** DR-053, DR-054
> **Scope:** Personal V1 and the Increment 0 Walking Skeleton

# 1. Purpose

این سند ساختار فنی اولیه‌ی Dotick را به اندازه‌ای تعریف می‌کند که پروژه قابل scaffold، تست و تکامل Incremental باشد. این سند behavior محصول را تعریف نمی‌کند؛ در تعارض، ترتیب authority ثبت‌شده در `README.md` حاکم است.

# 2. Architectural drivers

- یک codebase قابل نگه‌داری برای توسعه‌ی solo/small-team.
- client و server مستقل با REST/JSON contract.
- PostgreSQL به‌عنوان persistence اصلی.
- mobile-first و web-capable با مسیر قابل حفظ برای Android/iOS.
- ownership isolation از اولین query.
- قابلیت اجرای local-hosted.
- جداسازی core task management از AI و integrationهای خارجی.
- تکامل مرحله‌ای بدون طراحی فیزیکی همه‌ی Incrementها در ابتدا.

# 3. System context

```text
User
  |
  v
Expo / React Native / Web client
  |
  | HTTPS + JSON REST
  v
Django ASGI application
  |
  +--> PostgreSQL
  |
  +--> WebSocket notifications (only when owning Increment adds them)
  |
  +--> External identity / AI / integration adapters (later Increments)
```

REST source of truth است. WebSocket در آینده فقط signal تغییر، notification یا invalidation می‌فرستد؛ mutation authoritative از REST عبور می‌کند.

# 4. Architecture style

Backend یک **modular monolith** است. deployment واحد باقی می‌ماند، ولی module boundaryها باید از ابتدا روشن باشند:

```text
Interface (REST / WebSocket / admin)
        |
Application (use cases, transactions, authorization orchestration)
        |
Domain (rules, states, value objects)
        |
Infrastructure (Django ORM, PostgreSQL, external adapters)
```

قواعد dependency:

- Domain به HTTP، serializer، ORM request object یا provider خارجی وابسته نیست.
- Interface مستقیماً business rule را پیاده نمی‌کند.
- Application transaction و use case را هماهنگ می‌کند.
- Infrastructure interfaceهای موردنیاز application را پیاده می‌کند.
- cross-module write از application service عمومی module مالک عبور می‌کند.
- import مستقیم model خصوصی یک module در module دیگر ممنوع است، مگر contract صریح ثبت شده باشد.

# 5. Technology baseline

| Area | Baseline | Rationale |
|---|---|---|
| Backend language | Python 3.14 | runtime پشتیبانی‌شده در Django/DRF و موجود در محیط فعلی |
| Backend framework | Django 5.2 LTS | auth، ORM، migration و operational guardrail یکپارچه |
| REST API | Django REST Framework | validation، serialization، authentication/permission hooks و contract testing |
| Runtime model | ASGI | مسیر استاندارد برای HTTP و WebSocket آینده |
| Frontend | TypeScript + Expo SDK 57 + React Native + React Native for Web | client مستقل و mobile-first با reuse میان web/native |
| Database | PostgreSQL | الزام SRS و integrity/query capability |
| Python dependency management | `uv` + `pyproject.toml` + `uv.lock` | نصب cross-platform و reproducible |
| JavaScript runtime/package management | Node.js 24 LTS + npm workspace + `package-lock.json` | ابزار موجود، lockfile استاندارد و یک نسخه‌ی سازگار از React/React Native |
| Packaging | Docker/Compose | local-hosted و محیط توسعه/CI قابل بازتولید |

patch version دقیق dependencyها هنگام scaffold و پس از حل واقعی dependencyها pin می‌شود. manifest و CI نباید `latest` شناور داشته باشند.

# 6. Planned repository structure

```text
apps/
  api/                 Django project and deployable backend
  client/              Expo universal client
packages/
  api-contract/        generated/client-facing contract artifacts when introduced
project-docs/
  01-planning/
  02-requirements/
  03-design/
    adr/
    ui-ux/
  04-development/
  05-quality/
  06-operations/
  08-tracking/
  reference/
```

در backend، moduleها بر اساس capability محصول شکل می‌گیرند، نه صرفاً نوع فایل:

```text
apps/api/dotick/
  identity/
  organization/
  items/
  tasks/
  events/              added in I2
  routines/            added in I3
  ...
```

هر module می‌تواند زیرلایه‌های `domain`, `application`, `api` و `infrastructure` داشته باشد؛ ایجاد پوشه‌ی خالی برای Incrementهای آینده ممنوع است.

# 7. Increment 0 Walking Skeleton

Walking Skeleton باید یک resource persisted واقعی داشته باشد و این مسیر را اثبات کند:

```text
Client screen
  -> versioned REST endpoint
  -> application use case
  -> repository / Django ORM
  -> PostgreSQL row
  -> JSON response
  -> rendered client state
```

resource باید خنثی و قابل حذف باشد، یا اولین thin slice از Increment 1 باشد. `/health` و `/ready` برای عملیات لازم‌اند ولی جای این vertical slice را نمی‌گیرند.

# 8. API boundaries

- endpointها در Increment مالک و در OpenAPI تعریف می‌شوند؛ global endpoint inventory از قبل ساخته نمی‌شود.
- JSON field naming و error envelope در اولین contract Increment 1 ثابت می‌شوند.
- validation syntactic در serializer/interface و validation business در domain/application انجام می‌شود.
- API نباید Django model shape را به‌طور خودکار contract عمومی کند.
- authorization باید پیش از fetch/serialization داده‌ی خصوصی اعمال شود.
- pagination و filtering فقط برای query واقعی همان Increment اضافه می‌شوند.

# 9. Data and transaction boundaries

- PostgreSQL تنها system of record server-side است.
- storage strategy مطابق DR-054 explicit composition است.
- هر use case تغییردهنده یک transaction boundary روشن دارد.
- constraintهای قابل بیان در database فقط در application code رها نمی‌شوند.
- migration append-only است؛ migration اعمال‌شده rewrite نمی‌شود.
- timestamp ذخیره‌شده UTC است و local interpretation از timezone کاربر می‌آید.
- optimistic version metadata از Item foundation موجود است؛ sync semantics کامل در Increment 6 بسته می‌شود.

# 10. Authentication and authorization

- custom User model با UUID باید قبل از اولین migration تثبیت شود.
- password handling به API استاندارد Django واگذار می‌شود و algorithm policy در `project-docs/03-design/security-design.md` است.
- JWT، Google OAuth و Passkey در Increment 1 پشت adapter/use-caseهای مستقل قرار می‌گیرند.
- authentication method نباید ownership model را تغییر دهد.
- queryهای private با owner scope آغاز می‌شوند؛ object lookup بدون scope مجاز نیست.
- Group authorization تا Increment 7 وارد schema یا abstraction عمومی premature نمی‌شود.

# 11. Reliability and observability

- log ساخت‌یافته شامل timestamp، level، service، request/correlation id و event name است.
- secret، password، access token و payload حساس log نمی‌شود.
- `/health` فقط liveness process را می‌سنجد.
- `/ready` dependencyهای لازم مانند database را می‌سنجد.
- خطای provider خارجی به adapter محدود می‌شود و core manual workflow را unavailable نمی‌کند.
- background work باید idempotency و retry policy مخصوص use case داشته باشد؛ queue عمومی پیش از نیاز اضافه نمی‌شود.

# 12. Security boundaries

- production-like و local-hosted deployment از TLS در reverse proxy استفاده می‌کنند.
- loopback-only development می‌تواند HTTP داشته باشد؛ این exception نباید روی interface عمومی bind شود.
- CORS، allowed hosts و trusted origins allowlist هستند.
- state-changing endpointها authentication، authorization و validation صریح دارند.
- WebSocket آینده هنگام connect و subscription همان scope authorization REST را اعمال می‌کند.

# 13. Quality gates

هر change باید متناسب با risk این gateها را پاس کند:

- formatting and static analysis
- unit tests
- database/integration tests برای persistence و constraint
- API contract tests برای endpointها
- client component tests
- حداقل یک end-to-end test برای vertical slice فعال
- migration check و clean-database migration test
- secret/dependency scanning در CI پس از scaffold

# 14. Deferred decisions

موارد زیر عمداً در این baseline بسته نشده‌اند:

- endpointهای دقیق و error envelope تا Increment 1 API design.
- WebSocket channel topology تا Increment 7.
- background queue/Redis تا اولین use case نیازمند آن.
- offline sync metadata تا Increment 6.
- physical schema قابلیت‌های آینده تا Increment مالک.
- production cloud provider؛ local-hosted portability فعلاً کافی است.

# 15. Fitness checks

این architecture baseline زمانی معتبر می‌ماند که:

1. client بدون import یا اتصال مستقیم به backend internals build شود؛
2. core use case بدون framework request object قابل unit test باشد؛
3. clean database با migrationها ساخته شود؛
4. owner-scoped queries با تست منفی cross-user پوشش داده شوند؛
5. حذف یا failure adapter خارجی core task flow را نشکند؛
6. Walking Skeleton از client تا PostgreSQL و بازگشت response را طی کند.
