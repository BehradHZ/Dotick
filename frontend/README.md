# Dotick Frontend

React Native for Web (via Expo) frontend for Dotick. See `../ROADMAP.md` at
the project root for the full engineering roadmap and decision record.

## Stage 1 — Basic Foundation

This stage only proves the pipe works end to end: browser → Django →
PostgreSQL → response. The app has a single screen that calls the backend's
`/api/health/` endpoint and displays the result. No task/event/routine
features exist yet.

## Setup

1. **Backend running first.** Follow `../backend/README.md` to get the
   Django server running and reachable (`python manage.py runserver
   0.0.0.0:8000`), including adding your laptop's LAN IP to
   `DJANGO_ALLOWED_HOSTS` if you want to test from a phone.

2. **Node dependencies.**

   ```bash
   npm install
   ```

3. **Environment variables.**

   ```bash
   cp .env.example .env
   # edit .env: set EXPO_PUBLIC_API_URL to where the backend is reachable.
   # - laptop browser: http://localhost:8000 is fine
   # - phone browser (same network): use the laptop's LAN IP instead,
   #   e.g. http://192.168.1.23:8000
   ```

4. **Run.**

   ```bash
   npm run web       # laptop browser, opens automatically
   npm start         # prints a QR code — scan with Expo Go on your phone
   ```

5. **Verify.** The screen should show a green "✓ Connected" message with
   the raw `{"status": "ok"}` response from the backend. If it shows a red
   error instead, check that the backend is running and that
   `EXPO_PUBLIC_API_URL` / `DJANGO_ALLOWED_HOSTS` point at each other
   correctly.

## Project layout

```
frontend/
├── App.js          # the one Stage 1 screen: calls /api/health/, shows
│                    # loading / success / error state, with a Retry button
├── index.js         # Expo entry point (registers App.js as the root)
├── app.json          # Expo config (name, icons, web bundler = metro)
├── .env.example
└── package.json
```

## Why Expo

Per `ROADMAP.md` §3, the frontend is React Native for Web so the same
codebase can later extend to native mobile without a rewrite. Expo is used
as the tooling layer on top of that — it bundles Metro's web support,
handles the dev server, and lets the app be opened instantly on a phone via
Expo Go during development, without a native build step. This is
implementation tooling, not a change to the ROADMAP's stack decision.

## A note on `EXPO_PUBLIC_` env vars

Expo only exposes environment variables prefixed with `EXPO_PUBLIC_` to
client-side code (anything else in `.env` stays server/build-only). That's
why the backend URL is named `EXPO_PUBLIC_API_URL` rather than plain
`API_URL` — see `App.js` for where it's read.
