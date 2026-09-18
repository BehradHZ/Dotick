import { NativeModules, Platform } from 'react-native';

export type Checkpoint = { id: string; text: string; created_at: string };
export type Credentials = { email: string; password: string };

export type User = { email: string; handle: string; display_name: string };
export type Tokens = { access: string; refresh: string; user: User };
export type DefaultColumn = { id: string; is_default: true };
export type FolderRecord = {
  id: string;
  title: string;
  position: number;
  version: number;
  is_trashed: boolean;
  trashed_at: string | null;
};
export type ListRecord = {
  id: string;
  title: string;
  folder_id: string | null;
  is_inbox: boolean;
  position: number;
  version: number;
  is_trashed: boolean;
  trashed_at: string | null;
  default_column: DefaultColumn;
};
export type ColumnRecord = {
  id: string;
  list_id: string;
  title: string;
  position: number;
  version: number;
  is_default: boolean;
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
  trashed_at?: string | null;
};

export type Bootstrap = {
  preferences: { timezone: string };
  inbox: Pick<ListRecord, 'id' | 'title' | 'is_inbox' | 'default_column'>;
};

export type FolderCreate = { title: string; operation_id: string };
export type FolderUpdate = { version: number; title?: string; position?: number };
export type ListCreate = {
  title: string;
  operation_id: string;
  folder_id?: string | null;
  position?: number;
};
export type ListUpdate = {
  version: number;
  title?: string;
  folder_id?: string | null;
  position?: number;
};
export type ColumnCreate = { title: string; operation_id: string };
export type ColumnUpdate = { version: number; title?: string; position?: number };
export type TaskCreate = {
  title: string;
  operation_id: string;
  column_id?: string | null;
};
export type TaskUpdate = {
  version: number;
  title?: string;
  status?: TaskStatus;
  column_id?: string;
};
export type FolderItemResolution = 'move_to_inbox' | 'trash';
export type ListItemResolution = 'move_to_inbox' | 'trash';
export type ColumnItemResolution = 'move_to_default' | 'trash';
export type SessionInvalidationReason = 'sign_out' | 'refresh_revoked';
export type PrivateStateCleaner = (reason: SessionInvalidationReason) => void;

type PasskeyRequestOptionsJson = {
  challenge: string;
  rpId?: string;
  timeout?: number;
  userVerification?: UserVerificationRequirement;
  allowCredentials?: Array<{
    id: string;
    type: PublicKeyCredentialType;
    transports?: AuthenticatorTransport[];
  }>;
};

type PasskeyOptions = {
  challenge_id: string;
  public_key: PasskeyRequestOptionsJson;
};

const foundationBaseUrl = process.env.EXPO_PUBLIC_API_URL ?? 'http://127.0.0.1:8000';

function defaultErrorMessage(status: number, code?: string) {
  if (code === 'version_conflict') return 'This item changed elsewhere. Refresh and try again.';
  if (code === 'idempotency_conflict') {
    return 'This operation ID was already used for a different request.';
  }
  if (code === 'reauthentication_required') return 'Your session ended. Sign in again.';
  if (status === 401) return 'Check your email and password.';
  if (status === 403) return 'This action is not currently permitted.';
  if (status === 404) return 'The requested item is no longer available.';
  if (status === 409) return 'The request conflicts with the current server state.';
  return 'Could not complete the request. Please try again.';
}

export class ApiError extends Error {
  constructor(
    public readonly status: number,
    message?: string,
    public readonly code?: string,
    public readonly details?: unknown,
  ) {
    super(message ?? defaultErrorMessage(status, code));
    this.name = 'ApiError';
  }
}

export class ReauthenticationRequiredError extends ApiError {
  constructor(details?: unknown) {
    super(401, undefined, 'reauthentication_required', details);
    this.name = 'ReauthenticationRequiredError';
  }
}

export class PasskeyUnavailableError extends Error {
  constructor(message = 'Passkey sign-in is unavailable on this browser or deployment.') {
    super(message);
    this.name = 'PasskeyUnavailableError';
  }
}

export class PasskeyCancelledError extends Error {
  constructor() {
    super('Passkey sign-in was cancelled.');
    this.name = 'PasskeyCancelledError';
  }
}

