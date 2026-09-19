import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, expect, test, vi } from 'vitest';

import AuthScreen from './AuthScreen';

function json(data: unknown, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

const tokens = {
  access: 'access-token',
  refresh: 'refresh-token',
  user: { email: 'person@example.test', handle: 'person', display_name: 'Person' },
};

function installPasskeyBrowser(get: () => Promise<Credential | null>) {
  class FakeAssertionResponse {
    clientDataJSON = Uint8Array.from([1]).buffer;
    authenticatorData = Uint8Array.from([2]).buffer;
    signature = Uint8Array.from([3]).buffer;
    userHandle = Uint8Array.from([4]).buffer;
  }

  class FakePublicKeyCredential {
    id = 'credential-id';
    rawId = Uint8Array.from([5]).buffer;
    type = 'public-key';
    authenticatorAttachment = null;
    response = new FakeAssertionResponse();
    getClientExtensionResults() {
      return {};
    }
  }

  vi.stubGlobal('AuthenticatorAssertionResponse', FakeAssertionResponse);
  vi.stubGlobal('PublicKeyCredential', FakePublicKeyCredential);
  Object.defineProperty(navigator, 'credentials', {
    configurable: true,
    value: { get: vi.fn(get) },
  });

  return { FakePublicKeyCredential };
}

afterEach(() => {
  vi.unstubAllEnvs();
  delete window.google;
  Object.defineProperty(navigator, 'credentials', {
    configurable: true,
    value: undefined,
  });
});

test('hides Google sign-in when the public client ID is unconfigured and keeps password fallback', () => {
  vi.stubEnv('EXPO_PUBLIC_GOOGLE_CLIENT_ID', '');
  render(<AuthScreen onAuthenticated={vi.fn()} />);

  expect(screen.queryByRole('button', { name: 'Continue with Google' })).not.toBeInTheDocument();
  expect(screen.getByRole('button', { name: 'Sign in' })).toBeVisible();
  expect(screen.getByLabelText('Password')).toBeVisible();
});

test('uses the public Google client ID and hands the provider credential to the backend', async () => {
  vi.stubEnv('EXPO_PUBLIC_GOOGLE_CLIENT_ID', 'google-client-id.apps.exampleusercontent.com');
  const onAuthenticated = vi.fn();
  let googleCallback: ((response: { credential: string }) => void) | undefined;
  window.google = {
    accounts: {
      id: {
        initialize: vi.fn((input) => {
          expect(input.client_id).toBe('google-client-id.apps.exampleusercontent.com');
          googleCallback = input.callback;
        }),
        prompt: vi.fn(() => undefined),
      },
    },
  };
  const fetch = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    if (url.endsWith('/api/v1/auth/google')) {
      expect(JSON.parse(String(init?.body))).toEqual({ credential: 'google-id-credential' });
      return json(tokens);
    }
    throw new Error(`Unhandled request: ${url}`);
  });
  vi.stubGlobal('fetch', fetch);
  render(<AuthScreen onAuthenticated={onAuthenticated} />);

  fireEvent.click(screen.getByRole('button', { name: 'Continue with Google' }));
  await waitFor(() => expect(googleCallback).toBeDefined());
  googleCallback?.({ credential: 'google-id-credential' });

  await waitFor(() => expect(onAuthenticated).toHaveBeenCalledTimes(1));
});

test('retries Google script loading after a failed injection without hanging', async () => {
  vi.stubEnv('EXPO_PUBLIC_GOOGLE_CLIENT_ID', 'google-client-id.apps.exampleusercontent.com');
  const onAuthenticated = vi.fn();
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(json(tokens)));
  render(<AuthScreen onAuthenticated={onAuthenticated} />);

  fireEvent.click(screen.getByRole('button', { name: 'Continue with Google' }));
  const failedScript = await waitFor(() => {
    const script = document.querySelector<HTMLScriptElement>('script[data-dotick-google]');
    expect(script).not.toBeNull();
    return script as HTMLScriptElement;
  });
  failedScript.dispatchEvent(new Event('error'));
  expect(await screen.findByRole('alert')).toHaveTextContent('Google sign-in could not load.');

  let callback: ((response: { credential: string }) => void) | undefined;
  window.google = {
    accounts: {
      id: {
        initialize: vi.fn((input) => {
          callback = input.callback;
        }),
        prompt: vi.fn(() => undefined),
      },
    },
  };
  fireEvent.click(screen.getByRole('button', { name: 'Continue with Google' }));
  await waitFor(() => expect(callback).toBeDefined());
  callback?.({ credential: 'retry-credential' });
  await waitFor(() => expect(onAuthenticated).toHaveBeenCalledTimes(1));
});

