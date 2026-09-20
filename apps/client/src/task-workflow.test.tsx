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

function signIn() {
  fireEvent.change(screen.getByLabelText('Email'), { target: { value: user.email } });
  fireEvent.change(screen.getByLabelText('Password'), { target: { value: 'Safe-password-8!' } });
  fireEvent.click(screen.getByRole('button', { name: 'Sign in' }));
}
function openWork() {
  fireEvent.click(screen.getByRole('button', { name: 'Open Work' }));
}
afterEach(() => vi.unstubAllGlobals());

test('creates a Task in the selected List destination with a client operation ID', async () => {
  vi.stubGlobal('crypto', { randomUUID: vi.fn(() => 'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa') });
  let taskCreateBody: Record<string, unknown> | undefined;
  const created = {
    ...workTask,
    id: '88888888-8888-4888-8888-888888888888',
    title: 'New task',
    version: 1,
  };
  const fetch = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    if (url.endsWith('/api/v1/auth/token')) return json(tokens);
    if (url.endsWith('/api/v1/account/bootstrap'))
      return json({ preferences: { timezone: 'Europe/London' }, inbox });
    if (url.endsWith('/api/v1/lists')) return json({ results: [inbox, work] });
    if (url.endsWith('/api/v1/tasks') && init?.method === 'POST') {
      taskCreateBody = JSON.parse(String(init.body)) as Record<string, unknown>;
      return json(created, 201);
    }
    if (url.endsWith('/api/v1/tasks')) return json({ results: [workTask] });
    throw new Error(`Unhandled request: ${url}`);
  });
  vi.stubGlobal('fetch', fetch);
  render(<App />);
  signIn();
  await screen.findByRole('heading', { name: 'Inbox' });
  openWork();
  fireEvent.change(screen.getByLabelText('New task'), { target: { value: 'New task' } });
  fireEvent.click(screen.getByRole('button', { name: 'Add task' }));
  expect(await screen.findByText('New task')).toBeVisible();
  expect(taskCreateBody).toEqual({
    title: 'New task',
    column_id: work.default_column.id,
    operation_id: 'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',
  });
  expect(screen.getByLabelText('New task')).toHaveValue('');
});

test('creates a Task when the mobile keyboard submits the draft', async () => {
  vi.stubGlobal('crypto', { randomUUID: vi.fn(() => 'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa') });
  const created = {
    ...workTask,
    id: '88888888-8888-4888-8888-888888888888',
    title: 'Mobile task',
    version: 1,
  };
  let taskCreateBody: Record<string, unknown> | undefined;
  const fetch = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    if (url.endsWith('/api/v1/auth/token')) return json(tokens);
    if (url.endsWith('/api/v1/account/bootstrap'))
      return json({ preferences: { timezone: 'Europe/London' }, inbox });
    if (url.endsWith('/api/v1/lists')) return json({ results: [inbox, work] });
    if (url.endsWith('/api/v1/tasks') && init?.method === 'POST') {
      taskCreateBody = JSON.parse(String(init.body)) as Record<string, unknown>;
      return json(created, 201);
    }
    if (url.endsWith('/api/v1/tasks')) return json({ results: [] });
    throw new Error(`Unhandled request: ${url}`);
  });
  vi.stubGlobal('fetch', fetch);
  render(<App />);
  signIn();
  await screen.findByRole('heading', { name: 'Inbox' });
  openWork();
  const draft = screen.getByLabelText('New task');
  fireEvent.change(draft, { target: { value: 'Mobile task' } });
  fireEvent.keyDown(draft, { key: 'Enter', code: 'Enter' });

  expect(await screen.findByText('Mobile task')).toBeVisible();
  expect(taskCreateBody).toMatchObject({ title: 'Mobile task' });
});

test('preserves a failed Task draft and operation ID for retry', async () => {
  vi.stubGlobal('crypto', { randomUUID: vi.fn(() => 'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa') });
  const bodies: Array<Record<string, unknown>> = [];
  let posts = 0;
  const created = { ...workTask, title: 'Retry me', version: 1 };
  const fetch = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    if (url.endsWith('/api/v1/auth/token')) return json(tokens);
    if (url.endsWith('/api/v1/account/bootstrap'))
      return json({ preferences: { timezone: 'Europe/London' }, inbox });
    if (url.endsWith('/api/v1/lists')) return json({ results: [inbox, work] });
    if (url.endsWith('/api/v1/tasks') && init?.method === 'POST') {
      bodies.push(JSON.parse(String(init.body)) as Record<string, unknown>);
      posts += 1;
      if (posts === 1) throw new TypeError('offline');
      return json(created, 201);
    }
    if (url.endsWith('/api/v1/tasks')) return json({ results: [] });
    throw new Error(`Unhandled request: ${url}`);
  });
  vi.stubGlobal('fetch', fetch);
  render(<App />);
  signIn();
  await screen.findByRole('heading', { name: 'Inbox' });
  openWork();
  const draft = screen.getByLabelText('New task');
  fireEvent.change(draft, { target: { value: 'Retry me' } });
  fireEvent.click(screen.getByRole('button', { name: 'Add task' }));
  expect(await screen.findByRole('alert')).toHaveTextContent('Connection interrupted');
  expect(draft).toHaveValue('Retry me');
  fireEvent.click(screen.getByRole('button', { name: 'Add task' }));
  await screen.findByText('Retry me');
  expect(bodies[0]?.operation_id).toBe(bodies[1]?.operation_id);
});

