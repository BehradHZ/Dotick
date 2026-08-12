/**
 * Event list + create/edit form (§6 Stage 2 frontend: "Event list/view
 * reflecting the three time-driven states").
 *
 * Events carry no stored status at all (§4.5) — there is nothing to mark
 * complete, so the row has no checkbox and the detail panel offers only
 * Edit and Delete. Anything more would imply a completion model events
 * don't have.
 */

import { useMemo, useState } from 'react';
import { ScrollView, StyleSheet, Text, View } from 'react-native';

import { ApiError } from '../api/client';
import { DATETIME_HINT, formatDateTime, fromInputValue, toInputValue } from '../domain/datetime';
import { EVENT_STATUS_META, groupEvents } from '../domain/status';
import { palette, space, typography } from '../theme/tokens';
import { Button, ButtonRow, IconButton } from '../ui/Button';
import { Banner, EmptyState, GroupHeader, ScreenHeader, StatusChip } from '../ui/Chrome';
import { Field } from '../ui/Field';
import Panel from '../ui/Panel';
import { EventRow } from '../ui/Rows';

function EventForm({ visible, event, onClose, actions }) {
  const editing = Boolean(event);
  const [title, setTitle] = useState(event?.title ?? '');
  const [description, setDescription] = useState(event?.description ?? '');
  const [startTime, setStartTime] = useState(toInputValue(event?.start_time));
  const [endTime, setEndTime] = useState(toInputValue(event?.end_time));
  const [errors, setErrors] = useState({});
  const [saving, setSaving] = useState(false);

  const submit = async () => {
    const next = {};
    if (!title.trim()) next.title = 'A title is required.';

    const start = fromInputValue(startTime);
    if (start.error) next.start_time = start.error;
    else if (!start.value) next.start_time = 'An event needs a start time.';

    const end = fromInputValue(endTime);
    if (end.error) next.end_time = end.error;
    else if (!end.value) next.end_time = 'An event needs an end time.';

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
        start_time: start.value,
        end_time: end.value,
      };
      if (editing) await actions.updateEvent(event.id, payload);
      else await actions.createEvent(payload);
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
      title={editing ? 'Edit event' : 'New event'}
      subtitle="Upcoming, Ongoing and Past are computed from these two times."
      onClose={onClose}
      footer={
        <ButtonRow>
          <Button label="Cancel" onPress={onClose} variant="ghost" />
          <Button
            label={saving ? 'Saving…' : editing ? 'Save changes' : 'Create event'}
            onPress={submit}
            variant="primary"
            disabled={saving}
            full
          />
        </ButtonRow>
      }
    >
      {errors.form ? <Text style={styles.formError}>{errors.form}</Text> : null}
      <Field label="Title" value={title} onChangeText={setTitle} placeholder="What is happening?" error={errors.title} />
      <Field
        label="Description"
        value={description}
        onChangeText={setDescription}
        placeholder="Optional detail"
        multiline
        error={errors.description}
      />
      <Field
        label="Start time"
        value={startTime}
        onChangeText={setStartTime}
        placeholder={DATETIME_HINT}
        hint={DATETIME_HINT}
        error={errors.start_time}
      />
      <Field
        label="End time"
        value={endTime}
        onChangeText={setEndTime}
        placeholder={DATETIME_HINT}
        hint={DATETIME_HINT}
        error={errors.end_time}
      />
    </Panel>
  );
}

function EventDetail({ visible, event, onClose, onEdit, actions }) {
  const [busy, setBusy] = useState(false);
  if (!event) return null;

  const remove = async () => {
    setBusy(true);
    try {
      await actions.deleteEvent(event.id);
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
      title={event.title}
      subtitle={EVENT_STATUS_META[event.status]?.description}
      onClose={onClose}
      footer={
        <ButtonRow>
          <Button label="Edit" icon="edit" variant="secondary" onPress={onEdit} disabled={busy} />
          <Button label="Delete" icon="trash" variant="danger" onPress={remove} disabled={busy} />
        </ButtonRow>
      }
    >
      <View style={styles.chipRow}>
        <StatusChip status={event.status} />
      </View>
      {event.description ? <Text style={styles.description}>{event.description}</Text> : null}
      <View style={styles.detailRow}>
        <Text style={styles.detailLabel}>Starts</Text>
        <Text style={styles.detailValue}>{formatDateTime(event.start_time)}</Text>
      </View>
      <View style={styles.detailRow}>
        <Text style={styles.detailLabel}>Ends</Text>
        <Text style={styles.detailValue}>{formatDateTime(event.end_time)}</Text>
      </View>
      <Text style={styles.note}>
        Events have no stored status — this state is recomputed from the clock on
        every read, so it changes on its own as the start and end times pass.
      </Text>
    </Panel>
  );
}

export default function EventListScreen({ events, loading, error, actionError, actions }) {
  const [selected, setSelected] = useState(null);
  const [formFor, setFormFor] = useState(null); // null | 'new' | event

  const groups = useMemo(() => groupEvents(events), [events]);

  return (
    <View style={styles.screen}>
      <View style={styles.headerArea}>
        <ScreenHeader
          title="Events"
          meta={
            loading && !events.length
              ? 'Loading…'
              : `${events.length} event${events.length === 1 ? '' : 's'} · Upcoming / Ongoing / Past`
          }
          actions={
            <>
              <IconButton name="refresh" title="Reload events" onPress={() => actions.load('events')} />
              <Button label="New event" icon="plus" variant="primary" onPress={() => setFormFor('new')} />
            </>
          }
        />
        <Banner tone="error" message={error} />
        <Banner tone="error" message={actionError} onDismiss={actions.clearMessages} />
      </View>

      <ScrollView contentContainerStyle={styles.scrollContent}>
        {!groups.length ? (
          loading ? (
            <EmptyState message="Loading events…" />
          ) : (
            <EmptyState
              message="No events yet."
              hint="Create one spanning the current moment to see the Ongoing state."
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
              {group.items.map((event) => (
                <EventRow key={event.id} event={event} onPress={() => setSelected(event)} />
              ))}
            </View>
          ))
        )}
      </ScrollView>

      <EventDetail
        visible={Boolean(selected)}
        event={selected}
        onClose={() => setSelected(null)}
        onEdit={() => {
          setFormFor(selected);
          setSelected(null);
        }}
        actions={actions}
      />

      {formFor ? (
        <EventForm
          visible
          event={formFor === 'new' ? null : formFor}
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
  formError: {
    fontFamily: typography.fontFamily,
    fontSize: typography.size.sm,
    color: palette.danger,
    marginBottom: space[3],
  },
});
