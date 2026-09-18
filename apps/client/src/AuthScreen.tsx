import { useState } from 'react';
import {
  ActivityIndicator,
  Platform,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  type TextInputProps,
  View,
} from 'react-native';

import {
  ApiError,
  type ApiSession,
  defaultApiUrl,
  identityApi,
  PasskeyCancelledError,
  passkeyAuthenticationAvailable,
  PasskeyUnavailableError,
  signIn,
  signInWithGoogleCredential,
  signInWithPasskey,
} from './api';

type Mode = 'sign-in' | 'register' | 'verify' | 'reset-request' | 'reset-confirm';
type FieldProps = TextInputProps & { label: string; accessibilityLabel: string };

type GoogleIdentity = {
  accounts: {
    id: {
      initialize(input: {
        client_id: string;
        callback(response: { credential: string }): void;
      }): void;
      prompt(
        callback: (notification: {
          isNotDisplayed(): boolean;
          isSkippedMoment(): boolean;
          isDismissedMoment(): boolean;
        }) => void,
      ): void;
    };
  };
};

declare global {
  interface Window {
    google?: GoogleIdentity;
  }
}

function Field({ label, accessibilityLabel, style, ...props }: FieldProps) {
  return (
    <View style={styles.field}>
      <Text style={styles.label}>{label}</Text>
      <TextInput
        {...props}
        accessibilityLabel={accessibilityLabel}
        style={[styles.input, style]}
      />
    </View>
  );
}

function Button({
  title,
  onPress,
  disabled = false,
  link = false,
  secondary = false,
}: {
  title: string;
  onPress: () => void;
  disabled?: boolean;
  link?: boolean;
  secondary?: boolean;
}) {
  return (
    <Pressable
      accessibilityRole="button"
      accessibilityLabel={title}
      accessibilityState={{ disabled }}
      disabled={disabled}
      onPress={onPress}
      style={[
        link ? styles.link : styles.button,
        secondary && !link && styles.secondaryButton,
        disabled && styles.disabled,
      ]}
    >
      <Text style={link ? styles.linkText : styles.buttonText}>{title}</Text>
    </Pressable>
  );
}

function safeErrorMessage(error: unknown) {
  if (error instanceof PasskeyCancelledError || error instanceof PasskeyUnavailableError) {
    return error.message;
  }
  if (error instanceof ApiError) {
    if (error.status === 401) return 'Check your email and password.';
    if (error.status === 503) return 'This sign-in method is temporarily unavailable.';
    return error.message;
  }
  if (error instanceof Error && error.message.startsWith('Connection interrupted')) {
    return error.message;
  }
  if (error instanceof Error && error.message.startsWith('Google sign-in')) return error.message;
  return 'Could not complete the request. Please try again.';
}

async function loadGoogleIdentity() {
  if (typeof window === 'undefined' || typeof document === 'undefined') {
    throw new Error('Google sign-in is unavailable on this device.');
  }
  if (window.google) return window.google;

  await new Promise<void>((resolve, reject) => {
    const existing = document.querySelector<HTMLScriptElement>('script[data-dotick-google]');
    if (existing) {
      existing.addEventListener('load', () => resolve(), { once: true });
      existing.addEventListener(
        'error',
        () => reject(new Error('Google sign-in could not load.')),
        { once: true },
      );
      return;
    }

    const script = document.createElement('script');
    script.src = 'https://accounts.google.com/gsi/client';
    script.async = true;
    script.dataset.dotickGoogle = 'true';
    script.onload = () => resolve();
    script.onerror = () => reject(new Error('Google sign-in could not load.'));
    document.head.appendChild(script);
  });

  if (!window.google) throw new Error('Google sign-in could not load.');
  return window.google;
}

