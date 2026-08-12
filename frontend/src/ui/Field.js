/**
 * Form fields.
 *
 * `Field` wraps a labelled `TextInput`; `Toggle` is the switch the
 * deadline control needs (§4.3 — switching it off must hide the active
 * date input while keeping the stored value). `Switch` from RN core is
 * deliberately not used: its web styling can't be themed from tokens, and
 * a Pressable pill renders identically on web and native.
 */

import { Pressable, StyleSheet, Text, TextInput, View } from 'react-native';

import { palette, radius, space, typography } from '../theme/tokens';

export function Field({
  label,
  value,
  onChangeText,
  placeholder,
  error = null,
  hint = null,
  multiline = false,
  keyboardType,
}) {
  return (
    <View style={styles.field}>
      <Text style={styles.label}>{label}</Text>
      <TextInput
        value={value}
        onChangeText={onChangeText}
        placeholder={placeholder}
        placeholderTextColor={palette.textTertiary}
        multiline={multiline}
        keyboardType={keyboardType}
        accessibilityLabel={label}
        style={[
          styles.input,
          multiline && styles.inputMultiline,
          error ? styles.inputError : null,
        ]}
      />
      {error ? (
        <Text style={styles.error}>{error}</Text>
      ) : hint ? (
        <Text style={styles.hint}>{hint}</Text>
      ) : null}
    </View>
  );
}

export function Toggle({ label, value, onValueChange, hint = null }) {
  return (
    <View style={styles.toggleRow}>
      <View style={styles.toggleLabels}>
        <Text style={styles.label}>{label}</Text>
        {hint ? <Text style={styles.hint}>{hint}</Text> : null}
      </View>
      <Pressable
        onPress={() => onValueChange(!value)}
        accessibilityRole="switch"
        accessibilityLabel={label}
        accessibilityState={{ checked: value }}
        style={[styles.track, value && styles.trackOn]}
      >
        <View style={[styles.knob, value && styles.knobOn]} />
      </Pressable>
    </View>
  );
}

/** Small labelled segmented control (used for sort/group menus). */
export function Segmented({ options, value, onChange }) {
  return (
    <View style={styles.segmented}>
      {options.map((option) => {
        const active = option.key === value;
        return (
          <Pressable
            key={option.key}
            onPress={() => onChange(option.key)}
            accessibilityRole="button"
            accessibilityState={{ selected: active }}
            style={[styles.segment, active && styles.segmentActive]}
          >
            <Text style={[styles.segmentText, active && styles.segmentTextActive]}>
              {option.label}
            </Text>
          </Pressable>
        );
      })}
    </View>
  );
}

const styles = StyleSheet.create({
  field: { marginBottom: space[4] },
  label: {
    fontFamily: typography.fontFamily,
    fontSize: typography.size.sm,
    fontWeight: '600',
    color: palette.textSecondary,
    marginBottom: space[2],
  },
  input: {
    backgroundColor: palette.surface,
    borderWidth: 1,
    borderColor: palette.border,
    borderRadius: radius.sm,
    paddingHorizontal: space[3],
    paddingVertical: 10,
    color: palette.textPrimary,
    fontFamily: typography.fontFamily,
    fontSize: typography.size.body,
    outlineStyle: 'none',
  },
  inputMultiline: { minHeight: 74, textAlignVertical: 'top' },
  inputError: { borderColor: palette.danger },
  error: {
    marginTop: space[1],
    color: palette.danger,
    fontFamily: typography.fontFamily,
    fontSize: typography.size.xs,
  },
  hint: {
    marginTop: space[1],
    color: palette.textTertiary,
    fontFamily: typography.fontFamily,
    fontSize: typography.size.xs,
  },
  toggleRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: space[3],
    marginBottom: space[3],
  },
  toggleLabels: { flex: 1 },
  track: {
    width: 44,
    height: 26,
    borderRadius: radius.pill,
    backgroundColor: palette.surfaceActive,
    borderWidth: 1,
    borderColor: palette.border,
    padding: 2,
    justifyContent: 'center',
  },
  trackOn: { backgroundColor: palette.accentSoft, borderColor: palette.accent },
  knob: {
    width: 20,
    height: 20,
    borderRadius: radius.pill,
    backgroundColor: palette.textTertiary,
  },
  knobOn: { backgroundColor: palette.accent, transform: [{ translateX: 18 }] },
  segmented: {
    flexDirection: 'row',
    gap: space[1],
    backgroundColor: palette.surface,
    borderRadius: radius.pill,
    padding: 3,
    borderWidth: 1,
    borderColor: palette.border,
    alignSelf: 'flex-start',
  },
  segment: { paddingVertical: 5, paddingHorizontal: 11, borderRadius: radius.pill },
  segmentActive: { backgroundColor: palette.accentSoft },
  segmentText: {
    fontFamily: typography.fontFamily,
    fontSize: typography.size.xs,
    fontWeight: '600',
    color: palette.textSecondary,
  },
  segmentTextActive: { color: palette.accentStrong },
});

export default Field;
