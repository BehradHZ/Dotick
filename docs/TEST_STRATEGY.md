# Dotick Test Strategy

> **Status:** Increment 0 baseline
> **Date:** 2026-08-17
> **Process:** TDD + risk-based verification

# 1. Objectives

- requirementها پیش از implementation به acceptance قابل ارزیابی تبدیل شوند؛
- business ruleها بدون وابستگی به transport تست شوند؛
- PostgreSQL constraint و migration واقعاً تست شوند؛
- API contract و authorization regression سریع تشخیص داده شوند؛
- یک vertical slice واقعی از client تا database اثبات شود.

# 2. Test levels

| Level | Purpose | Default boundary |
|---|---|---|
| Domain unit | state transition، value object، rule | بدون database/network |
| Application/service | use case، authorization orchestration، transaction behavior | fake فقط برای portهای خارجی؛ database در صورت اهمیت query/invariant |
| Database integration | ORM mapping، constraint، migration، query scope | PostgreSQL واقعی |
| API contract | status، JSON schema، error envelope، auth | Django test client/ASGI + PostgreSQL |
| Client component | render، form validation، state transitions | network adapter mocked at boundary |
| End-to-end | critical user workflow | client + API + PostgreSQL |
| Security | isolation و abuse cases | API/integration/E2E |
| Performance | query count/latency/load target | فقط برای requirement مالک و محیط ثبت‌شده |

SQLite جای PostgreSQL integration test نیست.

# 3. TDD loop

برای هر behavior:

1. requirement و acceptance criterion مشخص؛
2. کوچک‌ترین test شکست‌خورده‌ی معنادار؛
3. حداقل implementation؛
4. refactor با test سبز؛
5. integration/negative path متناسب با risk؛
6. traceability update هنگام واقعی‌شدن artifact.

testی که فقط implementation detail را mirror می‌کند ارزش acceptance ندارد.

# 4. Increment 0 gates

- parser/check خودکار برای uniqueness و پوشش IDهای SRS/Traceability؛
- build و static analysis هر app؛
- clean migration روی PostgreSQL؛
- liveness و readiness tests؛
- Walking Skeleton E2E از client تا persisted row و retrieval؛
- failure test هنگام unavailable بودن database برای readiness؛
- production configuration check حداقلی.

# 5. Increment 1 critical suite

- email/password happy/error paths؛
- Google unavailable و fallback behavior؛
- Passkey registration/authentication boundaries؛
- Inbox و default Column creation invariants؛
- Task create/read/edit/Done/Won't_Do/soft-delete؛
- persistence پس از restart؛
- cross-user read/write/move denial؛
- owner/creator/source independence؛
- concurrent version update behavior؛
- API schema/error contract.

# 6. Test data

- factoryها باید owner scope را آشکار بسازند.
- testهای authorization حداقل دو user مستقل دارند.
- زمان در testهای lifecycle با clock قابل کنترل است؛ sleep واقعی ممنوع.
- timezone testها UTC، یک offset مثبت، یک offset منفی و DST-capable zone را شامل می‌شوند.
- secret و credential واقعی در fixture نیست.

# 7. Mocking policy

- provider خارجی، clock و random generator در port boundary قابل fake هستند.
- ORM behavior، PostgreSQL constraint و serializer contract mock نمی‌شوند وقتی همان behavior موضوع test است.
- mock chain طولانی نشانه‌ی boundary نامناسب است.
- E2E سرویس خارجی واقعی را صدا نمی‌زند؛ sandbox یا deterministic fake استفاده می‌شود.

# 8. CI policy

ترتیب fast-to-slow:

1. formatting/lint/static analysis؛
2. unit tests؛
3. PostgreSQL migration/integration؛
4. API contract؛
5. client build/component tests؛
6. Walking Skeleton E2E؛
7. security/dependency checks.

merge با gate قرمز مجاز نیست. flaky test باید defect تلقی، isolate و با owner مشخص اصلاح شود؛ retry بی‌حد راه‌حل نیست.

# 9. Coverage and quality signals

یک درصد global به تنهایی quality gate نیست. gateهای اصلی:

- همه‌ی acceptance criteria Increment مالک verification دارند؛
- branchهای business rule و error/security path پوشش دارند؛
- bug fix ابتدا regression test دارد؛
- query حساس query-count یا plan assertion متناسب دارد؛
- requirementهای owning Increment در پایان بدون test/result باقی نمی‌مانند.

# 10. Test result artifacts

- CI result منبع اجرای معمول است.
- benchmark، security review و test execution دستی در `docs/reports/` ثبت می‌شود.
- release/increment review نتیجه را به Requirement IDها متصل می‌کند.
- test ID یا path فقط بعد از ایجاد واقعی وارد Traceability می‌شود.
