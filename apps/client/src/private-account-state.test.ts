import { expect, test, vi } from 'vitest';

import { ReauthenticationRequiredError, signIn, type ListRecord, type Task } from './api';
import { createPrivateAccountState } from './private-account-state';

const baseUrl = 'https://api.example.test';
const user = { email: 'owner@example.test', handle: 'owner', display_name: 'Owner' };
const inbox: ListRecord = {
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
const task: Task = {
  id: '33333333-3333-4333-8333-333333333333',
  title: 'Private task',
  status: 'todo',
  version: 1,
  column_id: inbox.default_column.id,
  owner_user_id: '44444444-4444-4444-8444-444444444444',
  created_by_user_id: '44444444-4444-4444-8444-444444444444',
  source: { platform: 'manual', external_account_id: null, external_id: null },
  created_at: '2026-09-18T10:00:00Z',
  updated_at: '2026-09-18T10:00:00Z',
};

function json(data: unknown, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

function tokens() {
  return { access: 'access-one', refresh: 'refresh-one', user };
}

function expectPrivateStateCleared(state: ReturnType<typeof createPrivateAccountState>) {
  expect(state.snapshot()).toEqual({
    inbox: null,
    lists: [],
    tasks: [],
    trash: [],
    taskDraft: '',
    listDraft: '',
    cachedPrivateResponses: new Map(),
  });
}

test('sign-out clears account-private workspace state, drafts, and response cache', async () => {
  let logoutCalls = 0;
  const fetch = vi.fn(async (input: RequestInfo | URL) => {
    const url = String(input);
    if (url.endsWith('/api/v1/auth/token')) return json(tokens());
    if (url.endsWith('/api/v1/auth/logout')) {
      logoutCalls += 1;
      return new Response(null, { status: 204 });
    }
    throw new Error(`Unhandled request: ${url}`);
  });
  vi.stubGlobal('fetch', fetch);

  const session = await signIn(baseUrl, user.email, 'password');
  const state = createPrivateAccountState(session);
  state.hydrate({ inbox, lists: [inbox], tasks: [task], trash: [{ ...task, is_trashed: true }] });
  state.setTaskDraft('private task draft');
  state.setListDraft('private list draft');
  state.cachePrivateResponse('/api/v1/tasks', { results: [task] });

  await session.signOut();

  expectPrivateStateCleared(state);
  expect(session.isAuthenticated).toBe(false);
  expect(logoutCalls).toBe(1);
});

test('revoked refresh clears private state and requires a fresh sign-in', async () => {
  const fetch = vi.fn(async (input: RequestInfo | URL) => {
    const url = String(input);
    if (url.endsWith('/api/v1/auth/token')) return json(tokens());
    if (url.endsWith('/api/v1/tasks')) {
      return json({ error: { code: 'token_not_valid', details: 'Expired.' } }, 401);
    }
    if (url.endsWith('/api/v1/auth/token/refresh')) {
      return json({ error: { code: 'token_not_valid', details: 'Revoked.' } }, 401);
    }
    throw new Error(`Unhandled request: ${url}`);
  });
  vi.stubGlobal('fetch', fetch);

  const session = await signIn(baseUrl, user.email, 'password');
  const state = createPrivateAccountState(session);
  state.hydrate({ inbox, lists: [inbox], tasks: [task] });
  state.setTaskDraft('account-private draft');
  state.cachePrivateResponse('/api/v1/tasks', { results: [task] });

  await expect(session.tasks()).rejects.toBeInstanceOf(ReauthenticationRequiredError);

  expectPrivateStateCleared(state);
  expect(session.isAuthenticated).toBe(false);
});
