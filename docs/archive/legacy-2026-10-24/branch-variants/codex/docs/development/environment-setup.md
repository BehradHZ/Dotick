# Development environment

Status: Increment 1 backend and minimal Expo client, 2026-09-08. Run commands from the repository root.

## Prerequisites

- Python 3.14; local verification used 3.14.5.
- Node.js 24 LTS and npm 11; versions are in `.node-version` and `package.json`.
- Docker with its Linux engine running for the reproducible PostgreSQL/container path.
- Git. Dependencies are installed from `uv.lock` and `package-lock.json`.

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

The initializer generates private secrets in the ignored `.env` and preserves existing values. The developer email is `developer@example.test`; read `DOTICK_DEVELOPMENT_PASSWORD` in `.env` for its password. The provisioning command refuses to silently replace an existing account's password.

Google sign-in needs the same OAuth web client ID in backend `GOOGLE_OAUTH_CLIENT_ID` and public client `EXPO_PUBLIC_GOOGLE_CLIENT_ID`; a client ID is public, never put a client secret in an Expo variable. Passkey ceremonies need the deployed WebAuthn relying-party ID and exact browser origins in `WEBAUTHN_RP_ID` and `WEBAUTHN_ORIGINS`; local defaults target `localhost` and the Expo web origin. Google One Tap and Passkey sign-in are available on configured web builds. Expo Go uses email/password until a native provider build is configured. Phone-contact delivery is an application adapter and must be configured by the deployment before that endpoint is exposed. Automated tests replace only these external provider/delivery boundaries.

If a PostgreSQL server already uses port `55432`, choose a free `PGPORT` in `.env` before starting Compose. A local PostgreSQL 18 installation can also be used with a dedicated database/user; set its connection fields instead. Tests create and destroy `test_<PGDATABASE>`, so the development database role needs `CREATEDB`. Never point the test commands at production.

## Run the client and API

In one terminal:

```text
python -m uv run uvicorn config.asgi:application --app-dir apps/api --host 127.0.0.1 --port 8000 --no-access-log
```

In another:

```text
npm run dev
```

Open `http://127.0.0.1:8081`. Sign in, create a Task in Inbox or a new List, change its status/placement, and use Trash/restore. Reloading clears in-memory tokens; sign in again to verify PostgreSQL persistence.

The web client defaults to API `http://127.0.0.1:8000`. To change it, set `EXPO_PUBLIC_API_URL` in the client build environment and update `DJANGO_CORS_ORIGINS`. Expo public variables are bundled into the client and must never contain secrets.

### Open on a phone with Expo Go

Keep computer and phone on the same trusted private network. Find the computer's LAN IPv4 address, then include that exact address in the API host allowlist and bind the API to the LAN interface:

```text
Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -notlike '127.*'}
$env:DJANGO_ALLOWED_HOSTS='127.0.0.1,localhost,<LAN-IP>'
python -m uv run uvicorn config.asgi:application --app-dir apps/api --host 0.0.0.0 --port 8000 --no-access-log
```

In another terminal:

```text
npm run start:mobile --workspace @dotick/client
```

Scan the QR code in Expo Go. The client normally derives the API address from the Expo LAN host. If it does not, enter `http://<LAN-IP>:8000` in the sign-in screen's **API address** field. Allow Python/Node through the private-network firewall if prompted. Do not expose this development server on a public network.

## Run the built containers

```text
docker compose build
docker compose up -d postgres
docker compose run --rm api python apps/api/manage.py migrate --noinput
docker compose run --rm api python apps/api/manage.py create_developer
docker compose up -d api web
```

Use the same local web URL. Migrations are explicit and are not performed by every API process at startup. Ports bind only to loopback. This is a developer environment, not a supported end-user self-hosting product. `docker compose down` stops it and retains the database volume.

## Checks

```text
python scripts/check_traceability.py
python -m uv run ruff check apps/api scripts
python -m uv run ruff format --check apps/api scripts
python -m uv run python apps/api/manage.py makemigrations --check --dry-run
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

The E2E runner starts the API and exported-web server when they are not already running. It uses the provisioned local account from `.env`. CI provisions an ephemeral account/database. If Chromium's download is unavailable but Chrome is installed, set `PLAYWRIGHT_CHANNEL=chrome` before running E2E; this fallback was used on the current Windows machine. CI installs its matching Chromium build.

If port `8081` is already used or reserved by Windows, set `DOTICK_E2E_WEB_PORT` to a free loopback port and add the matching origin to `DJANGO_CORS_ORIGINS` for that test process. The regular development and Compose port remains `8081`.

For a production configuration check, set `DOTICK_ENV=production` and `DOTICK_FOUNDATION_ENABLED=0` in that process, then run `python -m uv run python apps/api/manage.py check --deploy --fail-level WARNING`. Keep required secrets supplied. The workbench is rejected at startup if enabled outside local/test.

See [dependency review](../quality/foundation-dependency-review.md) for the visible Expo/native-tooling advisory and CI threshold. Full verification evidence and remaining gates are in the [foundation review](../tracking/increment-0-foundation-review.md).
