import Constants from 'expo-constants';
import * as Crypto from 'expo-crypto';
import { Platform } from 'react-native';

export type User = { email: string; handle: string; display_name: string };
export type Tokens = { access: string; refresh: string; user: User };
export type ListRecord = {
  id: string;
  title: string;
  folder_id: string | null;
  is_inbox: boolean;
  position: number;
  is_trashed: boolean;
  trashed_at: string | null;
  default_column: { id: string; is_default: boolean };
};
export type TaskStatus = 'todo' | 'done' | 'wont_do';
export type Task = {
  id: string;
  title: string;
  status: TaskStatus;
  version: number;
  column_id: string;
  owner_user_id: string;
  created_by_user_id: string;
  source: {
    platform: string;
    external_account_id: string | null;
    external_id: string | null;
  };
  created_at: string;
  updated_at: string;
  is_trashed?: boolean;
  trashed_at?: string;
};

type Bootstrap = {
  preferences: { timezone: string };
  inbox: Pick<ListRecord, 'id' | 'title' | 'is_inbox' | 'default_column'>;
};

type ErrorBody = { detail?: string; code?: string; [key: string]: unknown };

export class ApiError extends Error {
  constructor(
    public readonly status: number,
    message?: string,
  ) {
    super(
      message ??
        (status === 401
          ? 'Check your email and password.'
          : status === 409
            ? 'This task changed elsewhere. Refresh and try again.'
            : 'Could not complete the request. Please try again.'),
    );
  }
}

function trimUrl(url: string) {
  return url.trim().replace(/\/+$/, '');
}

export function defaultApiUrl() {
  const configured = process.env.EXPO_PUBLIC_API_URL;
  if (configured) return trimUrl(configured);
  if (Platform.OS === 'web') return 'http://127.0.0.1:8000';
  const host = Constants.expoConfig?.hostUri?.split(':')[0];
  return host ? `http://${host}:8000` : 'http://127.0.0.1:8000';
}

function bodyMessage(body: unknown) {
  if (!body || typeof body !== 'object') return undefined;
  const error = body as ErrorBody;
  if (typeof error.detail === 'string') return error.detail;
  for (const value of Object.values(error)) {
    if (typeof value === 'string') return value;
    if (Array.isArray(value) && typeof value[0] === 'string') return value[0];
  }
  return undefined;
}

async function readBody(response: Response) {
  if (response.status === 204) return undefined;
  const text = await response.text();
  if (!text) return undefined;
  try {
    return JSON.parse(text) as unknown;
  } catch {
    return undefined;
  }
}

async function rawRequest<T>(baseUrl: string, path: string, init: RequestInit = {}) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 8000);
  try {
    const response = await fetch(`${trimUrl(baseUrl)}${path}`, {
      ...init,
      headers: {
        ...(init.body === undefined ? {} : { 'Content-Type': 'application/json' }),
        ...init.headers,
      },
      signal: controller.signal,
      cache: 'no-store',
    });
    const body = await readBody(response);
    if (!response.ok) throw new ApiError(response.status, bodyMessage(body));
    return body as T;
  } catch (error) {
    if (error instanceof ApiError) throw error;
    throw new Error('Connection interrupted. Your changes are still here. Try again.', {
      cause: error,
    });
  } finally {
    clearTimeout(timeout);
  }
}

export async function signIn(baseUrl: string, email: string, password: string) {
  const tokens = await rawRequest<Tokens>(baseUrl, '/api/v1/auth/token', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  });
  let access = tokens.access;
  let refresh = tokens.refresh;

  async function request<T>(path: string, init: RequestInit = {}, retry = true): Promise<T> {
    try {
      return await rawRequest<T>(baseUrl, path, {
        ...init,
        headers: { ...init.headers, Authorization: `Bearer ${access}` },
      });
    } catch (error) {
      if (!(error instanceof ApiError) || error.status !== 401 || !retry) throw error;
      const next = await rawRequest<{ access: string; refresh: string }>(
        baseUrl,
        '/api/v1/auth/token/refresh',
        { method: 'POST', body: JSON.stringify({ refresh }) },
      );
      access = next.access;
      refresh = next.refresh;
      return request<T>(path, init, false);
    }
  }

  return {
    user: tokens.user,
    bootstrap: (timezone: string) =>
      request<Bootstrap>('/api/v1/account/bootstrap', {
        method: 'PUT',
        body: JSON.stringify({ timezone }),
      }),
    lists: () => request<{ results: ListRecord[] }>('/api/v1/lists'),
    createList: (title: string) =>
      request<ListRecord>('/api/v1/lists', {
        method: 'POST',
        body: JSON.stringify({ title }),
      }),
    tasks: () => request<{ results: Task[] }>('/api/v1/tasks'),
    createTask: (title: string, columnId: string) =>
      request<Task>('/api/v1/tasks', {
        method: 'POST',
        body: JSON.stringify({
          title,
          column_id: columnId,
          operation_id: Crypto.randomUUID(),
        }),
      }),
    updateTask: (
      taskId: string,
      change: { version: number; title?: string; status?: TaskStatus; column_id?: string },
    ) =>
      request<Task>(`/api/v1/tasks/${taskId}`, {
        method: 'PATCH',
        body: JSON.stringify(change),
      }),
    trashTask: (taskId: string, version: number) =>
      request<void>(`/api/v1/tasks/${taskId}`, {
        method: 'DELETE',
        headers: { 'If-Match': String(version) },
      }),
    trash: () => request<{ results: Task[] }>('/api/v1/trash/tasks'),
    restoreTask: (taskId: string, version: number) =>
      request<Task>(`/api/v1/tasks/${taskId}/restore`, {
        method: 'POST',
        body: JSON.stringify({ version }),
      }),
    logout: () => request<void>('/api/v1/auth/logout', { method: 'POST' }, false),
  };
}

export type ApiSession = Awaited<ReturnType<typeof signIn>>;
