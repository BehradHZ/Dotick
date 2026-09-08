import { expect, test } from '@playwright/test';

test('task survives reload and can be completed and trashed', async ({ page }, testInfo) => {
  const email = process.env.DOTICK_E2E_EMAIL ?? 'developer@example.test';
  const password = process.env.DOTICK_DEVELOPMENT_PASSWORD;
  if (!password) {
    throw new Error('Set DOTICK_DEVELOPMENT_PASSWORD and provision the developer account first.');
  }
  const title = `Task from ${testInfo.project.name} ${crypto.randomUUID()}`;
  const errors: string[] = [];
  page.on('pageerror', (error) => errors.push(error.message));

  async function signIn() {
    await page.getByLabel('Email', { exact: true }).fill(email);
    await page.getByLabel('Password', { exact: true }).fill(password);
    await page.getByRole('button', { name: 'Sign in', exact: true }).click();
    await expect(page.getByRole('heading', { name: 'Inbox' })).toBeVisible();
  }

  await page.goto('/');
  await signIn();
  await page.getByLabel('New task', { exact: true }).fill(title);
  await page.getByRole('button', { name: 'Add task', exact: true }).click();
  await expect(page.getByText('Task created.', { exact: true })).toBeVisible();
  await page.getByRole('button', { name: `Edit ${title}` }).scrollIntoViewIfNeeded();
  await expect(page.getByRole('button', { name: `Edit ${title}` })).toBeVisible();

  await page.reload();
  await signIn();
  await page.getByRole('button', { name: `Edit ${title}` }).scrollIntoViewIfNeeded();
  await expect(page.getByRole('button', { name: `Edit ${title}` })).toBeVisible();
  await page.getByRole('button', { name: `Mark ${title} done` }).click();
  await expect(page.getByRole('button', { name: `Mark ${title} to do` })).toBeVisible();
  await page.getByRole('button', { name: `Trash ${title}` }).click();
  await expect(page.getByRole('button', { name: `Edit ${title}` })).toHaveCount(0);

  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth);
  expect(overflow).toBe(false);
  await page.screenshot({ path: testInfo.outputPath('increment-1.png'), fullPage: true });
  expect(errors).toEqual([]);
});
