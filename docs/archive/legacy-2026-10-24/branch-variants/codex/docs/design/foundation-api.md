# Increment 0 API contract

Status: implemented developer-only walking skeleton, 2026-09-06.

This disposable checkpoint resource proves the client → REST → application → PostgreSQL → response path required by roadmap §7.5. It is not an Item, Task, Event, or Routine and does not define product authentication, sync, history or deletion semantics.

| Method and path | Result |
|---|---|
| `GET /health` | `200 {"status":"ok"}` without database access |
| `GET /ready` | `200 {"status":"ready"}` or generic `503 {"status":"unavailable"}` after a database probe |
| `GET /api/v1/foundation/checkpoints` | `200 {"results":[...]}`; actor's latest 100 records, newest first |
| `POST /api/v1/foundation/checkpoints` | `201` checkpoint; accepts only `{"text":"..."}`, trimmed, 1–240 characters |
| `GET /api/v1/foundation/checkpoints/{id}` | `200` checkpoint or `404` for missing/out-of-scope IDs |

A checkpoint contains only UUID `id`, `text`, and UTC ISO timestamp `created_at`. Ownership comes from the authenticated actor and is never accepted from request input. UUID identity and creation time survive retrieval. Writes are transactional; `foundation_checkpoints` is separate from future domain tables.

Private endpoints require a developer account via HTTP Basic. The client retains credentials in memory only and erases its private screen state on sign-out. This temporary adapter is enabled only when `DOTICK_ENV=local|test` **and** `DOTICK_FOUNDATION_ENABLED=1`; production refuses to start with that flag enabled. Use loopback HTTP for developer-local execution. It does not substitute for I1 JWT, Google OAuth, Passkey, email verification or recovery.

Invalid input returns `400`; unsupported content type `415`; missing/invalid credentials `401`; bodies larger than 16 KiB `413`. Errors use `{"error":{"code":"...","details":...}}`, with optional details only for expected validation/auth errors. Internal errors never return exception text. Responses include a server-generated request ID and `Cache-Control: no-store`. Structured logging uses an explicit field allowlist and excludes bodies, credentials and exception messages.

Evidence: API/authorization tests in `apps/api/tests`, component network/failure tests in `apps/client/src/App.test.tsx`, and desktop/mobile PostgreSQL persistence checks in `e2e/walking-skeleton.spec.ts`.
