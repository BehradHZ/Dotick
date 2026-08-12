import { useCallback, useEffect, useMemo, useState } from 'react';
import { StyleSheet, View } from 'react-native';
import { StatusBar } from 'expo-status-bar';

import { countPostponable } from './src/domain/status';
import EventListScreen from './src/screens/EventListScreen';
import RoutineListScreen from './src/screens/RoutineListScreen';
import TaskDetail from './src/screens/TaskDetail';
import TaskForm from './src/screens/TaskForm';
import TaskListScreen from './src/screens/TaskListScreen';
import TodayScreen from './src/screens/TodayScreen';
import { StoreProvider, useStore } from './src/state/store';
import { palette } from './src/theme/tokens';
import { AppShell, Dock, useIsNarrow, ViewRail } from './src/ui/AppShell';

/**
 * Stage 2 frontend (ROADMAP.md §6 Stage 2).
 *
 * Navigation is a single `screen` string rather than a router: Stage 2 has
 * four destinations and no deep-linking requirement, so React Navigation
 * would add a dependency and a native-linking configuration for something
 * one piece of state covers. Revisit if URL-addressable screens become a
 * real need (a Stage 5 concern, once lists exist to link to).
 */

const DOCK_ITEMS = [
  { key: 'today', label: 'Today', icon: 'home' },
  { key: 'tasks', label: 'Tasks', icon: 'checkbox' },
  { key: 'events', label: 'Events', icon: 'calendar' },
  { key: 'routines', label: 'Routines', icon: 'routine' },
];

function Dotick() {
  const { tasks, events, routines, actionError, notice, actions } = useStore();
  const narrow = useIsNarrow();

  const [screen, setScreen] = useState('today');
  const [selectedTask, setSelectedTask] = useState(null);
  const [taskFormFor, setTaskFormFor] = useState(null); // null | 'new' | task

  useEffect(() => {
    actions.loadAll();
  }, [actions]);

  /**
   * The selected task is looked up fresh from the store on every render
   * rather than held as a snapshot: a mutation refetches the collection,
   * and the detail panel has to show the *new* computed status (postpone a
   * MISSED task and its status must visibly change).
   */
  const liveSelectedTask = useMemo(
    () => (selectedTask ? tasks.items.find((t) => t.id === selectedTask.id) ?? null : null),
    [selectedTask, tasks.items]
  );

  const openTask = useCallback((task) => setSelectedTask(task), []);

  // Rail entries are real counts from loaded data — no placeholder numbers.
  const railViews = useMemo(
    () => [
      { key: 'today', label: 'Today', icon: 'calendar' },
      { key: 'tasks', label: 'All tasks', icon: 'list', count: tasks.items.length },
      {
        key: 'attention',
        label: 'Overdue & missed',
        icon: 'filter',
        count: countPostponable(tasks.items),
      },
      { key: 'events', label: 'Events', icon: 'calendar', count: events.items.length },
      { key: 'routines', label: 'Routines', icon: 'routine', count: routines.items.length },
    ],
    [tasks.items, events.items.length, routines.items.length]
  );

  const railCurrent = screen;

  const content = (() => {
    switch (screen) {
      case 'tasks':
      case 'attention':
        return (
          <TaskListScreen
            tasks={
              screen === 'attention'
                ? tasks.items.filter((t) =>
                    ['OVERDUE', 'MISSED'].includes(t.effective_status)
                  )
                : tasks.items
            }
            loading={tasks.loading}
            error={tasks.error}
            actionError={actionError}
            notice={notice}
            actions={actions}
            onOpenTask={openTask}
            onNewTask={() => setTaskFormFor('new')}
          />
        );
      case 'events':
        return (
          <EventListScreen
            events={events.items}
            loading={events.loading}
            error={events.error}
            actionError={actionError}
            actions={actions}
          />
        );
      case 'routines':
        return (
          <RoutineListScreen
            routines={routines.items}
            loading={routines.loading}
            error={routines.error}
            actionError={actionError}
            actions={actions}
          />
        );
      default:
        return (
          <TodayScreen
            tasks={tasks.items}
            events={events.items}
            routines={routines.items}
            loading={tasks.loading || events.loading || routines.loading}
            actionError={actionError}
            notice={notice}
            actions={actions}
            onOpenTask={openTask}
          />
        );
    }
  })();

  return (
    <View style={styles.root}>
      <StatusBar style="light" />
      <AppShell
        rail={
          <ViewRail
            views={railViews}
            current={railCurrent}
            onSelect={setScreen}
            narrow={narrow}
          />
        }
        dock={
          <Dock
            items={DOCK_ITEMS}
            current={screen === 'attention' ? 'tasks' : screen}
            onSelect={setScreen}
          />
        }
      >
        {content}
      </AppShell>

      <TaskDetail
        visible={Boolean(liveSelectedTask)}
        task={liveSelectedTask}
        onClose={() => setSelectedTask(null)}
        onEdit={() => {
          setTaskFormFor(liveSelectedTask);
          setSelectedTask(null);
        }}
        actions={actions}
      />

      {taskFormFor ? (
        <TaskForm
          visible
          task={taskFormFor === 'new' ? null : taskFormFor}
          onClose={() => setTaskFormFor(null)}
          actions={actions}
        />
      ) : null}
    </View>
  );
}

export default function App() {
  return (
    <StoreProvider>
      <Dotick />
    </StoreProvider>
  );
}

const styles = StyleSheet.create({
  root: { flex: 1, backgroundColor: palette.canvas1 },
});
