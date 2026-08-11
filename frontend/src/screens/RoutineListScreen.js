/**
 * Routine occurrence list + create/edit form (§6 Stage 2 frontend:
 * "Simple manual routine occurrence view — create and mark done/won't-do
 * by hand, no recurrence UI yet, that's Stage 3").
 *
 * Each row is one occurrence, created by hand. There is deliberately no
 * recurrence rule control anywhere on this screen: recurrence is Stage 3
 * (§4.9), and a rule input that generated nothing would be a fake
 * control. The `period_end` field is the whole time model an occurrence
 * has (§4.6) — when it passes with no action, the backend reports
 * AUTO_WONT_DO.
 */

import { useMemo, useState } from 'react';
import { ScrollView, StyleSheet, Text, View } from 'react-native';

import { ApiError } from '../api/client';
import { DATETIME_HINT, formatDateTime, fromInputValue, toInputValue } from '../domain/datetime';
import { ROUTINE_STATUS_META, groupRoutines } from '../domain/status';
import { palette, space, typography } from '../theme/tokens';
import { Button, ButtonRow, IconButton } from '../ui/Button';
import { Banner, EmptyState, GroupHeader, ScreenHeader, StatusChip } from '../ui/Chrome';
import { Field } from '../ui/Field';
import Panel from '../ui/Panel';
import { RoutineRow } from '../ui/Rows';

function RoutineForm({ visible, routine, onClose, actions }) {
  const editing = Boolean(routine);
  const [title, setTitle] = useState(routine?.title ?? '');
  const [description, setDescription] = useState(routine?.description ?? '');
  const [periodEnd, setPeriodEnd] = useState(toInputValue(routine?.period_end));
  const [errors, setErrors] = useState({});
  const [saving, setSaving] = useState(false);

  const submit = async () => {
    const next = {};
    if (!title.trim()) next.title = 'A title is required.';

    const end = fromInputValue(periodEnd);
    if (end.error) next.period_end = end.error;
    else if (!end.value) next.period_end = "An occurrence needs a period end.";

    if (Object.keys(next).length) {
      setErrors(next);
      return;
    }

    setErrors({});
    setSaving(true);
    try {
      const payload = {
        title: title.trim(),
        description: description.trim(),
        period_end: end.value,
      };
      if (editing) await actions.updateRoutine(routine.id, payload);
      else await actions.createRoutine(payload);
      onClose();
    } catch (err) {
      if (err instanceof ApiError && err.fieldErrors) setErrors(err.fieldErrors);
      else setErrors({ form: err instanceof Error ? err.message : String(err) });
    } finally {
      setSaving(false);
    }
  };

  return (
    <Panel
      visible={visible}
      title={editing ? 'Edit occurrence' : 'New routine occurrence'}
      subtitle="One occurrence, entered by hand — automatic generation arrives in Stage 3."
      onClose={onClose}
      footer={
        <ButtonRow>
          <Button label="Cancel" onPress={onClose} variant="ghost" />
          <Button
            label={saving ? 'Saving…' : editing ? 'Save changes' : 'Create occurrence'}
            onPress={submit}
            variant="primary"
            disabled={saving}
            full
          />
        </ButtonRow>
      }
    >
      {errors.form ? <Text style={styles.formError}>{errors.form}</Text> : null}
      <Field
        label="Title"
        value={title}
        onChangeText={setTitle}
        placeholder="Which routine is this an occurrence of?"
        error={errors.title}
      />
      <Field
        label="Description"
        value={description}
        onChangeText={setDescription}
        placeholder="Optional detail"
        multiline
        error={errors.description}
      />
      <Field
        label="Period end"
        value={periodEnd}
        onChangeText={setPeriodEnd}
        placeholder={DATETIME_HINT}
        hint="After this moment, an unresolved occurrence reports Auto Won’t Do."
        error={errors.period_end}
      />
    </Panel>
  );
}

