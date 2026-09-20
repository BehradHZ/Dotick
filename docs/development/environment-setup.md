# Development environment

> **Status:** Increment 0 closed; Increment 1 backend/minimal product client implemented and hosted-CI verified
> **Reconciled:** 2026-09-20

Run commands from the repository root.

## Prerequisites

- Python 3.14; runtime version is pinned by `.python-version`/lock metadata.
- Node.js 24 LTS and npm workspace; versions are pinned by `.node-version`, `package.json` and `package-lock.json`.
- Docker with Linux containers for the reproducible PostgreSQL/container path.
- Git with enough history for migration-history checks.
- Dependencies are installed from `uv.lock` and `package-lock.json`.

## Initial setup

```text
python -m pip install uv==0.12.9
python scripts/init_local.py
python -m uv sync --frozen
npm ci
docker compose up -d postgres
python -m uv run python apps/api/manage.py migrate --noinput
python -m uv run python apps/api/manage.py create_developer
```

The initializer creates ignored local secrets without overwriting existing values. The developer account is `developer@example.test`; its password comes from `DOTICK_DEVELOPMENT_PASSWORD` in `.env`. Provisioning refuses to silently replace an existing account password.

Tests create and destroy `test_<PGDATABASE>` databases, so the development PostgreSQL role needs `CREATEDB`. Never point test commands at production.

## Identity provider and delivery configuration

Copy variable names from `.env.example`, but inject production secrets through deployment secret storage. Every `EXPO_PUBLIC_*` value is bundled into browser/native client code and is public by definition.

### Email

`DJANGO_EMAIL_BACKEND` selects the Django backend. SMTP uses `DJANGO_EMAIL_HOST`, `DJANGO_EMAIL_PORT`, optional paired `DJANGO_EMAIL_HOST_USER`/`DJANGO_EMAIL_HOST_PASSWORD`, `DJANGO_EMAIL_USE_TLS`, `DJANGO_EMAIL_USE_SSL`, and `DJANGO_DEFAULT_FROM_EMAIL`. The port must be between 1 and 65535; TLS and SSL cannot both be enabled; username and password must be supplied together. The local in-memory backend is suitable only for tests. Missing or failed contact-email delivery returns `503 contact_delivery_unavailable`; real registration/reset and contact delivery must still be smoke-tested in the target environment.

### SMS

`DOTICK_SMS_DELIVERY_ADAPTER` is a non-empty dotted import path to a deployment adapter implementing `send_verification_code(phone_number, code)`. The checked-in `dotick.identity.sms.UnavailableSmsDeliveryAdapter` is a deliberate safe default: phone contacts stay pending and the API returns `503 contact_delivery_unavailable`. Provider credentials belong to the adapter's server-only environment configuration, not this repository or the Expo bundle.

### Google

Google web sign-in uses the same public OAuth client ID in backend `GOOGLE_OAUTH_CLIENT_ID` and client `EXPO_PUBLIC_GOOGLE_CLIENT_ID`. The browser credential flow needs no Google client secret. If the backend ID is absent, Google authentication returns `503 provider_unavailable` without contacting Google; if the public ID is absent, the client hides Google sign-in. Independent email/password sign-in remains available.

### WebAuthn

Passkeys use `WEBAUTHN_RP_ID`, `WEBAUTHN_RP_NAME` and `WEBAUTHN_ORIGIN`. Local/test defaults use RP ID `localhost`, RP name `Dotick`, and `http://localhost:8081`. Non-local environments must set all three values explicitly. The origin must be a bare HTTPS origin with no credentials, path, query or fragment, and its host must equal the RP ID or be its subdomain. HTTP is accepted only for `localhost` development. Invalid configuration stops application startup.

### Identity ceremony edge limits

The four `DOTICK_EDGE_IDENTITY_CEREMONY_*` variables define the deployment-edge baseline: 10 requests per 60 seconds and 100 requests per 3,600 seconds, collectively across the operations in [`identity-rate-limit-policy.json`](../operations/identity-rate-limit-policy.json), keyed by verified client IP. Django intentionally does not read these as an in-process limiter. Configure them in the proxy/CDN, use only trusted connection metadata for client IP, and return `429` with `Retry-After` when either threshold is exceeded.

Email/SMS services are optional and unconfigured by default. Enabled real delivery, Google, WebAuthn authenticator and deployment-edge threshold smoke are Increment 11 production-readiness inputs, not I1 local setup requirements.

## Host/origin configuration

Local development defaults to explicit loopback allowlists. Outside local/test:

- `DJANGO_ALLOWED_HOSTS` is required and may not contain `*`;
- `DJANGO_CSRF_TRUSTED_ORIGINS` is required and must use HTTPS;
- `DJANGO_CORS_ORIGINS` is required and must use HTTPS;
- WebAuthn origin must use HTTPS.

