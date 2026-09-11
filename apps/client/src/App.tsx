import { useState } from 'react';
import {
  ActivityIndicator,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  useWindowDimensions,
  View,
} from 'react-native';
import { ApiError, type Checkpoint, type Credentials, foundationApi } from './api';

const colors = {
  paper: '#fffdf7',
  background: '#f4f1e8',
  ink: '#151515',
  muted: '#69675f',
  orange: '#ff7a00',
  soft: '#ffe2bf',
  green: '#daf4e2',
  red: '#b42318',
};

function Button({
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
        styles.button,
        secondary && styles.secondary,
        disabled && styles.disabled,
        pressed && styles.pressed,
      ]}
    >
      <Text style={styles.buttonText}>{title}</Text>
    </Pressable>
  );
}

function errorMessage(error: unknown) {
  return error instanceof ApiError
    ? error.message
    : 'Connection interrupted. Your text is still here. Try again when the API is available.';
}

export default function App() {
  const { width } = useWindowDimensions();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [credentials, setCredentials] = useState<Credentials | null>(null);
  const [checkpoints, setCheckpoints] = useState<Checkpoint[]>([]);
  const [text, setText] = useState('');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');

  async function signIn() {
    setError('');
    setBusy(true);
    const candidate = { email: email.trim(), password };
    try {
      const response = await foundationApi(candidate).list();
      setCheckpoints(response.results);
      setCredentials(candidate);
      setPassword('');
    } catch (failure) {
      setError(errorMessage(failure));
    } finally {
      setBusy(false);
    }
  }

  async function save() {
    if (!credentials || !text.trim() || busy) return;
    setError('');
    setNotice('');
    setBusy(true);
    try {
      const record = await foundationApi(credentials).create(text.trim());
      setCheckpoints((existing) => [record, ...existing].slice(0, 100));
      setText('');
      setNotice('Checkpoint saved.');
    } catch (failure) {
      setError(errorMessage(failure));
    } finally {
      setBusy(false);
    }
  }

  async function reload() {
    if (!credentials) return;
    setError('');
    setNotice('');
    setBusy(true);
    try {
      setCheckpoints((await foundationApi(credentials).list()).results);
      setNotice('Checkpoints refreshed.');
    } catch (failure) {
      setError(errorMessage(failure));
    } finally {
      setBusy(false);
    }
  }

  function signOut() {
    setCredentials(null);
    setCheckpoints([]);
    setText('');
    setError('');
    setNotice('');
    setPassword('');
  }

  return (
    <ScrollView style={styles.page} contentContainerStyle={styles.pageContent}>
      <View style={styles.topbar}>
        <View style={styles.brand}>
          <View style={styles.logo}>
            <Text style={styles.logoText}>✓</Text>
          </View>
          <View>
            <Text style={styles.brandName}>Dotick</Text>
            <Text style={styles.muted}>A little structure. A little momentum.</Text>
          </View>
        </View>
        {credentials && <Button title="Sign out" secondary disabled={busy} onPress={signOut} />}
      </View>
      <View style={styles.badge}>
        <Text style={styles.eyebrow}>INCREMENT 0 · DEVELOPMENT WORKBENCH</Text>
      </View>
      <View style={[styles.workspace, width < 800 && styles.stacked]}>
        <View style={[styles.intro, width < 800 && styles.introCompact]}>
          <Text accessibilityRole="header" style={styles.headline}>
            Good things{'\n'}start small.
          </Text>
          <Text style={styles.introText}>
            The first working piece of Dotick. Save a checkpoint, reload it, and keep building from
            a solid foundation.
          </Text>
          <View style={styles.roadmapCard}>
            <Text style={styles.eyebrow}>THE PATH AHEAD</Text>
            <View style={styles.step}>
              <Text style={styles.stepNumber}>00</Text>
              <View style={styles.stepBody}>
                <Text style={styles.stepTitle}>Make it work</Text>
                <Text style={styles.muted}>Engineering foundation · current</Text>
              </View>
            </View>
            <View style={styles.divider} />
            <View style={styles.step}>
              <Text style={[styles.stepNumber, styles.future]}>01</Text>
              <View style={styles.stepBody}>
                <Text style={styles.stepTitle}>Make it useful</Text>
                <Text style={styles.muted}>Identity, organization & basic tasks</Text>
              </View>
            </View>
          </View>
          <Text style={styles.caption}>
            This isolated workbench verifies persistence. Checkpoints are development data; Task,
            Event, and Routine flows follow their roadmap increments.
          </Text>
        </View>
        <View style={styles.panel}>
          <View style={styles.panelHeader}>
            <Text style={styles.eyebrow}>
              {credentials ? 'YOUR WORKSPACE' : 'LET’S GET STARTED'}
            </Text>
            <Text accessibilityRole="header" style={styles.panelTitle}>
              {credentials ? 'Checkpoints' : 'Open your workbench'}
            </Text>
            <Text style={styles.muted}>
              {credentials
                ? 'Your latest 100 saved checkpoints.'
                : 'Sign in with your local developer account.'}
            </Text>
          </View>
          <View style={styles.panelBody}>
            {!credentials ? (
              <View style={styles.form}>
                <Text style={styles.label}>Email</Text>
                <TextInput
                  accessibilityLabel="Email"
                  value={email}
                  onChangeText={setEmail}
                  autoCapitalize="none"
                  keyboardType="email-address"
                  autoComplete="email"
                  style={styles.input}
                  placeholder="you@example.test"
                  editable={!busy}
                />
                <Text style={styles.label}>Password</Text>
                <TextInput
                  accessibilityLabel="Password"
                  value={password}
                  onChangeText={setPassword}
                  secureTextEntry
                  autoComplete="current-password"
                  style={styles.input}
                  placeholder="Your developer password"
                  editable={!busy}
                  onSubmitEditing={() => {
                    if (email && password && !busy) void signIn();
                  }}
                />
                <Button
                  title="Open workbench"
                  disabled={busy || !email.trim() || !password}
                  onPress={() => void signIn()}
                />
                <Text style={styles.caption}>
                  Use the account created during local setup. Credentials are kept only for this
                  open session.
                </Text>
              </View>
            ) : (
              <>
                <Text style={styles.label}>New checkpoint</Text>
                <TextInput
                  accessibilityLabel="New checkpoint"
                  value={text}
                  onChangeText={setText}
                  maxLength={240}
                  multiline
                  editable={!busy}
                  style={[styles.input, styles.composer]}
                  placeholder="What would you like to remember?"
                />
                <View style={styles.actions}>
                  <Text style={styles.caption}>{text.length}/240</Text>
                  <Button
                    title="Save checkpoint"
                    disabled={busy || !text.trim()}
                    onPress={() => void save()}
                  />
                </View>
                <View style={styles.listHeader}>
                  <Text style={styles.eyebrow}>SAVED CHECKPOINTS</Text>
                  <Button title="Refresh" secondary disabled={busy} onPress={() => void reload()} />
                </View>
                {checkpoints.length === 0 ? (
                  <View style={styles.empty}>
                    <Text style={styles.emptyIcon}>✦</Text>
                    <Text style={styles.stepTitle}>A fresh start.</Text>
                    <Text style={styles.muted}>Your first checkpoint belongs here.</Text>
                  </View>
                ) : (
                  checkpoints.map((record) => (
                    <View key={record.id} style={styles.record}>
                      <View style={styles.recordDot}>
                        <Text>✓</Text>
                      </View>
                      <View style={styles.stepBody}>
                        <Text style={styles.recordText}>{record.text}</Text>
                        <Text style={styles.caption}>
                          {new Date(record.created_at).toLocaleString()}
                        </Text>
                      </View>
                    </View>
                  ))
                )}
              </>
            )}
            {busy && (
              <ActivityIndicator
                accessibilityLabel="Working"
                color={colors.orange}
                style={styles.spinner}
              />
            )}
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
      </View>
      <Text style={styles.footer}>DOTICK / ONE VERIFIED STEP AT A TIME</Text>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: 'transparent' },
  pageContent: {
    padding: 24,
    paddingBottom: 40,
    maxWidth: 1200,
    width: '100%',
    alignSelf: 'center',
    gap: 28,
  },
  topbar: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    gap: 16,
    flexWrap: 'wrap',
  },
  brand: { flexDirection: 'row', alignItems: 'center', gap: 12 },
  logo: {
    width: 44,
    height: 44,
    backgroundColor: colors.orange,
    borderWidth: 2,
    borderColor: colors.ink,
    borderRadius: 12,
    boxShadow: '3px 3px 0 #151515',
    alignItems: 'center',
    justifyContent: 'center',
    transform: [{ rotate: '-3deg' }],
  },
  logoText: { fontSize: 26, fontWeight: '900' },
  brandName: { fontSize: 23, fontWeight: '900', color: colors.ink },
  muted: { color: colors.muted, fontSize: 13, lineHeight: 20 },
  badge: {
    alignSelf: 'flex-start',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderWidth: 1.5,
    borderColor: colors.ink,
    borderRadius: 8,
    backgroundColor: colors.soft,
  },
  eyebrow: { fontSize: 10, letterSpacing: 1.3, fontWeight: '800', color: colors.ink },
  workspace: { flexDirection: 'row', gap: 48, alignItems: 'flex-start' },
  stacked: { flexDirection: 'column-reverse', gap: 28 },
  intro: { flex: 1, gap: 24, paddingTop: 10 },
  introCompact: { width: '100%', flex: undefined },
  headline: {
    fontSize: 52,
    fontWeight: '900',
    letterSpacing: -2,
    color: colors.ink,
    lineHeight: 56,
  },
  introText: { fontSize: 17, lineHeight: 28, color: colors.muted, maxWidth: 400 },
  roadmapCard: {
    padding: 20,
    borderWidth: 2,
    borderColor: colors.ink,
    borderRadius: 14,
    backgroundColor: colors.paper,
    gap: 18,
  },
  step: { flexDirection: 'row', alignItems: 'center', gap: 14 },
  stepNumber: {
    fontSize: 17,
    fontWeight: '900',
    backgroundColor: colors.soft,
    padding: 9,
    borderRadius: 10,
    overflow: 'hidden',
  },
  future: { backgroundColor: colors.background, color: colors.muted },
  stepBody: { flex: 1, gap: 4 },
  stepTitle: { fontSize: 15, fontWeight: '800', color: colors.ink },
  divider: { height: 1, backgroundColor: '#dedbd1' },
  caption: { color: colors.muted, fontSize: 12, lineHeight: 19 },
  panel: {
    flex: 1.35,
    width: '100%',
    backgroundColor: colors.paper,
    borderWidth: 2,
    borderColor: colors.ink,
    borderRadius: 18,
    boxShadow: '5px 5px 0 #151515',
    overflow: 'hidden',
  },
  panelHeader: { padding: 24, borderBottomWidth: 2, borderColor: colors.ink, gap: 8 },
  panelTitle: { fontSize: 28, fontWeight: '900', letterSpacing: -0.8, color: colors.ink },
  panelBody: { padding: 24, gap: 12 },
  form: { gap: 12 },
  label: { fontSize: 13, fontWeight: '800', color: colors.ink },
  input: {
    borderWidth: 2,
    borderColor: colors.ink,
    borderRadius: 10,
    backgroundColor: '#fff',
    padding: 13,
    fontSize: 15,
    color: colors.ink,
    minHeight: 48,
  },
  composer: { minHeight: 104, textAlignVertical: 'top' },
  button: {
    borderWidth: 2,
    borderColor: colors.ink,
    backgroundColor: colors.orange,
    borderRadius: 10,
    paddingVertical: 12,
    paddingHorizontal: 16,
    minHeight: 44,
    alignItems: 'center',
    justifyContent: 'center',
    boxShadow: '2px 2px 0 #151515',
  },
  buttonText: { fontSize: 13, fontWeight: '800', color: colors.ink },
  secondary: { backgroundColor: colors.paper },
  disabled: { opacity: 0.45 },
  pressed: { transform: [{ translateX: 2 }, { translateY: 2 }], boxShadow: '0 0 0 #151515' },
  actions: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', gap: 12 },
  listHeader: {
    marginTop: 20,
    paddingBottom: 12,
    borderBottomWidth: 1,
    borderColor: '#dedbd1',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: 12,
  },
  empty: { paddingVertical: 28, gap: 8, alignItems: 'center' },
  emptyIcon: { fontSize: 36, color: colors.orange },
  record: {
    flexDirection: 'row',
    gap: 12,
    padding: 14,
    borderWidth: 1.5,
    borderColor: '#c5c1b7',
    borderRadius: 10,
    backgroundColor: '#f8f4e9',
  },
  recordDot: {
    width: 27,
    height: 27,
    backgroundColor: colors.green,
    borderWidth: 1.5,
    borderColor: colors.ink,
    borderRadius: 8,
    alignItems: 'center',
    justifyContent: 'center',
  },
  recordText: { fontSize: 15, lineHeight: 23, fontWeight: '700', color: colors.ink },
  spinner: { marginTop: 8 },
  error: {
    color: colors.red,
    fontSize: 13,
    lineHeight: 20,
    padding: 12,
    backgroundColor: '#ffe6df',
    borderRadius: 8,
  },
  notice: { color: '#245e37', fontSize: 13, paddingVertical: 8 },
  footer: {
    fontSize: 10,
    letterSpacing: 1.5,
    color: colors.muted,
    textAlign: 'center',
    marginTop: 20,
  },
});
