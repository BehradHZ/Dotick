/**
 * List rows for the three entity types.
 *
 * The prototype's `.task-row` (52px, status-coloured circular checkbox,
 * title, right-aligned date) is the shape all three follow, so a row
 * reads the same whether it's a task, an event, or a routine occurrence.
 *
 * The checkbox is the primary status affordance and it is a real control:
 * tapping it sets `user_status` (§4.3 / §4.6). Tapping the rest of the row
 * opens the detail panel. Events have no checkbox — they are never
 * "completed" (§4.5) — so their row shows a status dot instead.
 */

import { Pressable, StyleSheet, Text, View } from 'react-native';

import { density, palette, radius, space, typography } from '../theme/tokens';
import { formatShortDate } from '../domain/datetime';
import { isResolved, statusColor, statusLabel } from '../domain/status';
import Icon from './Icon';
import { StatusDot } from './Chrome';

/**
 * Circular status checkbox. Cycles NULL → DONE → NULL on tap; the
 * Won't Do side is set from the detail panel, since a single tap can't
 * express three states unambiguously.
 */
function StatusCheckbox({ status, onPress, label }) {
  const done = status === 'DONE';
  const wontDo = status === 'WONT_DO' || status === 'AUTO_WONT_DO';
  const color = statusColor(status);

  return (
    <Pressable
      onPress={onPress}
      accessibilityRole="checkbox"
      accessibilityLabel={label}
      accessibilityState={{ checked: done }}
      hitSlop={8}
      style={[
        styles.checkbox,
        { borderColor: color },
        (done || wontDo) && { backgroundColor: color },
      ]}
    >
      {done ? <Icon name="check" size={11} color="#0d1a10" strokeWidth={3} /> : null}
      {wontDo ? <Icon name="close" size={10} color={palette.canvas1} strokeWidth={3} /> : null}
    </Pressable>
  );
}

export function TaskRow({ task, onPress, onToggleDone }) {
  const status = task.effective_status;
  const muted = isResolved(status);
  const dateColor =
    status === 'MISSED' || status === 'OVERDUE'
      ? statusColor(status)
      : formatShortDate(task.due_date) === 'Today'
        ? palette.accentStrong
        : palette.textTertiary;

  return (
    <Pressable
      onPress={onPress}
      accessibilityRole="button"
      accessibilityLabel={`${task.title} — ${statusLabel(status)}`}
      style={({ hovered }) => [styles.row, hovered && styles.rowHover]}
    >
      <StatusCheckbox
        status={status}
        onPress={onToggleDone}
        label={`Mark ${task.title} ${status === 'DONE' ? 'not done' : 'done'}`}
      />
      <Text style={[styles.title, muted && styles.titleMuted]} numberOfLines={1}>
        {task.title}
      </Text>
      <View style={styles.meta}>
        {task.deadline_enabled ? (
          <Icon name="clock" size={13} color={palette.textTertiary} />
        ) : null}
        <Text style={[styles.date, { color: dateColor }]}>
          {formatShortDate(task.due_date) || 'No date'}
        </Text>
      </View>
    </Pressable>
  );
}

export function EventRow({ event, onPress }) {
  const muted = event.status === 'PAST';
  return (
    <Pressable
      onPress={onPress}
      accessibilityRole="button"
      accessibilityLabel={`${event.title} — ${statusLabel(event.status)}`}
      style={({ hovered }) => [styles.row, hovered && styles.rowHover]}
    >
      <View style={styles.dotSlot}>
        <StatusDot status={event.status} size={9} />
      </View>
      <Text style={[styles.title, muted && styles.titleMutedSoft]} numberOfLines={1}>
        {event.title}
      </Text>
      <View style={styles.meta}>
        <Text style={[styles.date, { color: statusColor(event.status) }]}>
          {formatShortDate(event.start_time)}
        </Text>
      </View>
    </Pressable>
  );
}

export function RoutineRow({ routine, onPress, onToggleDone }) {
  const muted = isResolved(routine.status);
  return (
    <Pressable
      onPress={onPress}
      accessibilityRole="button"
      accessibilityLabel={`${routine.title} — ${statusLabel(routine.status)}`}
      style={({ hovered }) => [styles.row, hovered && styles.rowHover]}
    >
      <StatusCheckbox
        status={routine.status}
        onPress={onToggleDone}
        label={`Mark ${routine.title} ${routine.status === 'DONE' ? 'not done' : 'done'}`}
      />
      <Text style={[styles.title, muted && styles.titleMuted]} numberOfLines={1}>
        {routine.title}
      </Text>
      <View style={styles.meta}>
        <Text style={styles.date}>ends {formatShortDate(routine.period_end)}</Text>
      </View>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: space[3],
    paddingHorizontal: space[3],
    height: density.rowHeight,
    borderRadius: radius.sm,
    marginBottom: density.rowGap,
  },
  rowHover: { backgroundColor: palette.surface },
  checkbox: {
    width: 19,
    height: 19,
    borderRadius: 19,
    borderWidth: 1.5,
    alignItems: 'center',
    justifyContent: 'center',
    flexShrink: 0,
  },
  dotSlot: { width: 19, alignItems: 'center', justifyContent: 'center' },
  title: {
    flex: 1,
    fontFamily: typography.fontFamily,
    fontSize: typography.size.body,
    color: palette.textPrimary,
  },
  titleMuted: {
    color: palette.textTertiary,
    textDecorationLine: 'line-through',
    textDecorationColor: palette.textTertiary,
  },
  titleMutedSoft: { color: palette.textTertiary },
  meta: { flexDirection: 'row', alignItems: 'center', gap: space[2], flexShrink: 0 },
  date: {
    fontFamily: typography.fontFamily,
    fontSize: typography.size.sm,
    fontWeight: '500',
    color: palette.textTertiary,
  },
});
