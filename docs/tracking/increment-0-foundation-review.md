# Increment 0 implementation review

Date: 2026-09-09. Scope: roadmap §§7.1–7.6 engineering foundation.

**Status: CLOSED.** Increment 0 is implemented on branch `test` at implementation commit `88aa5986a5673224a3d4ea78fca164f742e9d83e`. Hosted GitHub Actions run `34330581198` completed successfully against that commit and passed every configured foundation gate.

## Delivered

- Locked Python 3.14 / Django / DRF / PostgreSQL and Node 24 / Expo / React Native for Web workspaces.
- Custom UUID user model before the initial migration, Argon2 password hashing, and case-insensitive email uniqueness.
- Disposable developer-only Foundation Checkpoints with authenticated owner-scoped create/list/read, strict validation, stable error envelopes, request IDs, no-store responses, bounded request bodies, and structured allowlisted logging.
- Golden Time Vector execution for UTC normalization, timezone offsets, DST gaps/overlaps, 23/24/25-hour all-day intervals, skipped calendar days, and Gregorian-to-Jalali conversion.
- A real responsive Walking Skeleton client replacing the default Expo screen.
- Developer-only sign-in against the Foundation REST API. Credentials exist only in React memory; they are not written to browser storage or persisted across reloads.
- Sign-out clears credentials, private checkpoint state, draft state, errors/notices, and the password field.
- Checkpoint create/list UI with loading, error, retry, refresh, draft-preservation-on-failure, and successful retry behavior.
- End-to-end `Client → REST → Application → ORM → PostgreSQL → Client` persistence flow.
- Vitest + Testing Library component/network tests and Playwright desktop/mobile E2E coverage.
- Backend and web Docker images, non-root runtime users, and Compose topology for PostgreSQL + API + web.
- GitHub Actions gates for locked installs, Ruff, ESLint, Prettier, TypeScript, schema drift, clean migrations, backend tests, frontend tests, web export, E2E, dependency audits, secret scan, Django deployment checks, container builds, container smoke, and restart persistence.

## Hosted verification

| Gate | Result |
|---|---|
| Clean hosted checkout | Passed; GitHub Actions initialized a clean checkout of `88aa5986` |
| Python locked install | Passed with `uv sync --frozen` from `uv.lock` |
| Frontend locked install | Passed with `npm ci` from `package-lock.json` |
| Ruff | Passed |
| ESLint | Passed |
| Prettier check | Passed |
| TypeScript check | Passed |
| Traceability | Passed; 419 unique requirements with exact coverage and valid decision references |
| Schema drift | Passed; `makemigrations --check --dry-run` reported no changes |
| Existing PostgreSQL migration graph | Passed; all migrations applied and `showmigrations` reported applied entries |
| Clean-database migration | Passed against a separately created empty PostgreSQL database, then dropped |
| Django backend suite | 30 tests passed |
| Golden Time backend suite | 14 tests passed |
| Client component/network/calendar suite | 8 tests passed |
| Client web export | Passed |
| Walking Skeleton E2E | 2 tests passed: desktop Chrome and mobile iPhone-13 viewport |
| Reload and re-sign-in persistence | Passed in both E2E projects |
| Django `check --deploy` | Passed with Foundation workbench disabled in production mode |
| Python dependency audit | Passed; no known vulnerabilities reported |
| npm dependency audit | Passed at high-severity gate; 10 moderate Expo/native-tooling transitive findings remain reviewed debt |
| Secret scan | Passed; Gitleaks reported no committed leaks |
| API image build | Passed |
| Web image build | Passed |
| Non-root runtime | Passed for both API and web containers |
| Container smoke | Passed |
| Persistence after API restart | Passed; a created Checkpoint remained retrievable after restarting the API container |
| Hosted CI | **Green** — run `34330581198` |

## Self-review

The Increment 0 implementation was reviewed against its intended boundary rather than future product behavior.

- Foundation Checkpoints remain a neutral disposable verification resource and do not establish Task, Event, Routine, recurrence, history, sync, or deletion semantics.
- HTTP Basic is limited to the local/test Foundation workbench and is not presented as product authentication.
- Client credentials are stored only in component memory. Reloading requires a new developer sign-in, and sign-out removes private client state.
- Failed API saves preserve the checkpoint draft; a later retry can persist the same text.
- Foundation reads are owner-scoped and cross-user access remains hidden.
- Golden Time tests consume the shared `docs/design/time-vectors.json` catalog rather than duplicating expected values in test code.
- `owning_increment_vectors` for recurrence and Dotick-Day behavior remain acceptance handoffs to I4/I10; Increment 0 does not falsely claim those product behaviors as implemented.
- Production settings keep the Foundation workbench disabled and pass Django deployment checks.
- The newer backend hardening already present on `test` was preserved while the verified I0 client, temporal, container, E2E, and CI pieces were selectively ported from the exact Codex I0 snapshot (`02e41e3`) rather than merging later Increment 1 implementation.

## Intentional technical debt

| ID | Debt | Rationale / owner |
|---|---|---|
| TD-I0-001 | Developer-only HTTP Basic transport | Intentionally temporary for the isolated Foundation Walking Skeleton; replaced by product authentication in I1. |
| TD-I0-002 | Foundation `Checkpoint` resource | Deliberately disposable engineering evidence, not a product Item model. Product domain persistence belongs to owning increments. |
| TD-I0-003 | 10 moderate npm audit findings in Expo/native tooling transitive dependencies | No high/critical finding blocks I0. The available forced remediation would introduce an inappropriate breaking Expo change; review during framework/toolchain upgrades. |
| TD-I0-004 | Web-focused Walking Skeleton | Native distribution, installable PWA/offline behavior, and product UI belong to later owning increments. |
| TD-I0-005 | No production release/tag/deployment claim | This Increment closes the engineering foundation gates only. Public release publication and production operational readiness are separate lifecycle actions. |

## Closure decision

All Increment 0 engineering gates requested for the Foundation baseline have executable evidence and the hosted CI run is green. No remaining item in the Increment 0 gate list blocks continuation to Increment 1.

**Increment 0 is formally closed as of 2026-09-09.**
