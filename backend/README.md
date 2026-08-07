# Dotick Backend

Django + Django REST Framework backend for Dotick. See `../ROADMAP.md` at
the project root for the full engineering roadmap and decision record.

## Stage 1 — Basic Foundation

This stage only proves the pipe works end to end: browser → Django →
PostgreSQL → response. No task/event/routine features exist yet.

## Setup

1. **PostgreSQL.** Have a PostgreSQL server running locally, then create a
   matching user and database (defaults below match `.env.example`):

   ```sql
   CREATE USER dotick WITH PASSWORD 'dotick' CREATEDB;
   CREATE DATABASE dotick OWNER dotick;
   ```

2. **Python environment.**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Environment variables.**

   ```bash
   cp .env.example .env
   # edit .env if your local Postgres credentials differ,
   # and add your laptop's LAN IP to DJANGO_ALLOWED_HOSTS so your
   # phone browser can reach the server too.
   ```

4. **Migrate and run.**

   ```bash
   python manage.py migrate
   python manage.py runserver 0.0.0.0:8000
   ```

5. **Verify.** From the laptop or a phone on the same network:

   ```
   curl http://<laptop-ip>:8000/api/health/
   # {"status": "ok"}
   ```

## Running tests

```bash
python manage.py test
```

Tests run against a real PostgreSQL test database (Django creates and
tears it down automatically using the same connection settings as `.env`).
There is no sqlite fallback — this project always tests against Postgres
per ROADMAP.md §3, to avoid divergent behavior between test and real
environments.

## Project layout

```
backend/
├── dotick/
│   ├── settings/
│   │   ├── base.py   # shared settings, all env-var driven
│   │   └── local.py  # dev-only defaults, loads .env
│   ├── urls.py        # root URLconf; /api/ -> core.urls
│   ├── asgi.py, wsgi.py
├── core/               # cross-cutting app; currently just health-check
│   ├── views.py
│   ├── urls.py
│   └── tests/
│       ├── test_health_check.py     # response-shape seam
│       └── test_health_check_db.py  # DB-connectivity seam
├── manage.py
├── requirements.txt
└── .env.example
```

## Settings modules

- `dotick.settings.base` — shared, environment-agnostic settings. Reads
  everything environment-specific from `os.environ`, with no hardcoded
  fallback secret key (so it fails loudly rather than running insecurely
  if misconfigured outside local dev).
- `dotick.settings.local` — used for local development (this is
  `manage.py`'s default). Loads `.env`, then supplies dev-only fallbacks
  (a throwaway secret key, `DEBUG=True`, `localhost`/`127.0.0.1` in
  `ALLOWED_HOSTS`).

Future stages (e.g. Stage 4 — Docker) will add further settings modules
under this same package rather than branching with `if` statements inside
one file.
