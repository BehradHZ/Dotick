/**
 * Date/time helpers.
 *
 * Two jobs, kept separate from any component so they can be unit-tested
 * without a renderer:
 *
 * 1. Formatting backend ISO timestamps for display.
 * 2. Parsing the plain-text `YYYY-MM-DD HH:mm` the forms use, back into
 *    the ISO string the API expects.
 *
 * A plain text field is used rather than `<input type="datetime-local">`
 * on purpose: ROADMAP.md §5.1 asks components to avoid web-only APIs
 * where reasonable so a later native build reuses them.
 *
 * Timezone posture (TESTING_PLAN.md §7): the backend stores and compares
 * UTC (`USE_TZ = True`, `TIME_ZONE = "UTC"`). Conversion happens only
 * here, at display/entry time, via the device's own offset — so a task
 * whose UTC "today" differs from the local "today" still shows the local
 * date the user expects, while the status the backend computed stays
 * authoritative.
 */

const pad = (n) => String(n).padStart(2, '0');

const MONTHS = [
  'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
];

export function parseIso(value) {
  if (!value) return null;
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? null : date;
}

function isSameLocalDay(a, b) {
  return (
    a.getFullYear() === b.getFullYear() &&
    a.getMonth() === b.getMonth() &&
    a.getDate() === b.getDate()
  );
}

function localDayDelta(date, now) {
  const a = new Date(date.getFullYear(), date.getMonth(), date.getDate());
  const b = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  return Math.round((a - b) / 86400000);
}

/**
 * Short label for a list row: "Today", "Tomorrow", "Yesterday", "Aug 2",
 * or "Aug 2, 2025" once the year differs from the current one.
 */
export function formatShortDate(value, now = new Date()) {
  const date = parseIso(value);
  if (!date) return '';

  if (isSameLocalDay(date, now)) return 'Today';
  const delta = localDayDelta(date, now);
  if (delta === 1) return 'Tomorrow';
  if (delta === -1) return 'Yesterday';

  const base = `${MONTHS[date.getMonth()]} ${date.getDate()}`;
  return date.getFullYear() === now.getFullYear()
    ? base
    : `${base}, ${date.getFullYear()}`;
}

/** Full label for the detail view: "Aug 2, 2026 · 14:30". */
export function formatDateTime(value) {
  const date = parseIso(value);
  if (!date) return '—';
  return (
    `${MONTHS[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}` +
    ` · ${pad(date.getHours())}:${pad(date.getMinutes())}`
  );
}

/** The form's editable representation of an instant: `YYYY-MM-DD HH:mm`. */
export function toInputValue(value) {
  const date = parseIso(value);
  if (!date) return '';
  return (
    `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} ` +
    `${pad(date.getHours())}:${pad(date.getMinutes())}`
  );
}

export const DATETIME_HINT = 'YYYY-MM-DD HH:mm';

/**
 * Parse the form format back to an ISO string for the API.
 *
 * Returns `{ value }` on success (with `value === null` for empty input,
 * which the API accepts for the nullable `due_date`/`deadline`), or
 * `{ error }` with a message meant to be shown under the field.
 * Rejecting bad input here — rather than letting `new Date()` coerce
 * something surprising — keeps a typo from silently becoming a real
 * timestamp that then drives a wrong computed status.
 */
export function fromInputValue(text) {
  const trimmed = (text || '').trim();
  if (!trimmed) return { value: null };

  const match = /^(\d{4})-(\d{1,2})-(\d{1,2})(?:[ T](\d{1,2}):(\d{2}))?$/.exec(trimmed);
  if (!match) return { error: `Use ${DATETIME_HINT} (time optional).` };

  const [, y, mo, d, h = '0', mi = '0'] = match;
  const year = Number(y);
  const month = Number(mo);
  const day = Number(d);
  const hour = Number(h);
  const minute = Number(mi);

  if (month < 1 || month > 12) return { error: 'Month must be between 1 and 12.' };
  if (day < 1 || day > 31) return { error: 'Day must be between 1 and 31.' };
  if (hour > 23 || minute > 59) return { error: 'Time must be between 00:00 and 23:59.' };

  const date = new Date(year, month - 1, day, hour, minute, 0, 0);
  // Catches non-existent dates that JS would otherwise roll over
  // (e.g. 2026-02-31 becoming March 3rd).
  if (date.getMonth() !== month - 1 || date.getDate() !== day) {
    return { error: 'That date does not exist.' };
  }

  return { value: date.toISOString() };
}

export function nowInputValue() {
  return toInputValue(new Date().toISOString());
}

/**
 * `grace_period` is a Django DurationField, which DRF serialises as
 * `"7 00:00:00"` (and accepts back in the same form). The UI only ever
 * needs whole days — §4.4's examples are "1 week, 1 month" — so these two
 * helpers convert at the boundary and keep the rest of the UI in days.
 */
export function graceDaysFromApi(value) {
  if (typeof value !== 'string') return null;
  const match = /^(-?\d+)\s/.exec(value.trim());
  if (match) return Number(match[1]);
  // No day component at all ("00:00:00") — under a day, shown as 0.
  return /^\d{1,2}:\d{2}:\d{2}$/.test(value.trim()) ? 0 : null;
}

export function graceDaysToApi(days) {
  const n = Number(days);
  if (!Number.isFinite(n) || n < 0) return null;
  return `${Math.floor(n)} 00:00:00`;
}