export function requiresReauthentication(error: unknown) {
  return error instanceof ReauthenticationRequiredError;
}

function trimUrl(url: string) {
  return url.trim().replace(/\/+$/, '');
}

function nativeDevelopmentHost() {
  const sourceCode = NativeModules.SourceCode as { scriptURL?: unknown } | undefined;
  if (typeof sourceCode?.scriptURL !== 'string') return undefined;
  return /^https?:\/\/([^/:]+)/.exec(sourceCode.scriptURL)?.[1];
}

export function defaultApiUrl() {
  const configured = process.env.EXPO_PUBLIC_API_URL;
  if (configured?.trim()) return trimUrl(configured);
  if (Platform.OS === 'web') return 'http://127.0.0.1:8000';
  const host = nativeDevelopmentHost();
  return host ? `http://${host}:8000` : 'http://127.0.0.1:8000';
}

export function createOperationId() {
  const cryptoObject = globalThis.crypto;
  if (typeof cryptoObject?.randomUUID === 'function') return cryptoObject.randomUUID();
  if (typeof cryptoObject?.getRandomValues !== 'function') {
    throw new Error('This runtime cannot generate operation IDs securely.');
  }
  const bytes = cryptoObject.getRandomValues(new Uint8Array(16));
  bytes[6] = ((bytes[6] ?? 0) & 0x0f) | 0x40;
  bytes[8] = ((bytes[8] ?? 0) & 0x3f) | 0x80;
  const hex = Array.from(bytes, (value) => value.toString(16).padStart(2, '0'));
  return [
    hex.slice(0, 4).join(''),
    hex.slice(4, 6).join(''),
    hex.slice(6, 8).join(''),
    hex.slice(8, 10).join(''),
    hex.slice(10).join(''),
  ].join('-');
}

type ErrorRecord = Record<string, unknown>;

function firstMessage(value: unknown): string | undefined {
  if (typeof value === 'string') return value;
  if (Array.isArray(value)) {
    for (const entry of value) {
      const message = firstMessage(entry);
      if (message) return message;
    }
    return undefined;
  }
  if (!value || typeof value !== 'object') return undefined;
  for (const entry of Object.values(value as ErrorRecord)) {
    const message = firstMessage(entry);
    if (message) return message;
  }
  return undefined;
}

