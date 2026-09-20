import { execFileSync } from 'node:child_process';

import { expect, test, type APIRequestContext, type Page } from '@playwright/test';

const apiBaseUrl = 'http://127.0.0.1:8000';

type Tokens = { access: string };
type ListResource = {
  id: string;
  version: number;
  default_column: { id: string };
};
type ColumnResource = { id: string; version: number };
type TaskResource = { id: string; version: number };

function developmentCredentials() {
  const password = process.env.DOTICK_DEVELOPMENT_PASSWORD;
  if (!password) {
    throw new Error('Set DOTICK_DEVELOPMENT_PASSWORD before running the E2E suite.');
  }
  return { email: process.env.DOTICK_E2E_EMAIL ?? 'developer@example.test', password };
}

async function signIn(page: Page) {
  const { email, password } = developmentCredentials();
  await page.goto('/');
  await page.getByLabel('Email', { exact: true }).fill(email);
  await page.getByLabel('Password', { exact: true }).fill(password);
  await page.getByRole('button', { name: 'Sign in', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Inbox' })).toBeVisible();
}

function provisionLocalAccount(email: string) {
  execFileSync(
    'python',
    ['-m', 'uv', 'run', 'python', 'apps/api/manage.py', 'create_developer', '--email', email],
    { cwd: process.cwd(), env: process.env, stdio: 'pipe' },
  );
}

async function accessToken(request: APIRequestContext, email: string, password: string) {
  const response = await request.post(`${apiBaseUrl}/api/v1/auth/token`, {
    data: { email, password },
  });
  expect(response.status()).toBe(200);
  return ((await response.json()) as Tokens).access;
}

function authorization(access: string) {
  return { Authorization: `Bearer ${access}` };
}

test('failed List and Task saves preserve their browser drafts', async ({ page }) => {
  await signIn(page);

  const listDraft = `Unsaved list ${crypto.randomUUID()}`;
  const listsRoute = '**/api/v1/lists';
  await page.route(listsRoute, async (route) => {
    if (route.request().method() === 'POST') await route.abort('failed');
    else await route.continue();
  });
  const listInput = page.getByLabel('New list', { exact: true });
  await listInput.pressSequentially(listDraft);
  await page.getByRole('button', { name: 'Add list' }).click();
  await expect(page.getByRole('alert')).toContainText('Connection interrupted');
  await expect(listInput).toHaveValue(listDraft);
  await page.unroute(listsRoute);

  const taskDraft = `Unsaved task ${crypto.randomUUID()}`;
  await page.route('**/api/v1/tasks', async (route) => {
    if (route.request().method() === 'POST') await route.abort('failed');
    else await route.continue();
  });
  const taskInput = page.getByLabel('New task', { exact: true });
  await taskInput.pressSequentially(taskDraft);
  await page.getByRole('button', { name: 'Add task' }).click();
  await expect(page.getByRole('alert')).toContainText('Connection interrupted');
  await expect(taskInput).toHaveValue(taskDraft);
});

test('accounts cannot read or mutate each other resources and operation IDs stay owner-scoped', async ({
  request,
}) => {
  const { password } = developmentCredentials();
  const suffix = crypto.randomUUID();
  const accountA = `e2e-a-${suffix}@example.test`;
  const accountB = `e2e-b-${suffix}@example.test`;
  provisionLocalAccount(accountA);
  provisionLocalAccount(accountB);

  const accessA = await accessToken(request, accountA, password);
  const accessB = await accessToken(request, accountB, password);
  const headersA = authorization(accessA);
  const headersB = authorization(accessB);
  for (const headers of [headersA, headersB]) {
    const bootstrap = await request.put(`${apiBaseUrl}/api/v1/account/bootstrap`, {
      headers,
      data: { timezone: 'Europe/Berlin' },
    });
    expect(bootstrap.status()).toBe(200);
  }

  const sharedListOperationId = crypto.randomUUID();
  const listAResponse = await request.post(`${apiBaseUrl}/api/v1/lists`, {
    headers: headersA,
    data: { title: 'Account A list', operation_id: sharedListOperationId },
  });
  const listBResponse = await request.post(`${apiBaseUrl}/api/v1/lists`, {
    headers: headersB,
    data: { title: 'Account B list', operation_id: sharedListOperationId },
  });
  expect(listAResponse.status()).toBe(201);
  expect(listBResponse.status()).toBe(201);
  const listA = (await listAResponse.json()) as ListResource;
  const listB = (await listBResponse.json()) as ListResource;
  expect(listB.id).not.toBe(listA.id);

  const columnAResponse = await request.get(
    `${apiBaseUrl}/api/v1/columns/${listA.default_column.id}`,
    { headers: headersA },
  );
  expect(columnAResponse.status()).toBe(200);
  const columnA = (await columnAResponse.json()) as ColumnResource;

  const sharedTaskOperationId = crypto.randomUUID();
  const taskAResponse = await request.post(`${apiBaseUrl}/api/v1/tasks`, {
    headers: headersA,
    data: {
      title: 'Account A task',
      column_id: listA.default_column.id,
      operation_id: sharedTaskOperationId,
    },
  });
  const taskBResponse = await request.post(`${apiBaseUrl}/api/v1/tasks`, {
    headers: headersB,
    data: {
      title: 'Account B task',
      column_id: listB.default_column.id,
      operation_id: sharedTaskOperationId,
    },
  });
  expect(taskAResponse.status()).toBe(201);
  expect(taskBResponse.status()).toBe(201);
  const taskA = (await taskAResponse.json()) as TaskResource;
  const taskB = (await taskBResponse.json()) as TaskResource;
  expect(taskB.id).not.toBe(taskA.id);

  const foreignReads = await Promise.all([
    request.get(`${apiBaseUrl}/api/v1/lists/${listA.id}`, { headers: headersB }),
    request.get(`${apiBaseUrl}/api/v1/columns/${columnA.id}`, { headers: headersB }),
    request.get(`${apiBaseUrl}/api/v1/tasks/${taskA.id}`, { headers: headersB }),
  ]);
  expect(foreignReads.map((response) => response.status())).toEqual([404, 404, 404]);

  const foreignMutations = await Promise.all([
    request.patch(`${apiBaseUrl}/api/v1/lists/${listA.id}`, {
      headers: headersB,
      data: { version: listA.version, title: 'Stolen list' },
    }),
    request.patch(`${apiBaseUrl}/api/v1/columns/${columnA.id}`, {
      headers: headersB,
      data: { version: columnA.version, title: 'Stolen column' },
    }),
    request.patch(`${apiBaseUrl}/api/v1/tasks/${taskA.id}`, {
      headers: headersB,
      data: { version: taskA.version, title: 'Stolen task' },
    }),
  ]);
  expect(foreignMutations.map((response) => response.status())).toEqual([404, 404, 404]);

  const foreignDestination = await request.post(`${apiBaseUrl}/api/v1/tasks`, {
    headers: headersB,
    data: {
      title: 'Rejected foreign destination',
      column_id: columnA.id,
      operation_id: crypto.randomUUID(),
    },
  });
  expect(foreignDestination.status()).toBe(404);
});
