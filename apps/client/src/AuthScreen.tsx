import { useState } from 'react';
import {
  ActivityIndicator,
  Platform,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  useWindowDimensions,
  View,
} from 'react-native';
import {
  ApiError,
  type ApiSession,
  defaultApiUrl,
  identityApi,
  signIn,
  signInWithGoogleCredential,
  signInWithPasskey,
} from './api';

type Mode = 'sign-in' | 'register' | 'verify' | 'reset-request' | 'reset-confirm';

const colors = {
  paper: '#fffdf7',
  background: '#f2eee3',
  ink: '#171717',
  muted: '#69675f',
  orange: '#ff7a00',
  soft: '#ffe2bf',
  green: '#d9f2df',
  red: '#b42318',
  redSoft: '#ffe5df',
};

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

async function googleCredential(clientId: string) {
  if (Platform.OS !== 'web' || typeof document === 'undefined') {
    throw new Error('Google sign-in needs the configured native provider build.');
  }
  if (!clientId) throw new Error('Google sign-in is not configured.');
  if (!window.google) {
    await new Promise<void>((resolve, reject) => {
      const existing = document.querySelector<HTMLScriptElement>('script[data-dotick-google]');
      if (existing) {
        existing.addEventListener('load', () => resolve(), { once: true });
        existing.addEventListener(
          'error',
          () => reject(new Error('Google sign-in could not load.')),
          {
            once: true,
          },
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
  }
  if (!window.google) throw new Error('Google sign-in could not start.');
  return new Promise<string>((resolve, reject) => {
    let settled = false;
    const timeout = window.setTimeout(() => {
      if (!settled) reject(new Error('Google sign-in timed out.'));
    }, 60_000);
    window.google?.accounts.id.initialize({
      client_id: clientId,
      callback: ({ credential }) => {
        settled = true;
        window.clearTimeout(timeout);
        resolve(credential);
      },
    });
    window.google?.accounts.id.prompt((notification) => {
      if (
        !settled &&
        (notification.isNotDisplayed() ||
          notification.isSkippedMoment() ||
          notification.isDismissedMoment())
      ) {
        window.clearTimeout(timeout);
        reject(new Error('Google sign-in was cancelled or unavailable.'));
      }
    });
  });
}

function errorMessage(error: unknown) {
  if (error instanceof ApiError) return error.message;
  if (error instanceof Error) return error.message;
  return 'Could not complete the request. Please try again.';
}

function Action({
  title,
  onPress,
  disabled = false,
  secondary = false,
}: {
  title: string;
  onPress: () => void;
  disabled?: boolean;
  secondary?: boolean;
}) {
  return (
    <Pressable
      accessibilityRole="button"
      accessibilityLabel={title}
      accessibilityState={{ disabled }}
      disabled={disabled}
      onPress={onPress}
      style={({ pressed }) => [
        styles.action,
        secondary && styles.secondaryAction,
        disabled && styles.disabled,
        pressed && styles.pressed,
      ]}
    >
      <Text style={styles.actionText}>{title}</Text>
    </Pressable>
  );
}

function Link({
  title,
  onPress,
  disabled = false,
}: {
  title: string;
  onPress: () => void;
  disabled?: boolean;
}) {
  return (
    <Pressable
      accessibilityRole="button"
      accessibilityLabel={title}
      disabled={disabled}
      onPress={onPress}
      style={styles.linkButton}
    >
      <Text style={styles.linkText}>{title}</Text>
    </Pressable>
  );
}

export default function AuthScreen({
  onAuthenticated,
}: {
  onAuthenticated: (session: ApiSession) => Promise<void>;
}) {
  const { width } = useWindowDimensions();
  const narrow = width < 760;
  const [mode, setMode] = useState<Mode>('sign-in');
  const [apiUrl, setApiUrl] = useState(defaultApiUrl);
  const [email, setEmail] = useState('developer@example.test');
  const [password, setPassword] = useState('');
  const [displayName, setDisplayName] = useState('');
  const [handle, setHandle] = useState('');
  const [code, setCode] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [showConnection, setShowConnection] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');

  function changeMode(next: Mode) {
    setMode(next);
    setError('');
    setNotice('');
    setCode('');
  }

  async function perform(work: () => Promise<void>) {
    if (busy) return;
    setBusy(true);
    setError('');
    setNotice('');
    try {
      await work();
    } catch (failure) {
      setError(errorMessage(failure));
    } finally {
      setBusy(false);
    }
  }

  async function authenticate(session: Promise<ApiSession>) {
    await onAuthenticated(await session);
    setPassword('');
  }

  const validEmail = email.trim().includes('@');
  const validPassword = password.length >= 8;

  return (
    <ScrollView style={styles.page} contentContainerStyle={styles.pageContent}>
      <View style={styles.brandRow}>
        <View style={styles.logo}>
          <Text style={styles.logoText}>✓</Text>
        </View>
        <View>
          <Text style={styles.brandName}>Dotick</Text>
          <Text style={styles.muted}>Turn loose thoughts into done work.</Text>
        </View>
      </View>
      <View style={[styles.layout, narrow && styles.layoutNarrow]}>
        <View style={styles.intro}>
          <Text style={styles.eyebrow}>WELCOME TO DOTICK</Text>
          <Text accessibilityRole="header" style={[styles.hero, narrow && styles.heroNarrow]}>
            Clear head.{`\n`}Small steps.
          </Text>
          <Text style={styles.introText}>
            One private account for Inbox, Lists, and every small win. Your credentials stay out of
            app storage.
          </Text>
          <View style={styles.promise}>
            <Text style={styles.promiseText}>✓ Session-scoped tokens</Text>
          </View>
          <View style={styles.promise}>
            <Text style={styles.promiseText}>✓ Verified email identity</Text>
          </View>
          <View style={styles.promise}>
            <Text style={styles.promiseText}>✓ Revocable access</Text>
          </View>
        </View>

        <View style={styles.card}>
          {mode === 'sign-in' && (
            <>
              <Text style={styles.eyebrow}>WELCOME BACK</Text>
              <Text accessibilityRole="header" style={styles.cardTitle}>
                Sign in
              </Text>
              <Text style={styles.subtext}>Continue with your Dotick account.</Text>
              <Action
                title="Continue with Google"
                secondary
                disabled={busy}
                onPress={() =>
                  void perform(async () => {
                    const credential = await googleCredential(
                      process.env.EXPO_PUBLIC_GOOGLE_CLIENT_ID ?? '',
                    );
                    await authenticate(signInWithGoogleCredential(apiUrl, credential));
                  })
                }
              />
              <Action
                title="Sign in with a passkey"
                secondary
                disabled={busy}
                onPress={() => void perform(() => authenticate(signInWithPasskey(apiUrl)))}
              />
              <View style={styles.dividerRow}>
                <View style={styles.divider} />
                <Text style={styles.dividerText}>OR USE EMAIL</Text>
                <View style={styles.divider} />
              </View>
              <Text style={styles.label}>Email</Text>
              <TextInput
                accessibilityLabel="Email"
                value={email}
                onChangeText={setEmail}
                autoCapitalize="none"
                keyboardType="email-address"
                autoComplete="email"
                editable={!busy}
                style={styles.input}
              />
              <View style={styles.labelRow}>
                <Text style={styles.label}>Password</Text>
                <Link
                  title="Forgot password?"
                  disabled={busy}
                  onPress={() => changeMode('reset-request')}
                />
              </View>
              <View style={styles.passwordRow}>
                <TextInput
                  accessibilityLabel="Password"
                  value={password}
                  onChangeText={setPassword}
                  secureTextEntry={!showPassword}
                  autoComplete="current-password"
                  editable={!busy}
                  style={[styles.input, styles.passwordInput]}
                  onSubmitEditing={() =>
                    void perform(() => authenticate(signIn(apiUrl, email.trim(), password)))
                  }
                />
                <Link
                  title={showPassword ? 'Hide password' : 'Show password'}
                  onPress={() => setShowPassword((current) => !current)}
                />
              </View>
              <Action
                title="Sign in"
                disabled={busy || !validEmail || !validPassword || !apiUrl.trim()}
                onPress={() =>
                  void perform(() => authenticate(signIn(apiUrl, email.trim(), password)))
                }
              />
              <View style={styles.centerRow}>
                <Text style={styles.subtext}>New to Dotick?</Text>
                <Link
                  title="Create account"
                  disabled={busy}
                  onPress={() => changeMode('register')}
                />
              </View>
            </>
          )}

          {mode === 'register' && (
            <>
              <Text style={styles.eyebrow}>NEW ACCOUNT</Text>
              <Text accessibilityRole="header" style={styles.cardTitle}>
                Create account
              </Text>
              <Text style={styles.label}>Display name</Text>
              <TextInput
                accessibilityLabel="Display name"
                value={displayName}
                onChangeText={setDisplayName}
                editable={!busy}
                style={styles.input}
              />
              <Text style={styles.label}>Handle</Text>
              <TextInput
                accessibilityLabel="Handle"
                value={handle}
                onChangeText={setHandle}
                autoCapitalize="none"
                autoCorrect={false}
                editable={!busy}
                style={styles.input}
                placeholder="letters_numbers"
              />
              <Text style={styles.label}>Email</Text>
              <TextInput
                accessibilityLabel="Registration email"
                value={email}
                onChangeText={setEmail}
                autoCapitalize="none"
                keyboardType="email-address"
                editable={!busy}
                style={styles.input}
              />
              <Text style={styles.label}>Password</Text>
              <TextInput
                accessibilityLabel="New password"
                value={password}
                onChangeText={setPassword}
                secureTextEntry={!showPassword}
                editable={!busy}
                style={styles.input}
              />
              <Text style={styles.hint}>
                Use at least 8 characters. Avoid common or personal passwords.
              </Text>
              <Action
                title="Create account"
                disabled={
                  busy ||
                  !validEmail ||
                  !validPassword ||
                  !displayName.trim() ||
                  !/^[A-Za-z0-9_]{3,30}$/.test(handle)
                }
                onPress={() =>
                  void perform(async () => {
                    await identityApi(apiUrl).register({
                      email: email.trim(),
                      password,
                      handle,
                      display_name: displayName.trim(),
                    });
                    setPassword('');
                    setMode('verify');
                    setNotice('Check your email for a 6-digit verification code.');
                  })
                }
              />
              <Link title="Back to sign in" disabled={busy} onPress={() => changeMode('sign-in')} />
            </>
          )}

          {mode === 'verify' && (
            <>
              <Text style={styles.eyebrow}>VERIFY EMAIL</Text>
              <Text accessibilityRole="header" style={styles.cardTitle}>
                Check your inbox
              </Text>
              <Text style={styles.subtext}>Enter the 6-digit code sent to {email.trim()}.</Text>
              <Text style={styles.label}>Verification code</Text>
              <TextInput
                accessibilityLabel="Verification code"
                value={code}
                onChangeText={setCode}
                keyboardType="number-pad"
                maxLength={6}
                editable={!busy}
                style={[styles.input, styles.codeInput]}
              />
              <Action
                title="Verify email"
                disabled={busy || !/^\d{6}$/.test(code)}
                onPress={() =>
                  void perform(async () => {
                    await identityApi(apiUrl).verifyEmail(email.trim(), code);
                    setMode('sign-in');
                    setCode('');
                    setNotice('Email verified. Sign in to continue.');
                  })
                }
              />
              <Link
                title="Resend code"
                disabled={busy}
                onPress={() =>
                  void perform(async () => {
                    await identityApi(apiUrl).resendVerification(email.trim());
                    setNotice('If the account is eligible, a new code was sent.');
                  })
                }
              />
              <Link title="Back to sign in" disabled={busy} onPress={() => changeMode('sign-in')} />
            </>
          )}

          {mode === 'reset-request' && (
            <>
              <Text style={styles.eyebrow}>PASSWORD RECOVERY</Text>
              <Text accessibilityRole="header" style={styles.cardTitle}>
                Reset password
              </Text>
              <Text style={styles.subtext}>
                Enter your email. The response never reveals whether an account exists.
              </Text>
              <Text style={styles.label}>Email</Text>
              <TextInput
                accessibilityLabel="Recovery email"
                value={email}
                onChangeText={setEmail}
                autoCapitalize="none"
                keyboardType="email-address"
                editable={!busy}
                style={styles.input}
              />
              <Action
                title="Send reset code"
                disabled={busy || !validEmail}
                onPress={() =>
                  void perform(async () => {
                    await identityApi(apiUrl).requestPasswordReset(email.trim());
                    setMode('reset-confirm');
                    setNotice('If the account is eligible, a reset code was sent.');
                  })
                }
              />
              <Link title="Back to sign in" disabled={busy} onPress={() => changeMode('sign-in')} />
            </>
          )}

          {mode === 'reset-confirm' && (
            <>
              <Text style={styles.eyebrow}>PASSWORD RECOVERY</Text>
              <Text accessibilityRole="header" style={styles.cardTitle}>
                Choose a new password
              </Text>
              <Text style={styles.label}>Reset code</Text>
              <TextInput
                accessibilityLabel="Reset code"
                value={code}
                onChangeText={setCode}
                keyboardType="number-pad"
                maxLength={6}
                editable={!busy}
                style={[styles.input, styles.codeInput]}
              />
              <Text style={styles.label}>New password</Text>
              <TextInput
                accessibilityLabel="Replacement password"
                value={password}
                onChangeText={setPassword}
                secureTextEntry={!showPassword}
                editable={!busy}
                style={styles.input}
              />
              <Action
                title="Update password"
                disabled={busy || !/^\d{6}$/.test(code) || !validPassword}
                onPress={() =>
                  void perform(async () => {
                    await identityApi(apiUrl).confirmPasswordReset(email.trim(), code, password);
                    setPassword('');
                    setCode('');
                    setMode('sign-in');
                    setNotice('Password updated. Sign in with your new password.');
                  })
                }
              />
              <Link
                title="Request another code"
                disabled={busy}
                onPress={() => changeMode('reset-request')}
              />
            </>
          )}

          <View style={styles.connectionBlock}>
            <Link
              title={showConnection ? 'Hide connection settings' : 'Connection settings'}
              onPress={() => setShowConnection((current) => !current)}
            />
            {showConnection && (
              <>
                <Text style={styles.label}>API address</Text>
                <TextInput
                  accessibilityLabel="API address"
                  value={apiUrl}
                  onChangeText={setApiUrl}
                  autoCapitalize="none"
                  autoCorrect={false}
                  editable={!busy}
                  style={styles.input}
                />
              </>
            )}
          </View>
          {busy && <ActivityIndicator accessibilityLabel="Working" color={colors.orange} />}
          {error !== '' && (
            <Text accessibilityRole="alert" style={styles.error}>
              {error}
            </Text>
          )}
          {notice !== '' && (
            <Text accessibilityLiveRegion="polite" style={styles.notice}>
              {notice}
            </Text>
          )}
        </View>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: colors.background },
  pageContent: {
    flexGrow: 1,
    width: '100%',
    maxWidth: 1120,
    alignSelf: 'center',
    padding: 24,
    gap: 52,
  },
  brandRow: { flexDirection: 'row', alignItems: 'center', gap: 12 },
  logo: {
    width: 48,
    height: 48,
    borderWidth: 2,
    borderColor: colors.ink,
    borderRadius: 13,
    backgroundColor: colors.orange,
    alignItems: 'center',
    justifyContent: 'center',
    boxShadow: '3px 3px 0 #171717',
    transform: [{ rotate: '-3deg' }],
  },
  logoText: { fontSize: 28, fontWeight: '900', color: colors.ink },
  brandName: { color: colors.ink, fontSize: 22, fontWeight: '900' },
  muted: { color: colors.muted, fontSize: 13, lineHeight: 20 },
  eyebrow: { color: colors.ink, fontSize: 10, fontWeight: '900', letterSpacing: 1.4 },
  layout: { flexDirection: 'row', alignItems: 'center', gap: 64 },
  layoutNarrow: { flexDirection: 'column', alignItems: 'stretch', gap: 28 },
  intro: { flex: 1, gap: 14 },
  hero: { color: colors.ink, fontSize: 58, lineHeight: 62, letterSpacing: -2.5, fontWeight: '900' },
  heroNarrow: { fontSize: 44, lineHeight: 48 },
  introText: { color: colors.muted, fontSize: 16, lineHeight: 26, maxWidth: 470, marginBottom: 8 },
  promise: {
    alignSelf: 'flex-start',
    backgroundColor: colors.paper,
    borderWidth: 1.5,
    borderColor: colors.ink,
    borderRadius: 9,
    paddingHorizontal: 11,
    paddingVertical: 7,
  },
  promiseText: { color: colors.ink, fontSize: 12, fontWeight: '800' },
  card: {
    flex: 1,
    width: '100%',
    maxWidth: 470,
    backgroundColor: colors.paper,
    borderWidth: 2,
    borderColor: colors.ink,
    borderRadius: 18,
    padding: 24,
    gap: 11,
    boxShadow: '5px 5px 0 #171717',
  },
  cardTitle: { color: colors.ink, fontSize: 27, fontWeight: '900', letterSpacing: -0.6 },
  subtext: { color: colors.muted, fontSize: 13, lineHeight: 19 },
  label: { color: colors.ink, fontSize: 12, fontWeight: '800', marginTop: 3 },
  labelRow: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', gap: 8 },
  input: {
    minHeight: 46,
    borderWidth: 2,
    borderColor: colors.ink,
    borderRadius: 10,
    backgroundColor: '#fff',
    color: colors.ink,
    paddingHorizontal: 12,
    paddingVertical: 10,
    fontSize: 15,
  },
  passwordRow: { flexDirection: 'row', alignItems: 'center', gap: 9 },
  passwordInput: { flex: 1 },
  codeInput: { fontSize: 22, letterSpacing: 8, textAlign: 'center' },
  hint: { color: colors.muted, fontSize: 11, lineHeight: 17 },
  action: {
    minHeight: 46,
    borderWidth: 2,
    borderColor: colors.ink,
    borderRadius: 10,
    backgroundColor: colors.orange,
    paddingHorizontal: 14,
    paddingVertical: 10,
    alignItems: 'center',
    justifyContent: 'center',
    boxShadow: '2px 2px 0 #171717',
  },
  secondaryAction: { backgroundColor: colors.paper },
  actionText: { color: colors.ink, fontSize: 13, fontWeight: '900' },
  disabled: { opacity: 0.42 },
  pressed: { transform: [{ translateX: 1 }, { translateY: 1 }], boxShadow: 'none' },
  linkButton: { minHeight: 28, justifyContent: 'center' },
  linkText: { color: '#7a3b00', fontSize: 12, fontWeight: '900', textDecorationLine: 'underline' },
  dividerRow: { flexDirection: 'row', alignItems: 'center', gap: 9, marginVertical: 3 },
  divider: { flex: 1, height: 1, backgroundColor: '#d2cec2' },
  dividerText: { color: colors.muted, fontSize: 9, fontWeight: '800', letterSpacing: 1 },
  centerRow: { flexDirection: 'row', justifyContent: 'center', alignItems: 'center', gap: 6 },
  connectionBlock: { borderTopWidth: 1, borderColor: '#d2cec2', paddingTop: 7, gap: 8 },
  error: {
    color: colors.red,
    backgroundColor: colors.redSoft,
    borderRadius: 8,
    padding: 11,
    fontSize: 13,
    lineHeight: 19,
  },
  notice: {
    color: '#245e37',
    backgroundColor: colors.green,
    borderRadius: 8,
    padding: 11,
    fontSize: 13,
    lineHeight: 19,
  },
});
