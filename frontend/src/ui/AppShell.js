/**
 * App shell — the prototype's layout foundation, reduced to the parts
 * Stage 2 can honestly fill.
 *
 * The prototype's three layers were: a floating bottom-centre dock, a
 * lists/folders rail, and the content column. Two of the three port
 * directly. The middle rail's original content (Lists, Folders, Filters)
 * cannot: lists and folders do not exist until Stage 5 (§6 Stage 5), and
 * §5.1 rules out shipping a control backed by nothing. So the rail keeps
 * its shape and hosts the views that *are* real — saved views computed
 * from the task/event/routine data the API already returns — and shows
 * "Lists · Stage 5" as a disabled placeholder so the layout's intent
 * stays visible without faking the feature.
 *
 * On a narrow viewport (phone browser, §1.2) the rail collapses and its
 * entries move into a horizontal scroller above the content, so the same
 * component tree serves both without a media-query-only web trick.
 */

import { Pressable, ScrollView, StyleSheet, Text, useWindowDimensions, View } from 'react-native';

import { density, palette, radius, shadow, space, typography } from '../theme/tokens';
import Icon from './Icon';

const NARROW_BREAKPOINT = 900;

export function useIsNarrow() {
  const { width } = useWindowDimensions();
  return width < NARROW_BREAKPOINT;
}

/** Bottom-centre floating pill (prototype layer 1). */
export function Dock({ items, current, onSelect, trailing = null }) {
  return (
    <View style={styles.dockWrap} pointerEvents="box-none">
      <View style={styles.dock}>
        {items.map((item) => {
          const active = item.key === current;
          return (
            <Pressable
              key={item.key}
              onPress={() => onSelect(item.key)}
              accessibilityRole="tab"
              accessibilityLabel={item.label}
              accessibilityState={{ selected: active }}
              style={({ hovered }) => [
                styles.dockIcon,
                active && styles.dockIconActive,
                hovered && !active && styles.dockIconHover,
              ]}
            >
              <Icon
                name={item.icon}
                size={19}
                color={active ? palette.accentStrong : palette.textTertiary}
              />
              {active ? <View style={styles.dockActiveDot} /> : null}
            </Pressable>
          );
        })}
        {trailing ? (
          <>
            <View style={styles.dockDivider} />
            {trailing}
          </>
        ) : null}
      </View>
    </View>
  );
}

/** Saved-view rail (prototype layer 2, honest contents). */
export function ViewRail({ views, current, onSelect, narrow }) {
  const content = views.map((view) => {
    const active = view.key === current;
    return (
      <Pressable
        key={view.key}
        onPress={view.disabled ? undefined : () => onSelect(view.key)}
        accessibilityRole="button"
        accessibilityLabel={view.label}
        accessibilityState={{ selected: active, disabled: Boolean(view.disabled) }}
        style={({ hovered }) => [
          narrow ? styles.railChip : styles.railItem,
          active && styles.railItemActive,
          hovered && !active && !view.disabled && styles.railItemHover,
          view.disabled && styles.railItemDisabled,
        ]}
      >
        <Icon
          name={view.icon}
          size={15}
          color={active ? palette.textPrimary : palette.textSecondary}
        />
        <Text style={[styles.railLabel, active && styles.railLabelActive]}>{view.label}</Text>
        {typeof view.count === 'number' ? (
          <Text style={[styles.railCount, active && styles.railCountActive]}>{view.count}</Text>
        ) : null}
      </Pressable>
    );
  });

  if (narrow) {
    return (
      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        style={styles.railScrollerH}
        contentContainerStyle={styles.railScrollerHContent}
      >
        {content}
      </ScrollView>
    );
  }

  return (
    <View style={styles.rail}>
      <ScrollView contentContainerStyle={styles.railContent}>
        {content}
        <Text style={styles.railSectionLabel}>Lists · Stage 5</Text>
        <Text style={styles.railSectionNote}>
          Folders, lists and tags arrive with Stage 5 — the rail keeps their place.
        </Text>
      </ScrollView>
    </View>
  );
}

