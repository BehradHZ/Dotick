# Dotick Architecture Baseline

> **Status:** Increment 0 closed; Increment 1 backend and minimal product client implemented and hosted-CI verified
> **Reconciled:** 2026-09-16
> **Decision sources:** DR-051, DR-052; client scope DR-066
> **Scope:** Personal V1; implemented I0/I1 boundaries only

## Purpose and authority

This document records the implemented technical architecture. It does not redefine product behavior. System Definition -> Decision Register -> SRS remains authoritative when implementation evidence and product behavior differ.

## Architecture style

Dotick is a modular monolith with an independent Expo client and a versioned REST/JSON API backed by PostgreSQL.

```text
Expo / React Native / Web client
        |
        | HTTPS + JSON REST
        v
Django ASGI modular monolith
        |
        +--> PostgreSQL
        +--> external identity/delivery adapters
```

Current backend capability modules are `foundation`, `identity`, `organization`, `items`, and `tasks`. Modules for Event, Routine, collaboration, full sync/history, AI and other later-Increment capabilities are intentionally not created before their owning Increment.

Application services own transaction and authorization orchestration. Interface code does not define domain policy, and provider adapters do not own User identity.

## Technology baseline

| Area | Implemented baseline |
|---|---|
| Backend | Python 3.14, Django 5.2 LTS, Django REST Framework, ASGI |
| Client | TypeScript, Expo SDK 57, React Native, React Native for Web |
| Database | PostgreSQL |
| Authentication transport | short-lived JWT plus database-backed revocable session state |
| Dependency management | `uv.lock` and `package-lock.json` |
| Packaging | non-root Docker images + Compose |
| Contract | committed OpenAPI 3.1 document with executable drift guards |

Exact package patch versions are owned by manifests/lockfiles rather than prose.

## Increment 0 foundation

Increment 0 is formally closed and established the real client -> API -> application -> ORM -> PostgreSQL -> response path, health/readiness endpoints, safe structured request logging, Golden Time execution, component/E2E tests, reproducible containers and hosted CI. The foundation Checkpoint workbench is developer-only and no longer powers the product UI.

## Increment 1 capability boundaries

### Identity and account

One stable UUID User is shared by password, Google and Passkey credentials. Profile fields, IANA timezone preferences, verified secondary contacts and revocable sessions extend that account without creating provider-specific ownership identities. External providers stay behind adapters.

### Organization

Folder, List and Column are explicit entities. A List may have no Folder. Inbox is a special List. Database constraints enforce at most one Inbox per owner and at most one default Column per List; application write paths create the required Inbox/default Column and create each new List with its default Column transactionally.

No `Tab` or `Section` entity exists in I1. The legacy `not_sectioned` concept is not a public model/contract.

### Item and Basic Task

Item owns shared identity/ownership/version/source metadata; Task is explicit one-to-one composition and owns Task status. Each Task has exactly one Column, with List derived through that Column. Mutations validate the authenticated owner and destination inside the write boundary.

Basic Task provides unscheduled create/read/edit/move, Todo/Done/Won't_Do, optimistic versions, idempotent creation and recoverable Trash/restore.

## API and security boundaries

`docs/design/openapi.json` is the executable published I1 contract. CI verifies OpenAPI 3.1 validity, a reviewed canonical contract hash, and exact equality with the non-foundation Django `/api/v1/` route set.

The current API boundary also enforces stable error envelopes, unknown-field rejection, JSON-only versioned write bodies, a 16 KiB request limit, malformed-request rejection, explicit trusted-origin CORS behavior and `If-Match` support for versioned mutations.

Production-like settings require explicit host/CSRF/CORS allowlists and HTTPS non-local origins. Identity-sensitive operations are classified in OpenAPI for deployment-edge rate limiting; deployment enforcement is a release concern rather than a second application authorization model.

## Data and migration boundaries

- PostgreSQL is the server-side system of record.
- Persisted identities use UUIDs independent of display title/position.
- Critical cardinality/integrity rules use database constraints and navigation access paths use explicit indexes.
- Mutable Item state uses server-owned optimistic versions; full branching history/offline reconciliation remains I6.
- Ordinary Trash preserves recovery metadata rather than treating delete as immediate permanent destruction.
- Historical numbered migrations are append-only; CI rejects changing, deleting or renaming an existing migration. Schema evolution adds a new migration.

## Client boundary

The Expo product client now exercises the I1 account-to-Task path: signed-out email flows, sign-in/bootstrap, Inbox/List navigation, List/Task creation, Task editing/status/move/Trash/restore, refresh/sign-out and configured web Google/Passkey entry points. Tokens intentionally remain session-memory only.

## Reliability and observability

- `/health` is process liveness and `/ready` checks required PostgreSQL readiness.
- structured request logs use correlation IDs and an allowlist that excludes credentials/tokens/bodies;
- provider failure remains isolated from the core manual Task path;
- retry behavior requires use-case-specific idempotency instead of a premature global queue abstraction.

## Quality gates

Hosted CI currently covers locked installs, static checks, traceability, migration/schema/fresh-database and append-only-history checks, backend/API/Golden Time tests, production settings, frontend tests, web export, desktop/mobile E2E, dependency audits, secret scan, non-root container builds and persistence smoke.

Audited implementation HEAD `7302ca3b18a79af35058828102bb62e845a56645` passed run `35057831342` before the documentation-reconciliation commits.

## Deferred scope and remaining I1 release gates

Event/Routine, rich hierarchy/descriptions/comments/audit, collaboration/realtime, full offline sync/history/undo, AI and later product capabilities remain in their owning increments.

Formal I1 closure still requires configured target-environment email, Google, real WebAuthn authenticator and phone-delivery smoke, deployment-edge rate-limit enforcement, and a formal I1 release record/publication. No production deployment or public GitHub Release is claimed.

See [API contracts](api-contracts.md), [security design](security-design.md), [Increment 1 readiness](../tracking/increment-1-readiness.md), and [the full development commit audit](../tracking/development-commit-audit.md).