The API CORS policy allows the `If-Match` header required by versioned mutations for configured trusted origins; wildcard origins and cross-origin credentials are disabled.

## Run the client and API

API:

```text
python -m uv run uvicorn config.asgi:application --app-dir apps/api --host 127.0.0.1 --port 8000 --no-access-log
```

Client:

```text
npm run dev
```

Open `http://127.0.0.1:8081`. The product flow supports sign-in/bootstrap, Inbox/List navigation, Basic Task create/edit/status/move/Trash/restore and PostgreSQL persistence. Client tokens are intentionally session-memory only, so a browser/app restart can require sign-in again.

The web client defaults to `http://127.0.0.1:8000`. To override it, set `EXPO_PUBLIC_API_URL` and keep `DJANGO_CORS_ORIGINS` aligned. Expo public variables are bundled into the client and must contain no secrets.

### Expo Go on a phone

Keep phone and computer on the same trusted private network. Find the host LAN IPv4 address, add it explicitly to the API host allowlist, and bind the API to the LAN interface:

```text
Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -notlike '127.*'}
$env:DJANGO_ALLOWED_HOSTS='127.0.0.1,localhost,<LAN-IP>'
python -m uv run uvicorn config.asgi:application --app-dir apps/api --host 0.0.0.0 --port 8000 --no-access-log
```

Then:

```text
npm run start:mobile --workspace @dotick/client
```

The client normally derives the API address from Expo's LAN host. If necessary, enter `http://<LAN-IP>:8000` in the sign-in screen API-address field. This HTTP/LAN path is for trusted development only; it is not the non-local production security model.

## Run built containers

```text
docker compose build
docker compose up -d postgres
docker compose run --rm api python apps/api/manage.py migrate --noinput
docker compose run --rm api python apps/api/manage.py create_developer
docker compose up -d api web
```

Published local Compose ports bind to loopback. Migrations are explicit deployment steps rather than automatic side effects of every API process startup.

## Verification commands

```text
python scripts/check_traceability.py
python -m uv run ruff check apps/api scripts
python -m uv run ruff format --check apps/api scripts
python scripts/check_migrations.py
python -m uv run python apps/api/manage.py makemigrations --check --dry-run
python -m uv run python apps/api/manage.py migrate --noinput
python -m uv run python apps/api/manage.py showmigrations
python -m uv run python scripts/verify_clean_database.py
python -m uv run python apps/api/manage.py test dotick
python -m uv run pytest
npm run lint
npm run format:check
npm run typecheck
npm test
npm run build
npx playwright install chromium
npm run test:e2e
python -m uv run pip-audit
npm audit --audit-level=high
```

### Append-only migration history

`scripts/check_migrations.py` now checks two things:

1. historical numbered migrations are append-only; existing migration files may not be modified, deleted or renamed;
2. Django reports no migration/model drift.

Locally, the append-only comparison defaults to the previous commit when no base is supplied. CI sets `MIGRATION_BASE_REF` to the pull-request base SHA or the previous push SHA and checks the full change range. If a schema change is required, add a new migration instead of rewriting history.

`verify_clean_database.py` creates a unique empty PostgreSQL database, applies all migrations, confirms no unapplied migration remains, prints migration state and removes the temporary database even after failure.

## E2E notes

The E2E runner starts the API and exported web server when they are not already running. It uses a provisioned test/developer account and an ephemeral CI database. If Playwright's bundled Chromium cannot be downloaded locally but Chrome is installed, `PLAYWRIGHT_CHANNEL=chrome` is the documented local fallback; hosted CI installs its matching browser.

If port `8081` is unavailable, set `DOTICK_E2E_WEB_PORT` to a free loopback port and add the corresponding origin to the CORS configuration for that test process.

## Production configuration check

For a production-like settings validation, provide explicit HTTPS origins/hosts and required signing secrets, set `DOTICK_ENV=production` and `DOTICK_FOUNDATION_ENABLED=0`, then run:

```text
python -m uv run python apps/api/manage.py check --deploy --fail-level WARNING
```

The developer workbench is rejected outside local/test. Production-like settings enforce HTTPS-related controls and explicit allowlists.

## Hosted evidence

GitHub Actions run `35057831342` completed successfully against audited implementation HEAD `7302ca3b18a79af35058828102bb62e845a56645` before this documentation reconciliation. It exercised the full current CI chain, including migration-history checks, backend/client tests, production settings, E2E, audits, container builds and persistence smoke.

See [the test strategy](../quality/test-strategy.md), [Increment 1 readiness](../tracking/increment-1-readiness.md), and [the full development commit audit](../tracking/development-commit-audit.md).
