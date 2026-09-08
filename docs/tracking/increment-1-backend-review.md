# Increment 1 backend review

Date: 2026-09-08. Result: locally complete backend checkpoint; not an Increment 1 release. Client work completed later the same day is recorded separately in [Increment 1 client review](increment-1-client-review.md).

## Delivered boundary

- product identity: verified email/password/reset, rotating revocable JWT sessions, Google ID assertion/linking, discoverable user-verified Passkeys, independent password fallback and verified secondary contacts;
- account: UUID identity, mutable unique handle, display name, optional profile-picture reference and shared IANA timezone;
- organization: concurrent-idempotent Inbox/default-Column bootstrap, optional Folder, List and Column CRUD/manual ordering, explicit owner scope and recoverable Folder/List deletion;
- Task: explicit Item/Task/Source composition, stable UUID, manual provenance, create/read/edit/move, Todo/Done/Won't_Do, optimistic version conflict, idempotent create and Trash/restore;
- contract: every published I1 backend route and stable failure class is represented in the validated OpenAPI 3.1 artifact.

## Local verification evidence

- `pytest`: 65 API/domain tests passed against PostgreSQL, including concurrent bootstrap, cross-account denial, stale-version/idempotency conflicts, provider simulations and WebAuthn option generation;
- `ruff check` and `ruff format --check`: passed for API and scripts;
- `makemigrations --check --dry-run`: no model/migration drift;
- development database migration: identity `0004..0007`, organization, items and tasks applied successfully;
- production Django deploy check with production-mode settings: no warnings;
- OpenAPI 3.1 validation and exact published-route-set check: passed;
- traceability checker: 419 unique requirements, exact family coverage and valid decision references;
- `pip-audit`: no known Python dependency vulnerabilities;
- API container built from the frozen lock and the container reported no pending migrations;
- unchanged client regression gates: ESLint, Prettier, TypeScript, 8 component tests and Expo web export passed;
- existing I0 Walking Skeleton: desktop and mobile Playwright runs passed using the documented installed-Chrome fallback.

## Explicit non-claims and remaining gates

- The product Expo client still uses the I0 workbench; it does not yet exercise the I1 product identity/organization/Task API.
- Google credentials, real WebAuthn browser/authenticator registration, real email transport and phone delivery require deployment-specific configuration and smoke evidence.
- The existing E2E proves the I0 checkpoint path, not I1-AC-04/05/10 product-client acceptance.
- Hosted CI, Increment review/release publication and the pre-existing I0 hosted gates remain open.
- Scheduling, Event/Routine, Audit/History, full Offline/Sync, collaboration and permanent Trash purge retain their later owning increments.

The backend can now be committed as a bounded milestone. Increment 1 closes only after the remaining client, configured-provider and release evidence is green.
