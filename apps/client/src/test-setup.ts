import '@testing-library/jest-dom/vitest';
import { cleanup } from '@testing-library/react';
import { afterEach, vi } from 'vitest';

vi.mock('expo-constants', () => ({ default: { expoConfig: null } }));
vi.mock('expo-crypto', () => ({ randomUUID: () => '99999999-9999-4999-8999-999999999999' }));

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});
