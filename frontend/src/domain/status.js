/**
 * Status vocabulary and list-shaping logic.
 *
 * The backend already computes every status (`effective_status` on Task,
 * `status` on Event/Routine — see core/models.py), and per ROADMAP.md §4.3
 * that computation is the source of truth. This module never recomputes a
 * status; it only decides how to *present* the value the API returned, and
 * how to group/sort a list of items.
 *
 * Kept pure and renderer-free so the grouping/sorting rules can be unit
 * tested directly.
 */

import { statusColors } from '../theme/tokens';
import { parseIso } from './datetime';

/** Task's six user-visible statuses (§4.3), in the order a list shows them. */
export const TASK_STATUS_ORDER = [
  'MISSED',
  'OVERDUE',
  'TODO',
  'AUTO_WONT_DO',
  'DONE',
  'WONT_DO',
];

export const TASK_STATUS_META = {
  TODO: {
    label: 'To Do',
    description: 'Not yet due, or no active deadline.',
  },
  OVERDUE: {
    label: 'Overdue',
    description: 'Due date passed; the hard deadline has not.',
  },
  MISSED: {
    label: 'Missed',
    description: 'Deadline passed, still inside the grace period.',
  },
  AUTO_WONT_DO: {
    label: "Auto Won't Do",
    description: 'Grace period elapsed with no action; closed automatically.',
  },
  DONE: {
    label: 'Done',
    description: 'Explicitly completed by you.',
  },
  WONT_DO: {
    label: "Won't Do",
    description: 'Explicitly skipped by you — reversible at any time.',
  },
};

/** Event's three purely time-driven states (§4.5). */
export const EVENT_STATUS_ORDER = ['ONGOING', 'UPCOMING', 'PAST'];

export const EVENT_STATUS_META = {
  UPCOMING: { label: 'Upcoming', description: 'Starts in the future.' },
  ONGOING: { label: 'Ongoing', description: 'Happening right now.' },
  PAST: { label: 'Past', description: 'Already ended.' },
};

/** Routine occurrence states (§4.6). */
export const ROUTINE_STATUS_ORDER = ['TODO', 'DONE', 'WONT_DO', 'AUTO_WONT_DO'];

export const ROUTINE_STATUS_META = {
  TODO: { label: 'To Do', description: 'This occurrence is unresolved.' },
  DONE: { label: 'Done', description: 'Marked complete.' },
  WONT_DO: { label: "Won't Do", description: 'Explicitly skipped — reversible.' },
  AUTO_WONT_DO: {
    label: "Auto Won't Do",
    description: "The occurrence's period elapsed with no action.",
  },
};

export function statusColor(status) {
  return statusColors[status] || statusColors.AUTO_WONT_DO;
}

export function statusLabel(status) {
  return (
    (TASK_STATUS_META[status] || EVENT_STATUS_META[status] || ROUTINE_STATUS_META[status] || {})
      .label || status
  );
}

/**
 * Which statuses the backend's `postpone_all` actually touches
 * (`TaskManager.postpone_all` → OVERDUE and MISSED only). Used to label
 * the bulk button honestly and to disable it when nothing qualifies,
 * rather than firing a POST that reports 0.
 */
export const POSTPONABLE_STATUSES = ['OVERDUE', 'MISSED'];

export function isPostponable(task) {
  return POSTPONABLE_STATUSES.includes(task.effective_status);
}

export function countPostponable(tasks) {
  return tasks.filter(isPostponable).length;
}

/** A task the user has resolved either way — shown muted and struck out. */
export function isResolved(status) {
  return status === 'DONE' || status === 'WONT_DO' || status === 'AUTO_WONT_DO';
}

// ---------------------------------------------------------------------------
// Grouping and sorting
//
// Options mirror the prototype's Group by / Sort by menu, applied to the
// real six-state model. "List" grouping is deliberately absent: lists do
// not exist until Stage 5 (§6 Stage 5), and offering an option backed by
// nothing would be a fake control.
// ---------------------------------------------------------------------------

