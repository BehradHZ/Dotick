import { fireEvent, render, screen } from '@testing-library/react';
import { expect, test, vi } from 'vitest';
import App from './App';

const checkpoint = { id: '1', text: 'A persisted checkpoint', created_at: '2026-09-06T10:00:00Z' };

function signIn() {
  fireEvent.change(screen.getByLabelText('Email'), { target: { value: 'developer@example.test' } });
  fireEvent.change(screen.getByLabelText('Password'), { target: { value: 'test-password' } });
  fireEvent.click(screen.getByRole('button', { name: 'Open workbench' }));
}

test('developer signs in and sees only the checkpoints returned by the API', async () => {
  vi.stubGlobal(
    'fetch',
    vi.fn().mockResolvedValue(new Response(JSON.stringify({ results: [checkpoint] }))),
  );
  render(<App />);
  signIn();
  expect(await screen.findByText(checkpoint.text)).toBeVisible();
  expect(screen.getByRole('button', { name: 'Sign out' })).toBeVisible();
});

test('failed save retains the draft and a successful retry shows the persisted response', async () => {
  const fetch = vi
    .fn()
    .mockResolvedValueOnce(new Response(JSON.stringify({ results: [] })))
    .mockRejectedValueOnce(new TypeError('offline'))
    .mockResolvedValueOnce(new Response(JSON.stringify(checkpoint), { status: 201 }));
  vi.stubGlobal('fetch', fetch);
  render(<App />);
  signIn();
  const input = await screen.findByLabelText('New checkpoint');
  fireEvent.change(input, { target: { value: 'A persisted checkpoint' } });
  fireEvent.click(screen.getByRole('button', { name: 'Save checkpoint' }));
  expect(await screen.findByRole('alert')).toHaveTextContent('Connection interrupted');
  expect(input).toHaveValue(checkpoint.text);
  fireEvent.click(screen.getByRole('button', { name: 'Save checkpoint' }));
  expect(await screen.findByText('Checkpoint saved.')).toBeVisible();
  expect(input).toHaveValue('');
  expect(screen.getByText(checkpoint.text)).toBeVisible();
});

test('bad credentials keep the user on the sign-in form', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(new Response('{}', { status: 401 })));
  render(<App />);
  signIn();
  expect(await screen.findByRole('alert')).toHaveTextContent('Check your email and password.');
  expect(screen.queryByLabelText('New checkpoint')).not.toBeInTheDocument();
});

test('signing out removes private records from the screen', async () => {
  vi.stubGlobal(
    'fetch',
    vi.fn().mockResolvedValue(new Response(JSON.stringify({ results: [checkpoint] }))),
  );
  render(<App />);
  signIn();
  await screen.findByText(checkpoint.text);
  fireEvent.click(screen.getByRole('button', { name: 'Sign out' }));
  expect(screen.queryByText(checkpoint.text)).not.toBeInTheDocument();
  expect(screen.getByLabelText('Password')).toHaveValue('');
});
