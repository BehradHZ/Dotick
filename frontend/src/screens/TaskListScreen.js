/**
 * Task list screen (§6 Stage 2 frontend: "Task list view showing all six
 * statuses with clear visual distinction" + "a visible way to trigger
 * Postpone All from the list view").
 *
 * All six statuses are rendered because the status grouping walks
 * `TASK_STATUS_ORDER` — including the two closed states — instead of
 * filtering to "active" tasks. A status the user never sees can't be
 * verified against the domain model, which is the whole point of this
 * stage's definition of done.
 *
 * "Postpone All" is honest about its scope: the backend touches OVERDUE
 * and MISSED only (`TaskManager.postpone_all`), so the button carries that
 * count and disables at zero rather than firing a POST that reports 0.
 */

import { useMemo, useState } from 'react';
import { Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';

import { countPostponable, groupTasks, GROUP_OPTIONS, SORT_OPTIONS } from '../domain/status';
import { palette, radius, space, typography } from '../theme/tokens';
import { Button, IconButton } from '../ui/Button';
import { Banner, EmptyState, GroupHeader, ScreenHeader } from '../ui/Chrome';
import { Segmented } from '../ui/Field';
import { TaskRow } from '../ui/Rows';

/** Inline "Postpone" pill on the Overdue/Missed group headers. */
function GroupPostponeAction({ onPress }) {
  return (
    <Pressable onPress={onPress} accessibilityRole="button" style={styles.groupAction}>
      <Text style={styles.groupActionText}>Postpone</Text>
    </Pressable>
  );
}

export default function TaskListScreen({
  tasks,
  loading,
  error,
  actionError,
  notice,
  actions,
  onOpenTask,
  onNewTask,
}) {
  const [groupBy, setGroupBy] = useState('status');
  const [sortBy, setSortBy] = useState('due');
  const [ascending, setAscending] = useState(true);
  const [showControls, setShowControls] = useState(false);
  const [collapsed, setCollapsed] = useState({});

  const groups = useMemo(
    () => groupTasks(tasks, { groupBy, sortBy, ascending }),
    [tasks, groupBy, sortBy, ascending]
  );
  const postponableCount = useMemo(() => countPostponable(tasks), [tasks]);

  const toggleGroup = (key) =>
    setCollapsed((prev) => ({ ...prev, [key]: !prev[key] }));

  /** Postpone every task in one group — same endpoint semantics, per row. */
  const postponeGroup = async (items) => {
    for (const task of items) {
      // Sequential on purpose: each row's postpone writes its own audit
      // log entry (§4.8) and the store refetches after each mutation, so
      // firing them in parallel would race the reload.
      await actions.postponeTask(task.id).catch(() => {});
    }
  };

  return (
    <View style={styles.screen}>
      <View style={styles.headerArea}>
        <ScreenHeader
          title="Tasks"
          meta={
            loading && !tasks.length
              ? 'Loading…'
              : `${tasks.length} task${tasks.length === 1 ? '' : 's'} · ${postponableCount} postponable`
          }
          actions={
            <>
              <IconButton
                name="sort"
                title="Group and sort"
                active={showControls}
                onPress={() => setShowControls((v) => !v)}
              />
              <IconButton name="refresh" title="Reload tasks" onPress={() => actions.load('tasks')} />
              <Button
                label={
                  postponableCount
                    ? `Postpone all (${postponableCount})`
                    : 'Postpone all'
                }
                icon="postpone"
                variant="soft"
                disabled={postponableCount === 0}
                onPress={actions.postponeAllTasks}
                accessibilityLabel="Postpone all overdue and missed tasks"
              />
              <Button label="New task" icon="plus" variant="primary" onPress={onNewTask} />
            </>
          }
        />

        {showControls ? (
          <View style={styles.controls}>
            <View style={styles.controlRow}>
              <Text style={styles.controlLabel}>Group by</Text>
              <Segmented options={GROUP_OPTIONS} value={groupBy} onChange={setGroupBy} />
            </View>
            <View style={styles.controlRow}>
              <Text style={styles.controlLabel}>Sort by</Text>
              <Segmented options={SORT_OPTIONS} value={sortBy} onChange={setSortBy} />
            </View>
            <View style={styles.controlRow}>
              <Text style={styles.controlLabel}>Direction</Text>
              <Segmented
                options={[
                  { key: 'asc', label: 'Ascending' },
                  { key: 'desc', label: 'Descending' },
                ]}
                value={ascending ? 'asc' : 'desc'}
                onChange={(key) => setAscending(key === 'asc')}
              />
            </View>
          </View>
        ) : null}

        <Banner tone="error" message={error} />
        <Banner tone="error" message={actionError} onDismiss={actions.clearMessages} />
        <Banner tone="notice" message={notice} onDismiss={actions.clearMessages} />
      </View>

      <ScrollView contentContainerStyle={styles.scrollContent}>
        {!groups.length ? (
          loading ? (
            <EmptyState message="Loading tasks…" />
          ) : (
            <EmptyState
              message="No tasks yet."
              hint="Create one to see the six statuses in action — set a due date in the past with the deadline switched on to watch it go Overdue, then Missed."
            />
          )
        ) : (
          groups.map((group) => {
            const isCollapsed = collapsed[group.key];
            const showPostpone =
              group.status === 'OVERDUE' || group.status === 'MISSED';
            return (
              <View key={group.key} style={styles.group}>
                <GroupHeader
                  title={group.title}
                  count={group.items.length}
                  status={group.status}
                  collapsed={isCollapsed}
                  onToggle={() => toggleGroup(group.key)}
                  action={
                    showPostpone ? (
                      <GroupPostponeAction onPress={() => postponeGroup(group.items)} />
                    ) : null
                  }
                />
                {isCollapsed
                  ? null
                  : group.items.map((task) => (
                      <TaskRow
                        key={task.id}
                        task={task}
                        onPress={() => onOpenTask(task)}
                        onToggleDone={() =>
                          actions.setTaskUserStatus(
                            task.id,
                            task.effective_status === 'DONE' ? null : 'DONE'
                          )
                        }
                      />
                    ))}
              </View>
            );
          })
        )}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1 },
  headerArea: { paddingHorizontal: space[6], paddingTop: space[5] },
  controls: {
    gap: space[3],
    padding: space[4],
    marginBottom: space[3],
    borderRadius: radius.md,
    backgroundColor: palette.surface,
    borderWidth: 1,
    borderColor: palette.border,
  },
  controlRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: space[3],
    flexWrap: 'wrap',
  },
  controlLabel: {
    width: 76,
    fontFamily: typography.fontFamily,
    fontSize: typography.size.sm,
    fontWeight: '600',
    color: palette.textSecondary,
  },
  scrollContent: { paddingHorizontal: space[6], paddingBottom: 110 },
  group: { marginBottom: space[5] },
  groupAction: {
    paddingVertical: 3,
    paddingHorizontal: 10,
    borderRadius: radius.pill,
    backgroundColor: palette.accentSoft,
  },
  groupActionText: {
    fontFamily: typography.fontFamily,
    fontSize: typography.size.xs,
    fontWeight: '700',
    color: palette.accentStrong,
  },
});
