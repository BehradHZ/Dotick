# Increment 1 backend review

Date: 2026-09-08. Result: locally complete backend checkpoint; not an Increment 1 release. Client work completed later the same day is recorded separately in [Increment 1 client review](increment-1-client-review.md).

## Delivered boundary at the checkpoint

- product identity: verified email/password/reset, rotating revocable JWT sessions, Google ID assertion/linking, discoverable user-verified Passkeys, independent password fallback and verified secondary contacts;
- account: UUID identity, mutable unique handle, display name, optional profile-picture reference and shared IANA timezone;
- organization: concurrent-idempotent Inbox/default-Column bootstrap, optional Folder, List and Column CRUD/manual ordering, explicit owner scope and recoverable Folder/List deletion;
- Task: explicit Item/Task/Source composition, stable UUID, manual provenance, create/read/edit/move, Todo/Done/Won't_Do, optimistic version conflict, idempotent create and Trash/restore;
- contract: every published I1 backend route and stable failure class is represented in the validated OpenAPI 3.1 artifact.

## Local verification evidence recorded on 2026-09-08

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

## Historical non-claims at that checkpoint

At the moment this review was written, the product-client and hosted-release evidence had not yet caught up with the backend checkpoint. Those statements are preserved as historical context rather than silently rewritten.

- The product Expo client had not yet been credited with I1 product identity/organization/Task acceptance in this review.
- Configured Google credentials, real WebAuthn browser/authenticator registration, real email transport and phone delivery still required deployment-specific smoke evidence.
- Hosted CI/release publication were not yet credited here.
- Scheduling, Event/Routine, Audit/History, full Offline/Sync, collaboration and permanent Trash purge remained later-Increment scope.

## Post-review reconciliation — 2026-09-16

The first and third historical non-claims above are now superseded by later commits and current branch evidence:

- The Expo product client now exercises the I1 account-to-Task slice, including signed-out email flows, sign-in/bootstrap, Inbox/List navigation, Task create/edit/status/move/Trash/restore and real API/PostgreSQL persistence.
- Desktop and mobile Playwright workflows now exercise that product path; the I0 workbench is no longer the product UI.
- Hosted CI run `35057831342` succeeded against audited implementation HEAD `7302ca3b18a79af35058828102bb62e845a56645` before this documentation reconciliation.
- I0 is already formally closed in repository tracking.
- The OpenAPI contract is now additionally guarded by a reviewed canonical hash and exact equality with the published Django I1 route set.
- API hardening now includes stable error codes, strict unknown-field handling, JSON-only versioned request boundaries, a 16 KiB body cap, malformed-request rejection, explicit CORS support for `If-Match`, production host/origin/HTTPS guards and identity-ceremony edge rate-limit declarations.
- Organization query paths include the explicit List `(folder, position)` index.
- Historical numbered migrations are protected by an append-only CI gate; existing migrations may not be changed, deleted or renamed.

The configured external-provider/delivery statement remains current: real target-environment email, Google, WebAuthn authenticator and phone-delivery smoke are still required, as is formal Increment 1 release/publication. Later-Increment scope remains deferred.

For the full post-reset history reconciliation, see [development-commit-audit.md](development-commit-audit.md).
