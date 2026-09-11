export type Checkpoint = { id: string; text: string; created_at: string };
export type Credentials = { email: string; password: string };

const baseUrl = process.env.EXPO_PUBLIC_API_URL ?? 'http://127.0.0.1:8000';

export class ApiError extends Error {
  constructor(public readonly status: number) {
    super(
      status === 401
        ? 'Check your email and password.'
        : 'Could not complete the request. Please try again.',
    );
  }
}

export function foundationApi(credentials: Credentials) {
  // Developer-only HTTP Basic credentials stay in memory; I1 replaces this transport.
  const bytes = new TextEncoder().encode(`${credentials.email}:${credentials.password}`);
  const authorization = `Basic ${btoa(Array.from(bytes, (byte) => String.fromCharCode(byte)).join(''))}`;

  async function request<T>(path: string, text?: string): Promise<T> {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 8000);
    try {
      const response = await fetch(`${baseUrl}/api/v1/foundation/checkpoints${path}`, {
        method: text === undefined ? 'GET' : 'POST',
        headers: {
          Authorization: authorization,
          ...(text === undefined ? {} : { 'Content-Type': 'application/json' }),
        },
        body: text === undefined ? undefined : JSON.stringify({ text }),
        signal: controller.signal,
        cache: 'no-store',
      });
      if (!response.ok) throw new ApiError(response.status);
      return (await response.json()) as T;
    } finally {
      clearTimeout(timeout);
    }
  }

  return {
    list: () => request<{ results: Checkpoint[] }>(''),
    create: (text: string) => request<Checkpoint>('', text),
  };
}
