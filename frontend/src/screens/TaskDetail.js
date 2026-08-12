/**
 * Task detail view (§6 Stage 2 frontend: "Task detail view with Done,
 * Won't Do (reversible), and Postpone actions").
 *
 * Two things this screen is careful about:
 *
 * 1. **Reversibility is visible.** §4.3 makes `WONT_DO` explicitly
 *    reversible and `DONE` reopenable — both by clearing `user_status`.
 *    So the buttons flip to "Reopen" / "Undo won't do" when that status is
 *    already set, rather than showing a dead-end.
 * 2. **Postpone tells the truth about what it will do.** §4.7 has two
 *    branches, and which one fires depends on the task's status. The
 *    button's caption states the branch, so a MISSED postpone doesn't
 *    silently disable the deadline behind the user's back.
 */

import { useState } from 'react';
import { StyleSheet, Text, View } from 'react-native';

import { formatDateTime, graceDaysFromApi } from '../domain/datetime';
import { TASK_STATUS_META, isPostponable } from '../domain/status';
import { palette, space, typography } from '../theme/tokens';
import { Button, ButtonRow } from '../ui/Button';
import { StatusChip } from '../ui/Chrome';
import Panel from '../ui/Panel';

function Row({ label, value, tone = 'default' }) {
  return (
    <View style={styles.detailRow}>
      <Text style={styles.detailLabel}>{label}</Text>
      <Text
        style={[
          styles.detailValue,
          tone === 'muted' && styles.detailValueMuted,
        ]}
      >
        {value}
      </Text>
    </View>
  );
}

/** The sentence under the Postpone button — which §4.7 branch applies. */
function postponeExplanation(task) {
  const status = task.effective_status;
  if (status === 'MISSED') {
    return 'Past the deadline: moves the due date to now and switches the deadline off. The stored deadline date is kept, not shifted.';
  }
  if (status === 'OVERDUE') {
    return 'Deadline has not passed: moves the due date to now and leaves the deadline alone.';
  }
  return 'Only Overdue and Missed tasks can be postponed.';
}

export default function TaskDetail({ visible, task, onClose, onEdit, actions }) {
  const [busy, setBusy] = useState(null);

  if (!task) return null;

  const status = task.effective_status;
  const meta = TASK_STATUS_META[status] || {};
  const grace = graceDaysFromApi(task.grace_period);

  const run = async (key, fn) => {
    setBusy(key);
    try {
      await fn();
    } catch {
      // The store already surfaced the message as a banner on the list
      // screen; keeping the panel open would hide it behind the overlay.
    } finally {
      setBusy(null);
    }
    onClose();
  };

  const isDone = status === 'DONE';
  const isWontDo = status === 'WONT_DO';

  return (
    <Panel
      visible={visible}
      title={task.title}
      subtitle={meta.description}
      onClose={onClose}
      footer={
        <View style={styles.footer}>
          <ButtonRow>
            <Button
              label={isDone ? 'Reopen' : 'Done'}
              icon={isDone ? 'undo' : 'check'}
              variant={isDone ? 'secondary' : 'primary'}
              disabled={busy !== null}
              onPress={() =>
                run('done', () => actions.setTaskUserStatus(task.id, isDone ? null : 'DONE'))
              }
            />
            <Button
              label={isWontDo ? "Undo won't do" : "Won't do"}
              icon={isWontDo ? 'undo' : 'close'}
              variant="secondary"
              disabled={busy !== null}
              onPress={() =>
                run('wontdo', () =>
                  actions.setTaskUserStatus(task.id, isWontDo ? null : 'WONT_DO')
                )
              }
            />
            <Button
              label="Postpone"
              icon="postpone"
              variant="soft"
              disabled={busy !== null || !isPostponable(task)}
              onPress={() => run('postpone', () => actions.postponeTask(task.id))}
            />
          </ButtonRow>
          <Text style={styles.footerNote}>{postponeExplanation(task)}</Text>
          <ButtonRow>
            <Button label="Edit" icon="edit" variant="ghost" onPress={onEdit} disabled={busy !== null} />
            <Button
              label="Delete"
              icon="trash"
              variant="danger"
              disabled={busy !== null}
              onPress={() => run('delete', () => actions.deleteTask(task.id))}
            />
          </ButtonRow>
        </View>
      }
    >
      <View style={styles.chipRow}>
        <StatusChip status={status} />
      </View>

      {task.description ? (
        <Text style={styles.description}>{task.description}</Text>
      ) : null}

      <Row label="Due date" value={formatDateTime(task.due_date)} />
      <Row
        label="Deadline"
        value={
          task.deadline
            ? `${formatDateTime(task.deadline)}${task.deadline_enabled ? '' : ' — inactive'}`
            : '—'
        }
        tone={task.deadline_enabled ? 'default' : 'muted'}
      />
      <Row
        label="Grace period"
        value={grace === null ? '—' : `${grace} day${grace === 1 ? '' : 's'} after the deadline`}
        tone={task.deadline_enabled ? 'default' : 'muted'}
      />
      <Row label="Created" value={formatDateTime(task.created_at)} tone="muted" />
      <Row label="Last updated" value={formatDateTime(task.updated_at)} tone="muted" />

      {!task.deadline_enabled && task.deadline ? (
        <Text style={styles.note}>
          The deadline is switched off, so this task can never become Missed or Auto
          Won&rsquo;t Do. Its stored date is preserved and comes back if you switch it on.
        </Text>
      ) : null}
    </Panel>
  );
}

const styles = StyleSheet.create({
  chipRow: { marginBottom: space[4] },
  description: {
    fontFamily: typography.fontFamily,
    fontSize: typography.size.body,
    lineHeight: 21,
    color: palette.textSecondary,
    marginBottom: space[4],
  },
  detailRow: {
    flexDirection: 'row',
    alignItems: 'baseline',
    justifyContent: 'space-between',
    gap: space[3],
    paddingVertical: space[2],
    borderBottomWidth: 1,
    borderBottomColor: palette.border,
  },
  detailLabel: {
    fontFamily: typography.fontFamily,
    fontSize: typography.size.sm,
    color: palette.textTertiary,
  },
  detailValue: {
    fontFamily: typography.fontFamily,
    fontSize: typography.size.sm,
    fontWeight: '500',
    color: palette.textPrimary,
    textAlign: 'right',
    flexShrink: 1,
  },
  detailValueMuted: { color: palette.textTertiary, fontWeight: '400' },
  note: {
    marginTop: space[4],
    fontFamily: typography.fontFamily,
    fontSize: typography.size.xs,
    lineHeight: 17,
    color: palette.textTertiary,
  },
  footer: { gap: space[3] },
  footerNote: {
    fontFamily: typography.fontFamily,
    fontSize: typography.size.xs,
    lineHeight: 16,
    color: palette.textTertiary,
  },
});
