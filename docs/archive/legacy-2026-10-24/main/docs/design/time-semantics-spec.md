# Dotick Time Semantics Baseline

Status: Increment 0 baseline, 2026-09-06. Refinement owners: I2, I4, I10.

Authority: [System Definition §§8.1–8.2](../requirements/system-definition.md), [SRS-DAY-013/014](../requirements/srs.md), and the [roadmap §7.3.1](../planning/increment-roadmap.md). This specification chooses representations within those behaviors.

## Representations and invariants

| Concept | Representation and invariant |
|---|---|
| Real instant | Offset-bearing ISO 8601 at the API boundary, normalized to UTC; PostgreSQL `timestamptz`. Reject offset-free input where an instant is required. |
| Calendar Day | A date interpreted in an explicit IANA timezone. Its duration can differ from 24 hours. |
| All-day schedule | Fixed half-open interval `[start_instant, end_instant)`, resolved when the date and timezone are selected. End is the beginning of the next Calendar Day, never `23:59:59`. |
| Dotick Day | A logical half-open interval with stable start/end instants and a business-date label. A current/historical interval is never recalculated from a later timezone or boundary preference. |
| `occurrence_date` | ISO date representing a RoutineCompletion business date, independent of when its action is recorded. Never derive it mechanically from `created_at`. |
| Credited/effective date | Explicit day attribution, possibly unresolved. Preserve it separately from action/recording instants. |
| Account timezone | Explicit IANA identifier. The device may suggest it; later device changes require user confirmation before changing Account semantics. |
| Calendar selection | Explicit `gregorian` or `jalali` calendar for date arithmetic/recurrence. ISO storage/transport of civil dates does not imply Gregorian recurrence arithmetic. |

Changing Account timezone changes presentation of an existing timed or all-day schedule, never its instants. It likewise does not silently re-anchor timed recurrence. Changing the intended future local schedule is a separate schedule edit.

## DST and invalid local times

The pure helper `dotick.temporal.resolve_wall_time` accepts an explicit local time and IANA timezone. A gap is rejected as nonexistent; an overlap requires explicit `fold=0` (first occurrence) or `fold=1` (second). No system/device-default timezone is consulted.

For Calendar Day intervals, choose the earliest occurrence of local midnight. If midnight is skipped by an offset transition, use the transition's first valid instant on that date. Reject an entirely skipped Calendar Day, such as `2011-12-30` in `Pacific/Apia`. Boundaries are resolved with timezone transition data, not by adding 24 elapsed hours.

Recurring schedules and future Dotick Day boundary generation must resolve gap/overlap choices consistently before persisting their intervals. I4/I10 own the schedule-specific policy, user interaction, and extended transition catalog; the I0 helper does not silently define recurrence or scoring behavior.

## Attribution and boundary changes

The configured boundary can be any valid time of day. Changes take effect starting with the next Dotick Day. An Account timezone change preserves the current/historical intervals and influences only future boundaries.

Without an explicit boundary, the default first 60 minutes after local midnight form the ambiguity window. Each completion independently chooses Today or Yesterday. Until that choice, its source action may remain recorded but it contributes to no day-based ring, streak, or statistic.

Finalization closes the previous day, freezes ring outcomes and final score/bonus, updates streaks, then attempts generation. An unavailable AI provider can defer generation; it cannot prevent deterministic finalization. Repeated/delayed processing uses the original effective boundary and must be idempotent. I10 implements this state machine; I0 does not create scoring tables.

## Calendar arithmetic and recurrence handoff

Jalali and Gregorian arithmetic must retain the selected calendar and original recurrence anchor. Validate month lengths and leap dates before creating an occurrence; an impossible date must not silently roll into another month or permanently drift the anchor. The owning recurrence specification must apply the canonical selected-policy behavior for short months/leap years and preserve real instants on Account timezone changes.

Gregorian leap-year arithmetic, Jalali Esfand leap behavior, negative/positive offsets, DST gaps/overlaps, and cross-calendar year boundaries are separate cases. Use supported calendar libraries/runtime calendar data rather than a hand-written Persian leap formula. The I0 web tests verify Gregorian/Jalali golden date conversions through the standard `Intl` Persian calendar. This is conversion verification, not a recurrence implementation.

## Executable evidence and ownership

[time-vectors.json](time-vectors.json) is the reusable catalog. Its `instants`, `wall_times`, and `all_day` cases execute in `apps/api/tests/test_time.py`; `calendar_dates` executes in `apps/client/src/time-vectors.test.ts`. The entries under `owning_increment_vectors` are explicit acceptance scenarios for I4/I10 and are **not claimed as passing product tests**.

I2 extends schedule edits, all-day display, and timezone-change integration. I4 adds recurrence anchoring, invalid-date policies, reminders, broader zone-transition cases, and matching server/client calendar arithmetic. I10 adds persisted day boundaries, ambiguity attribution, late finalization, historical correction and frozen-statistic checks. Timezone-data and calendar-library upgrades must rerun the shared vectors before acceptance.
