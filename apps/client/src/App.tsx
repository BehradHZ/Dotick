import { useMemo, useState } from 'react';
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
import {
  ApiError,
  type ApiSession,
  type ListRecord,
  type Task,
  type TaskStatus,
  defaultApiUrl,
  signIn as openSession,
} from './api';

const colors = {
  paper: '#fffdf7',
  background: '#f2eee3',
  ink: '#171717',
  muted: '#69675f',
  line: '#d2cec2',
  orange: '#ff7a00',
  soft: '#ffe2bf',
  green: '#d9f2df',
  red: '#b42318',
  redSoft: '#ffe5df',
};

type ViewName = 'tasks' | 'trash';

function Button({
  title,
  accessibilityLabel = title,
  onPress,
  disabled = false,
  secondary = false,
  danger = false,
  compact = false,
}: {
  title: string;
  accessibilityLabel?: string;
  onPress: () => void;
  disabled?: boolean;
  secondary?: boolean;
  danger?: boolean;
  compact?: boolean;
}) {
  return (
    <Pressable
      accessibilityRole="button"
      accessibilityLabel={accessibilityLabel}
      accessibilityState={{ disabled }}
      disabled={disabled}
      onPress={onPress}
      style={({ pressed }) => [
        styles.button,
        secondary && styles.buttonSecondary,
        danger && styles.buttonDanger,
        compact && styles.buttonCompact,
        disabled && styles.disabled,
        pressed && styles.pressed,
      ]}
    >
      <Text style={[styles.buttonText, danger && styles.dangerText]}>{title}</Text>
    </Pressable>
  );
}

function message(error: unknown) {
  if (error instanceof ApiError) return error.message;
  if (error instanceof Error && error.message.startsWith('Connection interrupted')) {
    return error.message;
  }
  return 'Could not complete the request. Please try again.';
}

function statusLabel(status: TaskStatus) {
  if (status === 'done') return 'Done';
  if (status === 'wont_do') return "Won't do";
  return 'To do';
}

function localTimezone() {
  try {
    return Intl.DateTimeFormat().resolvedOptions().timeZone || 'UTC';
  } catch {
    return 'UTC';
  }
}

