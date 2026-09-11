"""Shared instant vocabulary; business-date attribution belongs to its owning increment."""

from datetime import UTC, date, datetime, time, timedelta
from zoneinfo import ZoneInfo


def parse_instant(value: str) -> datetime:
    instant = datetime.fromisoformat(value)
    if instant.utcoffset() is None:
        raise ValueError("An instant requires an explicit UTC offset.")
    return instant.astimezone(UTC)


def _candidates(local: datetime, zone: ZoneInfo) -> dict[int, datetime]:
    candidates = {}
    for fold in (0, 1):
        instant = local.replace(tzinfo=zone, fold=fold).astimezone(UTC)
        if instant.astimezone(zone).replace(tzinfo=None) == local:
            candidates[fold] = instant
    return candidates


def resolve_wall_time(local: datetime, zone_name: str, *, fold: int | None = None) -> datetime:
    if local.tzinfo is not None:
        raise ValueError("Wall time must be timezone-free; supply the IANA timezone separately.")
    if fold not in (None, 0, 1):
        raise ValueError("fold must be 0 or 1.")
    candidates = _candidates(local, ZoneInfo(zone_name))
    if not candidates:
        raise ValueError("nonexistent local time; choose a valid time")
    if len(set(candidates.values())) > 1 and fold is None:
        raise ValueError("ambiguous local time; select fold 0 or 1")
    return candidates[0 if fold is None else fold]


def _day_start(day: date, zone: ZoneInfo) -> datetime:
    local = datetime.combine(day, time.min)
    candidates = _candidates(local, zone)
    if candidates:
        return min(candidates.values())
    # Find the forward transition itself, not a shifted wall-clock approximation.
    bounds = sorted(local.replace(tzinfo=zone, fold=fold).astimezone(UTC) for fold in (0, 1))
    low, high = bounds
    while high - low > timedelta(microseconds=1):
        middle = low + (high - low) // 2
        if middle.astimezone(zone).replace(tzinfo=None) < local:
            low = middle
        else:
            high = middle
    return high


def all_day_interval(day: date, zone_name: str) -> tuple[datetime, datetime]:
    zone = ZoneInfo(zone_name)
    start, end = _day_start(day, zone), _day_start(day + timedelta(days=1), zone)
    if start >= end or start.astimezone(zone).date() != day:
        raise ValueError("nonexistent Calendar Day in this timezone")
    return start, end
