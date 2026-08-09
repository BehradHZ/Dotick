"""
Application-level system logging (ROADMAP.md §6 Stage 1.5).

This module replaces the domain-level `TaskDeadlineHistory` table that was
in the original design (§4.8, superseded). Instead of a queryable table with
a `reason` ENUM, changes are written as structured JSON log lines through
the `dotick.audit` logger — enough to reconstruct "what happened" after the
fact by reading the log file, without a bespoke domain table.

Stage 2 will call `log_deadline_change()` from wherever it currently changes
a Task's `deadline` or `deadline_enabled` (manual edit, single Postpone, and
Postpone All — see §4.7). No Task model exists yet at Stage 1.5, so this
module only provides the logging seam and formatter; Stage 2 wires it in.
"""

import json
import logging
from datetime import datetime, timezone
from typing import Any

audit_logger = logging.getLogger("dotick.audit")


class JsonFormatter(logging.Formatter):
    """
    Formats each log record as a single JSON line.

    Kept intentionally simple (no external dependency like python-json-logger)
    per KISS (§2.3) — this project's log volume and needs don't yet justify
    pulling in a formatting library. `extra={...}` fields passed to the
    logger (see log_deadline_change below) are merged into the JSON object
    alongside the standard fields, so structured context survives even when
    read back with plain `json.loads` per line.
    """

    # Standard LogRecord attributes, used to distinguish "extra" fields
    # (the structured context we actually care about) from Python logging's
    # own bookkeeping attributes on the record.
    _RESERVED = frozenset(logging.LogRecord(
        "", 0, "", 0, "", (), None
    ).__dict__.keys()) | {"message", "asctime"}

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(
                record.created, tz=timezone.utc
            ).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        for key, value in record.__dict__.items():
            if key not in self._RESERVED:
                payload[key] = value

        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)

        return json.dumps(payload, default=str)


def log_deadline_change(
    *,
    task_id: int | str,
    action: str,
    old_deadline: Any = None,
    new_deadline: Any = None,
    old_deadline_enabled: bool | None = None,
    new_deadline_enabled: bool | None = None,
    old_due_date: Any = None,
    new_due_date: Any = None,
) -> None:
    """
    Write one structured audit log entry for a deadline-related change.

    This is the Stage 1.5 replacement for a `TaskDeadlineHistory` row
    (§4.8). Called from Stage 2's Task-mutation code at every point that
    previously would have written to that table: a `deadline` value change,
    a `deadline_enabled` toggle, or a `due_date` shift caused by Postpone.

    Parameters
    ----------
    task_id:
        The affected task's id. Accepts int or str since Stage 2 hasn't
        fixed the primary key type at the time this module was written.
    action:
        What triggered the change — expected values (per §4.7, §4.8):
        "postpone_single", "postpone_all", or "manual_edit". Not enforced
        as an enum here (that rigidity is exactly what the removed
        TaskDeadlineHistory `reason` ENUM cost, per §4.8) — Stage 2 is
        free to pass a new value if a new trigger is added later, and it
        will simply show up in the logs as-is.
    old_*/ new_*:
        Before/after values for whichever fields changed. Pass only what's
        relevant to the call site; fields left at None are still recorded,
        so "this wasn't touched" and "this was set to null" are both
        visible in the log line rather than silently omitted.
    """
    audit_logger.info(
        "deadline_change",
        extra={
            "event": "deadline_change",
            "task_id": task_id,
            "action": action,
            "old_deadline": old_deadline,
            "new_deadline": new_deadline,
            "old_deadline_enabled": old_deadline_enabled,
            "new_deadline_enabled": new_deadline_enabled,
            "old_due_date": old_due_date,
            "new_due_date": new_due_date,
        },
    )
