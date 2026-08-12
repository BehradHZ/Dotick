/**
 * Today screen — the shell's default destination (the prototype's "Today").
 *
 * Everything here is derived from the same three collections the other
 * screens use; nothing is invented. It answers the two questions the
 * roadmap's definition of done implies you ask daily: what needs
 * attention now, and did any status transition happen since I last
 * looked.
 *
 * The Stage 1 health check lives at the bottom rather than in its own
 * destination: it stays useful (it's the first thing to check when the
 * lists come up empty) but it isn't a daily-driver view anymore.
 */

import { useMemo } from 'react';
import { ScrollView, StyleSheet, Text, View } from 'react-native';

import { apiBaseUrl } from '../api/client';
import { formatShortDate, parseIso } from '../domain/datetime';
import { countPostponable, statusColor, statusLabel, TASK_STATUS_ORDER } from '../domain/status';
import { palette, radius, space, typography } from '../theme/tokens';
import { Button } from '../ui/Button';
import { Banner, EmptyState, ScreenHeader } from '../ui/Chrome';
import { EventRow, RoutineRow, TaskRow } from '../ui/Rows';

function isToday(value) {
  const date = parseIso(value);
  if (!date) return false;
  const now = new Date();
  return (
    date.getFullYear() === now.getFullYear() &&
    date.getMonth() === now.getMonth() &&
    date.getDate() === now.getDate()
  );
}

/** One tile per status, so all six are visible at a glance. */
function StatusTiles({ tasks }) {
  const counts = useMemo(() => {
    const map = Object.fromEntries(TASK_STATUS_ORDER.map((s) => [s, 0]));
    for (const task of tasks) {
      if (map[task.effective_status] !== undefined) map[task.effective_status] += 1;
    }
    return map;
  }, [tasks]);

  return (
    <View style={styles.tiles}>
      {TASK_STATUS_ORDER.map((status) => (
        <View key={status} style={[styles.tile, { borderColor: statusColor(status) }]}>
          <Text style={[styles.tileCount, { color: statusColor(status) }]}>
            {counts[status]}
          </Text>
          <Text style={styles.tileLabel}>{statusLabel(status)}</Text>
        </View>
      ))}
    </View>
  );
}

function Section({ title, children }) {
  return (
    <View style={styles.section}>
      <Text style={styles.sectionTitle}>{title}</Text>
      {children}
    </View>
  );
}

export default function TodayScreen({
  tasks,
  events,
  routines,
  loading,
  actionError,
  notice,
  actions,
  onOpenTask,
}) {
  const attention = useMemo(
    () =>
      tasks.filter((task) =>
        ['OVERDUE', 'MISSED'].includes(task.effective_status)
      ),
    [tasks]
  );

  const dueToday = useMemo(
    () =>
      tasks.filter(
        (task) => task.effective_status === 'TODO' && isToday(task.due_date)
      ),
    [tasks]
  );

  const liveEvents = useMemo(
    () => events.filter((event) => event.status !== 'PAST').slice(0, 5),
    [events]
  );

  const openRoutines = useMemo(
    () => routines.filter((routine) => routine.status === 'TODO'),
    [routines]
  );

  const postponable = countPostponable(tasks);
  const today = new Date();
  const meta = `${formatShortDate(today.toISOString())} · ${tasks.length} tasks · ${events.length} events · ${routines.length} occurrences`;

  return (
    <View style={styles.screen}>
      <View style={styles.headerArea}>
        <ScreenHeader
          title="Today"
          meta={loading ? 'Loading…' : meta}
          actions={
            <>
              <Button label="Reload" icon="refresh" variant="secondary" onPress={actions.loadAll} />
              <Button
                label={postponable ? `Postpone all (${postponable})` : 'Postpone all'}
                icon="postpone"
                variant="soft"
                disabled={postponable === 0}
                onPress={actions.postponeAllTasks}
              />
            </>
          }
        />
        <Banner tone="error" message={actionError} onDismiss={actions.clearMessages} />
        <Banner tone="notice" message={notice} onDismiss={actions.clearMessages} />
      </View>

      <ScrollView contentContainerStyle={styles.scrollContent}>
        <StatusTiles tasks={tasks} />

        <Section title="Needs attention">
          {attention.length ? (
            attention.map((task) => (
              <TaskRow
                key={task.id}
                task={task}
                onPress={() => onOpenTask(task)}
                onToggleDone={() => actions.setTaskUserStatus(task.id, 'DONE')}
              />
            ))
          ) : (
            <Text style={styles.sectionEmpty}>Nothing overdue or missed.</Text>
          )}
        </Section>

        <Section title="Due today">
          {dueToday.length ? (
            dueToday.map((task) => (
              <TaskRow
                key={task.id}
                task={task}
                onPress={() => onOpenTask(task)}
                onToggleDone={() => actions.setTaskUserStatus(task.id, 'DONE')}
              />
            ))
          ) : (
            <Text style={styles.sectionEmpty}>No task is due today.</Text>
          )}
        </Section>

        <Section title="Events now and next">
          {liveEvents.length ? (
            liveEvents.map((event) => <EventRow key={event.id} event={event} onPress={() => {}} />)
          ) : (
            <Text style={styles.sectionEmpty}>No upcoming or ongoing events.</Text>
          )}
        </Section>

        <Section title="Open routine occurrences">
          {openRoutines.length ? (
            openRoutines.map((routine) => (
              <RoutineRow
                key={routine.id}
                routine={routine}
                onPress={() => {}}
                onToggleDone={() => actions.setRoutineUserStatus(routine.id, 'DONE')}
              />
            ))
          ) : (
            <Text style={styles.sectionEmpty}>Nothing open.</Text>
          )}
        </Section>

        {!tasks.length && !events.length && !routines.length && !loading ? (
          <EmptyState
            message="Nothing here yet."
            hint={`Backend: ${apiBaseUrl() || 'EXPO_PUBLIC_API_URL is not set'}`}
          />
        ) : (
          <Text style={styles.backendNote}>Backend: {apiBaseUrl() || 'not configured'}</Text>
        )}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1 },
  headerArea: { paddingHorizontal: space[6], paddingTop: space[5] },
  scrollContent: { paddingHorizontal: space[6], paddingBottom: 110 },
  tiles: { flexDirection: 'row', flexWrap: 'wrap', gap: space[2], marginBottom: space[5] },
  tile: {
    minWidth: 96,
    flexGrow: 1,
    paddingVertical: space[3],
    paddingHorizontal: space[3],
    borderRadius: radius.md,
    borderWidth: 1,
    backgroundColor: palette.surface,
  },
  tileCount: {
    fontFamily: typography.fontFamilyMono,
    fontSize: typography.size.lg,
    fontWeight: '700',
  },
  tileLabel: {
    fontFamily: typography.fontFamily,
    fontSize: typography.size.xs,
    color: palette.textSecondary,
    marginTop: 2,
  },
  section: { marginBottom: space[5] },
  sectionTitle: {
    fontFamily: typography.fontFamily,
    fontSize: typography.size.xs,
    fontWeight: '700',
    letterSpacing: 0.8,
    textTransform: 'uppercase',
    color: palette.textTertiary,
    marginBottom: space[2],
  },
  sectionEmpty: {
    fontFamily: typography.fontFamily,
    fontSize: typography.size.sm,
    color: palette.textTertiary,
    paddingVertical: space[2],
  },
  backendNote: {
    fontFamily: typography.fontFamilyMono,
    fontSize: typography.size.xs,
    color: palette.textTertiary,
    opacity: 0.7,
    marginTop: space[3],
  },
});
