/**
 * Application state (resolves ROADMAP.md §10.3 — "state management
 * approach for the frontend").
 *
 * **Decision: React's own `useReducer` + one Context provider. No state
 * library.**
 *
 * Why: Stage 2's entire client state is three server-owned collections
 * (tasks, events, routines) plus which screen is open and which item is
 * selected. There is no client-derived state to speak of — every status
 * in the UI is computed by the backend (§4.3, §4.5, §4.6) and simply
 * displayed. That makes this a server-cache problem with a trivial cache
 * policy ("refetch after a mutation"), not a state-modelling problem, and
 * Redux/Zustand/React-Query would each add a dependency and a set of
 * conventions to learn for state that fits in one reducer.
 *
 * Alternatives weighed:
 *   - **Redux Toolkit** — the store/slice/thunk machinery only starts
 *     paying for itself when many unrelated components mutate shared
 *     state. Here one provider covers it. Rejected as premature per KISS
 *     (§2.3).
 *   - **TanStack Query** — genuinely the right answer for caching,
 *     background refetch, and optimistic updates. Deferred rather than
 *     rejected: revisit when a real need appears (multi-screen cache
 *     sharing, offline, or the polling that §3.1 already defers).
 *   - **Plain `useState` per screen** — would refetch and duplicate the
 *     same task list in several screens, and "Postpone All" on the list
 *     screen has to update the detail view too. Rejected.
 *
 * Consequence to keep in mind: after any mutation this reloads the
 * affected collection from the server rather than patching the local copy.
 * That is deliberate — statuses are computed server-side from `now`, so a
 * locally patched object would immediately be stale in a way the user can
 * see (postpone a MISSED task and its status has to change).
 */

import { createContext, useCallback, useContext, useMemo, useReducer } from 'react';

import api, { ApiError, isApiConfigured } from '../api/client';

const RESOURCES = ['tasks', 'events', 'routines'];

const emptyCollection = { items: [], loading: false, loaded: false, error: null };

const initialState = {
  tasks: { ...emptyCollection },
  events: { ...emptyCollection },
  routines: { ...emptyCollection },
  /** Last mutation failure, surfaced as a dismissible banner. */
  actionError: null,
  /** Human-readable confirmation of the last bulk action. */
  notice: null,
};

function reducer(state, action) {
  switch (action.type) {
    case 'load:start':
      return {
        ...state,
        [action.resource]: { ...state[action.resource], loading: true, error: null },
      };
    case 'load:success':
      return {
        ...state,
        [action.resource]: {
          items: action.items,
          loading: false,
          loaded: true,
          error: null,
        },
      };
    case 'load:failure':
      return {
        ...state,
        [action.resource]: {
          ...state[action.resource],
          loading: false,
          loaded: true,
          error: action.error,
        },
      };
    case 'action:error':
      return { ...state, actionError: action.error, notice: null };
    case 'action:notice':
      return { ...state, notice: action.notice, actionError: null };
    case 'action:clear':
      return { ...state, actionError: null, notice: null };
    default:
      return state;
  }
}

const StoreContext = createContext(null);

export function StoreProvider({ children }) {
  const [state, dispatch] = useReducer(reducer, initialState);

  const load = useCallback(async (resource) => {
    if (!isApiConfigured()) {
      dispatch({
        type: 'load:failure',
        resource,
        error:
          'EXPO_PUBLIC_API_URL is not set. Copy .env.example to .env and fill it in.',
      });
      return;
    }
    dispatch({ type: 'load:start', resource });
    try {
      const items = await api[resource].list();
      dispatch({ type: 'load:success', resource, items });
    } catch (err) {
      dispatch({ type: 'load:failure', resource, error: messageOf(err) });
    }
  }, []);

  const loadAll = useCallback(async () => {
    await Promise.all(RESOURCES.map((resource) => load(resource)));
  }, [load]);

  /**
   * Run a mutation, then reload the collection it touched.
   *
   * Rethrows so a form can keep the user's input on screen and show
   * per-field errors, while the banner state is set for the cases where
   * nobody is catching (a row's Done button, say).
   */
  const mutate = useCallback(
    async (resource, fn, { notice = null } = {}) => {
      try {
        const result = await fn();
        await load(resource);
        if (notice) dispatch({ type: 'action:notice', notice });
        else dispatch({ type: 'action:clear' });
        return result;
      } catch (err) {
        dispatch({ type: 'action:error', error: messageOf(err) });
        throw err;
      }
    },
    [load]
  );

  const actions = useMemo(
    () => ({
      load,
      loadAll,
      clearMessages: () => dispatch({ type: 'action:clear' }),

      // ---- Task actions ------------------------------------------------
      createTask: (data) => mutate('tasks', () => api.tasks.create(data)),
      updateTask: (id, data) => mutate('tasks', () => api.tasks.update(id, data)),
      deleteTask: (id) => mutate('tasks', () => api.tasks.remove(id)),

      /**
       * §4.3: `user_status` is the only stored piece of a task's status.
       * `DONE`/`WONT_DO` are set here; passing `null` clears it, which is
       * exactly the documented reversibility ("the user can change a
       * WONT_DO task back to active at any time by clearing user_status").
       */
      setTaskUserStatus: (id, userStatus) =>
        mutate('tasks', () => api.tasks.update(id, { user_status: userStatus })),

      /** §4.7 single-task Postpone. */
      postponeTask: (id) => mutate('tasks', () => api.tasks.postpone(id)),

      /** §4.7 "Postpone All" — the bulk entry point. */
      postponeAllTasks: async () => {
        const result = await mutate('tasks', () => api.tasks.postponeAll());
        const count = result?.postponed_count ?? 0;
        dispatch({
          type: 'action:notice',
          notice:
            count === 0
              ? 'Nothing to postpone — no overdue or missed tasks.'
              : `Postponed ${count} task${count === 1 ? '' : 's'}.`,
        });
        return result;
      },

      // ---- Event actions -----------------------------------------------
      createEvent: (data) => mutate('events', () => api.events.create(data)),
      updateEvent: (id, data) => mutate('events', () => api.events.update(id, data)),
      deleteEvent: (id) => mutate('events', () => api.events.remove(id)),

      // ---- Routine actions ---------------------------------------------
      createRoutine: (data) => mutate('routines', () => api.routines.create(data)),
      updateRoutine: (id, data) => mutate('routines', () => api.routines.update(id, data)),
      deleteRoutine: (id) => mutate('routines', () => api.routines.remove(id)),
      setRoutineUserStatus: (id, userStatus) =>
        mutate('routines', () => api.routines.update(id, { user_status: userStatus })),
    }),
    [load, loadAll, mutate]
  );

  const value = useMemo(() => ({ ...state, actions }), [state, actions]);

  return <StoreContext.Provider value={value}>{children}</StoreContext.Provider>;
}

export function useStore() {
  const value = useContext(StoreContext);
  if (!value) {
    throw new Error('useStore must be used inside <StoreProvider>.');
  }
  return value;
}

function messageOf(err) {
  if (err instanceof ApiError) return err.message;
  return err instanceof Error ? err.message : String(err);
}
