/**
 * Icon set.
 *
 * The same stroked 24×24 glyphs the prototype drew inline, moved into
 * react-native-svg so they render identically on web and on a future
 * native build (an inline `<svg>` would be web-only, which §5.1 asks us
 * to avoid where reasonable).
 */

import Svg, { Circle, Path, Rect } from 'react-native-svg';

import { palette } from '../theme/tokens';

const PATHS = {
  home: ['M4 11.5 12 4l8 7.5', 'M6 10v9a1 1 0 0 0 1 1h3v-6h4v6h3a1 1 0 0 0 1-1v-9'],
  check: ['m5 12 4 4 10-10'],
  checkbox: ['M9 11.5 11.2 14 15.5 9'],
  routine: ['M4 12a8 8 0 0 1 14-5.2M20 12a8 8 0 0 1-14 5.2', 'M18 4v3.2h-3.2M6 20v-3.2h3.2'],
  calendar: ['M3.5 9.5h17M8 3v4M16 3v4'],
  stats: ['M5 20V10M12 20V4M19 20v-7'],
  play: ['M6 4v16l14-8L6 4Z'],
  bell: ['M18 8a6 6 0 1 0-12 0c0 7-3 9-3 9h18s-3-2-3-9', 'M13.7 21a2 2 0 0 1-3.4 0'],
  settings: [
    'M19.4 15a1.7 1.7 0 0 0 .3 1.9l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.9-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1-1.6 1.7 1.7 0 0 0-1.9.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.9 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.6-1 1.7 1.7 0 0 0-.3-1.9l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.9.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.9-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.9V9c.2.6.7 1 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1Z',
  ],
  search: ['m20 20-4.3-4.3'],
  close: ['M6 6l12 12M18 6 6 18'],
  plus: ['M12 5v14M5 12h14'],
  postpone: ['M3 12a9 9 0 1 0 3-6.7', 'M3 4v5h5'],
  sort: ['M7 6h13M7 12h9M7 18h5', 'M3 6h.01M3 12h.01M3 18h.01'],
  chevronDown: ['m6 9 6 6 6-6'],
  chevronRight: ['m9 6 6 6-6 6'],
  chevronLeft: ['m15 6-6 6 6 6'],
  trash: ['M4 7h16', 'M9 7V4.5h6V7', 'M6 7l1 13h10l1-13', 'M10 11v6M14 11v6'],
  edit: ['M4 20h4L20 8l-4-4L4 16v4Z'],
  refresh: ['M20 12a8 8 0 1 1-2.3-5.6', 'M20 4v4h-4'],
  filter: ['M4 5h16M7 12h10M10 19h4'],
  inbox: ['M4 4h13l3 4-3 4H4V4Z', 'M4 12v8'],
  list: ['M3.5 10h17'],
  folder: [
    'M4 6.5a1.5 1.5 0 0 1 1.5-1.5h4l2 2.5h7A1.5 1.5 0 0 1 20 9v9a1.5 1.5 0 0 1-1.5 1.5h-13A1.5 1.5 0 0 1 4 18V6.5Z',
  ],
  clock: ['M12 7v5.2l3.4 2', 'M12 12'],
  undo: ['M9 10H4V5', 'M4 10a8 8 0 1 1 3 6.2'],
};

const RECTS = {
  checkbox: { x: 3.5, y: 4, width: 17, height: 17, rx: 3 },
  calendar: { x: 3.5, y: 5, width: 17, height: 16, rx: 2.5 },
  list: { x: 3.5, y: 4.5, width: 17, height: 16, rx: 2.5 },
};

const CIRCLES = {
  settings: { cx: 12, cy: 12, r: 3 },
  search: { cx: 11, cy: 11, r: 6.5 },
  clock: { cx: 12, cy: 12, r: 8.5 },
};

export default function Icon({ name, size = 18, color = palette.textSecondary, strokeWidth = 1.8 }) {
  const paths = PATHS[name] || [];
  const rect = RECTS[name];
  const circle = CIRCLES[name];

  return (
    <Svg width={size} height={size} viewBox="0 0 24 24" fill="none">
      {rect ? (
        <Rect {...rect} stroke={color} strokeWidth={strokeWidth} />
      ) : null}
      {circle ? (
        <Circle {...circle} stroke={color} strokeWidth={strokeWidth} />
      ) : null}
      {paths.map((d) => (
        <Path
          key={d}
          d={d}
          stroke={color}
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      ))}
    </Svg>
  );
}
