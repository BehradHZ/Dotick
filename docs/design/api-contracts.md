# API Contracts

> **Status:** Increment 1 published backend contract implemented and CI-guarded
> **Reconciled:** 2026-09-16

`docs/design/openapi.json` is the executable OpenAPI 3.1 handoff for every currently published product route. The contract covers Identity, Account, Folder/List/Column, Task scheduling/priority and Trash/restore boundaries. Foundation workbench routes are deliberately outside the published product contract.

## Contract rules

- Product endpoints use the `/api/v1/` prefix.
- Request/response bodies use JSON unless an endpoint explicitly documents no body.
- `/api/v1/` writes are subject to the shared JSON transport boundary: non-JSON bodies are rejected, malformed JSON returns the stable parse-error surface, and request bodies are capped at 16 KiB.
- Request serializers reject unknown fields rather than silently ignoring client mistakes.
- Public failures use the stable envelope `{"error": {"code": ..., "details": ...}}`.
- Private resources are resolved from the authenticated account scope before serialization or mutation; a client-supplied owner/source cannot grant access.
- JWT sessions provide the current I1 authentication transport; provider credentials resolve to the same internal User/session model.
- Versioned mutations use the documented optimistic-concurrency preconditions. CORS explicitly permits `If-Match` for the trusted product origin set without enabling wildcard origins or credentialed cross-origin requests.
- Success status codes and empty-body responses are part of the OpenAPI operation contract; `204` responses do not carry JSON payloads.
- Identity-sensitive ceremonies are annotated with `x-edge-rate-limit-policy: identity-ceremony`. The annotation declares the required deployment-edge policy; it is not, by itself, an in-process rate limiter implementation.

## Published I1 route families

The current contract includes:

- email registration/verification/resend, password sign-in/reset/change and logout/session/token operations;
- Google sign-in/linking;
- Passkey registration/authentication/list/delete;
- account detail, bootstrap and verified-contact lifecycle;
- Folder, List and Column operations;
- Task create/read/edit/move/status/schedule/priority/delete/restore;
- owner-scoped Trash queries and Folder/List/Task restore.

Routes for Event, Routine, collaboration, full sync/history and later-Increment capabilities are intentionally absent until their owning Increment.

## Organization mutation contract

Folder, List and Column responses expose a positive server-owned `version`. Clients must preserve the latest returned representation and use its version as the precondition for the next mutation.

| Operation | Precondition | Success | Retry/conflict behavior |
|---|---|---|---|
| Create Folder/List/Column | client-generated `operation_id` UUID in JSON | `201` with version `1` for the first committed creation | same owner, resource type, operation ID and immutable intent returns the original resource with `200`; changed intent returns `409 idempotency_conflict` |
| Update Folder/List/Column | positive current `version` in JSON | `200`; server atomically increments version | stale version returns `409 version_conflict` with current resource ID/version |
| Delete/Trash Folder/List/Column | positive current version in `If-Match`; quoted and unquoted decimal forms are accepted | `204` | stale version returns `409`; retry only after refetching and reapplying the user's intent |
| Restore Folder/List | positive current `version` in JSON | `200`; server atomically increments version | stale version returns `409 version_conflict` |

Create idempotency is scoped by authenticated owner, resource type and `operation_id`. The same UUID may therefore be used independently by another owner or for another resource type. Immutable intent is calculated from normalized create inputs: Folder title; List title/folder/explicit position; or Column parent List/title. Omitted List position and an explicit position are different intents because retry must reproduce the original request, not reinterpret current ordering.

The first create and its `OrganizationCreateOperation` record commit atomically. Concurrent identical requests serialize on a transaction-scoped PostgreSQL advisory lock: one returns `201`, the other resolves the stored operation and returns `200`. A retry never creates a second resource. If the stored result no longer exists within the same owner/type scope, replay returns `404` instead of silently creating a replacement.

Optimistic version checks run inside a transaction while locking the owned row. Versions are never accepted as replacement state, never decrease, and advance once for each accepted resource mutation. Folder/List cascades may also advance affected descendant List/Item versions. I1 versions are concurrency tokens only; they are not Sync vectors, audit entries or branching History.

All organization reads and mutations remain owner-scoped. Unknown and foreign identifiers share the `404` surface. The Inbox cannot be renamed or deleted, the default Column cannot be deleted, and destructive container/Column operations require the documented child-Item resolution when active Items exist.

## Executable drift guards

`apps/api/tests/test_openapi_contract.py` treats the committed document as a reviewed artifact and verifies all of the following:

1. the document validates as OpenAPI 3.1;
2. local references and operation identifiers remain valid/stable;
3. the reviewed canonical contract hash changes only with an intentional test update;
4. the set of documented paths exactly equals Django's published non-foundation `/api/v1/` route set;
5. the stable error schema remains present;
6. operations classified as identity ceremonies carry the edge-rate-limit policy extension.

Transport/security tests separately cover unknown input, stable errors, malformed/non-JSON/oversized request rejection and trusted/untrusted CORS behavior.

Any endpoint, schema, status/error contract or identity-ceremony classification change must update implementation, `openapi.json` and its contract tests in the same reviewed change.

See [the development commit audit](../tracking/development-commit-audit.md) for the history reconciliation that produced this status.
