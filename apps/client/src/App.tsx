import { useCallback, useEffect, useMemo, useState } from 'react';
import {
  ActivityIndicator,
  AppState,
  Platform,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  View,
} from 'react-native';

import AuthScreen from './AuthScreen';
import {
  type ApiSession,
  type Bootstrap,
  type ListRecord,
  ReauthenticationRequiredError,
  type Task,
} from './api';

const colors = {
  paper: '#fffdf7',
  background: '#f2eee3',
  ink: '#171717',
  muted: '#69675f',
  orange: '#ff7a00',
  red: '#b42318',
  redSoft: '#ffe5df',
};

function localTimezone() {
  try {
    return Intl.DateTimeFormat().resolvedOptions().timeZone || 'UTC';
  } catch {
    return 'UTC';
  }
}

function errorMessage(error: unknown) {
  if (error instanceof ReauthenticationRequiredError) return error.message;
  if (error instanceof Error) return error.message;
  return 'Could not load your workspace. Please try again.';
}

function Action({ title, onPress, disabled = false }: { title: string; onPress: () => void; disabled?: boolean }) {
  return (
    <Pressable accessibilityRole="button" accessibilityLabel={title} accessibilityState={{ disabled }} disabled={disabled} onPress={onPress} style={[styles.action, disabled && styles.disabled]}>
      <Text style={styles.actionText}>{title}</Text>
    </Pressable>
  );
}