export default function App() {
  const { width } = useWindowDimensions();
  const narrow = width < 760;
  const [apiUrl, setApiUrl] = useState(defaultApiUrl);
  const [email, setEmail] = useState('developer@example.test');
  const [password, setPassword] = useState('');
  const [session, setSession] = useState<ApiSession | null>(null);
  const [lists, setLists] = useState<ListRecord[]>([]);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [trash, setTrash] = useState<Task[]>([]);
  const [selectedListId, setSelectedListId] = useState('');
  const [view, setView] = useState<ViewName>('tasks');
  const [taskDraft, setTaskDraft] = useState('');
  const [listDraft, setListDraft] = useState('');
  const [editing, setEditing] = useState<Task | null>(null);
  const [editTitle, setEditTitle] = useState('');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');

  const selectedList = lists.find((list) => list.id === selectedListId) ?? lists[0];
  const visibleTasks = useMemo(
    () => tasks.filter((task) => task.column_id === selectedList?.default_column.id),
    [selectedList, tasks],
  );

  function clearFeedback() {
    setError('');
    setNotice('');
  }

  async function loadWorkspace(nextSession: ApiSession) {
    await nextSession.bootstrap(localTimezone());
    const [listResult, taskResult, trashResult] = await Promise.all([
      nextSession.lists(),
      nextSession.tasks(),
      nextSession.trash(),
    ]);
    setLists(listResult.results);
    setTasks(taskResult.results);
    setTrash(trashResult.results);
    setSelectedListId(
      listResult.results.find((list) => list.is_inbox)?.id ?? listResult.results[0]?.id ?? '',
    );
  }

  async function signIn() {
    if (busy || !email.trim() || !password || !apiUrl.trim()) return;
    clearFeedback();
    setBusy(true);
    try {
      const nextSession = await openSession(apiUrl, email.trim(), password);
      await loadWorkspace(nextSession);
      setSession(nextSession);
      setPassword('');
    } catch (failure) {
      setError(message(failure));
    } finally {
      setBusy(false);
    }
  }

  async function refresh() {
    if (!session || busy) return;
    clearFeedback();
    setBusy(true);
    try {
      await loadWorkspace(session);
      setNotice('Workspace refreshed.');
    } catch (failure) {
      setError(message(failure));
    } finally {
      setBusy(false);
    }
  }

  function signOut() {
    if (session) void session.logout().catch(() => undefined);
    setSession(null);
    setLists([]);
    setTasks([]);
    setTrash([]);
    setSelectedListId('');
    setTaskDraft('');
    setListDraft('');
    setEditing(null);
    setPassword('');
    clearFeedback();
  }

  async function createTask() {
    if (!session || !selectedList || !taskDraft.trim() || busy) return;
    clearFeedback();
    setBusy(true);
    try {
      const created = await session.createTask(taskDraft.trim(), selectedList.default_column.id);
      setTasks((current) => [created, ...current]);
      setTaskDraft('');
      setNotice('Task created.');
    } catch (failure) {
      setError(message(failure));
    } finally {
      setBusy(false);
    }
  }

  async function createList() {
    if (!session || !listDraft.trim() || busy) return;
    clearFeedback();
    setBusy(true);
    try {
      const created = await session.createList(listDraft.trim());
      setLists((current) => [...current, created]);
      setSelectedListId(created.id);
      setListDraft('');
      setView('tasks');
      setNotice('List created.');
    } catch (failure) {
      setError(message(failure));
    } finally {
      setBusy(false);
    }
  }

  function replaceTask(updated: Task) {
    setTasks((current) => current.map((task) => (task.id === updated.id ? updated : task)));
    setEditing((current) => (current?.id === updated.id ? updated : current));
  }

  async function updateTask(
    task: Task,
    change: { title?: string; status?: TaskStatus; column_id?: string },
  ) {
    if (!session || busy) return;
    clearFeedback();
    setBusy(true);
    try {
      const updated = await session.updateTask(task.id, { version: task.version, ...change });
      replaceTask(updated);
      setEditTitle(updated.title);
      setNotice('Task updated.');
    } catch (failure) {
      setError(message(failure));
    } finally {
      setBusy(false);
    }
  }

  async function trashTask(task: Task) {
    if (!session || busy) return;
    clearFeedback();
    setBusy(true);
    try {
      await session.trashTask(task.id, task.version);
      setTasks((current) => current.filter((record) => record.id !== task.id));
      setTrash((current) => [{ ...task, is_trashed: true }, ...current]);
      setEditing(null);
      setNotice('Task moved to Trash.');
    } catch (failure) {
      setError(message(failure));
    } finally {
      setBusy(false);
    }
  }

  async function restoreTask(task: Task) {
    if (!session || busy) return;
    clearFeedback();
    setBusy(true);
    try {
      const restored = await session.restoreTask(task.id, task.version);
      setTrash((current) => current.filter((record) => record.id !== task.id));
      setTasks((current) => [restored, ...current]);
      setNotice('Task restored.');
    } catch (failure) {
      setError(message(failure));
    } finally {
      setBusy(false);
    }
  }

  function selectForEdit(task: Task) {
    setEditing(task);
    setEditTitle(task.title);
  }

  if (!session) {
    return (
      <ScrollView style={styles.page} contentContainerStyle={styles.loginPage}>
        <View style={styles.brandRow}>
          <View style={styles.logo}>
            <Text style={styles.logoText}>✓</Text>
          </View>
          <View>
            <Text style={styles.brandName}>Dotick</Text>
            <Text style={styles.muted}>Turn loose thoughts into done work.</Text>
          </View>
        </View>
        <View style={[styles.loginLayout, narrow && styles.loginLayoutNarrow]}>
          <View style={styles.loginIntro}>
            <Text style={styles.eyebrow}>INCREMENT 1 · TASKS</Text>
            <Text accessibilityRole="header" style={[styles.hero, narrow && styles.heroNarrow]}>
              Clear head.{`\n`}Small steps.
            </Text>
            <Text style={styles.introText}>
              Capture tasks in Inbox, organize them in Lists, finish work, and recover mistakes from
              Trash.
            </Text>
          </View>
          <View style={styles.card}>
            <Text style={styles.eyebrow}>WELCOME BACK</Text>
            <Text accessibilityRole="header" style={styles.cardTitle}>
              Sign in
            </Text>
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
            <Text style={styles.label}>Password</Text>
            <TextInput
              accessibilityLabel="Password"
              value={password}
              onChangeText={setPassword}
              secureTextEntry
              autoComplete="current-password"
              editable={!busy}
              style={styles.input}
              onSubmitEditing={() => void signIn()}
            />
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
            <Button
              title="Sign in"
              disabled={busy || !email.trim() || !password || !apiUrl.trim()}
              onPress={() => void signIn()}
            />
            <Text style={styles.caption}>
              Credentials and tokens stay only in this open session.
            </Text>
            {busy && <ActivityIndicator accessibilityLabel="Working" color={colors.orange} />}
            {error !== '' && (
              <Text accessibilityRole="alert" style={styles.error}>
                {error}
              </Text>
            )}
          </View>
        </View>
      </ScrollView>
    );
  }

  return (
    <View style={styles.shell}>
      <View style={styles.topbar}>
        <View style={styles.brandRow}>
          <View style={styles.logoSmall}>
            <Text style={styles.logoTextSmall}>✓</Text>
          </View>
          <View>
            <Text style={styles.brandName}>Dotick</Text>
            <Text style={styles.caption}>{session.user.email}</Text>
          </View>
        </View>
        <View style={styles.actionRow}>
          <Button
            title="Refresh"
            secondary
            compact
            disabled={busy}
            onPress={() => void refresh()}
          />
          <Button title="Sign out" secondary compact onPress={signOut} />
        </View>
      </View>
      <View style={[styles.workspace, narrow && styles.workspaceNarrow]}>
        <ScrollView
          horizontal={narrow}
          style={[styles.sidebar, narrow && styles.sidebarNarrow]}
          contentContainerStyle={[styles.sidebarContent, narrow && styles.sidebarContentNarrow]}
        >
          <Text style={styles.eyebrow}>MY LISTS</Text>
          {lists.map((list) => (
            <Pressable
              key={list.id}
              accessibilityRole="button"
              accessibilityLabel={`Open ${list.title}`}
              onPress={() => {
                setSelectedListId(list.id);
                setView('tasks');
                setEditing(null);
              }}
              style={[
                styles.navItem,
                view === 'tasks' && selectedList?.id === list.id && styles.navItemActive,
              ]}
            >
              <Text style={styles.navIcon}>{list.is_inbox ? '⌂' : '•'}</Text>
              <Text style={styles.navText}>{list.title}</Text>
            </Pressable>
          ))}
          <Pressable
            accessibilityRole="button"
            accessibilityLabel="Open Trash"
            onPress={() => {
              setView('trash');
              setEditing(null);
            }}
            style={[styles.navItem, view === 'trash' && styles.navItemActive]}
          >
            <Text style={styles.navIcon}>⌫</Text>
            <Text style={styles.navText}>Trash ({trash.length})</Text>
          </Pressable>
          <View style={[styles.newList, narrow && styles.newListNarrow]}>
            <TextInput
              accessibilityLabel="New list"
              value={listDraft}
              onChangeText={setListDraft}
              placeholder="New list"
              maxLength={240}
              editable={!busy}
              style={[styles.input, styles.smallInput]}
            />
            <Button
              title="Add list"
              compact
              disabled={busy || !listDraft.trim()}
              onPress={() => void createList()}
            />
          </View>
        </ScrollView>

        <ScrollView style={styles.main} contentContainerStyle={styles.mainContent}>
          {view === 'tasks' && selectedList ? (
            <>
              <View style={styles.sectionHeader}>
                <View>
                  <Text style={styles.eyebrow}>{selectedList.is_inbox ? 'CAPTURE' : 'FOCUS'}</Text>
                  <Text accessibilityRole="header" style={styles.pageTitle}>
                    {selectedList.title}
                  </Text>
                </View>
                <View style={styles.countBadge}>
                  <Text style={styles.countText}>{visibleTasks.length}</Text>
                </View>
              </View>
              <View style={styles.composer}>
                <TextInput
                  accessibilityLabel="New task"
                  value={taskDraft}
                  onChangeText={setTaskDraft}
                  placeholder={`Add a task to ${selectedList.title}`}
                  maxLength={240}
                  editable={!busy}
                  style={[styles.input, styles.composerInput]}
                  onSubmitEditing={() => void createTask()}
                />
                <Button
                  title="Add task"
                  disabled={busy || !taskDraft.trim()}
                  onPress={() => void createTask()}
                />
              </View>
              {visibleTasks.length === 0 ? (
                <View style={styles.empty}>
                  <Text style={styles.emptyMark}>✦</Text>
                  <Text style={styles.cardTitle}>Nothing here yet.</Text>
                  <Text style={styles.muted}>Add one clear next action.</Text>
                </View>
              ) : (
                visibleTasks.map((task) => (
                  <View key={task.id} style={styles.taskCard}>
                    <Pressable
                      accessibilityRole="button"
                      accessibilityLabel={`Mark ${task.title} ${task.status === 'done' ? 'to do' : 'done'}`}
                      onPress={() =>
                        void updateTask(task, { status: task.status === 'done' ? 'todo' : 'done' })
                      }
                      style={[styles.checkbox, task.status === 'done' && styles.checkboxDone]}
                    >
                      <Text style={styles.checkboxText}>{task.status === 'done' ? '✓' : ''}</Text>
                    </Pressable>
                    <Pressable
                      accessibilityRole="button"
                      accessibilityLabel={`Edit ${task.title}`}
                      onPress={() => selectForEdit(task)}
                      style={styles.taskBody}
                    >
                      <Text
                        style={[styles.taskTitle, task.status !== 'todo' && styles.taskTitleDone]}
                      >
                        {task.title}
                      </Text>
                      <Text style={styles.caption}>{statusLabel(task.status)}</Text>
                    </Pressable>
                    <Button
                      title="Trash"
                      accessibilityLabel={`Trash ${task.title}`}
                      danger
                      compact
                      disabled={busy}
                      onPress={() => void trashTask(task)}
                    />
                  </View>
                ))
              )}
            </>
          ) : (
            <>
              <View style={styles.sectionHeader}>
                <View>
                  <Text style={styles.eyebrow}>RECOVERABLE FOR 30 DAYS</Text>
                  <Text accessibilityRole="header" style={styles.pageTitle}>
                    Trash
                  </Text>
                </View>
              </View>
              {trash.length === 0 ? (
                <View style={styles.empty}>
                  <Text style={styles.muted}>Trash is empty.</Text>
                </View>
              ) : (
                trash.map((task) => (
                  <View key={task.id} style={styles.taskCard}>
                    <View style={styles.taskBody}>
                      <Text style={styles.taskTitle}>{task.title}</Text>
                    </View>
                    <Button
                      title="Restore"
                      accessibilityLabel={`Restore ${task.title}`}
                      secondary
                      compact
                      disabled={busy}
                      onPress={() => void restoreTask(task)}
                    />
                  </View>
                ))
              )}
            </>
          )}
          {editing && narrow && (
            <View style={styles.mobileDetail}>
              <Text style={styles.eyebrow}>TASK DETAILS</Text>
              <Text style={styles.label}>Title</Text>
              <TextInput
                accessibilityLabel="Task title"
                value={editTitle}
                onChangeText={setEditTitle}
                maxLength={240}
                editable={!busy}
                style={[styles.input, styles.detailTitle]}
                multiline
              />
              <Button
                title="Save title"
                disabled={busy || !editTitle.trim() || editTitle.trim() === editing.title}
                onPress={() => void updateTask(editing, { title: editTitle.trim() })}
              />
              <Text style={styles.label}>Status</Text>
              <View style={styles.wrapRow}>
                {(['todo', 'done', 'wont_do'] as TaskStatus[]).map((status) => (
                  <Button
                    key={status}
                    title={statusLabel(status)}
                    secondary={editing.status !== status}
                    compact
                    disabled={busy || editing.status === status}
                    onPress={() => void updateTask(editing, { status })}
                  />
                ))}
              </View>
              <Text style={styles.label}>Move to</Text>
              <View style={styles.wrapRow}>
                {lists.map((list) => (
                  <Button
                    key={list.id}
                    title={`Move to ${list.title}`}
                    secondary
                    compact
                    disabled={busy || editing.column_id === list.default_column.id}
                    onPress={() => void updateTask(editing, { column_id: list.default_column.id })}
                  />
                ))}
              </View>
              <Button title="Close details" secondary compact onPress={() => setEditing(null)} />
            </View>
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
        </ScrollView>

        {editing && !narrow && (
          <ScrollView style={styles.detail} contentContainerStyle={styles.detailContent}>
            <Text style={styles.eyebrow}>TASK DETAILS</Text>
            <Text style={styles.label}>Title</Text>
            <TextInput
              accessibilityLabel="Task title"
              value={editTitle}
              onChangeText={setEditTitle}
              maxLength={240}
              editable={!busy}
              style={[styles.input, styles.detailTitle]}
              multiline
            />
            <Button
              title="Save title"
              disabled={busy || !editTitle.trim() || editTitle.trim() === editing.title}
              onPress={() => void updateTask(editing, { title: editTitle.trim() })}
            />
            <Text style={styles.label}>Status</Text>
            <View style={styles.wrapRow}>
              {(['todo', 'done', 'wont_do'] as TaskStatus[]).map((status) => (
                <Button
                  key={status}
                  title={statusLabel(status)}
                  secondary={editing.status !== status}
                  compact
                  disabled={busy || editing.status === status}
                  onPress={() => void updateTask(editing, { status })}
                />
              ))}
            </View>
            <Text style={styles.label}>Move to</Text>
            <View style={styles.wrapRow}>
              {lists.map((list) => (
                <Button
                  key={list.id}
                  title={`Move to ${list.title}`}
                  secondary
                  compact
                  disabled={busy || editing.column_id === list.default_column.id}
                  onPress={() => void updateTask(editing, { column_id: list.default_column.id })}
                />
              ))}
            </View>
            <Button title="Close details" secondary compact onPress={() => setEditing(null)} />
          </ScrollView>
        )}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: colors.background },
  loginPage: {
    flexGrow: 1,
    width: '100%',
    maxWidth: 1120,
    alignSelf: 'center',
    padding: 24,
    gap: 56,
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
  logoSmall: {
    width: 38,
    height: 38,
    borderWidth: 2,
    borderColor: colors.ink,
    borderRadius: 10,
    backgroundColor: colors.orange,
    alignItems: 'center',
    justifyContent: 'center',
  },
  logoTextSmall: { fontSize: 20, fontWeight: '900' },
  brandName: { color: colors.ink, fontSize: 22, fontWeight: '900' },
  muted: { color: colors.muted, fontSize: 13, lineHeight: 20 },
  caption: { color: colors.muted, fontSize: 11, lineHeight: 17 },
  eyebrow: { color: colors.ink, fontSize: 10, fontWeight: '900', letterSpacing: 1.4 },
  loginLayout: { flexDirection: 'row', alignItems: 'center', gap: 64 },
  loginLayoutNarrow: { flexDirection: 'column', alignItems: 'stretch', gap: 28 },
  loginIntro: { flex: 1, gap: 18 },
  hero: { color: colors.ink, fontSize: 58, lineHeight: 62, letterSpacing: -2.5, fontWeight: '900' },
  heroNarrow: { fontSize: 44, lineHeight: 48 },
  introText: { color: colors.muted, fontSize: 17, lineHeight: 28, maxWidth: 470 },
  card: {
    flex: 1,
    width: '100%',
    maxWidth: 470,
    backgroundColor: colors.paper,
    borderWidth: 2,
    borderColor: colors.ink,
    borderRadius: 18,
    padding: 24,
    gap: 12,
    boxShadow: '5px 5px 0 #171717',
  },
  cardTitle: { color: colors.ink, fontSize: 25, fontWeight: '900', letterSpacing: -0.5 },
  label: { color: colors.ink, fontSize: 12, fontWeight: '800', marginTop: 4 },
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
  button: {
    minHeight: 44,
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
  buttonSecondary: { backgroundColor: colors.paper },
  buttonDanger: { backgroundColor: colors.redSoft, borderColor: colors.red, boxShadow: 'none' },
  buttonCompact: { minHeight: 36, paddingHorizontal: 11, paddingVertical: 7 },
  buttonText: { color: colors.ink, fontSize: 12, fontWeight: '900' },
  dangerText: { color: colors.red },
  disabled: { opacity: 0.45 },
  pressed: { transform: [{ translateX: 1 }, { translateY: 1 }], boxShadow: 'none' },
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
  },
  shell: { flex: 1, backgroundColor: colors.background },
  topbar: {
    minHeight: 70,
    paddingHorizontal: 20,
    paddingVertical: 12,
    backgroundColor: colors.paper,
    borderBottomWidth: 2,
    borderColor: colors.ink,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    gap: 12,
  },
  actionRow: { flexDirection: 'row', alignItems: 'center', gap: 9 },
  workspace: { flex: 1, flexDirection: 'row' },
  workspaceNarrow: { flexDirection: 'column' },
  sidebar: {
    width: 230,
    flexGrow: 0,
    backgroundColor: colors.paper,
    borderRightWidth: 2,
    borderColor: colors.ink,
  },
  sidebarNarrow: { width: '100%', maxHeight: 118, borderRightWidth: 0, borderBottomWidth: 2 },
  sidebarContent: { padding: 16, gap: 9 },
  sidebarContentNarrow: { flexDirection: 'row', alignItems: 'center', minWidth: '100%' },
  navItem: {
    minHeight: 42,
    borderWidth: 1.5,
    borderColor: 'transparent',
    borderRadius: 9,
    paddingHorizontal: 10,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 9,
  },
  navItemActive: { borderColor: colors.ink, backgroundColor: colors.soft },
  navIcon: { width: 20, color: colors.ink, fontWeight: '900', fontSize: 17 },
  navText: { color: colors.ink, fontWeight: '800', fontSize: 13 },
  newList: { marginTop: 10, gap: 8 },
  newListNarrow: { marginTop: 0, flexDirection: 'row', alignItems: 'center' },
  smallInput: { minHeight: 40, flex: 1, minWidth: 100 },
  main: { flex: 1 },
  mainContent: { width: '100%', maxWidth: 760, alignSelf: 'center', padding: 22, gap: 12 },
  sectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: 16,
    marginBottom: 4,
  },
  pageTitle: {
    color: colors.ink,
    fontSize: 34,
    lineHeight: 40,
    fontWeight: '900',
    letterSpacing: -1,
  },
  countBadge: {
    width: 38,
    height: 38,
    borderWidth: 2,
    borderColor: colors.ink,
    borderRadius: 12,
    backgroundColor: colors.soft,
    alignItems: 'center',
    justifyContent: 'center',
  },
  countText: { fontWeight: '900', color: colors.ink },
  composer: { flexDirection: 'row', alignItems: 'stretch', gap: 9, marginBottom: 8 },
  composerInput: { flex: 1 },
  taskCard: {
    minHeight: 66,
    backgroundColor: colors.paper,
    borderWidth: 1.5,
    borderColor: colors.ink,
    borderRadius: 12,
    padding: 11,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 11,
  },
  checkbox: {
    width: 28,
    height: 28,
    borderWidth: 2,
    borderColor: colors.ink,
    borderRadius: 8,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#fff',
  },
  checkboxDone: { backgroundColor: colors.green },
  checkboxText: { color: colors.ink, fontWeight: '900' },
  taskBody: { flex: 1, gap: 3 },
  taskTitle: { color: colors.ink, fontSize: 15, lineHeight: 21, fontWeight: '800' },
  taskTitleDone: { color: colors.muted, textDecorationLine: 'line-through' },
  empty: { paddingVertical: 50, alignItems: 'center', gap: 8 },
  emptyMark: { color: colors.orange, fontSize: 38 },
  spinner: { marginTop: 8 },
  detail: {
    width: 310,
    flexGrow: 0,
    backgroundColor: colors.paper,
    borderLeftWidth: 2,
    borderColor: colors.ink,
  },
  mobileDetail: {
    marginTop: 14,
    padding: 16,
    gap: 12,
    backgroundColor: colors.paper,
    borderWidth: 2,
    borderColor: colors.ink,
    borderRadius: 14,
  },
  detailContent: { padding: 18, gap: 12 },
  detailTitle: { minHeight: 90, textAlignVertical: 'top' },
  wrapRow: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
});