test('hides Passkey sign-in when WebAuthn is unsupported and keeps password fallback', () => {
  render(<AuthScreen onAuthenticated={vi.fn()} />);

  expect(screen.queryByRole('button', { name: 'Sign in with a passkey' })).not.toBeInTheDocument();
  expect(screen.getByRole('button', { name: 'Sign in' })).toBeVisible();
});

test('completes a browser Passkey ceremony and sends its assertion to the backend', async () => {
  const credentialFactory: { current?: () => Credential } = {};
  const installed = installPasskeyBrowser(async () => credentialFactory.current?.() ?? null);
  credentialFactory.current = () =>
    new installed.FakePublicKeyCredential() as unknown as Credential;
  const onAuthenticated = vi.fn();
  const fetch = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    if (url.endsWith('/api/v1/auth/passkeys/authentication/options')) {
      return json({
        challenge_id: 'challenge-id',
        public_key: {
          challenge: 'AQ',
          rpId: 'example.test',
          userVerification: 'required',
          allowCredentials: [{ id: 'Ag', type: 'public-key' }],
        },
      });
    }
    if (url.endsWith('/api/v1/auth/passkeys/authentication/verify')) {
      const body = JSON.parse(String(init?.body));
      expect(body.challenge_id).toBe('challenge-id');
      expect(body.credential.id).toBe('credential-id');
      expect(body.credential.response).toMatchObject({
        clientDataJSON: 'AQ',
        authenticatorData: 'Ag',
        signature: 'Aw',
        userHandle: 'BA',
      });
      return json(tokens);
    }
    throw new Error(`Unhandled request: ${url}`);
  });
  vi.stubGlobal('fetch', fetch);
  render(<AuthScreen onAuthenticated={onAuthenticated} />);

  fireEvent.click(screen.getByRole('button', { name: 'Sign in with a passkey' }));

  await waitFor(() => expect(onAuthenticated).toHaveBeenCalledTimes(1));
});

test('reports a cancelled Passkey ceremony without removing password fallback', async () => {
  const crossRealmCancellation = Object.assign(Object.create(null) as object, {
    name: 'NotAllowedError',
  });
  installPasskeyBrowser(async () => {
    throw crossRealmCancellation;
  });
  vi.stubGlobal(
    'fetch',
    vi
      .fn()
      .mockResolvedValue(json({ challenge_id: 'challenge-id', public_key: { challenge: 'AQ' } })),
  );
  render(<AuthScreen onAuthenticated={vi.fn()} />);

  fireEvent.click(screen.getByRole('button', { name: 'Sign in with a passkey' }));

  expect(await screen.findByRole('alert')).toHaveTextContent('Passkey sign-in was cancelled.');
  expect(screen.getByRole('button', { name: 'Sign in' })).toBeVisible();
});

test('reports unavailable Passkey configuration without removing password fallback', async () => {
  installPasskeyBrowser(async () => null);
  vi.stubGlobal(
    'fetch',
    vi
      .fn()
      .mockResolvedValue(
        json({ error: { code: 'provider_unavailable', details: 'Passkeys not configured.' } }, 503),
      ),
  );
  render(<AuthScreen onAuthenticated={vi.fn()} />);

  fireEvent.click(screen.getByRole('button', { name: 'Sign in with a passkey' }));

  expect(await screen.findByRole('alert')).toHaveTextContent(
    'Passkey sign-in is unavailable on this browser or deployment.',
  );
  expect(screen.getByRole('button', { name: 'Sign in' })).toBeVisible();
});
