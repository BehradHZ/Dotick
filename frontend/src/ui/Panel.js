/**
 * Overlay panel — the prototype's `.specimen-overlay` / `.specimen-card`
 * material, reused as the container for the task detail view and the
 * create/edit forms.
 *
 * Modal from RN core is used so the panel escapes the scroll container and
 * covers the dock; it exists on both web and native, which §5.1 asks for.
 */

import { Modal, Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';

import { palette, radius, shadow, space, typography } from '../theme/tokens';
import { IconButton } from './Button';

export default function Panel({ visible, title, subtitle = null, onClose, children, footer = null }) {
  return (
    <Modal visible={visible} transparent animationType="fade" onRequestClose={onClose}>
      <View style={styles.overlay}>
        {/* Backdrop press closes, matching the prototype's overlay behaviour. */}
        <Pressable
          style={styles.backdrop}
          onPress={onClose}
          accessibilityLabel="Close panel"
        />
        <View style={styles.card}>
          <View style={styles.header}>
            <View style={styles.headerText}>
              <Text style={styles.title} numberOfLines={2}>
                {title}
              </Text>
              {subtitle ? <Text style={styles.subtitle}>{subtitle}</Text> : null}
            </View>
            <IconButton name="close" onPress={onClose} title="Close" />
          </View>

          <ScrollView style={styles.body} contentContainerStyle={styles.bodyContent}>
            {children}
          </ScrollView>

          {footer ? <View style={styles.footer}>{footer}</View> : null}
        </View>
      </View>
    </Modal>
  );
}

const styles = StyleSheet.create({
  overlay: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: space[4],
    backgroundColor: palette.overlay,
  },
  backdrop: { position: 'absolute', top: 0, left: 0, right: 0, bottom: 0 },
  card: {
    width: '100%',
    maxWidth: 560,
    maxHeight: '88%',
    backgroundColor: palette.canvas2,
    borderWidth: 1,
    borderColor: palette.borderStrong,
    borderRadius: radius.lg,
    overflow: 'hidden',
    ...shadow.panel,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: space[3],
    padding: space[5],
    paddingBottom: space[3],
  },
  headerText: { flex: 1 },
  title: {
    fontFamily: typography.fontFamily,
    fontSize: typography.size.lg,
    fontWeight: '800',
    letterSpacing: -0.3,
    color: palette.textPrimary,
  },
  subtitle: {
    fontFamily: typography.fontFamily,
    fontSize: typography.size.sm,
    color: palette.textTertiary,
    marginTop: 3,
  },
  body: { flexGrow: 0 },
  bodyContent: { paddingHorizontal: space[5], paddingBottom: space[5] },
  footer: {
    padding: space[4],
    borderTopWidth: 1,
    borderTopColor: palette.border,
    backgroundColor: palette.surface,
  },
});