export default function App() {
  const [session, setSession] = useState<ApiSession | null>(null);
  const [bootstrap, setBootstrap] = useState<Bootstrap | null>(null);
  const [lists, setLists] = useState<ListRecord[]>([]);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [selectedListId, setSelectedListId] = useState('');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');

  const clearWorkspace = useCallback(() => {
    setBootstrap(null);
    setLists([]);
    setTasks([]);
    setSelectedListId('');
    setError('');
  }, []);

  const loadWorkspace = useCallback(async (activeSession: ApiSession, preferredListId?: string) => {
    const nextBootstrap = await activeSession.bootstrap(localTimezone());
    const [listResult, taskResult] = await Promise.all([activeSession.lists(), activeSession.tasks()]);
    setBootstrap(nextBootstrap);
    setLists(listResult.results);
    setTasks(taskResult.results);
    setSelectedListId((current) => {
      const requested = preferredListId ?? current;
      if (requested && listResult.results.some((list) => list.id === requested)) return requested;
      if (listResult.results.some((list) => list.id === nextBootstrap.inbox.id)) return nextBootstrap.inbox.id;
      return listResult.results[0]?.id ?? '';
    });
    setError('');
  }, []);

  const handleSessionFailure = useCallback((failure: unknown) => {
    if (failure instanceof ReauthenticationRequiredError) {
      setSession(null);
      clearWorkspace();
      return true;
    }
    return false;
  }, [clearWorkspace]);

  const reloadWorkspace = useCallback(async (activeSession: ApiSession) => {
    if (busy) return;
    setBusy(true);
    try {
      await loadWorkspace(activeSession);
    } catch (failure) {
      if (!handleSessionFailure(failure)) setError(errorMessage(failure));
    } finally {
      setBusy(false);
    }
  }, [busy, handleSessionFailure, loadWorkspace]);

  useEffect(() => {
    if (!session) return undefined;
    const unregister = session.onPrivateStateClear(() => {
      setSession(null);
      clearWorkspace();
    });
    return () => { unregister(); };
  }, [clearWorkspace, session]);

  useEffect(() => {
    if (!session) return undefined;
    let previous = AppState.currentState;
    const subscription = AppState.addEventListener('change', (next) => {
      const returning = previous !== 'active' && next === 'active';
      previous = next;
      if (returning) void reloadWorkspace(session);
    });
    return () => subscription.remove();
  }, [reloadWorkspace, session]);

  useEffect(() => {
    if (!session || Platform.OS !== 'web' || typeof window === 'undefined') return undefined;
    const onFocus = () => void reloadWorkspace(session);
    window.addEventListener('focus', onFocus);
    return () => window.removeEventListener('focus', onFocus);
  }, [reloadWorkspace, session]);

  const selectedList = useMemo(() => lists.find((list) => list.id === selectedListId) ?? null, [lists, selectedListId]);
  const selectedColumnId = selectedList?.default_column.id ?? bootstrap?.inbox.default_column.id;
  const selectedTasks = useMemo(() => selectedColumnId ? tasks.filter((task) => task.column_id === selectedColumnId) : [], [selectedColumnId, tasks]);

  if (!session) {
    return <AuthScreen onAuthenticated={async (nextSession) => {
      setBusy(true);
      try {
        await loadWorkspace(nextSession);
        setSession(nextSession);
      } finally {
        setBusy(false);
      }
    }} />;
  }

  return (
    <View style={styles.page}>
      <View style={styles.topbar}>
        <View><Text style={styles.brand}>Dotick</Text><Text style={styles.muted}>{session.user.email}</Text></View>
        <View style={styles.topActions}>
          <Action title="Reload server state" disabled={busy} onPress={() => void reloadWorkspace(session)} />
          <Action title="Sign out" disabled={busy} onPress={() => {
            void session.signOut().catch(() => undefined).finally(() => { setSession(null); clearWorkspace(); });
          }} />
        </View>
      </View>
      <ScrollView contentContainerStyle={styles.content}>
        <View style={styles.sidebar}>
          <Text style={styles.eyebrow}>INCREMENT 1 WORKSPACE</Text>
          <Text style={styles.sectionTitle}>Inbox</Text>
          <Text style={styles.muted}>{lists.length} {lists.length === 1 ? 'list' : 'lists'} loaded from the server</Text>
          <Text style={styles.muted}>Timezone: {bootstrap?.preferences.timezone ?? '—'}</Text>
        </View>
        <View style={styles.main}>
          <Text accessibilityRole="header" style={styles.title}>{selectedList?.title ?? bootstrap?.inbox.title ?? 'Inbox'}</Text>
          <Text style={styles.muted}>{selectedTasks.length} {selectedTasks.length === 1 ? 'task' : 'tasks'} loaded from the server</Text>
          <View style={styles.placeholder}>
            <Text style={styles.placeholderTitle}>Your I1 workspace is connected.</Text>
            <Text style={styles.muted}>Lists and Tasks are reloaded from the API on authentication, manual refresh, and app re-entry.</Text>
          </View>
          {busy && <ActivityIndicator accessibilityLabel="Working" color={colors.orange} />}
          {error !== '' && <Text accessibilityRole="alert" style={styles.error}>{error}</Text>}
        </View>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: colors.background },
  topbar: { minHeight: 72, paddingHorizontal: 20, paddingVertical: 14, borderBottomWidth: 2, borderColor: colors.ink, backgroundColor: colors.paper, flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', gap: 12 },
  brand: { fontSize: 22, fontWeight: '900', color: colors.ink },
  muted: { color: colors.muted, fontSize: 12, lineHeight: 18 },
  topActions: { flexDirection: 'row', gap: 8, flexWrap: 'wrap', justifyContent: 'flex-end' },
  content: { flexGrow: 1, width: '100%', maxWidth: 1180, alignSelf: 'center', padding: 20, gap: 20, flexDirection: 'row', alignItems: 'flex-start' },
  sidebar: { width: 250, padding: 18, gap: 10, borderWidth: 2, borderColor: colors.ink, borderRadius: 14, backgroundColor: colors.paper },
  main: { flex: 1, minHeight: 360, padding: 22, gap: 14, borderWidth: 2, borderColor: colors.ink, borderRadius: 14, backgroundColor: colors.paper },
  eyebrow: { fontSize: 10, fontWeight: '900', letterSpacing: 1.2, color: colors.ink },
  sectionTitle: { fontSize: 18, fontWeight: '900', color: colors.ink },
  title: { fontSize: 30, fontWeight: '900', color: colors.ink },
  placeholder: { marginTop: 14, padding: 18, gap: 8, borderWidth: 1.5, borderColor: '#cfc9bb', borderRadius: 12, backgroundColor: '#f8f4e9' },
  placeholderTitle: { fontSize: 15, fontWeight: '800', color: colors.ink },
  action: { minHeight: 38, paddingHorizontal: 12, justifyContent: 'center', borderWidth: 1.5, borderColor: colors.ink, borderRadius: 9, backgroundColor: colors.paper },
  actionText: { fontSize: 12, fontWeight: '800', color: colors.ink },
  disabled: { opacity: 0.45 },
  error: { padding: 10, borderRadius: 8, color: colors.red, backgroundColor: colors.redSoft },
});
