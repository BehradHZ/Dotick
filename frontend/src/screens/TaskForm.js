/**
 * Task create/edit form (§6 Stage 2 frontend: "Basic create/edit forms …
 * including a toggle control next to the deadline field").
 *
 * The deadline toggle is the one control here with real domain meaning
 * (§4.3): switching it off hides the active date input but keeps the
 * entered value in local state and still sends it, so switching it back
 * on restores the date rather than asking for it again. That mirrors the
 * backend, which preserves the stored `deadline` while
 * `deadline_enabled` is false.
 *
 * Validation is split deliberately: format errors are caught locally by
 * `fromInputValue` (a typo must never become a real timestamp that then
 * drives a wrong status), while the `due_date <= deadline` rule is left
 * to the backend serializer and surfaced from its per-field response —
 * duplicating that rule client-side would create two sources of truth.
 */

import { useState } from 'react';
import { StyleSheet, Text, View } from 'react-native';

import { ApiError } from '../api/client';
import {
  DATETIME_HINT,
  fromInputValue,
  graceDaysFromApi,
  graceDaysToApi,
  toInputValue,
} from '../domain/datetime';
import { palette, space, typography } from '../theme/tokens';
import { Button, ButtonRow } from '../ui/Button';
import { Field, Toggle } from '../ui/Field';
import Panel from '../ui/Panel';

export default function TaskForm({ visible, task, onClose, actions }) {
  const editing = Boolean(task);

  const [title, setTitle] = useState(task?.title ?? '');
  const [description, setDescription] = useState(task?.description ?? '');
  const [dueDate, setDueDate] = useState(toInputValue(task?.due_date));
  const [deadline, setDeadline] = useState(toInputValue(task?.deadline));
  const [deadlineEnabled, setDeadlineEnabled] = useState(task?.deadline_enabled ?? false);
  const [graceDays, setGraceDays] = useState(
    String(graceDaysFromApi(task?.grace_period) ?? 7)
  );
  const [errors, setErrors] = useState({});
  const [saving, setSaving] = useState(false);

  const submit = async () => {
    const next = {};

    if (!title.trim()) next.title = 'A title is required.';

    const due = fromInputValue(dueDate);
    if (due.error) next.due_date = due.error;

    const dl = fromInputValue(deadline);
    if (dl.error) next.deadline = dl.error;

    const grace = graceDaysToApi(graceDays);
    if (grace === null) next.grace_period = 'Enter a whole number of days (0 or more).';

    if (Object.keys(next).length) {
      setErrors(next);
      return;
    }

    const payload = {
      title: title.trim(),
      description: description.trim(),
      due_date: due.value,
      // Sent even while the toggle is off: the backend keeps the value
      // inert but preserved (§4.3), which is what makes re-enabling it
      // later restore the date instead of losing it.
      deadline: dl.value,
      deadline_enabled: deadlineEnabled,
      grace_period: grace,
    };

    setErrors({});
    setSaving(true);
    try {
      if (editing) await actions.updateTask(task.id, payload);
      else await actions.createTask(payload);
      onClose();
    } catch (err) {
      // The serializer's due_date/deadline message lands on the field
      // that caused it; anything else falls back to a form-level note.
      if (err instanceof ApiError && err.fieldErrors) setErrors(err.fieldErrors);
      else setErrors({ form: err instanceof Error ? err.message : String(err) });
    } finally {
      setSaving(false);
    }
  };

  return (
    <Panel
      visible={visible}
      title={editing ? 'Edit task' : 'New task'}
      subtitle={
        editing
          ? 'Status is recomputed by the backend from these fields.'
          : 'Six statuses are derived from these two dates and the deadline toggle.'
      }
      onClose={onClose}
      footer={
        <ButtonRow>
          <Button label="Cancel" onPress={onClose} variant="ghost" />
          <Button
            label={saving ? 'Saving…' : editing ? 'Save changes' : 'Create task'}
            onPress={submit}
            variant="primary"
            disabled={saving}
            full
          />
        </ButtonRow>
      }
    >
      {errors.form ? <Text style={styles.formError}>{errors.form}</Text> : null}

      <Field label="Title" value={title} onChangeText={setTitle} placeholder="What needs doing?" error={errors.title} />

      <Field
        label="Description"
        value={description}
        onChangeText={setDescription}
        placeholder="Optional detail"
        multiline
        error={errors.description}
      />

      <Field
        label="Due date"
        value={dueDate}
        onChangeText={setDueDate}
        placeholder={DATETIME_HINT}
        hint={`${DATETIME_HINT} — leave empty for no due date.`}
        error={errors.due_date}
      />

      <View style={styles.deadlineBlock}>
        <Toggle
          label="Deadline"
          value={deadlineEnabled}
          onValueChange={setDeadlineEnabled}
          hint={
            deadlineEnabled
              ? 'Active: the task can become Overdue, then Missed, then Auto Won\u2019t Do.'
              : 'Off: the stored date is kept but ignored — the task stays To Do.'
          }
        />

        {deadlineEnabled ? (
          <>
            <Field
              label="Deadline date"
              value={deadline}
              onChangeText={setDeadline}
              placeholder={DATETIME_HINT}
              hint={`${DATETIME_HINT} — must not be earlier than the due date.`}
              error={errors.deadline}
            />
            <Field
              label="Grace period (days)"
              value={graceDays}
              onChangeText={setGraceDays}
              placeholder="7"
              keyboardType="numeric"
              hint="How long the task stays Missed before closing itself."
              error={errors.grace_period}
            />
          </>
        ) : deadline ? (
          <Text style={styles.retained}>
            Kept for later: {deadline}. Switch the toggle back on to use it again.
          </Text>
        ) : null}
      </View>
    </Panel>
  );
}

const styles = StyleSheet.create({
  formError: {
    fontFamily: typography.fontFamily,
    fontSize: typography.size.sm,
    color: palette.danger,
    marginBottom: space[3],
  },
  deadlineBlock: {
    borderTopWidth: 1,
    borderTopColor: palette.border,
    paddingTop: space[4],
    marginTop: space[1],
  },
  retained: {
    fontFamily: typography.fontFamily,
    fontSize: typography.size.xs,
    color: palette.textTertiary,
    fontStyle: 'italic',
  },
});