function errorMetadata(body: unknown) {
  if (!body || typeof body !== 'object') return {};
  const record = body as ErrorRecord;
  const envelope = record.error;
  if (envelope && typeof envelope === 'object') {
    const error = envelope as ErrorRecord;
    const code = typeof error.code === 'string' ? error.code : undefined;
    const details = error.details;
    return { code, details, message: firstMessage(details) };
  }
  const code = typeof record.code === 'string' ? record.code : undefined;
  const detail = typeof record.detail === 'string' ? record.detail : undefined;
  return { code, details: body, message: detail ?? firstMessage(body) };
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
    const headers = new Headers(init.headers);
    if (init.body !== undefined && !headers.has('Content-Type')) {
      headers.set('Content-Type', 'application/json');
    }
    const response = await fetch(`${trimUrl(baseUrl)}${path}`, {
      ...init,
      headers,
      signal: controller.signal,
      cache: 'no-store',
    });
    const body = await readBody(response);
    if (!response.ok) {
      const { code, details, message } = errorMetadata(body);
      throw new ApiError(response.status, message, code, details);
    }
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

export function identityApi(baseUrl = defaultApiUrl()) {
  const post = <T>(path: string, body: object) =>
    rawRequest<T>(baseUrl, path, { method: 'POST', body: JSON.stringify(body) });
  return {
    register: (input: { email: string; password: string; handle: string; display_name: string }) =>
      post<{ status: 'accepted' }>('/api/v1/auth/register', input),
    verifyEmail: (email: string, code: string) =>
      post<void>('/api/v1/auth/email/verify', { email, code }),
    resendVerification: (email: string) =>
      post<{ status: 'accepted' }>('/api/v1/auth/email/resend', { email }),
    requestPasswordReset: (email: string) =>
      post<{ status: 'accepted' }>('/api/v1/auth/password/reset/request', { email }),
    confirmPasswordReset: (email: string, code: string, password: string) =>
      post<void>('/api/v1/auth/password/reset/confirm', { email, code, password }),
  };
}

function resolutionPath(path: string, resolution?: string) {
  return resolution ? `${path}?items=${encodeURIComponent(resolution)}` : path;
}

function sessionFromTokens(baseUrl: string, tokens: Tokens) {
  let access: string | null = tokens.access;
  let refresh: string | null = tokens.refresh;
  let active = true;
  let invalidationReason: SessionInvalidationReason | null = null;
  let refreshInFlight: Promise<void> | null = null;
  const privateStateCleaners = new Set<PrivateStateCleaner>();

  function invalidate(reason: SessionInvalidationReason) {
    const shouldNotify = active;
    access = null;
    refresh = null;
    active = false;
    invalidationReason = reason;
    if (shouldNotify) {
      for (const cleaner of privateStateCleaners) cleaner(reason);
    }
  }

  function reauthenticationRequired(error?: ApiError) {
    invalidate('refresh_revoked');
    return new ReauthenticationRequiredError(error?.details);
  }

  function currentAccessToken() {
    if (!active || access === null || refresh === null) {
      throw new ReauthenticationRequiredError();
    }
    return access;
  }

  async function refreshSession() {
    if (refreshInFlight) return refreshInFlight;
    const currentRefresh = refresh;
    if (!active || currentRefresh === null) throw reauthenticationRequired();

    refreshInFlight = (async () => {
      try {
        const next = await rawRequest<{ access: string; refresh: string }>(
          baseUrl,
          '/api/v1/auth/token/refresh',
          { method: 'POST', body: JSON.stringify({ refresh: currentRefresh }) },
        );
        if (!active) throw new ReauthenticationRequiredError();
        access = next.access;
        refresh = next.refresh;
      } catch (error) {
        if (error instanceof ApiError && error.status === 401) {
          throw reauthenticationRequired(error);
        }
        throw error;
      } finally {
        refreshInFlight = null;
      }
    })();

    return refreshInFlight;
  }

  async function authorizedRequest<T>(path: string, init: RequestInit = {}) {
    const headers = new Headers(init.headers);
    headers.set('Authorization', `Bearer ${currentAccessToken()}`);
    return rawRequest<T>(baseUrl, path, { ...init, headers });
  }

  async function request<T>(path: string, init: RequestInit = {}, retry = true): Promise<T> {
    try {
      return await authorizedRequest<T>(path, init);
    } catch (error) {
      if (!(error instanceof ApiError) || error.status !== 401 || !retry) throw error;
      await refreshSession();
      try {
        return await authorizedRequest<T>(path, init);
      } catch (retryError) {
        if (retryError instanceof ApiError && retryError.status === 401) {
          throw reauthenticationRequired(retryError);
        }
        throw retryError;
      }
    }
  }

  function onPrivateStateClear(cleaner: PrivateStateCleaner) {
    privateStateCleaners.add(cleaner);
    if (!active && invalidationReason !== null) cleaner(invalidationReason);
    return () => privateStateCleaners.delete(cleaner);
  }

  async function signOut() {
    let failure: unknown;
    try {
      if (active) {
        await request<void>('/api/v1/auth/logout', { method: 'POST' });
      }
    } catch (error) {
      if (!(error instanceof ReauthenticationRequiredError)) failure = error;
    } finally {
      invalidate('sign_out');
    }
    if (failure !== undefined) throw failure;
  }

  return {
    user: tokens.user,
    get isAuthenticated() {
      return active && access !== null && refresh !== null;
    },
    onPrivateStateClear,
    bootstrap: (timezone: string) =>
      request<Bootstrap>('/api/v1/account/bootstrap', {
        method: 'PUT',
        body: JSON.stringify({ timezone }),
      }),
    folders: () => request<{ results: FolderRecord[] }>('/api/v1/folders'),
    getFolder: (folderId: string) => request<FolderRecord>(`/api/v1/folders/${folderId}`),
    createFolder: (input: FolderCreate) =>
      request<FolderRecord>('/api/v1/folders', {
        method: 'POST',
        body: JSON.stringify(input),
      }),
    updateFolder: (folderId: string, change: FolderUpdate) =>
      request<FolderRecord>(`/api/v1/folders/${folderId}`, {
        method: 'PATCH',
        body: JSON.stringify(change),
      }),
    trashFolder: (folderId: string, version: number, resolution?: FolderItemResolution) =>
      request<void>(resolutionPath(`/api/v1/folders/${folderId}`, resolution), {
        method: 'DELETE',
        headers: { 'If-Match': String(version) },
      }),
    restoreFolder: (folderId: string, version: number) =>
      request<FolderRecord>(`/api/v1/folders/${folderId}/restore`, {
        method: 'POST',
        body: JSON.stringify({ version }),
      }),
    trashedFolders: () => request<{ results: FolderRecord[] }>('/api/v1/trash/folders'),
    lists: () => request<{ results: ListRecord[] }>('/api/v1/lists'),
    getList: (listId: string) => request<ListRecord>(`/api/v1/lists/${listId}`),
    createList: (input: ListCreate) =>
      request<ListRecord>('/api/v1/lists', {
        method: 'POST',
        body: JSON.stringify(input),
      }),
    updateList: (listId: string, change: ListUpdate) =>
      request<ListRecord>(`/api/v1/lists/${listId}`, {
        method: 'PATCH',
        body: JSON.stringify(change),
      }),
    trashList: (listId: string, version: number, resolution?: ListItemResolution) =>
      request<void>(resolutionPath(`/api/v1/lists/${listId}`, resolution), {
        method: 'DELETE',
        headers: { 'If-Match': String(version) },
      }),
    restoreList: (listId: string, version: number) =>
      request<ListRecord>(`/api/v1/lists/${listId}/restore`, {
        method: 'POST',
        body: JSON.stringify({ version }),
      }),
    trashedLists: () => request<{ results: ListRecord[] }>('/api/v1/trash/lists'),
    columns: (listId: string) =>
      request<{ results: ColumnRecord[] }>(`/api/v1/lists/${listId}/columns`),
    getColumn: (columnId: string) => request<ColumnRecord>(`/api/v1/columns/${columnId}`),
    createColumn: (listId: string, input: ColumnCreate) =>
      request<ColumnRecord>(`/api/v1/lists/${listId}/columns`, {
        method: 'POST',
        body: JSON.stringify(input),
      }),
    updateColumn: (columnId: string, change: ColumnUpdate) =>
      request<ColumnRecord>(`/api/v1/columns/${columnId}`, {
        method: 'PATCH',
        body: JSON.stringify(change),
      }),
    deleteColumn: (columnId: string, version: number, resolution?: ColumnItemResolution) =>
      request<void>(resolutionPath(`/api/v1/columns/${columnId}`, resolution), {
        method: 'DELETE',
        headers: { 'If-Match': String(version) },
      }),
    tasks: () => request<{ results: Task[] }>('/api/v1/tasks'),
    getTask: (taskId: string) => request<Task>(`/api/v1/tasks/${taskId}`),
    createTask: (input: TaskCreate) =>
      request<Task>('/api/v1/tasks', {
        method: 'POST',
        body: JSON.stringify(input),
      }),
    updateTask: (taskId: string, change: TaskUpdate) =>
      request<Task>(`/api/v1/tasks/${taskId}`, {
        method: 'PATCH',
        body: JSON.stringify(change),
      }),
    trashTask: (taskId: string, version: number) =>
      request<void>(`/api/v1/tasks/${taskId}`, {
        method: 'DELETE',
        headers: { 'If-Match': String(version) },
      }),
    trashedTasks: () => request<{ results: Task[] }>('/api/v1/trash/tasks'),
    trash: () => request<{ results: Task[] }>('/api/v1/trash/tasks'),
    restoreTask: (taskId: string, version: number) =>
      request<Task>(`/api/v1/tasks/${taskId}/restore`, {
        method: 'POST',
        body: JSON.stringify({ version }),
      }),
    signOut,
    logout: signOut,
  };
}

export async function signIn(baseUrl: string, email: string, password: string) {
  const tokens = await rawRequest<Tokens>(baseUrl, '/api/v1/auth/token', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  });
  return sessionFromTokens(baseUrl, tokens);
}