test('edits Task title and status using the latest returned Task version', async () => {
  const patchBodies: Array<Record<string, unknown>> = [];
  const fetch = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    if (url.endsWith('/api/v1/auth/token')) return json(tokens);
    if (url.endsWith('/api/v1/account/bootstrap'))
      return json({ preferences: { timezone: 'Europe/London' }, inbox });
    if (url.endsWith('/api/v1/lists')) return json({ results: [inbox, work] });
    if (url.endsWith('/api/v1/tasks')) return json({ results: [workTask] });
    if (url.endsWith(`/api/v1/tasks/${workTask.id}`) && init?.method === 'PATCH') {
      const body = JSON.parse(String(init.body)) as Record<string, unknown>;
      patchBodies.push(body);
      if (patchBodies.length === 1) return json({ ...workTask, title: 'Updated task', version: 4 });
      return json({ ...workTask, title: 'Updated task', status: 'done', version: 5 });
    }
    throw new Error(`Unhandled request: ${url}`);
  });
  vi.stubGlobal('fetch', fetch);
  render(<App />);
  signIn();
  await screen.findByRole('heading', { name: 'Inbox' });
  openWork();
  expect(await screen.findByText('First task')).toBeVisible();
  fireEvent.click(screen.getByRole('button', { name: 'Edit First task' }));
  fireEvent.change(screen.getByLabelText('Task title'), { target: { value: 'Updated task' } });
  fireEvent.click(screen.getByRole('button', { name: 'Save task' }));
  expect(await screen.findByText('Updated task')).toBeVisible();
  const markDone = screen.getByRole('button', { name: 'Mark Updated task Done' });
  await waitFor(() => expect(markDone).toBeEnabled());
  fireEvent.click(markDone);
  await waitFor(() => expect(screen.getByText('Done')).toBeVisible());
  expect(patchBodies).toEqual([
    { version: 3, title: 'Updated task' },
    { version: 4, status: 'done' },
  ]);
});

test("supports Todo, Done, and Won't do status controls", async () => {
  let current = workTask;
  const statusBodies: Array<{ version: number; status: 'todo' | 'done' | 'wont_do' }> = [];
  const fetch = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    if (url.endsWith('/api/v1/auth/token')) return json(tokens);
    if (url.endsWith('/api/v1/account/bootstrap'))
      return json({ preferences: { timezone: 'Europe/London' }, inbox });
    if (url.endsWith('/api/v1/lists')) return json({ results: [inbox, work] });
    if (url.endsWith('/api/v1/tasks')) return json({ results: [current] });
    if (url.endsWith(`/api/v1/tasks/${workTask.id}`) && init?.method === 'PATCH') {
      const body = JSON.parse(String(init.body)) as {
        version: number;
        status: 'todo' | 'done' | 'wont_do';
      };
      statusBodies.push(body);
      current = { ...current, status: body.status, version: body.version + 1 };
      return json(current);
    }
    throw new Error(`Unhandled request: ${url}`);
  });
  vi.stubGlobal('fetch', fetch);
  render(<App />);
  signIn();
  await screen.findByRole('heading', { name: 'Inbox' });
  openWork();
  await screen.findByText('First task');
  fireEvent.click(screen.getByRole('button', { name: 'Mark First task Done' }));
  expect(await screen.findByText('Done')).toBeVisible();
  fireEvent.click(screen.getByRole('button', { name: "Mark First task Won't do" }));
  expect(await screen.findByText("Won't do")).toBeVisible();
  fireEvent.click(screen.getByRole('button', { name: 'Mark First task Todo' }));
  expect(await screen.findByText('Todo')).toBeVisible();
  expect(statusBodies).toEqual([
    { version: 3, status: 'done' },
    { version: 4, status: 'wont_do' },
    { version: 5, status: 'todo' },
  ]);
});
