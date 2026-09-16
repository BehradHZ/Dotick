# API Contracts

> **Status:** Increment 1 published backend contract implemented and CI-guarded
> **Reconciled:** 2026-09-16

`docs/design/openapi.json` is the executable OpenAPI 3.1 handoff for every currently published Increment 1 product route. The contract covers Identity, Account, Folder/List/Column, Basic Task and Trash/restore boundaries. Foundation workbench routes are deliberately outside the published I1 product contract.

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
- Basic Task create/read/edit/move/status/delete/restore;
- owner-scoped Trash queries and Folder/List/Task restore.

Routes for Event, Routine, collaboration, full sync/history and later-Increment capabilities are intentionally absent until their owning Increment.

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
