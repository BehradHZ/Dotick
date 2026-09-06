import json
from datetime import date, datetime
from pathlib import Path

import pytest
from dotick.temporal import all_day_interval, parse_instant, resolve_wall_time

VECTORS = json.loads(
    (Path(__file__).resolve().parents[3] / "docs/design/time-vectors.json").read_text()
)


@pytest.mark.parametrize("vector", VECTORS["instants"])
def test_offset_input_keeps_the_same_instant(vector):
    assert parse_instant(vector["input"]).isoformat() == vector["utc"]


def test_instant_rejects_timezone_free_input():
    with pytest.raises(ValueError, match="offset"):
        parse_instant("2026-09-06T12:00:00")


@pytest.mark.parametrize("vector", VECTORS["wall_times"])
def test_wall_time_resolution_is_explicit_at_dst_boundaries(vector):
    local = datetime.fromisoformat(vector["local"])
    if "error" in vector:
        with pytest.raises(ValueError, match=vector["error"]):
            resolve_wall_time(local, vector["zone"])
    else:
        actual = resolve_wall_time(local, vector["zone"], fold=vector.get("fold"))
        assert actual.isoformat() == vector["utc"]


@pytest.mark.parametrize("vector", VECTORS["all_day"])
def test_all_day_is_a_fixed_half_open_instant_interval(vector):
    if "error" in vector:
        with pytest.raises(ValueError, match=vector["error"]):
            all_day_interval(date.fromisoformat(vector["date"]), vector["zone"])
    else:
        start, end = all_day_interval(date.fromisoformat(vector["date"]), vector["zone"])
        assert start.isoformat() == vector["start"]
        assert end.isoformat() == vector["end"]
        assert (end - start).total_seconds() == vector["hours"] * 3600
