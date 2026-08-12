/**
 * Small shared display pieces: status dot/chip, section banner, empty
 * state, group header, and the screen header block. All ported from the
 * prototype's equivalents (`.status-dot`, `.group-header`,
 * `.content-header`, `.empty-state`).
 */

import { Pressable, StyleSheet, Text, View } from 'react-native';

import { palette, radius, space, typography } from '../theme/tokens';
import { statusColor, statusLabel } from '../domain/status';
import Icon from './Icon';

export function StatusDot({ status, size = 7 }) {
  return (
    <View
      style={{
        width: size,
        height: size,
        borderRadius: size,
        backgroundColor: statusColor(status),
      }}
    />
  );
}

/** Status pill used in the detail panel and the event/routine rows. */
export function StatusChip({ status }) {
  const color = statusColor(status);
  return (
    <View style={[styles.chip, { borderColor: color }]}>
      <StatusDot status={status} size={6} />
      <Text style={[styles.chipText, { color }]}>{statusLabel(status)}</Text>
    </View>
  );
}

/**
 * Dismissible message strip. `tone` is 'error' | 'notice'; errors from a
 * mutation and the confirmation from Postpone All both land here rather
 * than in an alert, so the message stays readable on a phone browser.
 */
export function Banner({ tone = 'notice', message, onDismiss }) {
  if (!message) return null;
  const isError = tone === 'error';
  return (
    <View
      style={[
        styles.banner,
        {
          backgroundColor: isError ? palette.dangerSoft : palette.accentSoft,
          borderColor: isError ? palette.danger : palette.accent,
        },
      ]}
    >
      <Icon
        name={isError ? 'close' : 'check'}
        size={14}
        color={isError ? palette.danger : palette.accentStrong}
      />
      <Text
        style={[
          styles.bannerText,
          { color: isError ? palette.danger : palette.accentStrong },
        ]}
      >
        {message}
      </Text>
      {onDismiss ? (
        <Pressable onPress={onDismiss} accessibilityLabel="Dismiss message">
          <Icon name="close" size={14} color={palette.textTertiary} />
        </Pressable>
      ) : null}
    </View>
  );
}

export function EmptyState({ message, hint = null }) {
  return (
    <View style={styles.empty}>
      <Text style={styles.emptyText}>{message}</Text>
      {hint ? <Text style={styles.emptyHint}>{hint}</Text> : null}
    </View>
  );
}

/**
 * Collapsible group header. `action` renders the prototype's inline
 * "Postpone" pill on the Overdue/Missed groups.
 */
export function GroupHeader({ title, count, status = null, collapsed, onToggle, action = null }) {
  return (
    <View style={styles.groupHeader}>
      <Pressable
        onPress={onToggle}
        accessibilityRole="button"
        accessibilityState={{ expanded: !collapsed }}
        accessibilityLabel={`${title}, ${count} item${count === 1 ? '' : 's'}`}
        style={styles.groupHeaderMain}
      >
        <Icon name={collapsed ? 'chevronRight' : 'chevronDown'} size={14} color={palette.textTertiary} />
        {status ? <StatusDot status={status} /> : null}
        <Text style={styles.groupTitle}>{title}</Text>
        <Text style={styles.groupCount}>{count}</Text>
      </Pressable>
      {action}
    </View>
  );
}

export function ScreenHeader({ title, meta, actions = null }) {
  return (
    <View style={styles.screenHeader}>
      <View style={styles.screenHeaderText}>
        <Text style={styles.screenTitle}>{title}</Text>
        {meta ? <Text style={styles.screenMeta}>{meta}</Text> : null}
      </View>
      {actions ? <View style={styles.screenActions}>{actions}</View> : null}
    </View>
  );
}

const styles = StyleSheet.create({
  chip: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: space[2],
    alignSelf: 'flex-start',
    paddingVertical: 4,
    paddingHorizontal: 10,
    borderRadius: radius.pill,
    borderWidth: 1,
  },
  chipText: {
    fontFamily: typography.fontFamily,
    fontSize: typography.size.xs,
    fontWeight: '700',
    letterSpacing: 0.02,
  },
  banner: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: space[2],
    borderWidth: 1,
    borderRadius: radius.sm,
    paddingVertical: space[2],
    paddingHorizontal: space[3],
    marginBottom: space[3],
  },
  bannerText: {
    flex: 1,
    fontFamily: typography.fontFamily,
    fontSize: typography.size.sm,
  },
  empty: { paddingVertical: 54, paddingHorizontal: space[4], alignItems: 'center' },
  emptyText: {
    fontFamily: typography.fontFamily,
    fontSize: typography.size.body,
    color: palette.textTertiary,
    textAlign: 'center',
  },
  emptyHint: {
    fontFamily: typography.fontFamily,
    fontSize: typography.size.sm,
    color: palette.textTertiary,
    opacity: 0.75,
    marginTop: space[2],
    textAlign: 'center',
  },
  groupHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: space[2],
    paddingVertical: space[2],
  },
  groupHeaderMain: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: space[2],
    flex: 1,
  },
  groupTitle: {
    fontFamily: typography.fontFamily,
    fontSize: typography.size.sm,
    fontWeight: '700',
    color: palette.textPrimary,
  },
  groupCount: {
    fontFamily: typography.fontFamilyMono,
    fontSize: typography.size.xs,
    color: palette.textTertiary,
  },
  screenHeader: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    justifyContent: 'space-between',
    gap: space[3],
    paddingBottom: space[4],
    flexWrap: 'wrap',
  },
  screenHeaderText: { flexShrink: 1, minWidth: 180 },
  screenTitle: {
    fontFamily: typography.fontFamily,
    fontSize: typography.size.title,
    fontWeight: '800',
    letterSpacing: -0.5,
    color: palette.textPrimary,
  },
  screenMeta: {
    fontFamily: typography.fontFamily,
    fontSize: typography.size.sm,
    color: palette.textTertiary,
    marginTop: 2,
  },
  screenActions: { flexDirection: 'row', alignItems: 'center', gap: space[2] },
});
