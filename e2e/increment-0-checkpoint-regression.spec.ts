import { expect, test } from '@playwright/test';

test.describe('Increment 0 Checkpoint regression', () => {
  test('persists an owner-scoped Checkpoint through the foundation API', async ({ request }) => {
    const email = process.env.DOTICK_E2E_EMAIL ?? 'developer@example.test';
    const password = process.env.DOTICK_DEVELOPMENT_PASSWORD;
    if (!password) {
      throw new Error('Set DOTICK_DEVELOPMENT_PASSWORD and provision the developer account first.');
    }

    const authorization = `Basic ${Buffer.from(`${email}:${password}`).toString('base64')}`;
    const text = `Increment 0 regression ${crypto.randomUUID()}`;
    const create = await request.post('http://127.0.0.1:8000/api/v1/foundation/checkpoints', {
      headers: { Authorization: authorization },
      data: { text },
    });
    expect(create.status()).toBe(201);
    const checkpoint = (await create.json()) as { id: string; text: string };
    expect(checkpoint.text).toBe(text);

    const retrieve = await request.get(
      `http://127.0.0.1:8000/api/v1/foundation/checkpoints/${checkpoint.id}`,
      { headers: { Authorization: authorization } },
    );
    expect(retrieve.status()).toBe(200);
    await expect(retrieve.json()).resolves.toMatchObject({ id: checkpoint.id, text });

    const list = await request.get('http://127.0.0.1:8000/api/v1/foundation/checkpoints', {
      headers: { Authorization: authorization },
    });
    expect(list.status()).toBe(200);
    const payload = (await list.json()) as { results: Array<{ id: string; text: string }> };
    expect(payload.results).toContainEqual(expect.objectContaining({ id: checkpoint.id, text }));
  });
});
