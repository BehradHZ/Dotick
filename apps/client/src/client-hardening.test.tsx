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
  version: 4,
  default_column: { id: '66666666-6666-4666-8666-666666666666', is_default: true },
};
const taskBase = {
  id: '77777777-7777-4777-8777-777777777777',
  title: 'Private task',
  status: 'todo',
  version: 1,
  column_id: work.default_column.id,
  owner_user_id: '44444444-4444-4444-8444-444444444444',
  created_by_user_id: '44444444-4444-4444-8444-444444444444',
  source: { platform: 'manual', external_account_id: null, external_id: null },
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

function workspaceFetch(options?: {
  lists?: () => Array<typeof inbox>;
  tasks?: () => Array<typeof taskBase>;
}) {
  return vi.fn(async (input: RequestInfo | URL) => {
    const url = String(input);
    if (url.endsWith('/api/v1/auth/token')) return json(tokens);
    if (url.endsWith('/api/v1/account/bootstrap')) {
      return json({ preferences: { timezone: 'Europe/London' }, inbox });
    }
    if (url.endsWith('/api/v1/lists')) {
      return json({ results: options?.lists?.() ?? [inbox, work] });
    }
    if (url.endsWith('/api/v1/tasks')) return json({ results: options?.tasks?.() ?? [] });
    throw new Error(`Unhandled request: ${url}`);
  });
}

afterEach(() => vi.unstubAllGlobals());

test('preserves a List edit draft after a transient network failure', async () => {
  const fetch = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    if (url.endsWith('/api/v1/auth/token')) return json(tokens);
    if (url.endsWith('/api/v1/account/bootstrap')) {
      return json({ preferences: { timezone: 'Europe/London' }, inbox });
    }
    if (url.endsWith('/api/v1/lists')) return json({ results: [inbox, work] });
    if (url.endsWith(`/api/v1/lists/${work.id}`) && init?.method === 'PATCH') {
      throw new TypeError('offline');
    }
    if (url.endsWith('/api/v1/tasks')) return json({ results: [] });
    throw new Error(`Unhandled request: ${url}`);
  });
  vi.stubGlobal('fetch', fetch);
  render(<App />);
  signIn();
  await screen.findByRole('heading', { name: 'Inbox' });
  openWork();

  const edit = screen.getByLabelText('List title');
  fireEvent.change(edit, { target: { value: 'Keep this list edit' } });
  fireEvent.click(screen.getByRole('button', { name: 'Rename list' }));

  expect(await screen.findByRole('alert')).toHaveTextContent('Connection interrupted');
  expect(screen.getByLabelText('List title')).toHaveValue('Keep this list edit');
});

test('preserves Persian, English, and mixed RTL/LTR Task titles exactly', async () => {
  const operationIds = [
    'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',
    'bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb',
    'cccccccc-cccc-4ccc-8ccc-cccccccccccc',
  ] as const;
  const taskIds = [
    '88888888-8888-4888-8888-888888888881',
    '88888888-8888-4888-8888-888888888882',
    '88888888-8888-4888-8888-888888888883',
  ] as const;
  vi.stubGlobal('crypto', {
    randomUUID: vi
      .fn()
      .mockReturnValueOnce(operationIds[0])
      .mockReturnValueOnce(operationIds[1])
      .mockReturnValueOnce(operationIds[2]),
  });
  const bodies: Array<Record<string, unknown>> = [];
  let createdCount = 0;
  const fetch = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    if (url.endsWith('/api/v1/auth/token')) return json(tokens);
    if (url.endsWith('/api/v1/account/bootstrap')) {
      return json({ preferences: { timezone: 'Europe/London' }, inbox });
    }
    if (url.endsWith('/api/v1/lists')) return json({ results: [inbox, work] });
    if (url.endsWith('/api/v1/tasks') && init?.method === 'POST') {
      const body = JSON.parse(String(init.body)) as Record<string, unknown>;
      bodies.push(body);
      const created = {
        ...taskBase,
        id: taskIds[createdCount],
        title: body.title as string,
        column_id: body.column_id as string,
      };
      createdCount += 1;
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

  const titles = ['خرید نان', 'Write report', 'جلسه Project X ساعت 10'];
  for (const title of titles) {
    const draft = screen.getByLabelText('New task');
    fireEvent.change(draft, { target: { value: title } });
    expect(draft).toHaveValue(title);
    fireEvent.click(screen.getByRole('button', { name: 'Add task' }));
    expect(await screen.findByText(title, { exact: true })).toBeVisible();
  }

  expect(bodies.map((body) => body.title)).toEqual(titles);
  expect(bodies.map((body) => body.column_id)).toEqual([
    work.default_column.id,
    work.default_column.id,
    work.default_column.id,
  ]);
  expect(bodies.map((body) => body.operation_id)).toEqual(operationIds);
});

test('keeps Inbox visually distinct from ordinary Lists', async () => {
  vi.stubGlobal('fetch', workspaceFetch());
  render(<App />);
  signIn();
  await screen.findByRole('heading', { name: 'Inbox' });

  expect(screen.getByRole('button', { name: 'Open Inbox' })).toHaveTextContent('⌂ Inbox');
  expect(screen.getByRole('button', { name: 'Open Work' })).not.toHaveTextContent('⌂');
});

test('removes private workspace UI before the sign-out request finishes', async () => {
  let resolveLogout: ((response: Response) => void) | undefined;
  const logoutResponse = new Promise<Response>((resolve) => {
    resolveLogout = resolve;
  });
  const fetch = vi.fn(async (input: RequestInfo | URL) => {
    const url = String(input);
    if (url.endsWith('/api/v1/auth/token')) return json(tokens);
    if (url.endsWith('/api/v1/account/bootstrap')) {
      return json({ preferences: { timezone: 'Europe/London' }, inbox });
    }
    if (url.endsWith('/api/v1/lists')) return json({ results: [inbox, work] });
    if (url.endsWith('/api/v1/tasks')) return json({ results: [taskBase] });
    if (url.endsWith('/api/v1/auth/logout')) return logoutResponse;
    throw new Error(`Unhandled request: ${url}`);
  });
  vi.stubGlobal('fetch', fetch);
  render(<App />);
  signIn();
  await screen.findByRole('heading', { name: 'Inbox' });
  openWork();
  await screen.findByText('Private task');

  fireEvent.click(screen.getByRole('button', { name: 'Sign out' }));

  expect(screen.getByRole('heading', { name: 'Sign in' })).toBeVisible();
  expect(screen.queryByText('Private task')).not.toBeInTheDocument();
  expect(screen.queryByText(user.email)).not.toBeInTheDocument();
  resolveLogout?.(new Response(null, { status: 204 }));
  await Promise.resolve();
});

test('reloads authoritative server state when the web client is re-entered', async () => {
  let listLoads = 0;
  const serverWork = { ...work, title: 'Server Work', version: 5 };
  vi.stubGlobal(
    'fetch',
    workspaceFetch({
      lists: () => {
        listLoads += 1;
        return listLoads === 1 ? [inbox, work] : [inbox, serverWork];
      },
    }),
  );
  render(<App />);
  signIn();
  await screen.findByRole('heading', { name: 'Inbox' });
  openWork();
  expect(await screen.findByRole('heading', { name: 'Work' })).toBeVisible();

  fireEvent.focus(window);

  expect(await screen.findByRole('heading', { name: 'Server Work' })).toBeVisible();
  await waitFor(() => expect(listLoads).toBe(2));
});
