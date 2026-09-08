import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { expect, test, vi } from 'vitest';
import App from './App';

const inbox = {
  id: '11111111-1111-4111-8111-111111111111',
  title: 'Inbox',
  folder_id: null,
  is_inbox: true,
  position: 0,
  is_trashed: false,
  trashed_at: null,
  default_column: { id: '22222222-2222-4222-8222-222222222222', is_default: true },
};

const task = {
  id: '33333333-3333-4333-8333-333333333333',
  title: 'خرید نان',
  status: 'todo',
  version: 1,
  column_id: inbox.default_column.id,
  owner_user_id: '44444444-4444-4444-8444-444444444444',
  created_by_user_id: '44444444-4444-4444-8444-444444444444',
  source: { platform: 'manual', external_account_id: null, external_id: null },
  created_at: '2026-09-08T10:00:00Z',
  updated_at: '2026-09-08T10:00:00Z',
};

function json(data: unknown, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

function api(extra?: (url: string, init?: RequestInit) => Response | undefined) {
  return vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    const overridden = extra?.(url, init);
    if (overridden) return overridden;
    if (url.endsWith('/api/v1/auth/token')) {
      return json({
        access: 'access-token',
        refresh: 'refresh-token',
        user: { email: 'developer@example.test', handle: '', display_name: '' },
      });
    }
    if (url.endsWith('/api/v1/account/bootstrap')) {
      return json({ preferences: { timezone: 'UTC' }, inbox });
    }
    if (url.endsWith('/api/v1/lists')) return json({ results: [inbox] });
    if (url.endsWith('/api/v1/tasks')) return json({ results: [task] });
    if (url.endsWith('/api/v1/trash/tasks')) return json({ results: [] });
    throw new Error(`Unhandled request: ${url}`);
  });
}

async function signIn() {
  fireEvent.change(screen.getByLabelText('Email'), {
    target: { value: 'developer@example.test' },
  });
  fireEvent.change(screen.getByLabelText('Password'), { target: { value: 'test-password' } });
  fireEvent.click(screen.getByRole('button', { name: 'Sign in' }));
  await screen.findByText('خرید نان');
}

test('signs in and shows persisted Inbox tasks', async () => {
  vi.stubGlobal('fetch', api());
  render(<App />);
  await signIn();
  expect(screen.getByRole('button', { name: 'Open Inbox' })).toBeVisible();
  expect(screen.getByRole('button', { name: 'Sign out' })).toBeVisible();
});

test('failed task creation retains draft and successful retry adds task', async () => {
  let attempts = 0;
  vi.stubGlobal(
    'fetch',
    api((url, init) => {
      if (url.endsWith('/api/v1/tasks') && init?.method === 'POST') {
        attempts += 1;
        if (attempts === 1) throw new TypeError('offline');
        return json({ ...task, id: '55555555-5555-4555-8555-555555555555' }, 201);
      }
      return undefined;
    }),
  );
  render(<App />);
  await signIn();
  const input = screen.getByLabelText('New task');
  fireEvent.change(input, { target: { value: 'خرید نان' } });
  fireEvent.click(screen.getByRole('button', { name: 'Add task' }));
  expect(await screen.findByRole('alert')).toHaveTextContent('Connection interrupted');
  expect(input).toHaveValue('خرید نان');
  fireEvent.click(screen.getByRole('button', { name: 'Add task' }));
  expect(await screen.findByText('Task created.')).toBeVisible();
  expect(input).toHaveValue('');
});

test('marks task done using optimistic version', async () => {
  const fetch = api((url, init) => {
    if (url.endsWith(`/api/v1/tasks/${task.id}`) && init?.method === 'PATCH') {
      return json({ ...task, status: 'done', version: 2 });
    }
    return undefined;
  });
  vi.stubGlobal('fetch', fetch);
  render(<App />);
  await signIn();
  fireEvent.click(screen.getByRole('button', { name: 'Mark خرید نان done' }));
  expect(await screen.findByText('Done')).toBeVisible();
  await waitFor(() => {
    const call = fetch.mock.calls.find(([url]) => String(url).endsWith(`/api/v1/tasks/${task.id}`));
    expect(JSON.parse(String(call?.[1]?.body))).toEqual({ version: 1, status: 'done' });
  });
});

test('signing out removes private tasks', async () => {
  vi.stubGlobal('fetch', api());
  render(<App />);
  await signIn();
  fireEvent.click(screen.getByRole('button', { name: 'Sign out' }));
  expect(screen.queryByText('خرید نان')).not.toBeInTheDocument();
  expect(screen.getByLabelText('Password')).toHaveValue('');
});