export async function signInWithGoogleCredential(baseUrl: string, credential: string) {
  const tokens = await rawRequest<Tokens>(baseUrl, '/api/v1/auth/google', {
    method: 'POST',
    body: JSON.stringify({ credential }),
  });
  return sessionFromTokens(baseUrl, tokens);
}

function decodeBase64Url(value: string) {
  const normalized = value.replace(/-/g, '+').replace(/_/g, '/');
  const binary = atob(normalized.padEnd(Math.ceil(normalized.length / 4) * 4, '='));
  return Uint8Array.from(binary, (character) => character.charCodeAt(0));
}

function encodeBase64Url(value: ArrayBuffer) {
  const binary = String.fromCharCode(...new Uint8Array(value));
  return btoa(binary).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

export function passkeyAuthenticationAvailable() {
  return (
    Platform.OS === 'web' &&
    typeof navigator !== 'undefined' &&
    typeof navigator.credentials?.get === 'function' &&
    typeof globalThis.PublicKeyCredential !== 'undefined'
  );
}

function passkeyRequestOptions(options: PasskeyRequestOptionsJson): PublicKeyCredentialRequestOptions {
  return {
    challenge: decodeBase64Url(options.challenge),
    rpId: options.rpId,
    timeout: options.timeout,
    userVerification: options.userVerification,
    allowCredentials: options.allowCredentials?.map((credential) => ({
      id: decodeBase64Url(credential.id),
      type: credential.type,
      transports: credential.transports,
    })),
  };
}

function isCancelledCredentialError(error: unknown) {
  if (!(error instanceof Error)) return false;
  return error.name === 'AbortError' || error.name === 'NotAllowedError';
}

export async function signInWithPasskey(baseUrl: string) {
  if (!passkeyAuthenticationAvailable()) throw new PasskeyUnavailableError();

  let options: PasskeyOptions;
  try {
    options = await rawRequest<PasskeyOptions>(
      baseUrl,
      '/api/v1/auth/passkeys/authentication/options',
      { method: 'POST', body: '{}' },
    );
  } catch (error) {
    if (error instanceof ApiError && error.status === 503) {
      throw new PasskeyUnavailableError();
    }
    throw error;
  }

  let credential: Credential | null;
  try {
    credential = await navigator.credentials.get({
      publicKey: passkeyRequestOptions(options.public_key),
    });
  } catch (error) {
    if (isCancelledCredentialError(error)) throw new PasskeyCancelledError();
    throw new Error('Passkey sign-in failed.', { cause: error });
  }

  if (!(credential instanceof PublicKeyCredential)) {
    throw new Error('Passkey sign-in did not return a credential.');
  }

  const response = credential.response;
  if (!(response instanceof AuthenticatorAssertionResponse)) {
    throw new Error('Passkey sign-in returned an invalid assertion.');
  }

  const tokens = await rawRequest<Tokens>(baseUrl, '/api/v1/auth/passkeys/authentication/verify', {
    method: 'POST',
    body: JSON.stringify({
      challenge_id: options.challenge_id,
      credential: {
        id: credential.id,
        rawId: encodeBase64Url(credential.rawId),
        type: credential.type,
        authenticatorAttachment: credential.authenticatorAttachment,
        clientExtensionResults: credential.getClientExtensionResults(),
        response: {
          clientDataJSON: encodeBase64Url(response.clientDataJSON),
          authenticatorData: encodeBase64Url(response.authenticatorData),
          signature: encodeBase64Url(response.signature),
          userHandle: response.userHandle ? encodeBase64Url(response.userHandle) : null,
        },
      },
    }),
  });
  return sessionFromTokens(baseUrl, tokens);
}

export type ApiSession = Awaited<ReturnType<typeof signIn>>;

export function foundationApi(credentials: Credentials) {
  const bytes = new TextEncoder().encode(`${credentials.email}:${credentials.password}`);
  const encoded = btoa(Array.from(bytes, (byte) => String.fromCharCode(byte)).join(''));
  const authorization = `Basic ${encoded}`;

  async function request<T>(path: string, text?: string): Promise<T> {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 8000);
    try {
      const response = await fetch(`${foundationBaseUrl}/api/v1/foundation/checkpoints${path}`, {
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
