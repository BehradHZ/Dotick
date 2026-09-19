import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { expect, test, vi } from 'vitest';

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
const task = {
  id: '33333333-3333-4333-8333-333333333333',
  title: 'Server task',
  status: 'todo',
  version: 1,
  column_id: inbox.default_column.id,
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

test('replaces the Checkpoint workbench with a server-backed I1 workspace', async () => {
  const fetch = vi.fn(async (input: RequestInfo | URL) => {
    const url = String(input);
    if (url.endsWith('/api/v1/auth/token')) return json(tokens);
    if (url.endsWith('/api/v1/account/bootstrap'))
      return json({ preferences: { timezone: 'Europe/London' }, inbox });
    if (url.endsWith('/api/v1/lists')) return json({ results: [inbox] });
    if (url.endsWith('/api/v1/tasks')) return json({ results: [task] });
    throw new Error(`Unhandled request: ${url}`);
  });
  vi.stubGlobal('fetch', fetch);
  render(<App />);
  expect(screen.queryByText(/Checkpoint/i)).not.toBeInTheDocument();
  signIn();
  expect(await screen.findByRole('heading', { name: 'Inbox' })).toBeVisible();
  expect(screen.getByText('Timezone: Europe/London')).toBeVisible();
  expect(screen.getByText('1 list loaded from the server')).toBeVisible();
  expect(screen.getByText('1 task loaded from the server')).toBeVisible();
  expect(screen.getByText('Server task')).toBeVisible();
});

test('reloads authoritative server state instead of keeping an old local snapshot', async () => {
  let listLoads = 0;
  const secondList = {
    ...inbox,
    id: '55555555-5555-4555-8555-555555555555',
    title: 'Later',
    is_inbox: false,
  };
  const fetch = vi.fn(async (input: RequestInfo | URL) => {
    const url = String(input);
    if (url.endsWith('/api/v1/auth/token')) return json(tokens);
    if (url.endsWith('/api/v1/account/bootstrap'))
      return json({ preferences: { timezone: 'Europe/London' }, inbox });
    if (url.endsWith('/api/v1/lists')) {
      listLoads += 1;
      return json({ results: listLoads === 1 ? [inbox] : [inbox, secondList] });
    }
    if (url.endsWith('/api/v1/tasks')) return json({ results: [task] });
    throw new Error(`Unhandled request: ${url}`);
  });
  vi.stubGlobal('fetch', fetch);
  render(<App />);
  signIn();
  expect(await screen.findByText('1 list loaded from the server')).toBeVisible();
  fireEvent.click(screen.getByRole('button', { name: 'Reload server state' }));
  expect(await screen.findByText('2 lists loaded from the server')).toBeVisible();
  expect(listLoads).toBe(2);
});

test('returns to signed-out identity when refresh reauthentication fails', async () => {
  let listLoads = 0;
  const fetch = vi.fn(async (input: RequestInfo | URL) => {
    const url = String(input);
    if (url.endsWith('/api/v1/auth/token')) return json(tokens);
    if (url.endsWith('/api/v1/account/bootstrap'))
      return json({ preferences: { timezone: 'Europe/London' }, inbox });
    if (url.endsWith('/api/v1/lists')) {
      listLoads += 1;
      if (listLoads === 1) return json({ results: [inbox] });
      return json({ error: { code: 'token_not_valid', details: 'Expired.' } }, 401);
    }
    if (url.endsWith('/api/v1/tasks')) return json({ results: [task] });
    if (url.endsWith('/api/v1/auth/token/refresh'))
      return json({ error: { code: 'token_not_valid', details: 'Revoked.' } }, 401);
    throw new Error(`Unhandled request: ${url}`);
  });
  vi.stubGlobal('fetch', fetch);
  render(<App />);
  signIn();
  await screen.findByRole('heading', { name: 'Inbox' });
  fireEvent.click(screen.getByRole('button', { name: 'Reload server state' }));
  await waitFor(() => expect(screen.getByRole('heading', { name: 'Sign in' })).toBeVisible());
  expect(screen.queryByText('Timezone: Europe/London')).not.toBeInTheDocument();
});

test('never applies a slow Account A reload after Account B signs in', async () => {
  let tokenCalls = 0;
  let accountAReload = false;
  const pending: Array<(response: Response) => void> = [];
  const accountB = { email: 'b@example.test', handle: 'person_b', display_name: 'Person B' };
  const bInbox = {
    ...inbox,
    id: 'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',
    default_column: { id: 'bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb', is_default: true },
  };
  const fetch = vi.fn(async (input: RequestInfo | URL) => {
    const url = String(input);
    if (url.endsWith('/api/v1/auth/token')) {
      tokenCalls += 1;
      return json(
        tokenCalls === 1 ? tokens : { access: 'access-b', refresh: 'refresh-b', user: accountB },
      );
    }
    if (url.endsWith('/api/v1/auth/logout')) return new Response(null, { status: 204 });
    if (accountAReload) {
      return new Promise<Response>((resolve) => pending.push(resolve));
    }
    const activeInbox = tokenCalls === 1 ? inbox : bInbox;
    if (url.endsWith('/api/v1/account/bootstrap'))
      return json({ preferences: { timezone: 'Europe/Berlin' }, inbox: activeInbox });
    if (url.endsWith('/api/v1/lists')) return json({ results: [activeInbox] });
    if (url.endsWith('/api/v1/tasks')) return json({ results: [] });
    throw new Error(`Unhandled request: ${url}`);
  });
  vi.stubGlobal('fetch', fetch);
  render(<App />);
  signIn();
  await screen.findByText(user.email);

  accountAReload = true;
  fireEvent.click(screen.getByRole('button', { name: 'Reload server state' }));
  await waitFor(() => expect(pending).toHaveLength(3));
  fireEvent.click(screen.getByRole('button', { name: 'Sign out' }));
  await screen.findByRole('heading', { name: 'Sign in' });
  accountAReload = false;
  fireEvent.change(screen.getByLabelText('Email'), { target: { value: accountB.email } });
  fireEvent.change(screen.getByLabelText('Password'), { target: { value: 'Safe-password-8!' } });
  fireEvent.click(screen.getByRole('button', { name: 'Sign in' }));
  expect(await screen.findByText(accountB.email)).toBeVisible();

  pending[0]?.(json({ preferences: { timezone: 'Account/A' }, inbox }));
  pending[1]?.(json({ results: [{ ...inbox, title: 'Account A private list' }] }));
  pending[2]?.(json({ results: [{ ...task, title: 'Account A private task' }] }));
  await Promise.resolve();
  expect(screen.getByText(accountB.email)).toBeVisible();
  expect(screen.queryByText('Account A private list')).not.toBeInTheDocument();
  expect(screen.queryByText('Account A private task')).not.toBeInTheDocument();
});

test('does not let an older reload overwrite a newer server snapshot', async () => {
  let batch = 0;
  const pending: Array<(response: Response) => void> = [];
  const oldList = {
    ...inbox,
    id: 'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',
    title: 'Old snapshot',
    is_inbox: false,
  };
  const newList = { ...oldList, id: 'bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb', title: 'New snapshot' };
  const fetch = vi.fn(async (input: RequestInfo | URL) => {
    const url = String(input);
    if (url.endsWith('/api/v1/auth/token')) return json(tokens);
    if (url.endsWith('/api/v1/account/bootstrap')) {
      batch += 1;
      if (batch === 2) return new Promise<Response>((resolve) => pending.push(resolve));
      return json({ preferences: { timezone: 'Europe/London' }, inbox });
    }
    if (batch === 2 && (url.endsWith('/api/v1/lists') || url.endsWith('/api/v1/tasks'))) {
      return new Promise<Response>((resolve) => pending.push(resolve));
    }
    if (url.endsWith('/api/v1/lists'))
      return json({ results: batch >= 3 ? [inbox, newList] : [inbox] });
    if (url.endsWith('/api/v1/tasks')) return json({ results: [] });
    throw new Error(`Unhandled request: ${url}`);
  });
  vi.stubGlobal('fetch', fetch);
  render(<App />);
  signIn();
  await screen.findByText('1 list loaded from the server');

  fireEvent.focus(window);
  await waitFor(() => expect(pending).toHaveLength(3));
  fireEvent.focus(window);
  expect(await screen.findByText('2 lists loaded from the server')).toBeVisible();
  expect(screen.getByRole('button', { name: 'Open New snapshot' })).toBeVisible();

  pending[0]?.(json({ preferences: { timezone: 'Old/Zone' }, inbox }));
  pending[1]?.(json({ results: [inbox, oldList] }));
  pending[2]?.(json({ results: [] }));
  await Promise.resolve();
  expect(screen.getByRole('button', { name: 'Open New snapshot' })).toBeVisible();
  expect(screen.queryByRole('button', { name: 'Open Old snapshot' })).not.toBeInTheDocument();
});
