/**
 * API client for the Stage 2 backend (ROADMAP.md §6 Stage 2 — "CRUD
 * endpoints for Task, Event, and Routine", plus the Postpone actions of
 * §4.7).
 *
 * One thin layer over fetch, deliberately free of React: every screen
 * talks to the backend through here, so the URL shape, the error shape,
 * and the JSON handling live in exactly one place.
 *
 * Endpoints (from backend/core/urls.py):
 *   GET/POST        /api/tasks/
 *   GET/PATCH/DELETE /api/tasks/<id>/
 *   POST            /api/tasks/<id>/postpone/
 *   POST            /api/tasks/postpone_all/
 *   …same CRUD shape for /api/events/ and /api/routines/
 */

const API_URL = process.env.EXPO_PUBLIC_API_URL;

/**
 * Errors thrown by this module. `fieldErrors` carries DRF's
 * `{"due_date": ["due_date must not be after deadline."]}` shape so a
 * form can show the message next to the field that caused it — the
 * `due_date <= deadline` rule from serializers.validate() is the one
 * validation Stage 2's UI must surface properly.
 */
export class ApiError extends Error {
  constructor(message, { status = null, fieldErrors = null } = {}) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.fieldErrors = fieldErrors;
  }
}

export function isApiConfigured() {
  return Boolean(API_URL);
}

export function apiBaseUrl() {
  return API_URL;
}

function endpoint(path) {
  if (!API_URL) {
    throw new ApiError(
      'EXPO_PUBLIC_API_URL is not set. Copy .env.example to .env and fill it in.'
    );
  }
  return `${API_URL}/api${path}`;
}

/**
 * Turn a DRF error body into a single readable sentence, keeping the
 * per-field detail available separately.
 */
function describeErrorBody(body, status) {
  if (!body || typeof body !== 'object') {
    return { message: `Backend responded with HTTP ${status}.`, fieldErrors: null };
  }
  if (typeof body.detail === 'string') {
    return { message: body.detail, fieldErrors: null };
  }

  const fieldErrors = {};
  const parts = [];
  for (const [field, value] of Object.entries(body)) {
    const text = Array.isArray(value) ? value.join(' ') : String(value);
    fieldErrors[field] = text;
    parts.push(field === 'non_field_errors' ? text : `${field}: ${text}`);
  }
  return {
    message: parts.length ? parts.join(' · ') : `Backend responded with HTTP ${status}.`,
    fieldErrors: Object.keys(fieldErrors).length ? fieldErrors : null,
  };
}

async function request(path, { method = 'GET', body } = {}) {
  const url = endpoint(path);

  let response;
  try {
    response = await fetch(url, {
      method,
      headers: body ? { 'Content-Type': 'application/json' } : undefined,
      body: body ? JSON.stringify(body) : undefined,
    });
  } catch (err) {
    // No HTTP status at all: the request never reached the backend.
    // Most often the backend is down, EXPO_PUBLIC_API_URL points at the
    // wrong host (localhost from a phone resolves to the phone), or the
    // browser blocked it as cross-origin — see backend/.env.example's
    // DJANGO_CORS_ALLOWED_ORIGINS.
    const detail = err instanceof Error ? err.message : String(err);
    throw new ApiError(
      `${detail} — backend unreachable at ${url}. If it is running, this is ` +
        `usually a CORS or wrong-host issue (check the browser console, and ` +
        `see backend/.env.example).`
    );
  }

  if (response.status === 204) return null;

  const payload = await response.json().catch(() => null);

  if (!response.ok) {
    const { message, fieldErrors } = describeErrorBody(payload, response.status);
    throw new ApiError(message, { status: response.status, fieldErrors });
  }

  return payload;
}

/**
 * DRF's DefaultRouter returns a bare list unless pagination is enabled;
 * accept either shape so turning pagination on later doesn't break the UI.
 */
function asList(payload) {
  if (Array.isArray(payload)) return payload;
  if (payload && Array.isArray(payload.results)) return payload.results;
  return [];
}

function crud(resource) {
  return {
    list: async () => asList(await request(`/${resource}/`)),
    create: (data) => request(`/${resource}/`, { method: 'POST', body: data }),
    update: (id, data) => request(`/${resource}/${id}/`, { method: 'PATCH', body: data }),
    remove: (id) => request(`/${resource}/${id}/`, { method: 'DELETE' }),
  };
}

export const api = {
  health: () => request('/health/'),

  tasks: {
    ...crud('tasks'),
    /** §4.7 single-task Postpone. Returns the updated task. */
    postpone: (id) => request(`/tasks/${id}/postpone/`, { method: 'POST' }),
    /** §4.7 "Postpone All". Returns `{ postponed_count }`. */
    postponeAll: () => request('/tasks/postpone_all/', { method: 'POST' }),
  },

  events: crud('events'),
  routines: crud('routines'),
};

export default api;