export const GROUP_OPTIONS = [
  { key: 'status', label: 'Status' },
  { key: 'due', label: 'Due Date' },
  { key: 'none', label: 'None' },
];

export const SORT_OPTIONS = [
  { key: 'due', label: 'Due Date' },
  { key: 'title', label: 'Title' },
  { key: 'created', label: 'Created' },
];

function dueBucket(task, now) {
  const date = parseIso(task.due_date);
  if (!date) return { key: 'nodate', label: 'No due date', rank: 5 };

  const startOfToday = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const delta = Math.round(
    (new Date(date.getFullYear(), date.getMonth(), date.getDate()) - startOfToday) / 86400000
  );

  if (delta < 0) return { key: 'past', label: 'Earlier', rank: 0 };
  if (delta === 0) return { key: 'today', label: 'Today', rank: 1 };
  if (delta === 1) return { key: 'tomorrow', label: 'Tomorrow', rank: 2 };
  if (delta <= 7) return { key: 'week', label: 'Next 7 days', rank: 3 };
  return { key: 'later', label: 'Later', rank: 4 };
}

function compareTasks(a, b, sortKey) {
  if (sortKey === 'title') {
    return String(a.title).localeCompare(String(b.title));
  }
  if (sortKey === 'created') {
    return (parseIso(a.created_at) || 0) - (parseIso(b.created_at) || 0);
  }
  // 'due': tasks without a due date sort last, so an unscheduled task
  // never pushes a dated one down the list.
  const da = parseIso(a.due_date);
  const db = parseIso(b.due_date);
  if (!da && !db) return String(a.title).localeCompare(String(b.title));
  if (!da) return 1;
  if (!db) return -1;
  return da - db;
}

/**
 * Shape a task array into the `[{ key, title, color, items }]` list the
 * task screen renders.
 *
 * @param {Array} tasks     tasks as returned by the API
 * @param {object} options  { groupBy, sortBy, ascending, now }
 */
export function groupTasks(tasks, { groupBy = 'status', sortBy = 'due', ascending = true, now = new Date() } = {}) {
  const direction = ascending ? 1 : -1;
  const sorted = [...tasks].sort((a, b) => compareTasks(a, b, sortBy) * direction);

  if (groupBy === 'none') {
    return [{ key: 'all', title: 'All tasks', color: null, items: sorted }];
  }

  if (groupBy === 'due') {
    const buckets = new Map();
    for (const task of sorted) {
      const bucket = dueBucket(task, now);
      if (!buckets.has(bucket.key)) {
        buckets.set(bucket.key, { key: bucket.key, title: bucket.label, color: null, rank: bucket.rank, items: [] });
      }
      buckets.get(bucket.key).items.push(task);
    }
    return [...buckets.values()].sort((a, b) => a.rank - b.rank);
  }

  // groupBy === 'status'
  return TASK_STATUS_ORDER.map((status) => ({
    key: status,
    title: statusLabel(status),
    color: statusColor(status),
    status,
    items: sorted.filter((task) => task.effective_status === status),
  })).filter((group) => group.items.length > 0);
}

/** Same idea for events, grouped by their three states, soonest first. */
export function groupEvents(events, { now = new Date() } = {}) {
  void now;
  const sorted = [...events].sort(
    (a, b) => (parseIso(a.start_time) || 0) - (parseIso(b.start_time) || 0)
  );
  return EVENT_STATUS_ORDER.map((status) => ({
    key: status,
    title: statusLabel(status),
    color: statusColor(status),
    status,
    items: sorted.filter((event) => event.status === status),
  })).filter((group) => group.items.length > 0);
}

/** And for routine occurrences (§4.6), earliest period end first. */
export function groupRoutines(routines) {
  const sorted = [...routines].sort(
    (a, b) => (parseIso(a.period_end) || 0) - (parseIso(b.period_end) || 0)
  );
  return ROUTINE_STATUS_ORDER.map((status) => ({
    key: status,
    title: statusLabel(status),
    color: statusColor(status),
    status,
    items: sorted.filter((routine) => routine.status === status),
  })).filter((group) => group.items.length > 0);
}
