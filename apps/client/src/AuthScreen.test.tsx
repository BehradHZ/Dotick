import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { expect, test, vi } from 'vitest';
import AuthScreen from './AuthScreen';

function json(data: unknown, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

test('registers and verifies a new email account', async () => {
  const fetch = vi.fn(async (input: RequestInfo | URL, _init?: RequestInit) => {
    void _init;
    const url = String(input);
    if (url.endsWith('/api/v1/auth/register')) return json({ status: 'accepted' }, 202);
    if (url.endsWith('/api/v1/auth/email/verify')) return new Response(null, { status: 204 });
    throw new Error(`Unhandled request: ${url}`);
  });
  vi.stubGlobal('fetch', fetch);
  render(<AuthScreen onAuthenticated={vi.fn()} />);

  fireEvent.click(screen.getByRole('button', { name: 'Create account' }));
  fireEvent.change(screen.getByLabelText('Display name'), { target: { value: 'New Person' } });
  fireEvent.change(screen.getByLabelText('Handle'), { target: { value: 'new_person' } });
  fireEvent.change(screen.getByLabelText('Registration email'), {
    target: { value: 'new@example.test' },
  });
  fireEvent.change(screen.getByLabelText('New password'), {
    target: { value: 'Safe-password-for-tests-8!' },
  });
  fireEvent.click(screen.getByRole('button', { name: 'Create account' }));

  expect(await screen.findByRole('heading', { name: 'Check your inbox' })).toBeVisible();
  expect(screen.getByText(/6-digit verification code/)).toBeVisible();
  fireEvent.change(screen.getByLabelText('Verification code'), { target: { value: '123456' } });
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
  });
});

test('requests a reset and confirms a replacement password', async () => {
  const fetch = vi.fn(async (input: RequestInfo | URL) => {
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

test('shows backend field validation without exposing raw envelopes', async () => {
  vi.stubGlobal(
    'fetch',
    vi
      .fn()
      .mockResolvedValue(
        json(
          { error: { code: 'validation_error', details: { handle: ['Handle is unavailable.'] } } },
          400,
        ),
      ),
  );
  render(<AuthScreen onAuthenticated={vi.fn()} />);
  fireEvent.click(screen.getByRole('button', { name: 'Create account' }));
  fireEvent.change(screen.getByLabelText('Display name'), { target: { value: 'New Person' } });
  fireEvent.change(screen.getByLabelText('Handle'), { target: { value: 'new_person' } });
  fireEvent.change(screen.getByLabelText('Registration email'), {
    target: { value: 'new@example.test' },
  });
  fireEvent.change(screen.getByLabelText('New password'), {
    target: { value: 'Safe-password-for-tests-8!' },
  });
  fireEvent.click(screen.getByRole('button', { name: 'Create account' }));
  expect(await screen.findByRole('alert')).toHaveTextContent('Handle is unavailable.');
});
