# Dotick Deployment Baseline

> **Status:** Increment 0 deployment baseline implemented and hosted-CI verified; Increment 1 product slice verified in CI; configured external-provider/release deployment remains open
> **Reconciled:** 2026-09-20
> **Primary target:** reproducible developer-local and CI execution; self-hosting is permitted under AGPL-3.0, while guaranteed production deployment/support is a separate professional-service boundary

## 1. Deployment units

The implemented local/CI topology uses `compose.yaml` with PostgreSQL, an unprivileged ASGI API and an unprivileged server for the Expo web export. Published development ports bind to loopback.

```text
reverse proxy / TLS termination (production-like, not yet a shipped deployment)
  +-- /api -> Django ASGI API
  +-- / -> client web build

api -> PostgreSQL
```

Realtime/WebSocket infrastructure is not part of the current I1 deployment and remains owned by later increments.

## 2. Environments

| Environment | Purpose | Data/evidence |
|---|---|---|
| local-dev | fast edit/test | disposable developer data |
| test/CI | deterministic automated verification | ephemeral PostgreSQL |
| developer-local | private engineering runtime | persistent/disposable development volume |
| production-like | HTTPS/config/migration/provider rehearsal | non-production data |
| production | future Personal V1 release | not claimed by current branch |

## 3. Configuration and fail-closed production settings

Configuration comes from environment variables; `.env.example` contains names/default guidance, not real secrets.

Outside local/test, the application requires explicit:

- allowed hosts;
- CSRF trusted origins;
- CORS origins;
- JWT signing key;
- WebAuthn RP ID, RP name and HTTPS origin.

Wildcard host/origin trust is rejected. Production trusted/CORS/WebAuthn origins must use HTTPS. Secure redirect, secure cookies, HSTS and trusted proxy HTTPS-header handling are enabled in production-like settings.

The Expo bundle may contain public configuration such as a Google client ID or public API URL, but never client secrets or server signing material.

Identity delivery/provider configuration is deployment-owned:

- configure SMTP through the `DJANGO_EMAIL_*` variables and keep the host password in secret storage;
- replace the default unavailable `DOTICK_SMS_DELIVERY_ADAPTER` with a tested deployment adapter and supply its provider credentials server-side;
- set matching `GOOGLE_OAUTH_CLIENT_ID` and `EXPO_PUBLIC_GOOGLE_CLIENT_ID` values; both are public identifiers and no Google secret belongs in the client;
- set `WEBAUTHN_RP_ID`, `WEBAUTHN_RP_NAME` and `WEBAUTHN_ORIGIN` consistently with the final HTTPS application domain.

Omitting Google or leaving the SMS unavailable adapter does not break password-based core Task access, but those provider paths are unavailable and cannot satisfy release smoke. Invalid WebAuthn production-like configuration fails startup.

## 4. Images and runtime

- dependency installation is lockfile-driven;
- deployment containers run as non-root users;
- runtime config is injected rather than baked as secrets into images;
- source development bind mounts are not the release artifact;
- hosted CI builds the deployment containers and runs smoke/persistence checks.

## 5. Database lifecycle and migration policy

- PostgreSQL is the server-side system of record.
- Migrations are an explicit controlled deployment step, not a side effect of every API replica startup.
- Fresh-database migration/schema-drift verification runs in CI.
- Historical numbered migrations are append-only: existing migration files may not be modified, deleted or renamed. CI compares migration history against the relevant base ref and requires schema evolution to add a new migration.
- High-risk/destructive production evolution still requires backup, restore rehearsal and upgrade-path review.
- Rollback does not assume blind reverse migrations; restore plus the previous image may be the safe path.

## 6. Health and readiness

- `/health` is process liveness and does not expose dependency detail.
- `/ready` verifies PostgreSQL availability required by the API.
- external Google/WebAuthn/email/phone availability is not a core manual-Task readiness dependency.
- container health checks use bounded timeout/interval behavior.

## 7. Network boundary

Local loopback/LAN development may use HTTP only in explicitly trusted development scenarios. Non-local deployment is HTTPS-only at the configured origin boundary.

