import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import {
  ActivityIndicator,
  AppState,
  Platform,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
} from 'react-native';

import AuthScreen from './AuthScreen';
import {
  type ApiSession,
  ApiError,
  type Bootstrap,
  createOperationId,
  type ListRecord,
  ReauthenticationRequiredError,
  type Task,
  type TaskStatus,
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
  const [listDraft, setListDraft] = useState('');
  const [listTitleDraft, setListTitleDraft] = useState('');
  const listCreateAttempt = useRef<{ intent: string; operationId: string } | null>(null);
  const [taskDraft, setTaskDraft] = useState('');
  const taskCreateAttempt = useRef<{ intent: string; operationId: string } | null>(null);
  const [editingTaskId, setEditingTaskId] = useState<string | null>(null);
  const [taskTitleDraft, setTaskTitleDraft] = useState('');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');

  const clearWorkspace = useCallback(() => {
    setBootstrap(null);
    setLists([]);
    setTasks([]);
    setSelectedListId('');
    setListDraft('');
    setListTitleDraft('');
    listCreateAttempt.current = null;
    setTaskDraft('');
    taskCreateAttempt.current = null;
    setEditingTaskId(null);
    setTaskTitleDraft('');
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

  useEffect(() => {
    setListTitleDraft(selectedList?.title ?? '');
  }, [selectedList?.id, selectedList?.title, selectedList?.version]);

  function changeListDraft(value: string) {
    setListDraft(value);
    const nextIntent = value.trim();
    if (listCreateAttempt.current && listCreateAttempt.current.intent !== nextIntent) listCreateAttempt.current = null;
  }

  async function createList() {
    const intent = listDraft.trim();
    if (!session || !intent || busy) return;
    if (!listCreateAttempt.current || listCreateAttempt.current.intent !== intent) {
      listCreateAttempt.current = { intent, operationId: createOperationId() };
    }
    const operationId = listCreateAttempt.current.operationId;
    setBusy(true);
    setError('');
    try {
      const created = await session.createList({ title: intent, operation_id: operationId });
      setLists((current) => [...current.filter((list) => list.id !== created.id), created]);
      setSelectedListId(created.id);
      setListDraft('');
      listCreateAttempt.current = null;
    } catch (failure) {
      if (failure instanceof ApiError && failure.code === 'idempotency_conflict') listCreateAttempt.current = null;
      if (!handleSessionFailure(failure)) setError(errorMessage(failure));
    } finally {
      setBusy(false);
    }
  }

  async function renameSelectedList() {
    const title = listTitleDraft.trim();
    if (!session || !selectedList || selectedList.is_inbox || !title || title === selectedList.title || busy) return;
    setBusy(true);
    setError('');
    try {
      const updated = await session.updateList(selectedList.id, { version: selectedList.version, title });
      setLists((current) => current.map((list) => list.id === updated.id ? updated : list));
    } catch (failure) {
      if (failure instanceof ApiError && failure.code === 'version_conflict') {
        await loadWorkspace(session, selectedList.id);
        setError(failure.message);
      } else if (!handleSessionFailure(failure)) {
        setError(errorMessage(failure));
      }
    } finally {
      setBusy(false);
    }
  }

  function replaceTask(updated: Task) {
    setTasks((current) => current.map((task) => task.id === updated.id ? updated : task));
  }

  function changeTaskDraft(value: string) {
    setTaskDraft(value);
    const columnId = selectedList?.default_column.id ?? '';
    const nextIntent = `${columnId}::${value.trim()}`;
    if (taskCreateAttempt.current && taskCreateAttempt.current.intent !== nextIntent) taskCreateAttempt.current = null;
  }

  async function createTask() {
    const title = taskDraft.trim();
    const columnId = selectedList?.default_column.id;
    if (!session || !columnId || !title || busy) return;
    const intent = `${columnId}::${title}`;
    if (!taskCreateAttempt.current || taskCreateAttempt.current.intent !== intent) {
      taskCreateAttempt.current = { intent, operationId: createOperationId() };
    }
    setBusy(true);
    setError('');
    try {
      const created = await session.createTask({ title, column_id: columnId, operation_id: taskCreateAttempt.current.operationId });
      setTasks((current) => [created, ...current.filter((task) => task.id !== created.id)]);
      setTaskDraft('');
      taskCreateAttempt.current = null;
    } catch (failure) {
      if (failure instanceof ApiError && failure.code === 'idempotency_conflict') taskCreateAttempt.current = null;
      if (!handleSessionFailure(failure)) setError(errorMessage(failure));
    } finally {
      setBusy(false);
    }
  }

  async function updateTask(task: Task, change: { title?: string; status?: TaskStatus }) {
    if (!session || busy) return;
    setBusy(true);
    setError('');
    try {
      const updated = await session.updateTask(task.id, { version: task.version, ...change });
      replaceTask(updated);
      if (editingTaskId === task.id) {
        setTaskTitleDraft(updated.title);
        setEditingTaskId(null);
      }
    } catch (failure) {
      if (!handleSessionFailure(failure)) setError(errorMessage(failure));
    } finally {
      setBusy(false);
    }
  }

  if (!session) {
    return <AuthScreen onAuthenticated={async (nextSession) => {
      setBusy(true);
      try { await loadWorkspace(nextSession); setSession(nextSession); } finally { setBusy(false); }
    }} />;
  }

  return (
    <View style={styles.page}>
      <View style={styles.topbar}>
        <View><Text style={styles.brand}>Dotick</Text><Text style={styles.muted}>{session.user.email}</Text></View>
        <View style={styles.topActions}>
          <Action title="Reload server state" disabled={busy} onPress={() => void reloadWorkspace(session)} />
          <Action title="Sign out" disabled={busy} onPress={() => { void session.signOut().catch(() => undefined).finally(() => { setSession(null); clearWorkspace(); }); }} />
        </View>
      </View>
      <ScrollView contentContainerStyle={styles.content}>
        <View style={styles.sidebar}>
          <Text style={styles.eyebrow}>LISTS</Text>
          {lists.map((list) => (
            <Pressable key={list.id} accessibilityRole="button" accessibilityLabel={`Open ${list.title}`} onPress={() => setSelectedListId(list.id)} style={[styles.listItem, selectedListId === list.id && styles.listItemActive]}>
              <Text style={styles.listItemText}>{list.is_inbox ? '⌂ ' : ''}{list.title}</Text>
            </Pressable>
          ))}
          <TextInput accessibilityLabel="New list" value={listDraft} onChangeText={changeListDraft} placeholder="New list" maxLength={240} editable={!busy} style={styles.input} />
          <Action title="Add list" disabled={busy || !listDraft.trim()} onPress={() => void createList()} />
          <Text style={styles.muted}>Timezone: {bootstrap?.preferences.timezone ?? '—'}</Text>
        </View>
        <View style={styles.main}>
          <Text accessibilityRole="header" style={styles.title}>{selectedList?.title ?? bootstrap?.inbox.title ?? 'Inbox'}</Text>
          <Text style={styles.muted}>{selectedTasks.length} {selectedTasks.length === 1 ? 'task' : 'tasks'} loaded from the server</Text>
          <View style={styles.composerRow}>
            <TextInput accessibilityLabel="New task" value={taskDraft} onChangeText={changeTaskDraft} placeholder="Add a task" maxLength={240} editable={!busy} style={[styles.input, styles.flexInput]} />
            <Action title="Add task" disabled={busy || !taskDraft.trim() || !selectedList} onPress={() => void createTask()} />
          </View>
          {!selectedList?.is_inbox && selectedList && (
            <View style={styles.inlineEditor}>
              <TextInput accessibilityLabel="List title" value={listTitleDraft} onChangeText={setListTitleDraft} maxLength={240} editable={!busy} style={[styles.input, styles.flexInput]} />
              <Action title="Rename list" disabled={busy || !listTitleDraft.trim() || listTitleDraft.trim() === selectedList.title} onPress={() => void renameSelectedList()} />
            </View>
          )}
          {selectedTasks.length === 0 ? (
            <View style={styles.placeholder}><Text style={styles.placeholderTitle}>No tasks here yet.</Text><Text style={styles.muted}>Create the first Task for this List.</Text></View>
          ) : selectedTasks.map((task) => (
            <View key={task.id} style={styles.taskCard}>
              {editingTaskId === task.id ? (
                <View style={styles.inlineEditor}>
                  <TextInput accessibilityLabel="Task title" value={taskTitleDraft} onChangeText={setTaskTitleDraft} maxLength={240} editable={!busy} style={[styles.input, styles.flexInput]} />
                  <Action title="Save task" disabled={busy || !taskTitleDraft.trim() || taskTitleDraft.trim() === task.title} onPress={() => void updateTask(task, { title: taskTitleDraft.trim() })} />
                </View>
              ) : (
                <View style={styles.taskHeader}>
                  <View style={styles.flexInput}><Text style={styles.taskTitle}>{task.title}</Text><Text style={styles.muted}>{task.status === 'wont_do' ? "Won't do" : task.status === 'done' ? 'Done' : 'Todo'}</Text></View>
                  <Action title={`Edit ${task.title}`} disabled={busy} onPress={() => { setEditingTaskId(task.id); setTaskTitleDraft(task.title); }} />
                </View>
              )}
              <View style={styles.statusRow}>
                <Action title={`Mark ${task.title} Todo`} disabled={busy || task.status === 'todo'} onPress={() => void updateTask(task, { status: 'todo' })} />
                <Action title={`Mark ${task.title} Done`} disabled={busy || task.status === 'done'} onPress={() => void updateTask(task, { status: 'done' })} />
                <Action title={`Mark ${task.title} Won't do`} disabled={busy || task.status === 'wont_do'} onPress={() => void updateTask(task, { status: 'wont_do' })} />
              </View>
            </View>
          ))}
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
  title: { fontSize: 30, fontWeight: '900', color: colors.ink },
  placeholder: { marginTop: 14, padding: 18, gap: 8, borderWidth: 1.5, borderColor: '#cfc9bb', borderRadius: 12, backgroundColor: '#f8f4e9' },
  placeholderTitle: { fontSize: 15, fontWeight: '800', color: colors.ink },
  listItem: { minHeight: 38, justifyContent: 'center', paddingHorizontal: 10, borderRadius: 8 },
  listItemActive: { backgroundColor: '#ffe2bf' },
  listItemText: { fontSize: 13, fontWeight: '800', color: colors.ink },
  input: { minHeight: 42, paddingHorizontal: 10, borderWidth: 1.5, borderColor: colors.ink, borderRadius: 8, backgroundColor: '#fff', color: colors.ink },
  inlineEditor: { flexDirection: 'row', gap: 8, alignItems: 'center' },
  composerRow: { flexDirection: 'row', gap: 8, alignItems: 'center' },
  flexInput: { flex: 1 },
  taskCard: { padding: 12, gap: 10, borderWidth: 1.5, borderColor: '#cfc9bb', borderRadius: 10, backgroundColor: '#f8f4e9' },
  taskHeader: { flexDirection: 'row', gap: 8, alignItems: 'center' },
  taskTitle: { fontSize: 15, fontWeight: '800', color: colors.ink },
  statusRow: { flexDirection: 'row', gap: 6, flexWrap: 'wrap' },
  action: { minHeight: 38, paddingHorizontal: 12, justifyContent: 'center', borderWidth: 1.5, borderColor: colors.ink, borderRadius: 9, backgroundColor: colors.paper },
  actionText: { fontSize: 12, fontWeight: '800', color: colors.ink },
  disabled: { opacity: 0.45 },
  error: { padding: 10, borderRadius: 8, color: colors.red, backgroundColor: colors.redSoft },
});
