import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { expect, test, vi } from 'vitest';

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

function openRegistration() {
  fireEvent.click(screen.getByRole('button', { name: 'Create account' }));
}

function fillRegistration() {
  fireEvent.change(screen.getByLabelText('Display name'), { target: { value: 'New Person' } });
  fireEvent.change(screen.getByLabelText('Handle'), { target: { value: 'new_person' } });
  fireEvent.change(screen.getByLabelText('Registration email'), {
    target: { value: 'new@example.test' },
  });
  fireEvent.change(screen.getByLabelText('New password'), {
    target: { value: 'Safe-password-for-tests-8!' },
  });
}

test('registers with the complete identity request and verifies a six-digit code', async () => {
  const fetch = vi.fn(async (input: RequestInfo | URL, _init?: RequestInit) => {
    void _init;
    const url = String(input);
    if (url.endsWith('/api/v1/auth/register')) return json({ status: 'accepted' }, 202);
    if (url.endsWith('/api/v1/auth/email/verify')) return new Response(null, { status: 204 });
    throw new Error(`Unhandled request: ${url}`);
  });
  vi.stubGlobal('fetch', fetch);
  render(<AuthScreen onAuthenticated={vi.fn()} />);

  openRegistration();
  fillRegistration();
  fireEvent.click(screen.getByRole('button', { name: 'Create account' }));

  expect(await screen.findByRole('heading', { name: 'Check your inbox' })).toBeVisible();
  expect(
    screen.getByText(
      'If registration can proceed, check your email for a 6-digit verification code.',
    ),
  ).toBeVisible();
  fireEvent.change(screen.getByLabelText('Verification code'), {
    target: { value: '12a34 56' },
  });
  expect(screen.getByLabelText('Verification code')).toHaveValue('123456');
  fireEvent.click(screen.getByRole('button', { name: 'Verify email' }));

  expect(await screen.findByText('Email verified. Sign in to continue.')).toBeVisible();
  expect(screen.getByRole('heading', { name: 'Sign in' })).toBeVisible();
  await waitFor(() => {
    const register = fetch.mock.calls.find(([url]) => String(url).endsWith('/auth/register'));
    expect(JSON.parse(String(register?.[1]?.body))).toEqual({
      email: 'new@example.test',
      password: 'Safe-password-for-tests-8!',
      handle: 'new_person',
      display_name: 'New Person',
    });
    const verify = fetch.mock.calls.find(([url]) => String(url).endsWith('/auth/email/verify'));
    expect(JSON.parse(String(verify?.[1]?.body))).toEqual({
      email: 'new@example.test',
      code: '123456',
    });
  });
});

test('resends verification with enumeration-safe copy', async () => {
  const fetch = vi.fn(async (input: RequestInfo | URL, _init?: RequestInit) => {
    void _init;
    const url = String(input);
    if (url.endsWith('/api/v1/auth/register')) return json({ status: 'accepted' }, 202);
    if (url.endsWith('/api/v1/auth/email/resend')) return json({ status: 'accepted' }, 202);
    throw new Error(`Unhandled request: ${url}`);
  });
  vi.stubGlobal('fetch', fetch);
  render(<AuthScreen onAuthenticated={vi.fn()} />);

  openRegistration();
  fillRegistration();
  fireEvent.click(screen.getByRole('button', { name: 'Create account' }));
  await screen.findByRole('heading', { name: 'Check your inbox' });
  fireEvent.click(screen.getByRole('button', { name: 'Resend code' }));

  expect(await screen.findByText('If the account is eligible, a new code was sent.')).toBeVisible();
  expect(screen.queryByText(/account exists/i)).not.toBeInTheDocument();
});