CORS is an explicit allowlist, does not permit wildcard origins or cross-origin credentials, and permits `If-Match` for versioned mutations for configured trusted origins.

Database ports are not intended for public exposure. Reverse-proxy trust is explicit through the configured forwarded-protocol handling.

## 8. API edge controls

Versioned `/api/v1/` write requests are constrained before view dispatch:

- JSON-only non-empty request bodies;
- 16 KiB maximum request body;
- stable errors for malformed/unsupported/oversized requests.

Sensitive identity operations are annotated in OpenAPI with `x-edge-rate-limit-policy: identity-ceremony`. [`identity-rate-limit-policy.json`](identity-rate-limit-policy.json) is the deployment contract: it lists every protected operation and defines a per-verified-client-IP burst limit of 10 requests per 60 seconds plus a sustained limit of 100 requests per 3,600 seconds. The four `DOTICK_EDGE_IDENTITY_CEREMONY_*` environment variables configure those edge thresholds.

The proxy/CDN must apply both limits collectively across the listed operations, derive client IP only from trusted connection metadata, and return `429` with `Retry-After` when either threshold is exceeded. Multi-instance enforcement needs edge/shared state. Django intentionally has no process-local substitute. Increment 11 production deployment must configure and smoke-test the policy before production release.

## 9. Logging and operations

- application/request logs are structured and include a correlation/request ID;
- only allowlisted request metadata is logged;
- credentials, tokens, request bodies and secrets are excluded from the ordinary structured request log;
- runtime/host owns log rotation/retention until a production monitoring stack is selected;
- backup, migration and readiness failures must be visible and actionable.

## 10. Hosted verification

Current CI verifies:

1. locked dependency installs;
2. static formatting/type checks;
3. traceability;
4. migration/schema drift, append-only migration history and fresh DB reconstruction;
5. backend/API/Golden Time tests against PostgreSQL;
6. production Django/security settings;
7. frontend tests and web export;
8. desktop/mobile product E2E;
9. dependency audits and secret scan;
10. non-root container builds;
11. container smoke and persistence after API restart.

Audited implementation HEAD `7302ca3b18a79af35058828102bb62e845a56645` passed hosted run `35057831342` before the documentation-reconciliation commits.

## 11. Increment 0 closure

Increment 0's deployment/verification baseline is formally closed in repository tracking. `releases/v0.1.0.md` is the repository release record for that foundation checkpoint. No public GitHub Release, public tag or production deployment is implied by that record.

## 12. Remaining Increment 1 release gates

Formal I1 release still requires target-environment evidence for:

- real email delivery;
- configured Google OAuth client/redirect flow;
- WebAuthn with the target RP ID/origins and a real browser/authenticator;
- phone verification delivery adapter;
- deployed edge rate limits matching the declared identity-ceremony policy;
- formal Increment 1 release record/publication.

Hosted CI itself is no longer an open engineering gate.

## 13. Deferred deployment choices

- production cloud/provider topology;
- horizontal scaling and HA/SLA;
- Redis/channel layer and realtime topology;
- worker/scheduler infrastructure until an owning use case exists;
- mobile store release;
- full production monitoring/alerting stack.

See [environment setup](../development/environment-setup.md), [security design](../design/security-design.md), [Increment 1 readiness](../tracking/increment-1-readiness.md), and [the full post-reset commit audit](../tracking/development-commit-audit.md).


## 14. AGPL-3.0 self-hosting and professional-services boundary

The software in this repository may be self-hosted under AGPL-3.0. That permission is distinct from an operational support commitment.

The project does not guarantee free installation assistance, production architecture review, migrations, incident response, upgrades, monitoring, backup operation, security hardening, SLA, or troubleshooting for arbitrary third-party environments. Any of those may be offered separately as paid professional services or managed hosting.

A paid services agreement changes service obligations between the parties; it does not remove or narrow software rights already granted by AGPL-3.0. The Dotick name, logos, domains, and product identity are governed separately and are not granted by the software license.
