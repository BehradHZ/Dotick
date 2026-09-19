import { expect, test } from '@playwright/test';

test('Increment 1 workspace persists a List and Task through task recovery', async ({
  page,
}, testInfo) => {
  const email = process.env.DOTICK_E2E_EMAIL ?? 'developer@example.test';
  const password = process.env.DOTICK_DEVELOPMENT_PASSWORD;
  if (!password) {
    throw new Error('Set DOTICK_DEVELOPMENT_PASSWORD and provision the developer account first.');
  }

  const suffix = crypto.randomUUID();
  const listTitle = `E2E list ${suffix}`;
  const taskTitle = `E2E task ${suffix}`;
  const browserErrors: string[] = [];
  page.on('pageerror', (error) => browserErrors.push(error.message));
  page.on('console', (message) => {
    if (
      (message.type() === 'error' || message.type() === 'warning') &&
      !message.text().startsWith('Failed to load resource:')
    ) {
      browserErrors.push(`${message.type()}: ${message.text()}`);
    }
  });
  page.on('response', (response) => {
    if (response.status() >= 400 && response.url().includes('/api/')) {
      browserErrors.push(`${response.status()} ${response.url()}`);
    }
  });

  await page.goto('/');
  await page.getByLabel('Email', { exact: true }).fill(email);
  await page.getByLabel('Password', { exact: true }).fill(password);
  await page.getByRole('button', { name: 'Sign in', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Inbox' })).toBeVisible();

  await page.getByLabel('New list', { exact: true }).fill(listTitle);
  await page.getByRole('button', { name: 'Add list' }).click();
  await expect(page.getByRole('heading', { name: listTitle })).toBeVisible();
  await page.getByLabel('New task', { exact: true }).fill(taskTitle);
  await page.getByRole('button', { name: 'Add task' }).click();
  const task = page.getByText(taskTitle, { exact: true });
  await task.scrollIntoViewIfNeeded();
  await expect(task).toBeVisible();
  await page.getByRole('button', { name: `Mark ${taskTitle} Done` }).click();
  await expect(page.getByRole('button', { name: `Mark ${taskTitle} Done` })).toBeDisabled();

  await page.getByRole('button', { name: `Trash ${taskTitle}` }).click();
  await expect(page.getByText(taskTitle, { exact: true })).toHaveCount(0);
  await page.getByRole('button', { name: 'Open Trash' }).click();
  await page.getByText(taskTitle, { exact: true }).scrollIntoViewIfNeeded();
  await expect(page.getByText(taskTitle, { exact: true })).toBeVisible();
  await page.getByRole('button', { name: `Restore ${taskTitle}` }).click();
  await page.getByRole('button', { name: `Open ${listTitle}` }).click();
  await page.getByText(taskTitle, { exact: true }).scrollIntoViewIfNeeded();
  await expect(page.getByText(taskTitle, { exact: true })).toBeVisible();

  await page.reload();
  await page.getByLabel('Email', { exact: true }).fill(email);
  await page.getByLabel('Password', { exact: true }).fill(password);
  await page.getByRole('button', { name: 'Sign in', exact: true }).click();
  await page.getByRole('button', { name: `Open ${listTitle}` }).click();
  await page.getByText(taskTitle, { exact: true }).scrollIntoViewIfNeeded();
  await expect(page.getByText(taskTitle, { exact: true })).toBeVisible();
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth);
  expect(overflow).toBe(false);
  await page.screenshot({ path: testInfo.outputPath('workspace.png'), fullPage: true });
  await page.getByRole('button', { name: 'Sign out' }).click();
  await expect(page.getByRole('heading', { name: 'Sign in' })).toBeVisible();
  expect(browserErrors).toEqual([]);
});
