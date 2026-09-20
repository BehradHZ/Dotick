import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, expect, test, vi } from 'vitest';
import App from './App';
function json(data: unknown, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}
const user = { email: 'person@example.test', handle: 'person', display_name: 'Person' };
const tokens = { access: 'access-one', refresh: 'refresh-one', user };
const inbox = {
  id: '11111111-1111-4111-8111-111111111111',
  title: 'Inbox',
  folder_id: null,
  is_inbox: true,
  position: 0,
  version: 1,
  is_trashed: false,
  trashed_at: null,
  default_column: { id: '22222222-2222-4222-8222-222222222222', is_default: true },
};
const work = {
  ...inbox,
  id: '55555555-5555-4555-8555-555555555555',
  title: 'Work',
  is_inbox: false,
  version: 2,
  default_column: { id: '66666666-6666-4666-8666-666666666666', is_default: true },
};
const workTask = {
  id: '77777777-7777-4777-8777-777777777777',
  title: 'First task',
  status: 'todo',
  priority: 'none',
  due_at: null,
  end_at: null,
  is_all_day: false,
  deadline_at: null,
  grace_period_days: 0,
  version: 3,
  column_id: work.default_column.id,
  owner_user_id: '44444444-4444-4444-8444-444444444444',
  created_by_user_id: '44444444-4444-4444-8444-444444444444',
  source: { platform: 'dotick', external_account_id: null, external_id: null },
  created_at: '2026-09-19T06:00:00Z',
  updated_at: '2026-09-19T06:00:00Z',
};
const defaultColumn = {
  id: work.default_column.id,
  list_id: work.id,
  title: 'not_sectioned',
  position: 0,
  version: 1,
  is_default: true,
};
const doingColumn = {
  id: '88888888-8888-4888-8888-888888888888',
  list_id: work.id,
  title: 'Doing',
  position: 1,
  version: 1,
  is_default: false,
};
function signIn() {
  fireEvent.change(screen.getByLabelText('Email'), { target: { value: user.email } });
  fireEvent.change(screen.getByLabelText('Password'), { target: { value: 'Safe-password-8!' } });
  fireEvent.click(screen.getByRole('button', { name: 'Sign in' }));
}
function openWork() {
  fireEvent.click(screen.getByRole('button', { name: 'Open Work' }));
}
afterEach(() => vi.unstubAllGlobals());

test('moves a Task between Lists using its current version', async () => {
  let currentTask = workTask;
  let patchBody: Record<string, unknown> | undefined;
  const fetch = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    if (url.endsWith('/api/v1/auth/token')) return json(tokens);
    if (url.endsWith('/api/v1/account/bootstrap'))
      return json({ preferences: { timezone: 'Europe/London' }, inbox });
    if (url.endsWith('/api/v1/lists')) return json({ results: [inbox, work] });
    if (url.endsWith('/api/v1/tasks')) return json({ results: [currentTask] });
    if (url.endsWith(`/api/v1/tasks/${workTask.id}`) && init?.method === 'PATCH') {
      patchBody = JSON.parse(String(init.body)) as Record<string, unknown>;
      currentTask = { ...currentTask, column_id: inbox.default_column.id, version: 4 };
      return json(currentTask);
    }
    throw new Error(`Unhandled request: ${url}`);
  });
  vi.stubGlobal('fetch', fetch);
  render(<App />);
  signIn();
  await screen.findByRole('heading', { name: 'Inbox' });
  openWork();
  await screen.findByText('First task');
  fireEvent.click(screen.getByRole('button', { name: 'Move First task to Inbox' }));
  await waitFor(() => expect(screen.queryByText('First task')).not.toBeInTheDocument());
  expect(patchBody).toEqual({ version: 3, column_id: inbox.default_column.id });
  fireEvent.click(screen.getByRole('button', { name: 'Open Inbox' }));
  expect(await screen.findByText('First task')).toBeVisible();
});