/** Full shell: rail + content column + floating dock. */
export function AppShell({ rail, children, dock }) {
  const narrow = useIsNarrow();

  return (
    <View style={styles.shell}>
      <View style={narrow ? styles.bodyNarrow : styles.bodyWide}>
        {narrow ? null : rail}
        <View style={styles.content}>
          {narrow ? rail : null}
          {children}
        </View>
      </View>
      {dock}
    </View>
  );
}

const styles = StyleSheet.create({
  shell: { flex: 1, backgroundColor: palette.canvas1 },
  bodyWide: { flex: 1, flexDirection: 'row' },
  bodyNarrow: { flex: 1, flexDirection: 'column' },
  content: { flex: 1, backgroundColor: palette.canvas3, overflow: 'hidden' },

  rail: {
    width: density.railWidth,
    backgroundColor: palette.canvas2,
    borderRightWidth: 1,
    borderRightColor: palette.border,
  },
  railContent: { padding: space[3], paddingTop: space[4] },
  railScrollerH: {
    flexGrow: 0,
    borderBottomWidth: 1,
    borderBottomColor: palette.border,
    backgroundColor: palette.canvas2,
  },
  railScrollerHContent: {
    flexDirection: 'row',
    gap: space[2],
    paddingHorizontal: space[3],
    paddingVertical: space[2],
  },
  railItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: space[3],
    paddingVertical: 8,
    paddingHorizontal: 10,
    borderRadius: radius.sm,
    marginBottom: 2,
  },
  railChip: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: space[2],
    paddingVertical: 7,
    paddingHorizontal: 12,
    borderRadius: radius.pill,
    backgroundColor: palette.surface,
  },
  railItemActive: { backgroundColor: palette.accentSoft },
  railItemHover: { backgroundColor: palette.surfaceHover },
  railItemDisabled: { opacity: 0.45 },
  railLabel: {
    fontFamily: typography.fontFamily,
    fontSize: typography.size.sm,
    fontWeight: '500',
    color: palette.textSecondary,
  },
  railLabelActive: { color: palette.textPrimary },
  railCount: {
    marginLeft: 'auto',
    fontFamily: typography.fontFamilyMono,
    fontSize: typography.size.xs,
    color: palette.textTertiary,
  },
  railCountActive: { color: palette.accentStrong },
  railSectionLabel: {
    fontFamily: typography.fontFamily,
    fontSize: typography.size.xs,
    fontWeight: '700',
    letterSpacing: 0.7,
    textTransform: 'uppercase',
    color: palette.textTertiary,
    marginTop: space[5],
    marginBottom: space[2],
    marginHorizontal: space[2],
  },
  railSectionNote: {
    fontFamily: typography.fontFamily,
    fontSize: typography.size.xs,
    lineHeight: 16,
    color: palette.textTertiary,
    opacity: 0.7,
    marginHorizontal: space[2],
  },

  dockWrap: {
    position: 'absolute',
    left: 0,
    right: 0,
    bottom: 20,
    alignItems: 'center',
  },
  dock: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 2,
    padding: 6,
    borderRadius: radius.pill,
    backgroundColor: palette.surfaceRaised,
    borderWidth: 1,
    borderColor: palette.borderStrong,
    ...shadow.dock,
  },
  dockIcon: {
    width: 40,
    height: 40,
    borderRadius: radius.pill,
    alignItems: 'center',
    justifyContent: 'center',
  },
  dockIconActive: { backgroundColor: palette.accentSoft },
  dockIconHover: { backgroundColor: palette.surfaceHover },
  dockActiveDot: {
    position: 'absolute',
    bottom: 4,
    width: 4,
    height: 4,
    borderRadius: 4,
    backgroundColor: palette.accent,
  },
  dockDivider: {
    width: 1,
    height: 22,
    marginHorizontal: 4,
    backgroundColor: palette.borderStrong,
  },
});

export default AppShell;