async function googleCredential(clientId: string) {
  if (Platform.OS !== 'web') throw new Error('Google sign-in is unavailable on this device.');
  if (!clientId) throw new Error('Google sign-in is not configured.');
  const google = await loadGoogleIdentity();

  return new Promise<string>((resolve, reject) => {
    let settled = false;
    const finish = (work: () => void) => {
      if (settled) return;
      settled = true;
      work();
    };
    const timeout = window.setTimeout(
      () => finish(() => reject(new Error('Google sign-in timed out.'))),
      60_000,
    );

    google.accounts.id.initialize({
      client_id: clientId,
      callback: ({ credential }) => {
        finish(() => {
          window.clearTimeout(timeout);
          resolve(credential);
        });
      },
    });
    google.accounts.id.prompt((notification) => {
      if (
        notification.isNotDisplayed() ||
        notification.isSkippedMoment() ||
        notification.isDismissedMoment()
      ) {
        finish(() => {
          window.clearTimeout(timeout);
          reject(new Error('Google sign-in was cancelled or unavailable.'));
        });
      }
    });
  });
}

export default function AuthScreen({
  onAuthenticated,
}: {
  onAuthenticated: (session: ApiSession) => Promise<void> | void;
}) {
  const [mode, setMode] = useState<Mode>('sign-in');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [displayName, setDisplayName] = useState('');
  const [handle, setHandle] = useState('');
  const [code, setCode] = useState('');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');
  const apiUrl = defaultApiUrl();
  const googleClientId = process.env.EXPO_PUBLIC_GOOGLE_CLIENT_ID?.trim() ?? '';
  const googleAvailable = Platform.OS === 'web' && googleClientId !== '';
  const passkeyAvailable = passkeyAuthenticationAvailable();
  const hasProviderSignIn = googleAvailable || passkeyAvailable;

  const normalizedEmail = email.trim();
  const validEmail = /^\S+@\S+\.\S+$/.test(normalizedEmail);
  const validPassword = password.length >= 8;
  const validHandle = /^[A-Za-z0-9_]{3,30}$/.test(handle);
  const validCode = /^\d{6}$/.test(code);

  function switchMode(next: Mode) {
    setMode(next);
    setPassword('');
    setCode('');
    setError('');
    setNotice('');
  }

  async function perform(work: () => Promise<void>) {
    if (busy) return;
    setBusy(true);
    setError('');
    setNotice('');
    try {
      await work();
    } catch (failure) {
      setError(safeErrorMessage(failure));
    } finally {
      setBusy(false);
    }
  }

  function updateCode(value: string) {
    setCode(value.replace(/\D/g, '').slice(0, 6));
  }

  async function completeAuthentication(sessionPromise: Promise<ApiSession>) {
    const session = await sessionPromise;
    await onAuthenticated(session);
    setPassword('');
  }

  async function authenticatePassword() {
    await completeAuthentication(signIn(apiUrl, normalizedEmail, password));
  }

  async function authenticateGoogle() {
    const credential = await googleCredential(googleClientId);
    await completeAuthentication(signInWithGoogleCredential(apiUrl, credential));
  }

  async function authenticatePasskey() {
    await completeAuthentication(signInWithPasskey(apiUrl));
  }

  return (
    <ScrollView style={styles.page} contentContainerStyle={styles.content}>
      <View style={styles.card}>
        <Text style={styles.brand}>Dotick</Text>

        {mode === 'sign-in' && (
          <>
            <Text accessibilityRole="header" style={styles.title}>Sign in</Text>
            {googleAvailable && (
              <Button
                title="Continue with Google"
                secondary
                disabled={busy}
                onPress={() => void perform(authenticateGoogle)}
              />
            )}
            {passkeyAvailable && (
              <Button
                title="Sign in with a passkey"
                secondary
                disabled={busy}
                onPress={() => void perform(authenticatePasskey)}
              />
            )}
            {hasProviderSignIn && <Text style={styles.separator}>OR USE EMAIL</Text>}
            <Field
              label="Email"
              accessibilityLabel="Email"
              value={email}
              onChangeText={setEmail}
              autoCapitalize="none"
              autoCorrect={false}
              keyboardType="email-address"
              autoComplete="email"
              editable={!busy}
            />
            <Field
              label="Password"
              accessibilityLabel="Password"
              value={password}
              onChangeText={setPassword}
              secureTextEntry
              autoComplete="current-password"
              editable={!busy}
              onSubmitEditing={() => {
                if (validEmail && validPassword) void perform(authenticatePassword);
              }}
            />
            <Button
              title="Sign in"
              disabled={busy || !validEmail || !validPassword}
              onPress={() => void perform(authenticatePassword)}
            />
            <Button
              title="Forgot password?"
              link
              disabled={busy}
              onPress={() => switchMode('reset-request')}
            />
            <Button
              title="Create account"
              link
              disabled={busy}
              onPress={() => switchMode('register')}
            />
          </>
        )}

        {mode === 'register' && (
          <>
            <Text accessibilityRole="header" style={styles.title}>Create account</Text>
            <Field
              label="Display name"
              accessibilityLabel="Display name"
              value={displayName}
              onChangeText={setDisplayName}
              editable={!busy}
            />
            <Field
              label="Handle"
              accessibilityLabel="Handle"
              value={handle}
              onChangeText={setHandle}
              autoCapitalize="none"
              autoCorrect={false}
              maxLength={30}
              placeholder="letters_numbers"
              editable={!busy}
            />
            <Field
              label="Email"
              accessibilityLabel="Registration email"
              value={email}
              onChangeText={setEmail}
              autoCapitalize="none"
              autoCorrect={false}
              keyboardType="email-address"
              autoComplete="email"
              editable={!busy}
            />
            <Field
              label="Password"
              accessibilityLabel="New password"
              value={password}
              onChangeText={setPassword}
              secureTextEntry
              autoComplete="new-password"
              editable={!busy}
            />
            <Text style={styles.hint}>Use at least 8 characters and avoid common passwords.</Text>
            <Button
              title="Create account"
              disabled={
                busy || !validEmail || !validPassword || !displayName.trim() || !validHandle
              }
              onPress={() =>
                void perform(async () => {
                  await identityApi(apiUrl).register({
                    email: normalizedEmail,
                    password,
                    handle,
                    display_name: displayName.trim(),
                  });
                  setPassword('');
                  setMode('verify');
                  setNotice(
                    'If registration can proceed, check your email for a 6-digit verification code.',
                  );
                })
              }
            />
            <Button
              title="Back to sign in"
              link
              disabled={busy}
              onPress={() => switchMode('sign-in')}
            />
          </>
        )}

        {mode === 'verify' && (
          <>
            <Text accessibilityRole="header" style={styles.title}>Check your inbox</Text>
            <Text style={styles.hint}>
              Enter the 6-digit verification code for {normalizedEmail}.
            </Text>
            <Field
              label="Verification code"
              accessibilityLabel="Verification code"
              value={code}
              onChangeText={updateCode}
              keyboardType="number-pad"
              maxLength={6}
              editable={!busy}
              style={styles.code}
            />
            <Button
              title="Verify email"
              disabled={busy || !validCode}
              onPress={() =>
                void perform(async () => {
                  await identityApi(apiUrl).verifyEmail(normalizedEmail, code);
                  setCode('');
                  setMode('sign-in');
                  setNotice('Email verified. Sign in to continue.');
                })
              }
            />
            <Button
              title="Resend code"
              link
              disabled={busy || !validEmail}
              onPress={() =>
                void perform(async () => {
                  await identityApi(apiUrl).resendVerification(normalizedEmail);
                  setNotice('If the account is eligible, a new code was sent.');
                })
              }
            />
            <Button
              title="Back to sign in"
              link
              disabled={busy}
              onPress={() => switchMode('sign-in')}
            />
          </>
        )}

        {mode === 'reset-request' && (
          <>
            <Text accessibilityRole="header" style={styles.title}>Reset password</Text>
            <Text style={styles.hint}>The response does not reveal whether an account exists.</Text>
            <Field
              label="Email"
              accessibilityLabel="Recovery email"
              value={email}
              onChangeText={setEmail}
              autoCapitalize="none"
              autoCorrect={false}
              keyboardType="email-address"
              autoComplete="email"
              editable={!busy}
            />
            <Button
              title="Send reset code"
              disabled={busy || !validEmail}
              onPress={() =>
                void perform(async () => {
                  await identityApi(apiUrl).requestPasswordReset(normalizedEmail);
                  setMode('reset-confirm');
                  setNotice('If the account is eligible, a reset code was sent.');
                })
              }
            />
            <Button
              title="Back to sign in"
              link
              disabled={busy}
              onPress={() => switchMode('sign-in')}
            />
          </>
        )}

        {mode === 'reset-confirm' && (
          <>
            <Text accessibilityRole="header" style={styles.title}>Choose a new password</Text>
            <Field
              label="Reset code"
              accessibilityLabel="Reset code"
              value={code}
              onChangeText={updateCode}
              keyboardType="number-pad"
              maxLength={6}
              editable={!busy}
              style={styles.code}
            />
            <Field
              label="New password"
              accessibilityLabel="Replacement password"
              value={password}
              onChangeText={setPassword}
              secureTextEntry
              autoComplete="new-password"
              editable={!busy}
            />
            <Button
              title="Update password"
              disabled={busy || !validCode || !validPassword}
              onPress={() =>
                void perform(async () => {
                  await identityApi(apiUrl).confirmPasswordReset(normalizedEmail, code, password);
                  setPassword('');
                  setCode('');
                  setMode('sign-in');
                  setNotice('Password updated. Sign in with your new password.');
                })
              }
            />
            <Button
              title="Request another code"
              link
              disabled={busy}
              onPress={() => switchMode('reset-request')}
            />
          </>
        )}

        {busy && <ActivityIndicator accessibilityLabel="Working" />}
        {error !== '' && <Text accessibilityRole="alert" style={styles.error}>{error}</Text>}
        {notice !== '' && (
          <Text accessibilityLiveRegion="polite" style={styles.notice}>
            {notice}
          </Text>
        )}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: '#f2eee3' },
  content: { flexGrow: 1, justifyContent: 'center', alignItems: 'center', padding: 24 },
  card: {
    width: '100%',
    maxWidth: 480,
    gap: 12,
    padding: 24,
    backgroundColor: '#fffdf7',
    borderWidth: 2,
    borderColor: '#171717',
    borderRadius: 18,
    boxShadow: '5px 5px 0 #171717',
  },
  brand: { fontSize: 20, fontWeight: '900', color: '#171717' },
  title: { fontSize: 28, fontWeight: '900', color: '#171717' },
  field: { gap: 6 },
  label: { fontSize: 12, fontWeight: '800', color: '#171717' },
  input: {
    minHeight: 46,
    paddingHorizontal: 12,
    borderWidth: 2,
    borderColor: '#171717',
    borderRadius: 10,
    backgroundColor: '#fff',
    color: '#171717',
  },
  code: { fontSize: 22, letterSpacing: 8, textAlign: 'center' },
  hint: { fontSize: 12, lineHeight: 18, color: '#69675f' },
  separator: { textAlign: 'center', fontSize: 10, fontWeight: '800', color: '#69675f' },
  button: {
    minHeight: 46,
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 14,
    borderWidth: 2,
    borderColor: '#171717',
    borderRadius: 10,
    backgroundColor: '#ff7a00',
  },
  secondaryButton: { backgroundColor: '#fffdf7' },
  buttonText: { fontSize: 13, fontWeight: '900', color: '#171717' },
  link: { minHeight: 30, alignItems: 'center', justifyContent: 'center' },
  linkText: { fontSize: 12, fontWeight: '800', color: '#7a3b00', textDecorationLine: 'underline' },
  disabled: { opacity: 0.45 },
  error: { padding: 10, borderRadius: 8, color: '#b42318', backgroundColor: '#ffe5df' },
  notice: { padding: 10, borderRadius: 8, color: '#245e37', backgroundColor: '#d9f2df' },
});
