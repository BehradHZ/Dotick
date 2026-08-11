/**
 * Design tokens — the theming foundation.
 *
 * Ported from the `dotick-layout-foundation.html` prototype's `:root`
 * custom-property block. The prototype's central idea is kept intact: a
 * theme swaps *roles* (canvas / surface / text / accent / status) and
 * *shape* (radius, spacing, density, motion), not just an accent colour.
 * Everything downstream reads from here, so no component hardcodes a
 * colour or a radius.
 *
 * Plain JS objects rather than CSS custom properties, because §5.1 of
 * ROADMAP.md asks components to avoid web-only APIs where reasonable so a
 * later native build reuses them — `var(--x)` would not survive that move.
 */

export const palette = {
  canvas1: '#14100c',
  canvas2: '#1c1611',
  canvas3: '#241c15',

  surface: 'rgba(255, 255, 255, 0.045)',
  surfaceHover: 'rgba(255, 255, 255, 0.08)',
  surfaceActive: 'rgba(255, 255, 255, 0.12)',
  surfaceRaised: 'rgba(30, 23, 17, 0.96)',

  border: 'rgba(255, 255, 255, 0.08)',
  borderStrong: 'rgba(255, 255, 255, 0.14)',

  textPrimary: '#f5efe7',
  textSecondary: '#a89a89',
  textTertiary: '#6f6255',

  accent: '#ff7a1a',
  accentSoft: 'rgba(255, 122, 26, 0.16)',
  accentStrong: '#ff8c3d',
  accentGlow: 'rgba(255, 122, 26, 0.35)',

  overlay: 'rgba(10, 7, 4, 0.75)',
  danger: '#ef4444',
  dangerSoft: 'rgba(239, 68, 68, 0.14)',
};

/**
 * Status colours, keyed by the exact status strings the backend returns
 * (`Task.Status`, `Event.Status`, `Routine.Status` in core/models.py) so
 * a colour lookup never needs a translation layer.
 */
export const statusColors = {
  // Task — the six states of ROADMAP.md §4.3
  TODO: '#ff9640',
  OVERDUE: '#ff5a3c',
  MISSED: '#ef4444',
  AUTO_WONT_DO: '#8a7c6c',
  DONE: '#4ade80',
  WONT_DO: '#8a7c6c',
  // Event — §4.5
  UPCOMING: '#ff9640',
  ONGOING: '#4ade80',
  PAST: '#8a7c6c',
};

export const radius = {
  sm: 8,
  md: 14,
  lg: 20,
  pill: 999,
};

export const space = {
  1: 4,
  2: 8,
  3: 12,
  4: 16,
  5: 20,
  6: 28,
};

/** Density is a theme lever, not a hardcoded row height (prototype note). */
export const density = {
  rowHeight: 52,
  rowGap: 6,
  railWidth: 240,
};

export const typography = {
  // Inter is the prototype's licensed stand-in for SF Pro; on web it is
  // loaded by index.html's font link, and the platform stack behind it
  // keeps native builds sane without an embedded font file.
  fontFamily:
    'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
  fontFamilyMono:
    '"JetBrains Mono", ui-monospace, "SF Mono", Menlo, Consolas, monospace',
  size: {
    xs: 11,
    sm: 12.5,
    body: 14.5,
    md: 16,
    lg: 20,
    title: 26,
  },
};

export const motion = {
  durationFast: 120,
  durationStandard: 200,
};

export const shadow = {
  dock: {
    shadowColor: '#000',
    shadowOpacity: 0.45,
    shadowRadius: 40,
    shadowOffset: { width: 0, height: 16 },
    elevation: 12,
  },
  panel: {
    shadowColor: '#000',
    shadowOpacity: 0.45,
    shadowRadius: 50,
    shadowOffset: { width: 0, height: 20 },
    elevation: 16,
  },
};

export default {
  palette,
  statusColors,
  radius,
  space,
  density,
  typography,
  motion,
  shadow,
};
