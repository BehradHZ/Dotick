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

function signIn() {
  fireEvent.change(screen.getByLabelText('Email'), { target: { value: user.email } });
  fireEvent.change(screen.getByLabelText('Password'), { target: { value: 'Safe-password-8!' } });
  fireEvent.click(screen.getByRole('button', { name: 'Sign in' }));
}

function baseFetch() {
  return vi.fn(async (input: RequestInfo | URL) => {
    const url = String(input);
    if (url.endsWith('/api/v1/auth/token')) return json(tokens);
    if (url.endsWith('/api/v1/account/bootstrap')) {
      return json({ preferences: { timezone: 'Europe/London' }, inbox });
    }
    if (url.endsWith('/api/v1/lists')) return json({ results: [inbox, work] });
    if (url.endsWith('/api/v1/tasks')) return json({ results: [] });
    throw new Error(`Unhandled request: ${url}`);
  });
}

afterEach(() => vi.unstubAllGlobals());

test('renders and selects server Lists without exposing the technical default Column', async () => {
  vi.stubGlobal('fetch', baseFetch());
  render(<App />);
  signIn();
  await screen.findByRole('heading', { name: 'Inbox' });
  fireEvent.click(screen.getByRole('button', { name: 'Open Work' }));
  expect(await screen.findByRole('heading', { name: 'Work' })).toBeVisible();
  expect(screen.queryByText(/default column/i)).not.toBeInTheDocument();
  expect(screen.getByLabelText('List title')).toHaveValue('Work');
});

test('reuses the same operation ID for the same failed List draft', async () => {
  vi.stubGlobal('crypto', {
    randomUUID: vi.fn(() => 'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa'),
  });
  const bodies: Array<Record<string, unknown>> = [];
  let posts = 0;
  const created = { ...work, id: '77777777-7777-4777-8777-777777777777', title: 'Personal', version: 7 };
  const fetch = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    if (url.endsWith('/api/v1/auth/token')) return json(tokens);
    if (url.endsWith('/api/v1/account/bootstrap')) return json({ preferences: { timezone: 'Europe/London' }, inbox });
    if (url.endsWith('/api/v1/lists') && init?.method === 'POST') {
      bodies.push(JSON.parse(String(init.body)) as Record<string, unknown>);
      posts += 1;
      if (posts === 1) throw new TypeError('offline');
      return json(created, 201);
    }
    if (url.endsWith('/api/v1/lists')) return json({ results: [inbox, work] });
    if (url.endsWith('/api/v1/tasks')) return json({ results: [] });
    throw new Error(`Unhandled request: ${url}`);
  });
  vi.stubGlobal('fetch', fetch);
  render(<App />);
  signIn();
  await screen.findByRole('heading', { name: 'Inbox' });
  const draft = screen.getByLabelText('New list');
  fireEvent.change(draft, { target: { value: 'Personal' } });
  fireEvent.click(screen.getByRole('button', { name: 'Add list' }));
  expect(await screen.findByRole('alert')).toHaveTextContent('Connection interrupted');
  expect(draft).toHaveValue('Personal');
  fireEvent.click(screen.getByRole('button', { name: 'Add list' }));
  expect(await screen.findByRole('heading', { name: 'Personal' })).toBeVisible();
  expect(draft).toHaveValue('');
  expect(bodies).toHaveLength(2);
  expect(bodies[0]?.operation_id).toBe('aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa');
  expect(bodies[1]?.operation_id).toBe(bodies[0]?.operation_id);
});

test('generates a new operation ID when the failed List draft intent changes', async () => {
  const randomUUID = vi
    .fn()
    .mockReturnValueOnce('aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa')
    .mockReturnValueOnce('bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb');
  vi.stubGlobal('crypto', { randomUUID });
  const bodies: Array<Record<string, unknown>> = [];
  const fetch = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    if (url.endsWith('/api/v1/auth/token')) return json(tokens);
    if (url.endsWith('/api/v1/account/bootstrap')) return json({ preferences: { timezone: 'Europe/London' }, inbox });
    if (url.endsWith('/api/v1/lists') && init?.method === 'POST') {
      bodies.push(JSON.parse(String(init.body)) as Record<string, unknown>);
      throw new TypeError('offline');
    }
    if (url.endsWith('/api/v1/lists')) return json({ results: [inbox, work] });
    if (url.endsWith('/api/v1/tasks')) return json({ results: [] });
    throw new Error(`Unhandled request: ${url}`);
  });
  vi.stubGlobal('fetch', fetch);
  render(<App />);
  signIn();
  await screen.findByRole('heading', { name: 'Inbox' });
  const draft = screen.getByLabelText('New list');
  fireEvent.change(draft, { target: { value: 'First' } });
  fireEvent.click(screen.getByRole('button', { name: 'Add list' }));
  await screen.findByRole('alert');
  fireEvent.change(draft, { target: { value: 'Second' } });
  fireEvent.click(screen.getByRole('button', { name: 'Add list' }));
  await waitFor(() => expect(bodies).toHaveLength(2));
  expect(bodies[0]?.operation_id).not.toBe(bodies[1]?.operation_id);
});

test('uses the current List version and reloads server state on version conflict', async () => {
  let listLoads = 0;
  const serverWork = { ...work, title: 'Server Work', version: 5 };
  const fetch = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    if (url.endsWith('/api/v1/auth/token')) return json(tokens);
    if (url.endsWith('/api/v1/account/bootstrap')) return json({ preferences: { timezone: 'Europe/London' }, inbox });
    if (url.endsWith(`/api/v1/lists/${work.id}`) && init?.method === 'PATCH') {
      expect(JSON.parse(String(init.body))).toEqual({ version: 4, title: 'My overwrite' });
      return json({ error: { code: 'version_conflict', details: { current: { id: work.id, version: 5 } } } }, 409);
    }
    if (url.endsWith('/api/v1/lists')) {
      listLoads += 1;
      return json({ results: listLoads === 1 ? [inbox, work] : [inbox, serverWork] });
    }
    if (url.endsWith('/api/v1/tasks')) return json({ results: [] });
    throw new Error(`Unhandled request: ${url}`);
  });
  vi.stubGlobal('fetch', fetch);
  render(<App />);
  signIn();
  await screen.findByRole('heading', { name: 'Inbox' });
  fireEvent.click(screen.getByRole('button', { name: 'Open Work' }));
  fireEvent.change(screen.getByLabelText('List title'), { target: { value: 'My overwrite' } });
  fireEvent.click(screen.getByRole('button', { name: 'Rename list' }));
  expect(await screen.findByRole('heading', { name: 'Server Work' })).toBeVisible();
  expect(screen.getByLabelText('List title')).toHaveValue('Server Work');
  expect(await screen.findByRole('alert')).toHaveTextContent('changed elsewhere');
  expect(listLoads).toBe(2);
});