test('requests and confirms a password reset without disclosing account existence', async () => {
  const fetch = vi.fn(async (input: RequestInfo | URL, _init?: RequestInit) => {
    void _init;
    const url = String(input);
    if (url.endsWith('/api/v1/auth/password/reset/request')) {
      return json({ status: 'accepted' }, 202);
    }
    if (url.endsWith('/api/v1/auth/password/reset/confirm')) {
      return new Response(null, { status: 204 });
    }
    throw new Error(`Unhandled request: ${url}`);
  });
  vi.stubGlobal('fetch', fetch);
  render(<AuthScreen onAuthenticated={vi.fn()} />);

  fireEvent.click(screen.getByRole('button', { name: 'Forgot password?' }));
  fireEvent.change(screen.getByLabelText('Recovery email'), {
    target: { value: 'person@example.test' },
  });
  fireEvent.click(screen.getByRole('button', { name: 'Send reset code' }));

  expect(await screen.findByRole('heading', { name: 'Choose a new password' })).toBeVisible();
  expect(screen.getByText('If the account is eligible, a reset code was sent.')).toBeVisible();
  fireEvent.change(screen.getByLabelText('Reset code'), { target: { value: '654321' } });
  fireEvent.change(screen.getByLabelText('Replacement password'), {
    target: { value: 'Replacement-password-9!' },
  });
  fireEvent.click(screen.getByRole('button', { name: 'Update password' }));

  expect(
    await screen.findByText('Password updated. Sign in with your new password.'),
  ).toBeVisible();
  expect(screen.getByRole('heading', { name: 'Sign in' })).toBeVisible();
});

test('signs in with email and password and hands the secure session to the client', async () => {
  const onAuthenticated = vi.fn();
  const fetch = vi.fn(async (input: RequestInfo | URL, _init?: RequestInit) => {
    void _init;
    const url = String(input);
    if (url.endsWith('/api/v1/auth/token')) return json(tokens);
    throw new Error(`Unhandled request: ${url}`);
  });
  vi.stubGlobal('fetch', fetch);
  render(<AuthScreen onAuthenticated={onAuthenticated} />);

  fireEvent.change(screen.getByLabelText('Email'), {
    target: { value: 'person@example.test' },
  });
  fireEvent.change(screen.getByLabelText('Password'), {
    target: { value: 'Safe-password-for-tests-8!' },
  });
  fireEvent.click(screen.getByRole('button', { name: 'Sign in' }));

  await waitFor(() => expect(onAuthenticated).toHaveBeenCalledTimes(1));
  expect(screen.getByLabelText('Password')).toHaveValue('');
  const tokenCall = fetch.mock.calls.find(([url]) => String(url).endsWith('/auth/token'));
  expect(JSON.parse(String(tokenCall?.[1]?.body))).toEqual({
    email: 'person@example.test',
    password: 'Safe-password-for-tests-8!',
  });
});

test('keeps authentication failures generic even when a response contains account-specific text', async () => {
  vi.stubGlobal(
    'fetch',
    vi.fn().mockResolvedValue(
      json(
        {
          error: {
            code: 'not_authenticated',
            details: 'No account exists for person@example.test.',
          },
        },
        401,
      ),
    ),
  );
  render(<AuthScreen onAuthenticated={vi.fn()} />);

  fireEvent.change(screen.getByLabelText('Email'), {
    target: { value: 'person@example.test' },
  });
  fireEvent.change(screen.getByLabelText('Password'), {
    target: { value: 'Safe-password-for-tests-8!' },
  });
  fireEvent.click(screen.getByRole('button', { name: 'Sign in' }));

  const alert = await screen.findByRole('alert');
  expect(alert).toHaveTextContent('Check your email and password.');
  expect(alert).not.toHaveTextContent('No account exists');
});

test('renders safe validation text instead of the raw backend error envelope', async () => {
  vi.stubGlobal(
    'fetch',
    vi.fn().mockResolvedValue(
      json(
        {
          error: {
            code: 'validation_error',
            details: { handle: ['Handle is unavailable.'] },
          },
        },
        400,
      ),
    ),
  );
  render(<AuthScreen onAuthenticated={vi.fn()} />);

  openRegistration();
  fillRegistration();
  fireEvent.click(screen.getByRole('button', { name: 'Create account' }));

  const alert = await screen.findByRole('alert');
  expect(alert).toHaveTextContent('Could not complete the request. Please try again.');
  expect(alert).not.toHaveTextContent('Handle is unavailable.');
  expect(alert).not.toHaveTextContent('validation_error');
  expect(alert).not.toHaveTextContent('{');
});