test('loads Columns on demand and moves to a validated loaded Column', async () => {
  let currentTask = workTask;
  let patchBody: Record<string, unknown> | undefined;
  const fetch = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    if (url.endsWith('/api/v1/auth/token')) return json(tokens);
    if (url.endsWith('/api/v1/account/bootstrap'))
      return json({ preferences: { timezone: 'Europe/London' }, inbox });
    if (url.endsWith('/api/v1/lists')) return json({ results: [inbox, work] });
    if (url.endsWith(`/api/v1/lists/${work.id}/columns`))
      return json({ results: [defaultColumn, doingColumn] });
    if (url.endsWith('/api/v1/tasks')) return json({ results: [currentTask] });
    if (url.endsWith(`/api/v1/tasks/${workTask.id}`) && init?.method === 'PATCH') {
      patchBody = JSON.parse(String(init.body)) as Record<string, unknown>;
      currentTask = { ...currentTask, column_id: doingColumn.id, version: 4 };
      return json(currentTask);
    }
    throw new Error(`Unhandled request: ${url}`);
  });
  vi.stubGlobal('fetch', fetch);
  render(<App />);
  signIn();
  await screen.findByRole('heading', { name: 'Inbox' });
  openWork();
  await screen.findByText('First task');
  fireEvent.click(screen.getByRole('button', { name: 'Load columns' }));
  expect(
    await screen.findByText('Multiple columns are available for Task movement.'),
  ).toBeVisible();
  expect(screen.queryByText('not_sectioned')).not.toBeInTheDocument();
  fireEvent.click(screen.getByRole('button', { name: 'Move First task to column Doing' }));
  await waitFor(() => expect(patchBody).toEqual({ version: 3, column_id: doingColumn.id }));
  expect(screen.getByText('First task')).toBeVisible();
});

test('trashes, loads Trash, and restores using current versions', async () => {
  let activeTasks = [workTask];
  const trashed = { ...workTask, version: 4, is_trashed: true, trashed_at: '2026-09-19T07:00:00Z' };
  const restored = { ...workTask, version: 5, is_trashed: false, trashed_at: null };
  let trashIfMatch: string | null = null;
  let restoreBody: Record<string, unknown> | undefined;
  const fetch = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    if (url.endsWith('/api/v1/auth/token')) return json(tokens);
    if (url.endsWith('/api/v1/account/bootstrap'))
      return json({ preferences: { timezone: 'Europe/London' }, inbox });
    if (url.endsWith('/api/v1/lists')) return json({ results: [inbox, work] });
    if (url.endsWith('/api/v1/trash/tasks')) return json({ results: [trashed] });
    if (url.endsWith(`/api/v1/tasks/${workTask.id}/restore`) && init?.method === 'POST') {
      restoreBody = JSON.parse(String(init.body)) as Record<string, unknown>;
      activeTasks = [restored];
      return json(restored);
    }
    if (url.endsWith(`/api/v1/tasks/${workTask.id}`) && init?.method === 'DELETE') {
      trashIfMatch = new Headers(init.headers).get('If-Match');
      activeTasks = [];
      return new Response(null, { status: 204 });
    }
    if (url.endsWith('/api/v1/tasks')) return json({ results: activeTasks });
    throw new Error(`Unhandled request: ${url}`);
  });
  vi.stubGlobal('fetch', fetch);
  render(<App />);
  signIn();
  await screen.findByRole('heading', { name: 'Inbox' });
  openWork();
  await screen.findByText('First task');
  fireEvent.click(screen.getByRole('button', { name: 'Trash First task' }));
  await waitFor(() => expect(screen.queryByText('First task')).not.toBeInTheDocument());
  expect(trashIfMatch).toBe('3');
  fireEvent.click(screen.getByRole('button', { name: 'Open Trash' }));
  expect(await screen.findByRole('heading', { name: 'Trash' })).toBeVisible();
  expect(screen.getByText('First task')).toBeVisible();
  fireEvent.click(screen.getByRole('button', { name: 'Restore First task' }));
  await waitFor(() => expect(screen.queryByText('First task')).not.toBeInTheDocument());
  expect(restoreBody).toEqual({ version: 4 });
  fireEvent.click(screen.getByRole('button', { name: 'Open Work' }));
  expect(await screen.findByText('First task')).toBeVisible();
});

