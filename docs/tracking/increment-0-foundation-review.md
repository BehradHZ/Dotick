# Increment 0 implementation review

Date: 2026-09-06. Scope: roadmap §§7.1–7.6 engineering foundation.

Status: implementation and local verification complete; hosted CI execution and release remain pending. Increment 1 product implementation has not started; its [readiness baseline](increment-1-readiness.md) is prepared. This is a working foundation, not the completed Dotick product.

## Delivered

- Locked Python/Django/DRF/PostgreSQL and TypeScript/Expo 57/React Native for Web workspaces.
- Custom UUID user model before the initial migration, Argon2 hashing, and case-insensitive email uniqueness.
- Disposable developer-only checkpoints, with authenticated owner-scoped create/list/read, explicit transaction, strict input, and stable UUID/UTC metadata.
- Responsive workbench drawing paper/orange/black-border styling from the supplied prototype; real API states, draft-preserving errors, refresh and sign-out.
- Health/readiness, bounded input, generic errors, request IDs, private/no-store responses and structured logs without payloads or credentials.
- Time Semantics baseline, executable UTC/DST/all-day/Jalali vectors and explicit I4/I10 acceptance handoffs.
- CI workflow, dependency/secret checks, nonroot container builds and loopback-only developer Compose topology.
- Current document/decision links and SRS-to-matrix coverage, including the previously untraced `SRS-SHARE-034` (419 requirements total).

## Verification

| Check | Result |
|---|---|
| Python test suite | 33 passed against PostgreSQL 18.4; includes actual database-outage readiness, owner isolation, validation, hashing, time vectors and production workbench rejection |
| Client component/calendar tests | 8 passed |
| TypeScript, ESLint, Prettier, Ruff | Passed |
| Schema drift check and clean database migrations | Passed |
| Desktop/mobile E2E | 2 passed; saved data survives browser reload and fresh sign-in; no page errors or horizontal overflow |
| Container build from locked dependencies | API and web images built successfully with isolated dependency installation |
| Clean Git clone | Commit `02e41e3`, fresh virtual environment/npm install and separate PostgreSQL 18.4 volume: migrations, 33 API tests, 8 client tests, static checks, web export and 2 desktop/mobile E2E passed; servers started from the clone with existing-server reuse disabled |
| Container smoke | Clean PostgreSQL migration, account provisioning and desktop/mobile persistence workflow passed; API and web run as nonroot |
| Production settings inspection | Django `check --deploy --fail-level WARNING` passed with workbench disabled |
| Traceability | 419 unique SRS IDs, exact matrix coverage, valid explicit decision references |
| Python dependency audit | No known vulnerabilities reported |
| npm dependency audit | No high/critical findings; ten moderate entries from one native-tooling advisory, reviewed in `docs/quality/foundation-dependency-review.md` |
| Source secret scan | Gitleaks v8.28.0 reported no leaks in the current source snapshot |
| Hosted CI / release | Workflow added; no remote run or release claimed |

Windows verification used Python 3.14.5, Node 24.19.0, npm 11.17.0 and installed Chrome. The Playwright Chromium download returned a regional 403, so the documented Chrome channel was used for local E2E. Docker images also built on Linux with clean lockfile installs. CI installs its own matching Chromium build.

## Readiness decisions and limits

The roadmap explicitly permits a disposable neutral resource for I0. Checkpoints are not Items and do not establish product status, persistence, history, sync, or deletion behavior. HTTP Basic and developer provisioning are isolated temporary transports; the workbench cannot be enabled under production settings. There is no demo bypass that chooses an actor from a client-supplied ID.

The prototype HTML remains unchanged. Native client release, PWA install/offline mechanics, provider credentials, product authentication and Task/Event/Routine screens have not been claimed complete. All remain with their roadmap owners.

Before I1 persistence/API design is finalized, reconcile the older data-table proposals with current System Definition and I6 compatibility requirements: stable IDs, version ordering, tombstones/restore, idempotency, history branches and server-current authorization. In particular, do not copy the older container cascade or deletion proposals mechanically into migrations.

Next implementation scope is roadmap Increment 1: identity (email/password, Google and Passkey), preferences/timezone, Folder/List/Column and Inbox invariants, and the basic Task MVP. Its [readiness baseline](increment-1-readiness.md) records canonical corrections, I6 compatibility and public-boundary acceptance scenarios. A hosted green CI run and completed increment release record are still required to formally close I0 under the roadmap's completion rule. The [v0.1.0 candidate](../../releases/v0.1.0.md) is prepared, not published or tagged.
