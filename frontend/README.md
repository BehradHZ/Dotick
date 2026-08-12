# Dotick Frontend

React Native for Web (via Expo) frontend for Dotick. See `../ROADMAP.md` at
the project root for the full engineering roadmap and decision record.

## Stage 2 — Core Task, Event, and Routine Management

The app is now a usable single-user task manager over the Stage 2 backend.
Every status shown here is the one the backend computed (§4.3, §4.5, §4.6) —
the frontend never recomputes a status, it only presents it.

What's built:

- **Today** — status tiles for all six task statuses, the tasks needing
  attention, what's due today, live/next events, and open routine
  occurrences.
- **Tasks** — the full list, grouped by status (all six appear, including the
  closed ones), by due date, or ungrouped; sortable by due date / title /
  created, either direction. Group headers for Overdue and Missed carry an
  inline Postpone, and the header has **Postpone all**, labelled with the
  number of tasks the backend will actually touch.
- **Task detail** — Done, Won't Do, and Postpone, all reversible where the
  domain says they are (§4.3), plus Edit and Delete. The Postpone button
  states which §4.7 branch will fire, so a Missed postpone doesn't silently
  switch the deadline off behind your back.
- **Task create/edit** — with the deadline **toggle** (§4.3): off hides the
  date input but keeps the value, so switching it back on restores the date
  instead of asking again. Grace period is editable in whole days.
- **Events** — grouped by the three time-driven states. No checkbox and no
  completion action, because events aren't completed (§4.5).
- **Routines** — manual occurrences, each with Done / Won't Do (reversible)
  / Edit / Delete. No recurrence UI — that's Stage 3 (§4.9).

Deliberately absent: lists, folders, and tags. They don't exist until Stage 5,
and §5.1 rules out shipping a control backed by nothing. The rail keeps their
place with a disabled `Lists · Stage 5` marker.

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

## Verifying it

### Automated smoke check

```bash
npm run smoke
```

This exports the real web bundle and boots it in jsdom against a stubbed API
containing one task per status, one event per state, and two routine
occurrences. It asserts that all six task statuses render, each dock
destination is reachable, `Postpone all` reports the right count, a Missed
task's detail panel names the deadline-disabling branch and POSTs to
`/api/tasks/<id>/postpone/`, and the deadline toggle actually reveals and
hides the deadline/grace inputs.

It is a smoke check, not a substitute for the manual pass — it proves the
bundle renders and wires up, not that the app is pleasant to use.

### Manual check (the one that matters — `TESTING_PLAN.md` §3, §7)

With the backend running:

1. Create a task with a due date in the future and the deadline off → **To Do**.
2. Create one with a due date in the past and the deadline on, in the future →
   **Overdue**. Postpone it from the detail view; the due date moves to now
   and the deadline stays on.
3. Create one with both due date and deadline in the past, inside the grace
   period → **Missed**. Postpone it; the deadline switches **off** and the
   stored date is still shown as inactive in the detail view.
4. Push a deadline further back than the grace period → **Auto Won't Do**.
5. Mark one Done, then Reopen it. Mark one Won't Do, then undo it.
6. Try a task whose due date is after its deadline → the backend rejects it
   and the message appears under the **Due date** field.
7. Create an event spanning now → **Ongoing**; one in the future →
   **Upcoming**; one in the past → **Past**.
8. Create a routine occurrence, mark it Done, reopen it; let a period end
   pass with no action → **Auto Won't Do**.
9. Open the same app from a phone browser on the same network and confirm the
   rail collapses into a horizontal scroller and everything is still reachable.

## Project layout

```
frontend/
├── App.js                       # shell + navigation between the four destinations
├── index.js                     # Expo entry point
├── src/
│   ├── api/client.js            # fetch wrapper; ApiError carries DRF field errors
│   ├── domain/
│   │   ├── datetime.js          # ISO ↔ `YYYY-MM-DD HH:mm`, grace-period days
│   │   └── status.js            # status vocabulary, grouping and sorting
│   ├── state/store.js           # useReducer + Context (resolves §10.3)
│   ├── theme/tokens.js          # design tokens ported from the prototype
│   ├── ui/                      # AppShell, Button, Field, Panel, Rows, Chrome, Icon
│   └── screens/                 # Today, TaskList, TaskDetail, TaskForm, Events, Routines
├── scripts/smoke-web.mjs        # jsdom smoke check over the exported bundle
├── dotick-layout-foundation.html  # the layout prototype this UI is ported from
└── package.json
```

### Why these choices

- **State: `useReducer` + one Context, no state library.** Stage 2's client
  state is three server-owned collections plus which screen is open. The
  full reasoning, and what would justify TanStack Query later, is in the
  header comment of `src/state/store.js`.
- **Navigation: one `screen` string, no router.** Four destinations, no
  deep-linking requirement. Revisit when Stage 5 introduces lists worth
  linking to.
- **Plain text datetime fields, not `<input type="datetime-local">`.** §5.1
  asks components to avoid web-only APIs where reasonable so a later native
  build reuses them. Parsing is strict (`src/domain/datetime.js`) so a typo
  can't silently become a real timestamp that then drives a wrong status.
- **Icons via `react-native-svg`, not inline `<svg>`.** Same reason.
