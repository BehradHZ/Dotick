import { afterEach, expect, test, vi } from 'vitest';

import {
  ApiError,
  defaultApiUrl,
  ReauthenticationRequiredError,
  signIn,
  type ColumnRecord,
  type FolderRecord,
  type ListRecord,
} from './api';

const baseUrl = 'https://api.example.test';
const user = { email: 'owner@example.test', handle: 'owner', display_name: 'Owner' };
const folder: FolderRecord = {
  id: '11111111-1111-4111-8111-111111111111',
  title: 'Focus',
  position: 0,
  version: 1,
  is_trashed: false,
  trashed_at: null,
};
const list: ListRecord = {
  id: '22222222-2222-4222-8222-222222222222',
  title: 'Work',
  folder_id: folder.id,
  is_inbox: false,
  position: 3,
  version: 2,
  is_trashed: false,
  trashed_at: null,
  default_column: { id: '33333333-3333-4333-8333-333333333333', is_default: true },
};
const column: ColumnRecord = {
  id: '44444444-4444-4444-8444-444444444444',
  list_id: list.id,
  title: 'Doing',
  position: 1,
  version: 4,
  is_default: false,
};

function json(data: unknown, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

function tokens(access = 'access-one', refresh = 'refresh-one') {
  return { access, refresh, user };
}

function storageText(storage: Storage) {
  return Array.from({ length: storage.length }, (_, index) => {
    const key = storage.key(index) ?? '';
    return `${key}:${storage.getItem(key) ?? ''}`;
  }).join('\n');
}

afterEach(() => {
  window.localStorage.clear();
  window.sessionStorage.clear();
  vi.unstubAllGlobals();
  vi.unstubAllEnvs();
});

test('discovers and normalizes a configured API URL', () => {
  vi.stubEnv('EXPO_PUBLIC_API_URL', ' https://api.example.test/// ');
  expect(defaultApiUrl()).toBe(baseUrl);
});

test('acquires email/password tokens without persisting credentials or tokens', async () => {
  const fetch = vi.fn(async (_input: RequestInfo | URL, init?: RequestInit) => {
    expect(new Headers(init?.headers).get('Authorization')).toBeNull();
    expect(JSON.parse(String(init?.body))).toEqual({
      email: user.email,
      password: 'correct horse battery staple',
    });
    return json(tokens());
  });
  vi.stubGlobal('fetch', fetch);

  const session = await signIn(baseUrl, user.email, 'correct horse battery staple');

  expect(session.isAuthenticated).toBe(true);
  expect(storageText(window.localStorage)).not.toContain('access-one');
  expect(storageText(window.localStorage)).not.toContain('refresh-one');
  expect(storageText(window.sessionStorage)).not.toContain('access-one');
  expect(storageText(window.sessionStorage)).not.toContain('refresh-one');
});

test('refreshes a private bearer session once after an expired access token', async () => {
  const authorizations: Array<string | null> = [];
  let folderAttempts = 0;
  const fetch = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    if (url.endsWith('/api/v1/auth/token')) return json(tokens());
    if (url.endsWith('/api/v1/auth/token/refresh')) {
      expect(new Headers(init?.headers).get('Authorization')).toBeNull();
      expect(JSON.parse(String(init?.body))).toEqual({ refresh: 'refresh-one' });
      return json({ access: 'access-two', refresh: 'refresh-two' });
    }
    if (url.endsWith('/api/v1/folders')) {
      folderAttempts += 1;
      authorizations.push(new Headers(init?.headers).get('Authorization'));
      if (folderAttempts === 1) {
        return json({ error: { code: 'token_not_valid', details: 'Expired.' } }, 401);
      }
      return json({ results: [folder] });
    }
    throw new Error(`Unhandled request: ${url}`);
  });
  vi.stubGlobal('fetch', fetch);

  const session = await signIn(baseUrl, user.email, 'password');
  await expect(session.folders()).resolves.toEqual({ results: [folder] });
  expect(authorizations).toEqual(['Bearer access-one', 'Bearer access-two']);
  expect(storageText(window.localStorage)).not.toContain('refresh-two');
  expect(storageText(window.sessionStorage)).not.toContain('refresh-two');
});

test('does not enter a refresh loop when the retried request is still unauthorized', async () => {
  let refreshAttempts = 0;
  let folderAttempts = 0;
  const fetch = vi.fn(async (input: RequestInfo | URL) => {
    const url = String(input);
    if (url.endsWith('/api/v1/auth/token')) return json(tokens());
    if (url.endsWith('/api/v1/auth/token/refresh')) {
      refreshAttempts += 1;
      return json({ access: 'access-two', refresh: 'refresh-two' });
    }
    if (url.endsWith('/api/v1/folders')) {
      folderAttempts += 1;
      return json({ error: { code: 'token_not_valid', details: 'Rejected.' } }, 401);
    }
    throw new Error(`Unhandled request: ${url}`);
  });
  vi.stubGlobal('fetch', fetch);

  const session = await signIn(baseUrl, user.email, 'password');
  await expect(session.folders()).rejects.toBeInstanceOf(ReauthenticationRequiredError);
  expect(refreshAttempts).toBe(1);
  expect(folderAttempts).toBe(2);
  expect(session.isAuthenticated).toBe(false);
});

