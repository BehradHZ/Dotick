# Dotick Test Strategy

> **Status:** Increment 0 closed; Increment 1 automated verification implemented and hosted-CI green
> **Reconciled:** 2026-09-16
> **Process:** TDD + risk-based verification

## 1. Objectives

- requirementها پیش از implementation به acceptance قابل ارزیابی تبدیل شوند؛
- business ruleها بدون وابستگی غیرضروری به transport تست شوند؛
- PostgreSQL constraint/query/migration واقعاً تست شوند؛
- API contract، authorization و request-boundary regression سریع تشخیص داده شوند؛
- vertical slice واقعی client -> API -> PostgreSQL اثبات شود؛
- migration history و published API surface بدون review خاموش drift نکنند.

SQLite جای PostgreSQL integration test نیست.

## 2. Test levels

| Level | Purpose | Current boundary |
|---|---|---|
| Domain/unit | state/value/rule helpers | no network; DB only when rule is a DB invariant |
| Application/service | use case, authorization orchestration, transaction behavior | PostgreSQL where locking/query semantics matter; fake only external ports |
| Database integration | ORM mapping, constraints, indexes, migration, query scope | real PostgreSQL |
| API contract | status, JSON/error schema, auth, owner isolation, idempotency/version | DRF/Django + PostgreSQL |
| Request/security boundary | body/media limits, CORS, production settings, malformed input | Django request stack |
| Client component | render/forms/state/network failure behavior | network adapter mocked at boundary |
| End-to-end | critical account-to-Task workflow | product client + Django API + PostgreSQL |
| Supply/deployment | dependency/secret/container/configuration controls | hosted CI + Docker |

## 3. TDD loop

For each behavior:

1. identify requirement/acceptance criterion;
2. add the smallest meaningful failing test;
3. implement the minimum behavior;
4. refactor with tests green;
5. add integration/negative cases proportional to risk;
6. update implementation documentation when the artifact/evidence becomes real.

Tests do not create product requirements. Canonical behavior is still defined by the product documents.

## 4. Increment 0 gates — closed

I0 established and hosted-verified:

- SRS/Traceability ID checks;
- build/static analysis;
- clean PostgreSQL migration;
- health/readiness tests;
- executable Golden Time vectors;
- client-to-database Walking Skeleton E2E;
- production configuration check;
- dependency/secret checks;
- non-root container build and persistence smoke.

See `docs/tracking/increment-0-foundation-review.md` for closure evidence.

## 5. Increment 1 critical suite — implemented

The current I1 automated suite covers:

- email registration/verification/resend/password reset and negative paths;
- JWT issue/refresh/revocation/logout/session management;
- Google assertion/linking/failure behavior with deterministic provider simulation;
- Passkey registration/authentication/list/delete, recent-auth and user-verification boundaries;
- account profile/timezone and verified contact lifecycle, including pending-contact exclusion and E.164 phone validation;
- concurrent/idempotent bootstrap of UserPreferences + exactly one Inbox/default Column;
- Folder/List/Column CRUD/order/ownership, immutable Inbox/default Column and recoverable container rules;
- explicit Item/Task/Source composition and model constraints;
- Task create/read/edit/move/Todo/Done/Won't_Do/Trash/restore;
- owner isolation, foreign-destination denial and ordinary-staff non-bypass;
- optimistic version conflict and create idempotency/retry behavior;
- JSON-only request boundary, 16 KiB body cap, malformed/non-JSON rejection and stable errors;
- trusted/untrusted CORS and `If-Match` support;
- OpenAPI 3.1 validity, reviewed contract hash, exact published route set and edge-rate-limit classification;
- I1 query indexes;
- I6 compatibility guards that prevent I1 shortcuts from breaking stable identity/history/sync evolution.

## 6. Client and E2E evidence

The product client is no longer an I0-only workbench. Automated evidence covers registration/verification/password recovery, sign-in/bootstrap, persisted Inbox rendering, List/Task creation, draft retention after failure, versioned status changes, sign-out privacy and time vectors.

Playwright desktop and mobile flows exercise the real product client against Django + PostgreSQL for sign-in, bootstrap, Task creation, re-authentication/reload, retrieval, completion and Trash behavior.

Configured external email/Google/WebAuthn/phone systems are intentionally not called by deterministic E2E; they require target-environment smoke before formal I1 closure.

## 7. Test data and mocking policy

- authorization tests use at least two independent users;
- owner scope is visible in factories/fixtures;
- ORM/PostgreSQL constraints are not mocked when they are the behavior under test;
- external provider, delivery, clock and random boundaries may use deterministic fakes;
- lifecycle tests avoid real sleeps where a controllable time boundary is possible;
- timezone tests retain UTC, offset and DST-capable cases;
- real secrets/credentials never appear in fixtures.

## 8. CI policy — current hosted pipeline

Fast-to-slow hosted verification currently includes:

1. locked Python/Node dependency installation;
2. Ruff, ESLint, Prettier and TypeScript;
3. requirements traceability check;
4. migration/schema-drift checks, append-only migration-history guard and fresh-database verification;
5. backend/API/domain and Golden Time tests on PostgreSQL;
6. Django production deployment/security check;
7. client component/network/time-vector tests;
8. Expo web export;
9. desktop/mobile Playwright E2E;
10. Python/npm dependency audit and secret scan;
11. non-root deployment container builds;
12. container smoke and persistence after API restart.

Audited implementation HEAD `7302ca3b18a79af35058828102bb62e845a56645` passed run `35057831342` before the documentation-reconciliation commits.

A red required gate blocks acceptance. Flaky behavior is treated as a defect; unbounded retry is not a substitute for diagnosis.

## 9. Migration verification policy

Historical numbered migrations are immutable once committed into history. `scripts/check_migrations.py` compares migration paths against the relevant base ref and rejects modification, deletion or rename; new schema evolution is expressed in a new migration.

CI also retains `makemigrations --check --dry-run`, migration application and clean/fresh PostgreSQL reconstruction checks.

## 10. Coverage and quality signals

No single global coverage percentage is the primary quality gate. The important signals are:

- owning-Increment acceptance scenarios have executable evidence;
- business/error/security branches have negative-path tests;
- bug fixes arrive with regression tests;
- critical constraints and access paths are tested against PostgreSQL;
- contract changes require deliberate OpenAPI/test review;
- release-only provider/deployment evidence is explicitly separated from deterministic automated tests.

## 11. Test result artifacts

- hosted CI is the normal execution record;
- increment/release reviews summarize accepted evidence and remaining gates;
- manual/configured-provider/recovery evidence belongs in quality/operations reports when executed;
- requirement/test/code references are added only after the referenced artifact exists.

See [Increment 1 readiness](../tracking/increment-1-readiness.md) and [the 148-commit development audit](../tracking/development-commit-audit.md).
