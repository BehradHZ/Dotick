/**
 * Buttons.
 *
 * Two shapes cover every action in Stage 2's screens: a labelled
 * `Button` (with the prototype's pill/accent-soft treatment) and a square
 * `IconButton` for the header actions. Both read from tokens only, so a
 * later theme swap changes them without touching call sites.
 */

import { Pressable, StyleSheet, Text, View } from 'react-native';

import { palette, radius, space, typography } from '../theme/tokens';
import Icon from './Icon';

const VARIANTS = {
  primary: { bg: palette.accent, border: palette.accent, text: '#1a1006' },
  soft: { bg: palette.accentSoft, border: 'transparent', text: palette.accentStrong },
  secondary: { bg: palette.surface, border: palette.border, text: palette.textPrimary },
  danger: { bg: palette.dangerSoft, border: 'transparent', text: palette.danger },
  ghost: { bg: 'transparent', border: 'transparent', text: palette.textSecondary },
};

export function Button({
  label,
  onPress,
  variant = 'secondary',
  icon = null,
  disabled = false,
  full = false,
  accessibilityLabel,
}) {
  const v = VARIANTS[variant] || VARIANTS.secondary;

  return (
    <Pressable
      onPress={disabled ? undefined : onPress}
      accessibilityRole="button"
      accessibilityLabel={accessibilityLabel || label}
      accessibilityState={{ disabled }}
      style={({ hovered, pressed }) => [
        styles.button,
        {
          backgroundColor: v.bg,
          borderColor: v.border,
          opacity: disabled ? 0.45 : pressed ? 0.8 : hovered ? 0.92 : 1,
        },
        full && styles.full,
      ]}
    >
      {icon ? <Icon name={icon} size={15} color={v.text} /> : null}
      <Text style={[styles.buttonText, { color: v.text }]}>{label}</Text>
    </Pressable>
  );
}

export function IconButton({ name, onPress, title, active = false, disabled = false, size = 16 }) {
  return (
    <Pressable
      onPress={disabled ? undefined : onPress}
      accessibilityRole="button"
      accessibilityLabel={title}
      accessibilityState={{ disabled, selected: active }}
      style={({ hovered, pressed }) => [
        styles.iconButton,
        active && styles.iconButtonActive,
        { opacity: disabled ? 0.4 : pressed ? 0.75 : hovered ? 0.9 : 1 },
      ]}
    >
      <Icon
        name={name}
        size={size}
        color={active ? palette.accentStrong : palette.textSecondary}
      />
    </Pressable>
  );
}

/** A horizontal group of actions with consistent spacing. */
export function ButtonRow({ children, wrap = true }) {
  return <View style={[styles.row, wrap && styles.rowWrap]}>{children}</View>;
}

const styles = StyleSheet.create({
  button: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: space[2],
    paddingVertical: 9,
    paddingHorizontal: 14,
    borderRadius: radius.pill,
    borderWidth: 1,
  },
  full: { flex: 1 },
  buttonText: {
    fontFamily: typography.fontFamily,
    fontSize: typography.size.sm,
    fontWeight: '600',
  },
  iconButton: {
    width: 34,
    height: 34,
    borderRadius: radius.sm,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: palette.surface,
    borderWidth: 1,
    borderColor: palette.border,
  },
  iconButtonActive: {
    backgroundColor: palette.accentSoft,
    borderColor: 'transparent',
  },
  row: { flexDirection: 'row', alignItems: 'center', gap: space[2] },
  rowWrap: { flexWrap: 'wrap' },
});

export default Button;