test('refreshes server Task state on stale conflict instead of overwriting it', async () => {
  let taskLoads = 0;
  const serverTask = { ...workTask, title: 'Server title', version: 4 };
  const fetch = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    if (url.endsWith('/api/v1/auth/token')) return json(tokens);
    if (url.endsWith('/api/v1/account/bootstrap'))
      return json({ preferences: { timezone: 'Europe/London' }, inbox });
    if (url.endsWith('/api/v1/lists')) return json({ results: [inbox, work] });
    if (url.endsWith(`/api/v1/tasks/${workTask.id}`) && init?.method === 'PATCH') {
      expect(JSON.parse(String(init.body))).toEqual({ version: 3, title: 'My stale edit' });
      return json(
        {
          error: {
            code: 'version_conflict',
            details: { current: { id: workTask.id, version: 4 } },
          },
        },
        409,
      );
    }
    if (url.endsWith('/api/v1/tasks')) {
      taskLoads += 1;
      return json({ results: taskLoads === 1 ? [workTask] : [serverTask] });
    }
    throw new Error(`Unhandled request: ${url}`);
  });
  vi.stubGlobal('fetch', fetch);
  render(<App />);
  signIn();
  await screen.findByRole('heading', { name: 'Inbox' });
  openWork();
  await screen.findByText('First task');
  fireEvent.click(screen.getByRole('button', { name: 'Edit First task' }));
  fireEvent.change(screen.getByLabelText('Task title'), { target: { value: 'My stale edit' } });
  fireEvent.click(screen.getByRole('button', { name: 'Save task' }));
  expect(await screen.findByRole('alert')).toHaveTextContent('changed elsewhere');
  expect(screen.getByLabelText('Task title')).toHaveValue('My stale edit');
  expect(screen.queryByText('Server title')).not.toBeInTheDocument();
  expect(taskLoads).toBe(2);
});

test('preserves a failed Task edit on network error', async () => {
  const fetch = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    if (url.endsWith('/api/v1/auth/token')) return json(tokens);
    if (url.endsWith('/api/v1/account/bootstrap'))
      return json({ preferences: { timezone: 'Europe/London' }, inbox });
    if (url.endsWith('/api/v1/lists')) return json({ results: [inbox, work] });
    if (url.endsWith('/api/v1/tasks')) return json({ results: [workTask] });
    if (url.endsWith(`/api/v1/tasks/${workTask.id}`) && init?.method === 'PATCH')
      throw new TypeError('offline');
    throw new Error(`Unhandled request: ${url}`);
  });
  vi.stubGlobal('fetch', fetch);
  render(<App />);
  signIn();
  await screen.findByRole('heading', { name: 'Inbox' });
  openWork();
  await screen.findByText('First task');
  fireEvent.click(screen.getByRole('button', { name: 'Edit First task' }));
  const edit = screen.getByLabelText('Task title');
  fireEvent.change(edit, { target: { value: 'Keep this edit' } });
  fireEvent.click(screen.getByRole('button', { name: 'Save task' }));
  expect(await screen.findByRole('alert')).toHaveTextContent('Connection interrupted');
  expect(screen.getByLabelText('Task title')).toHaveValue('Keep this edit');
});

test('refreshes active Tasks and Trash after a restore conflict', async () => {
  let taskLoads = 0;
  let trashLoads = 0;
  const staleTrash = {
    ...workTask,
    title: 'Stale trashed task',
    version: 4,
    is_trashed: true,
    trashed_at: '2026-09-19T07:00:00Z',
  };
  const currentTrash = { ...staleTrash, title: 'Current trashed task', version: 5 };
  const currentActive = { ...workTask, title: 'Current active task', version: 6 };
  const fetch = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    if (url.endsWith('/api/v1/auth/token')) return json(tokens);
    if (url.endsWith('/api/v1/account/bootstrap')) {
      return json({ preferences: { timezone: 'Europe/London' }, inbox });
    }
    if (url.endsWith('/api/v1/lists')) return json({ results: [inbox, work] });
    if (url.endsWith('/api/v1/tasks')) {
      taskLoads += 1;
      return json({ results: taskLoads === 1 ? [workTask] : [currentActive] });
    }
    if (url.endsWith('/api/v1/trash/tasks')) {
      trashLoads += 1;
      return json({ results: trashLoads === 1 ? [staleTrash] : [currentTrash] });
    }
    if (url.endsWith(`/api/v1/tasks/${workTask.id}/restore`) && init?.method === 'POST') {
      expect(JSON.parse(String(init.body))).toEqual({ version: 4 });
      return json({ error: { code: 'version_conflict', details: {} } }, 409);
    }
    throw new Error(`Unhandled request: ${url}`);
  });
  vi.stubGlobal('fetch', fetch);
  render(<App />);
  signIn();
  await screen.findByRole('heading', { name: 'Inbox' });
  fireEvent.click(screen.getByRole('button', { name: 'Open Trash' }));
  await screen.findByText('Stale trashed task');
  fireEvent.click(screen.getByRole('button', { name: 'Restore Stale trashed task' }));

  expect(await screen.findByText('Current trashed task')).toBeVisible();
  expect(await screen.findByRole('alert')).toHaveTextContent('changed elsewhere');
  fireEvent.click(screen.getByRole('button', { name: 'Open Work' }));
  expect(await screen.findByText('Current active task')).toBeVisible();
  expect(taskLoads).toBe(2);
  expect(trashLoads).toBe(2);
});
