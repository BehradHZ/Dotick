"""
Stage 1.5 — Application Logging.

Seam under test: core.logging_utils (JsonFormatter, log_deadline_change).
See ROADMAP.md §6 Stage 1.5 and §4.8 (deadline-change tracking moved from a
domain history table to application-level logging).
"""

import json
import logging

from django.test import SimpleTestCase

from core.logging_utils import JsonFormatter, audit_logger, log_deadline_change


class JsonFormatterTests(SimpleTestCase):
    """The formatter produces one valid, parseable JSON object per record."""

    def _format(self, record: logging.LogRecord) -> dict:
        formatted = JsonFormatter().format(record)
        return json.loads(formatted)

    def test_basic_record_is_valid_json_with_expected_fields(self):
        record = logging.LogRecord(
            name="dotick.audit",
            level=logging.INFO,
            pathname=__file__,
            lineno=1,
            msg="hello",
            args=(),
            exc_info=None,
        )
        payload = self._format(record)
        self.assertEqual(payload["message"], "hello")
        self.assertEqual(payload["level"], "INFO")
        self.assertEqual(payload["logger"], "dotick.audit")
        self.assertIn("timestamp", payload)

    def test_extra_fields_are_merged_into_payload(self):
        record = logging.LogRecord(
            name="dotick.audit",
            level=logging.INFO,
            pathname=__file__,
            lineno=1,
            msg="deadline_change",
            args=(),
            exc_info=None,
        )
        record.task_id = 42
        record.action = "postpone_single"

        payload = self._format(record)
        self.assertEqual(payload["task_id"], 42)
        self.assertEqual(payload["action"], "postpone_single")


class LogDeadlineChangeTests(SimpleTestCase):
    """
    log_deadline_change() writes one structured, reconstructable entry per
    call — this is the seam Stage 2 will call from Postpone/manual-edit
    code instead of writing to a TaskDeadlineHistory row (§4.8).
    """

    def test_writes_one_info_record_with_full_context(self):
        with self.assertLogs("dotick.audit", level="INFO") as captured:
            log_deadline_change(
                task_id=7,
                action="postpone_all",
                old_deadline="2026-08-01T00:00:00+00:00",
                new_deadline="2026-08-01T00:00:00+00:00",
                old_deadline_enabled=True,
                new_deadline_enabled=False,
                old_due_date="2026-07-30T00:00:00+00:00",
                new_due_date="2026-08-09T00:00:00+00:00",
            )

        self.assertEqual(len(captured.records), 1)
        record = captured.records[0]

        # Reconstructability: every field needed to answer "what changed,
        # on which task, why, and to/from what" must be present on the
        # record (this is what the definition of done requires — a change
        # must be reconstructable from the logs alone).
        self.assertEqual(record.task_id, 7)
        self.assertEqual(record.action, "postpone_all")
        self.assertEqual(record.old_deadline_enabled, True)
        self.assertEqual(record.new_deadline_enabled, False)
        self.assertEqual(record.old_due_date, "2026-07-30T00:00:00+00:00")
        self.assertEqual(record.new_due_date, "2026-08-09T00:00:00+00:00")

    def test_output_round_trips_through_json_formatter(self):
        """
        End-to-end: format() the actual record produced by
        log_deadline_change() and confirm it parses back to the same
        values — this is what "reconstructed from the logs alone" means
        in practice, since the real handler writes formatted text to a
        file, not live LogRecord objects.
        """
        with self.assertLogs("dotick.audit", level="INFO") as captured:
            log_deadline_change(
                task_id=99,
                action="manual_edit",
                old_deadline=None,
                new_deadline="2026-09-01T00:00:00+00:00",
                old_deadline_enabled=False,
                new_deadline_enabled=True,
            )

        record = captured.records[0]
        formatted = JsonFormatter().format(record)
        payload = json.loads(formatted)

        self.assertEqual(payload["task_id"], 99)
        self.assertEqual(payload["action"], "manual_edit")
        self.assertIsNone(payload["old_deadline"])
        self.assertEqual(payload["new_deadline"], "2026-09-01T00:00:00+00:00")
        self.assertFalse(payload["old_deadline_enabled"])
        self.assertTrue(payload["new_deadline_enabled"])

    def test_uses_the_dotick_audit_logger(self):
        self.assertEqual(audit_logger.name, "dotick.audit")