function RoutineDetail({ visible, routine, onClose, onEdit, actions }) {
  const [busy, setBusy] = useState(false);
  if (!routine) return null;

  const status = routine.status;
  const isDone = status === 'DONE';
  const isWontDo = status === 'WONT_DO';

  const run = async (fn) => {
    setBusy(true);
    try {
      await fn();
    } catch {
      // Surfaced as a banner on the list screen behind this panel.
    } finally {
      setBusy(false);
    }
    onClose();
  };

  return (
    <Panel
      visible={visible}
      title={routine.title}
      subtitle={ROUTINE_STATUS_META[status]?.description}
      onClose={onClose}
      footer={
        <View style={styles.footer}>
          <ButtonRow>
            <Button
              label={isDone ? 'Reopen' : 'Done'}
              icon={isDone ? 'undo' : 'check'}
              variant={isDone ? 'secondary' : 'primary'}
              disabled={busy}
              onPress={() =>
                run(() => actions.setRoutineUserStatus(routine.id, isDone ? null : 'DONE'))
              }
            />
            <Button
              label={isWontDo ? "Undo won't do" : "Won't do"}
              icon={isWontDo ? 'undo' : 'close'}
              variant="secondary"
              disabled={busy}
              onPress={() =>
                run(() =>
                  actions.setRoutineUserStatus(routine.id, isWontDo ? null : 'WONT_DO')
                )
              }
            />
          </ButtonRow>
          <ButtonRow>
            <Button label="Edit" icon="edit" variant="ghost" onPress={onEdit} disabled={busy} />
            <Button
              label="Delete"
              icon="trash"
              variant="danger"
              disabled={busy}
              onPress={() => run(() => actions.deleteRoutine(routine.id))}
            />
          </ButtonRow>
        </View>
      }
    >
      <View style={styles.chipRow}>
        <StatusChip status={status} />
      </View>
      {routine.description ? (
        <Text style={styles.description}>{routine.description}</Text>
      ) : null}
      <View style={styles.detailRow}>
        <Text style={styles.detailLabel}>Period ends</Text>
        <Text style={styles.detailValue}>{formatDateTime(routine.period_end)}</Text>
      </View>
      <View style={styles.detailRow}>
        <Text style={styles.detailLabel}>Created</Text>
        <Text style={styles.detailValue}>{formatDateTime(routine.created_at)}</Text>
      </View>
      <Text style={styles.note}>
        An occurrence has one period, not a due date and a deadline — so it never
        becomes Overdue or Missed. Won&rsquo;t Do is reversible here, same as on a task.
      </Text>
    </Panel>
  );
}

export default function RoutineListScreen({ routines, loading, error, actionError, actions }) {
  const [selected, setSelected] = useState(null);
  const [formFor, setFormFor] = useState(null); // null | 'new' | routine

  const groups = useMemo(() => groupRoutines(routines), [routines]);

  return (
    <View style={styles.screen}>
      <View style={styles.headerArea}>
        <ScreenHeader
          title="Routines"
          meta={
            loading && !routines.length
              ? 'Loading…'
              : `${routines.length} occurrence${routines.length === 1 ? '' : 's'} · entered by hand until Stage 3`
          }
          actions={
            <>
              <IconButton
                name="refresh"
                title="Reload routines"
                onPress={() => actions.load('routines')}
              />
              <Button
                label="New occurrence"
                icon="plus"
                variant="primary"
                onPress={() => setFormFor('new')}
              />
            </>
          }
        />
        <Banner tone="error" message={error} />
        <Banner tone="error" message={actionError} onDismiss={actions.clearMessages} />
      </View>

      <ScrollView contentContainerStyle={styles.scrollContent}>
        {!groups.length ? (
          loading ? (
            <EmptyState message="Loading routines…" />
          ) : (
            <EmptyState
              message="No routine occurrences yet."
              hint="Add one by hand — recurrence rules that generate these automatically are Stage 3."
            />
          )
        ) : (
          groups.map((group) => (
            <View key={group.key} style={styles.group}>
              <GroupHeader
                title={group.title}
                count={group.items.length}
                status={group.status}
                collapsed={false}
                onToggle={() => {}}
              />
              {group.items.map((routine) => (
                <RoutineRow
                  key={routine.id}
                  routine={routine}
                  onPress={() => setSelected(routine)}
                  onToggleDone={() =>
                    actions.setRoutineUserStatus(
                      routine.id,
                      routine.status === 'DONE' ? null : 'DONE'
                    )
                  }
                />
              ))}
            </View>
          ))
        )}
      </ScrollView>

      <RoutineDetail
        visible={Boolean(selected)}
        routine={selected}
        onClose={() => setSelected(null)}
        onEdit={() => {
          setFormFor(selected);
          setSelected(null);
        }}
        actions={actions}
      />

      {formFor ? (
        <RoutineForm
          visible
          routine={formFor === 'new' ? null : formFor}
          onClose={() => setFormFor(null)}
          actions={actions}
        />
      ) : null}
    </View>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1 },
  headerArea: { paddingHorizontal: space[6], paddingTop: space[5] },
  scrollContent: { paddingHorizontal: space[6], paddingBottom: 110 },
  group: { marginBottom: space[5] },
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
  },
  note: {
    marginTop: space[4],
    fontFamily: typography.fontFamily,
    fontSize: typography.size.xs,
    lineHeight: 17,
    color: palette.textTertiary,
  },
  footer: { gap: space[3] },
  formError: {
    fontFamily: typography.fontFamily,
    fontSize: typography.size.sm,
    color: palette.danger,
    marginBottom: space[3],
  },
});
