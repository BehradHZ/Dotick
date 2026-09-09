import { expect, test } from '@playwright/test';

test('checkpoint survives reload and a new authenticated session', async ({ page }, testInfo) => {
  const email = process.env.DOTICK_E2E_EMAIL ?? 'developer@example.test';
  const password = process.env.DOTICK_DEVELOPMENT_PASSWORD;
  if (!password)
    throw new Error('Set DOTICK_DEVELOPMENT_PASSWORD and provision the developer account first.');
  const title = `Saved from ${testInfo.project.name} ${crypto.randomUUID()}`;
  const errors: string[] = [];
  page.on('pageerror', (error) => errors.push(error.message));
  await page.goto('/');
  await page.getByLabel('Email', { exact: true }).fill(email);
  await page.getByLabel('Password', { exact: true }).fill(password);
  await page.getByRole('button', { name: 'Open workbench' }).click();
  await page.getByLabel('New checkpoint', { exact: true }).fill(title);
  await page.getByRole('button', { name: 'Save checkpoint' }).click();
  await expect(page.getByText('Checkpoint saved.', { exact: true })).toBeVisible();
  await expect(page.getByText(title, { exact: true })).toBeVisible();
  await page.reload();
  await page.getByLabel('Email', { exact: true }).fill(email);
  await page.getByLabel('Password', { exact: true }).fill(password);
  await page.getByRole('button', { name: 'Open workbench' }).click();
  await expect(page.getByText(title, { exact: true })).toBeVisible();
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth);
  expect(overflow).toBe(false);
  await page.screenshot({ path: testInfo.outputPath('workbench.png'), fullPage: true });
  await page.getByRole('button', { name: 'Sign out' }).click();
  await expect(page.getByText(title, { exact: true })).toHaveCount(0);
  expect(errors).toEqual([]);
});
