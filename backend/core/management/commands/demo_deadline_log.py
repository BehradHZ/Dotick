"""
Stage 1.5 definition-of-done check (ROADMAP.md §6 Stage 1.5):

    "log output can be inspected and a deadline change (e.g., from a test
    Postpone action) can be reconstructed from the logs alone, before
    Stage 2 begins."

No Task model exists yet at Stage 1.5, so this command stands in for a real
Postpone action: it calls the same `log_deadline_change()` seam Stage 2 will
call, with representative before/after values, so the logging path can be
verified end to end before any domain code depends on it.

Usage:
    python manage.py demo_deadline_log
"""

from django.core.management.base import BaseCommand

from core.logging_utils import log_deadline_change


class Command(BaseCommand):
    help = "Write a sample deadline-change audit log entry (Stage 1.5 verification)."

    def handle(self, *args, **options):
        log_deadline_change(
            task_id=1,
            action="postpone_single",
            old_deadline="2026-08-10T00:00:00+00:00",
            new_deadline="2026-08-10T00:00:00+00:00",
            old_deadline_enabled=True,
            new_deadline_enabled=True,
            old_due_date="2026-08-07T00:00:00+00:00",
            new_due_date="2026-08-09T00:00:00+00:00",
        )
        self.stdout.write(
            self.style.SUCCESS(
                "Wrote a sample deadline_change entry to the dotick.audit logger. "
                "Check LOG_DIR/audit.log (see .env / DOTICK_LOG_DIR)."
            )
        )
