/**
 * Smoke check for the exported web bundle.
 *
 * Not a unit test — it boots the *real* built bundle in jsdom against a
 * stubbed API and asserts the Stage 2 surface actually renders: all six
 * task statuses, the Postpone All control, and each dock destination.
 *
 * Run after `npx expo export --platform web --output-dir <dir>`:
 *   node scripts/smoke-web.mjs <exportDir>
 */

import { readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import { JSDOM, VirtualConsole } from 'jsdom';

const exportDir = process.argv[2] || '/tmp/dotick-web-check';
const jsDir = join(exportDir, '_expo/static/js/web');
const bundleName = readdirSync(jsDir).find((f) => f.endsWith('.js'));
const bundle = readFileSync(join(jsDir, bundleName), 'utf8');

const now = Date.now();
const iso = (offsetMs) => new Date(now + offsetMs).toISOString();
const DAY = 86400000;

/** One task per status, so every one of the six must render. */
const TASKS = [
  { id: 1, title: 'Todo task', description: '', user_status: null, due_date: iso(DAY), deadline: iso(2 * DAY), deadline_enabled: true, grace_period: '7 00:00:00', effective_status: 'TODO', created_at: iso(-DAY), updated_at: iso(-DAY) },
  { id: 2, title: 'Overdue task', description: '', user_status: null, due_date: iso(-DAY), deadline: iso(DAY), deadline_enabled: true, grace_period: '7 00:00:00', effective_status: 'OVERDUE', created_at: iso(-2 * DAY), updated_at: iso(-2 * DAY) },
  { id: 3, title: 'Missed task', description: '', user_status: null, due_date: iso(-5 * DAY), deadline: iso(-2 * DAY), deadline_enabled: true, grace_period: '7 00:00:00', effective_status: 'MISSED', created_at: iso(-6 * DAY), updated_at: iso(-6 * DAY) },
  { id: 4, title: 'Auto closed task', description: '', user_status: null, due_date: iso(-30 * DAY), deadline: iso(-20 * DAY), deadline_enabled: true, grace_period: '7 00:00:00', effective_status: 'AUTO_WONT_DO', created_at: iso(-31 * DAY), updated_at: iso(-31 * DAY) },
  { id: 5, title: 'Done task', description: '', user_status: 'DONE', due_date: iso(-DAY), deadline: null, deadline_enabled: false, grace_period: '7 00:00:00', effective_status: 'DONE', created_at: iso(-3 * DAY), updated_at: iso(-DAY) },
  { id: 6, title: 'Skipped task', description: '', user_status: 'WONT_DO', due_date: iso(-DAY), deadline: null, deadline_enabled: false, grace_period: '7 00:00:00', effective_status: 'WONT_DO', created_at: iso(-3 * DAY), updated_at: iso(-DAY) },
];

const EVENTS = [
  { id: 1, title: 'Ongoing event', description: '', start_time: iso(-3600000), end_time: iso(3600000), status: 'ONGOING', created_at: iso(-DAY), updated_at: iso(-DAY) },
  { id: 2, title: 'Upcoming event', description: '', start_time: iso(DAY), end_time: iso(DAY + 3600000), status: 'UPCOMING', created_at: iso(-DAY), updated_at: iso(-DAY) },
  { id: 3, title: 'Past event', description: '', start_time: iso(-2 * DAY), end_time: iso(-2 * DAY + 3600000), status: 'PAST', created_at: iso(-3 * DAY), updated_at: iso(-3 * DAY) },
];

const ROUTINES = [
  { id: 1, title: 'Open occurrence', description: '', user_status: null, period_end: iso(DAY), status: 'TODO', created_at: iso(-DAY), updated_at: iso(-DAY) },
  { id: 2, title: 'Completed occurrence', description: '', user_status: 'DONE', period_end: iso(-DAY), status: 'DONE', created_at: iso(-2 * DAY), updated_at: iso(-DAY) },
];

const virtualConsole = new VirtualConsole();
const consoleErrors = [];
virtualConsole.on('jsdomError', (err) => consoleErrors.push(String(err)));
virtualConsole.on('error', (...args) => consoleErrors.push(args.join(' ')));

const dom = new JSDOM(
  '<!doctype html><html><head></head><body><div id="root"></div></body></html>',
  { runScripts: 'dangerously', pretendToBeVisual: true, url: 'http://localhost/', virtualConsole }
);

const { window } = dom;
window.process = { env: { EXPO_PUBLIC_API_URL: 'http://backend.test:8000', NODE_ENV: 'production' } };

const routes = {
  '/api/tasks/': TASKS,
  '/api/events/': EVENTS,
  '/api/routines/': ROUTINES,
};

// The API base URL is inlined into the bundle at export time, so match on
// the path suffix rather than on a base URL this script can't know.
const requested = [];
window.fetch = (url) => {
  const raw = String(url);
  requested.push(raw);
  const key = Object.keys(routes).find((path) => raw.endsWith(path));
  if (!key) {
    return Promise.resolve({
      ok: false,
      status: 404,
      json: () => Promise.resolve({ detail: `no stub for ${raw}` }),
    });
  }
  return Promise.resolve({ ok: true, status: 200, json: () => Promise.resolve(routes[key]) });
};

window.eval(bundle);

const text = () => window.document.body.textContent || '';

const failures = [];
const expect = (label, condition) => {
  if (!condition) failures.push(label);
};

await new Promise((resolve) => setTimeout(resolve, 1200));

// --- Today screen (default destination) --------------------------------
const today = text();
expect('Today screen renders its title', today.includes('Today'));
for (const label of ['To Do', 'Overdue', 'Missed', "Auto Won", 'Done', "Won"]) {
  expect(`Today shows a "${label}" status tile`, today.includes(label));
}
expect('Today lists an attention task', today.includes('Overdue task'));
expect('Postpone All is present and counts the postponable tasks', today.includes('Postpone all (2)'));

// --- Task list ---------------------------------------------------------
const clickAria = (label) => {
  const el = window.document.querySelector(`[aria-label="${label}"]`);
  if (!el) return false;
  el.dispatchEvent(new window.MouseEvent('click', { bubbles: true }));
  return true;
};

expect('Tasks destination is reachable from the dock', clickAria('Tasks'));
await new Promise((resolve) => setTimeout(resolve, 400));
const taskScreen = text();
for (const title of TASKS.map((t) => t.title)) {
  expect(`Task list renders "${title}"`, taskScreen.includes(title));
}
expect('Task list groups by status heading "Missed"', taskScreen.includes('Missed'));

// --- Events -----------------------------------------------------------
expect('Events destination is reachable', clickAria('Events'));
await new Promise((resolve) => setTimeout(resolve, 400));
const eventScreen = text();
for (const title of EVENTS.map((e) => e.title)) {
  expect(`Event list renders "${title}"`, eventScreen.includes(title));
}

// --- Routines ---------------------------------------------------------
expect('Routines destination is reachable', clickAria('Routines'));
await new Promise((resolve) => setTimeout(resolve, 400));
const routineScreen = text();
for (const title of ROUTINES.map((r) => r.title)) {
  expect(`Routine list renders "${title}"`, routineScreen.includes(title));
}

// --- Task detail: the two Postpone branches of §4.7 -------------------
const mutations = [];
const baseFetch = window.fetch;
window.fetch = (url, options = {}) => {
  if (options.method && options.method !== 'GET') {
    mutations.push(`${options.method} ${String(url)}`);
  }
  return baseFetch(url, options);
};

expect('Back to the task list', clickAria('Tasks'));
await new Promise((resolve) => setTimeout(resolve, 400));

expect(
  'A MISSED task row opens its detail panel',
  clickAria('Missed task — Missed')
);
await new Promise((resolve) => setTimeout(resolve, 400));
const detail = text();
expect(
  'MISSED detail states the deadline-disabling branch',
  detail.includes('switches the deadline off')
);
expect('Detail offers a reversible Won\u2019t do', detail.includes("Won't do"));

expect('Postpone is actionable on a MISSED task', clickAria('Postpone'));
await new Promise((resolve) => setTimeout(resolve, 500));
expect(
  'Postpone POSTs to the single-task endpoint',
  mutations.some((m) => m.includes('POST') && m.includes('/api/tasks/3/postpone/'))
);

// --- Task form: the deadline toggle (§4.3) ----------------------------
expect('New task opens the form', clickAria('New task'));
await new Promise((resolve) => setTimeout(resolve, 400));
const formClosed = text();
expect('Form explains the off state', formClosed.includes('stored date is kept but ignored'));
expect(
  'Deadline date input is hidden while the toggle is off',
  !window.document.querySelector('[aria-label="Deadline date"]')
);

expect('Deadline toggle is operable', clickAria('Deadline'));
await new Promise((resolve) => setTimeout(resolve, 300));
expect(
  'Switching the toggle on reveals the deadline date input',
  Boolean(window.document.querySelector('[aria-label="Deadline date"]'))
);
expect(
  'Switching the toggle on reveals the grace period input',
  Boolean(window.document.querySelector('[aria-label="Grace period (days)"]'))
);

const realErrors = consoleErrors.filter((e) => !/Not implemented|css|font/i.test(e));
if (realErrors.length) failures.push(`Console errors: ${realErrors.slice(0, 3).join(' | ')}`);

if (failures.length) {
  console.error(`FAIL (${failures.length})`);
  for (const f of failures) console.error(`  ✗ ${f}`);
  console.error(`  fetch calls seen: ${JSON.stringify(requested)}`);
  console.error(`  body text: ${text().slice(0, 600)}`);
  process.exit(1);
}

console.log('PASS — Stage 2 surface renders: 6 task statuses, 3 event states, routine occurrences, Postpone All.');