test('requires reauthentication when the refresh session has been revoked', async () => {
  let refreshAttempts = 0;
  let folderAttempts = 0;
  const fetch = vi.fn(async (input: RequestInfo | URL) => {
    const url = String(input);
    if (url.endsWith('/api/v1/auth/token')) return json(tokens());
    if (url.endsWith('/api/v1/folders')) {
      folderAttempts += 1;
      return json({ error: { code: 'token_not_valid', details: 'Expired.' } }, 401);
    }
    if (url.endsWith('/api/v1/auth/token/refresh')) {
      refreshAttempts += 1;
      return json({ error: { code: 'token_not_valid', details: 'Session revoked.' } }, 401);
    }
    throw new Error(`Unhandled request: ${url}`);
  });
  vi.stubGlobal('fetch', fetch);

  const session = await signIn(baseUrl, user.email, 'password');
  const error = await session.folders().catch((failure: unknown) => failure);
  expect(error).toBeInstanceOf(ReauthenticationRequiredError);
  expect(error).toMatchObject({ status: 401, code: 'reauthentication_required' });
  expect(session.isAuthenticated).toBe(false);

  await expect(session.folders()).rejects.toBeInstanceOf(ReauthenticationRequiredError);
  expect(refreshAttempts).toBe(1);
  expect(folderAttempts).toBe(1);
});

test(
  'refreshes once when necessary so sign-out can revoke the current server session',
  async () => {
    let logoutAttempts = 0;
    let refreshAttempts = 0;
    const authorizations: Array<string | null> = [];
    const fetch = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (url.endsWith('/api/v1/auth/token')) return json(tokens());
      if (url.endsWith('/api/v1/auth/token/refresh')) {
        refreshAttempts += 1;
        return json({ access: 'access-two', refresh: 'refresh-two' });
      }
      if (url.endsWith('/api/v1/auth/logout')) {
        logoutAttempts += 1;
        authorizations.push(new Headers(init?.headers).get('Authorization'));
        return logoutAttempts === 1
          ? json({ error: { code: 'token_not_valid', details: 'Expired.' } }, 401)
          : new Response(null, { status: 204 });
      }
      throw new Error(`Unhandled request: ${url}`);
    });
    vi.stubGlobal('fetch', fetch);

    const session = await signIn(baseUrl, user.email, 'password');
    await session.signOut();

    expect(logoutAttempts).toBe(2);
    expect(refreshAttempts).toBe(1);
    expect(authorizations).toEqual(['Bearer access-one', 'Bearer access-two']);
    expect(session.isAuthenticated).toBe(false);
    await expect(session.tasks()).rejects.toBeInstanceOf(ReauthenticationRequiredError);
  },
);

test('preserves stable API error code and details from the current envelope', async () => {
  vi.stubGlobal(
    'fetch',
    vi
      .fn()
      .mockResolvedValueOnce(json(tokens()))
      .mockResolvedValueOnce(
        json(
          {
            error: {
              code: 'version_conflict',
              details: {
                message: 'The Folder changed after the supplied version.',
                current: { id: folder.id, version: 2 },
              },
            },
          },
          409,
        ),
      ),
  );

  const session = await signIn(baseUrl, user.email, 'password');
  const error = await session
    .updateFolder(folder.id, { version: 1, title: 'Later' })
    .catch((failure: unknown) => failure);

  expect(error).toBeInstanceOf(ApiError);
  expect(error).toMatchObject({
    status: 409,
    code: 'version_conflict',
    details: {
      message: 'The Folder changed after the supplied version.',
      current: { id: folder.id, version: 2 },
    },
    message: 'The Folder changed after the supplied version.',
  });
});

test('sends current organization idempotency and optimistic-concurrency contracts', async () => {
  const calls: Array<{ url: string; init?: RequestInit }> = [];
  const fetch = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    if (url.endsWith('/api/v1/auth/token')) return json(tokens());
    calls.push({ url, init });
    if (url.endsWith('/api/v1/folders')) return json(folder, 201);
    if (url.endsWith('/api/v1/lists')) return json(list, 201);
    if (url.endsWith(`/api/v1/lists/${list.id}/columns`)) return json(column, 201);
    if (url.endsWith(`/api/v1/columns/${column.id}`) && init?.method === 'PATCH') {
      return json({ ...column, title: 'Done', version: 5 });
    }
    if (url.includes(`/api/v1/columns/${column.id}?items=move_to_default`)) {
      return new Response(null, { status: 204 });
    }
    throw new Error(`Unhandled request: ${url}`);
  });
  vi.stubGlobal('fetch', fetch);

  const session = await signIn(baseUrl, user.email, 'password');
  await session.createFolder({
    title: folder.title,
    operation_id: 'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',
  });
  await session.createList({
    title: list.title,
    operation_id: 'bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb',
    folder_id: folder.id,
    position: 3,
  });
  await session.createColumn(list.id, {
    title: column.title,
    operation_id: 'cccccccc-cccc-4ccc-8ccc-cccccccccccc',
  });
  await session.updateColumn(column.id, { version: 4, title: 'Done' });
  await session.deleteColumn(column.id, 5, 'move_to_default');

  expect(JSON.parse(String(calls[0]?.init?.body))).toEqual({
    title: 'Focus',
    operation_id: 'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',
  });
  expect(JSON.parse(String(calls[1]?.init?.body))).toEqual({
    title: 'Work',
    operation_id: 'bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb',
    folder_id: folder.id,
    position: 3,
  });
  expect(JSON.parse(String(calls[2]?.init?.body))).toEqual({
    title: 'Doing',
    operation_id: 'cccccccc-cccc-4ccc-8ccc-cccccccccccc',
  });
  expect(JSON.parse(String(calls[3]?.init?.body))).toEqual({ version: 4, title: 'Done' });
  expect(new Headers(calls[4]?.init?.headers).get('If-Match')).toBe('5');
  expect(calls[4]?.url).toBe(`${baseUrl}/api/v1/columns/${column.id}?items=move_to_default`);
});
