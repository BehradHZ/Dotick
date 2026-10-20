# Dotick Test Strategy

> **Policy status:** Reconciled for the 2026-10-20 engineering-process adoption.
> **Process authority:** [Engineering Process](../development/engineering-process.md), particularly Sections 5–6. Testing is risk-adaptive, not mandatory TDD for every change.
> **Evidence boundary:** The I0/I1 and Django-specific lists below describe the **historical v0.2.0 implementation**. No Rust implementation or new CI change is claimed by this document.

## 1. Objectives

- Independently verify the accepted *observable user behavior* and important negative/failure outcomes.
- Match evidence to risk; prioritize data integrity, authorization, recurrence/time, offline/sync and real client → API → PostgreSQL paths over test count.
- Use real PostgreSQL for behavior that depends on transactions, locking, constraints, migrations or query semantics; SQLite is not a substitute.
- Preserve already-effective security/regression coverage. Changing process text does not authorize deleting a check, weakening an assertion, or lowering a required CI gate.
- Distinguish unit/integration/contract/user-journey evidence from unrun live-provider/device/recovery checks. Test results are not product requirements.

## 2. Risk and test levels

| Risk | Evidence expected | Examples |
| --- | --- | --- |
| A — Low | Applicable format/lint/typecheck/build and direct visual/behavior inspection; no obligatory new test/spec/doc | Copy, styling, isolated UI |
| B — Medium | Focused behavior and integration tests, significant error paths, diff review and changed user journey | Domain logic, API, query and integration |
| C — High | Explicit threat/failure review, independent positive and negative scenarios, real relevant boundaries, rollback/recovery plan and required approval | Identity, authorization, secrets, personal data, sync/conflict, destructive migration |

Risk is about **impact, not change size**. Reuse existing evidence instead of writing duplicate tests. Prefer stable observable boundaries, avoid implementation-coupled/tautological assertions, mock external providers at their boundary only. Never weaken a test to pass CI.

Choose applicable levels for the slice: domain/unit invariants; application/transaction behavior; PostgreSQL integration; HTTP/OpenAPI contract and request/security boundary; client component; critical client → API → PostgreSQL E2E; supply/deployment checks. No requirement to generate a separate test artifact at each level.

## 3. Verification loop

1. Derive expected outcome/acceptance independently of the implementation.
2. Decide the minimum *meaningful* tests and checks for the change's risk; use TDD when it clarifies complex/risky behavior, not as a universal ritual.
3. Implement the whole slice, run pertinent static and automated checks, and exercise the actual changed user journey where applicable.
4. Check material negative/failure/security cases, investigate failures and perform a focused diff review.
5. Report checks **run/passed, failed, and not run**, plus outstanding risk; only claim completion on fresh evidence.

Bug fixes should cover the escaped failure with a focused regression test. Historical I0/I1 coverage is retained below as evidence; the rebuild must prove its own acceptance independently.

## 4. Historical Increment 0 gates — closed

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

## 5. Historical Increment 1 critical suite — implemented

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

## 6. Historical client and E2E evidence

The product client is no longer an I0-only workbench. Automated evidence covers registration/verification/password recovery, sign-in/bootstrap, persisted Inbox rendering, List/Task creation, draft retention after failure, versioned status changes, sign-out privacy and time vectors.

`e2e/workspace.spec.ts` is the I1 Playwright acceptance evidence. Its desktop and mobile flows exercise the real product client against Django + PostgreSQL for sign-in, bootstrap, Task creation, re-authentication/reload, retrieval, completion and Trash behavior.

`e2e/increment-0-checkpoint-regression.spec.ts` is retained only as an I0 foundation regression. It verifies the disposable Checkpoint API and PostgreSQL path in CI; it is not I1 acceptance evidence.

Configured external email/SMS, Google and WebAuthn systems are intentionally not called by deterministic E2E. Enabled target-environment provider/device smoke belongs to Increment 11 production readiness and is not claimed by I1.

## 7. Test data and mocking policy

- authorization tests use at least two independent users;
- owner scope is visible in factories/fixtures;
- ORM/PostgreSQL constraints are not mocked when they are the behavior under test;
- external provider, delivery, clock and random boundaries may use deterministic fakes;
- lifecycle tests avoid real sleeps where a controllable time boundary is possible;
- timezone tests retain UTC, offset and DST-capable cases;
- real secrets/credentials never appear in fixtures.

## 8. CI policy — existing pipeline and rebuild transition

**No CI workflow or test implementation is changed by this policy edit.** Preserve all existing required checks until a separately reviewed replacement has independently shown equivalent assurance. For local work, run the relevant subset; for integrated release acceptance, run its required CI and high-risk/user-flow gates. A red required gate blocks acceptance; flaky failures must be diagnosed rather than masked by retries.

Historical v0.2.0 hosted pipeline (still-existing configuration, subject to future verified transition):

1. Locked Python/Node dependency installation.
2. Ruff, ESLint, Prettier and TypeScript.
3. Requirements traceability check.
4. Migration/schema-drift, append-only migration-history and fresh-database checks.
5. Backend/API/domain and Golden Time tests on PostgreSQL.
6. Django production deployment/security check.
7. Client component/network/time-vector tests.
8. Expo web export.
9. Desktop/mobile Playwright E2E.
10. Python/npm dependency audit and secret scan.
11. Non-root deployment container builds.
12. Container smoke and persistence after API restart.

The historical audited implementation HEAD `7302ca3b18a79af35058828102bb62e845a56645` passed run `35057831342` before subsequent documentation changes; this **is not evidence of current rebuild/CI success**.

For the Rust rebuild, choose toolchain equivalents (format/clippy/check/build, domain/API/PostgreSQL tests, contract, security/dependency, migration and critical-path E2E) with the first complete slice. Retain meaningful source behavior and authorization/integrity assertions; don't copy obsolete Django-only implementation tests merely to inflate coverage. Record which checks were actually run.

## 9. Migration and persistence verification

Existing committed migrations and their historical evidence must not be silently deleted or rewritten during process adoption. For the current Django implementation, its append-only migration guard, schema-drift, fresh PostgreSQL rebuild and `makemigrations --check --dry-run` remain effective until an approved transition.

For a Rust rebuild, specify the new migration mechanism when persistence is implemented. Verify migration application on a clean PostgreSQL database and meaningful upgrade/data-preservation paths where applicable; require recovery/rollback planning for high-risk or destructive changes. Do not claim that Django-specific gates verify Rust persistence.

## 10. Coverage and quality signals

No global line-coverage percentage, fixed test count or report count is the main gate. Prefer:

- Accepted slice scenarios with fresh independent evidence, including important negative paths.
- Cross-user permission checks and meaningful integrity/error/concurrency tests where risk demands.
- Real PostgreSQL boundary checks for affected transactions/constraints and migration paths.
- Deliberate OpenAPI/client contract review where interfaces change.
- A real critical user journey, regression of escaped defects and tracked delivery friction/rework.
- External providers, production devices, disaster recovery and live deployment explicitly marked **tested** or **not run**, never inferred from deterministic mocks.

## 11. Evidence ownership

- CI logs and focused test executions are normal evidence; no universal standalone Increment review or per-slice document is required.
- Summarize accepted outcomes, checks actually run, unrun checks and residual risks with the delivered slice/release.
- Keep historical I0/I1 readiness and [development audit](../tracking/development-commit-audit.md) as prior-implementation evidence.
- Update a contract/decision/doc only if behavior or a consequential constraint really changed. Requirements and tests must not be circularly derived from generated code.

See [Engineering Process](../development/engineering-process.md) for DoD, release planning and Agent/Git safety.

