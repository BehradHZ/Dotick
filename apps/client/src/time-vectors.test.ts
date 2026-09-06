import { expect, test } from 'vitest';
import vectors from '../../../docs/design/time-vectors.json';

test.each(vectors.calendar_dates)(
  'Gregorian $gregorian represents Jalali $persian',
  ({ gregorian, persian }) => {
    const parts = new Intl.DateTimeFormat('en-US-u-ca-persian-nu-latn', {
      timeZone: 'UTC',
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
    }).formatToParts(new Date(`${gregorian}T12:00:00Z`));
    const part = (name: string) => parts.find((value) => value.type === name)?.value;
    expect(`${part('year')}-${part('month')}-${part('day')}`).toBe(persian);
  },
);
