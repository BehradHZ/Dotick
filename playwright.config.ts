import { defineConfig, devices } from '@playwright/test';
import { existsSync } from 'node:fs';

if (existsSync('.env')) process.loadEnvFile('.env');

const configuredWebPort = process.env.DOTICK_E2E_WEB_PORT ?? '8081';
const webPort = Number(configuredWebPort);
if (!Number.isInteger(webPort) || webPort < 1 || webPort > 65535) {
  throw new Error('DOTICK_E2E_WEB_PORT must be an integer between 1 and 65535.');
}
const webBaseUrl = `http://127.0.0.1:${webPort}`;

export default defineConfig({
  testDir: './e2e',
  fullyParallel: false,
  workers: 1,
  retries: 0,
  reporter: 'list',
  use: {
    baseURL: webBaseUrl,
    trace: 'retain-on-failure',
    channel: process.env.PLAYWRIGHT_CHANNEL,
  },
  projects: [
    { name: 'desktop', use: { ...devices['Desktop Chrome'] } },
    { name: 'mobile', use: { ...devices['iPhone 13'], defaultBrowserType: 'chromium' } },
  ],
  webServer: [
    {
      command:
        'python -m uv run uvicorn config.asgi:application --app-dir apps/api --host 127.0.0.1 --port 8000 --no-access-log',
      url: 'http://127.0.0.1:8000/ready',
      reuseExistingServer: !process.env.CI,
      timeout: 30_000,
    },
    {
      command: 'node scripts/serve-web.mjs',
      url: webBaseUrl,
      reuseExistingServer: !process.env.CI,
      timeout: 30_000,
    },
  ],
});
