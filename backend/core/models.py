"""
Stage 2 domain models (ROADMAP.md §4).

Class Table Inheritance (§4.1): BaseEvent is the parent table holding
fields shared by every schedulable item. Task, Event, and Routine are
independent child types (§4.2), each linked back to BaseEvent via
Django's multi-table inheritance (an implicit OneToOneField primary key
Django creates automatically for models that subclass a non-abstract
model).
"""

from datetime import timedelta

from django.db import models
from django.utils import timezone


class BaseEvent(models.Model):
    """
    CTI parent table (§4.1). Holds fields common to every schedulable
    item: title, description, and created/updated timestamps.
    """

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "base_events"

    def __str__(self) -> str:
        return self.title


class TaskManager(models.Manager):
    def postpone_all(self) -> int:
        """
        "Postpone All" (§4.7): apply the same postpone() logic to every
        OVERDUE/MISSED task at once. AUTO_WONT_DO tasks are past the
        deadline too but are excluded — the grace period elapsing is a
        deliberate close, not something a bulk sweep should silently
        reopen. TODO tasks aren't touched (nothing to postpone).

        Reuses the single-task postpone() method per row so both entry
        points share one source of truth for the branching behavior;
        each affected task logs its own entry via §4.8's seam.

        Iterates in Python rather than a bulk SQL UPDATE because
        effective_status is a computed property, not a queryable
        column — consistent with §4.3's "no background worker" design.
        Bulk SQL is the kind of optimization §3.1 defers until real data
        volume proves a plain per-row loop insufficient.
        """
        postponable = {Task.Status.OVERDUE, Task.Status.MISSED}
        count = 0
        for task in self.all():
            if task.effective_status in postponable:
                task.postpone(action="postpone_all")
                count += 1
        return count


class Task(BaseEvent):
    """
    CTI child table (§4.2, §4.3). Independent of Event/Routine beyond
    the shared BaseEvent parent.

    Status is derived primarily from time, with `user_status` capturing
    explicit user intent (§4.3). `deadline` is a toggleable field, not a
    plain nullable date (§4.3, §4.7): `deadline_enabled=False` preserves
    the stored `deadline` value but makes it inert for status purposes.

    `grace_period` is stored at the task level for now with a sensible
    default, per the Stage 2 roadmap note — it becomes a genuinely
    per-list setting once Stage 5 introduces lists.
    """

    class UserStatus(models.TextChoices):
        DONE = "DONE", "Done"
        WONT_DO = "WONT_DO", "Won't Do"

    class Status(models.TextChoices):
        TODO = "TODO", "To Do"
        OVERDUE = "OVERDUE", "Overdue"
        MISSED = "MISSED", "Missed"
        AUTO_WONT_DO = "AUTO_WONT_DO", "Automatically Won't Do"
        DONE = "DONE", "Done"
        WONT_DO = "WONT_DO", "Won't Do"

    DEFAULT_GRACE_PERIOD = timedelta(days=7)

    objects = TaskManager()

    user_status = models.CharField(
        max_length=16,
        choices=UserStatus.choices,
        null=True,
        blank=True,
        default=None,
    )
    due_date = models.DateTimeField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    deadline_enabled = models.BooleanField(default=False)
    grace_period = models.DurationField(default=DEFAULT_GRACE_PERIOD)

    class Meta:
        db_table = "tasks"

    @property
    def effective_status(self) -> str:
        """
        The six user-visible statuses (§4.3), computed at read time.

        When `user_status` is set, it wins outright (DONE / WONT_DO are
        explicit and terminal-but-reversible). Otherwise the status is a
        pure function of `now` and the task's own time fields — no
        background worker needed.
        """
        if self.user_status == self.UserStatus.DONE:
            return self.Status.DONE
        if self.user_status == self.UserStatus.WONT_DO:
            return self.Status.WONT_DO

        now = timezone.now()

        if not self.deadline_enabled:
            # No active deadline: behaves like a plain due-date-only
            # task and can never be MISSED/AUTO_WONT_DO (§4.3 note).
            return self.Status.TODO

        if self.due_date is not None and now <= self.due_date:
            return self.Status.TODO

        if self.deadline is not None and now <= self.deadline:
            return self.Status.OVERDUE

        if self.deadline is not None and now <= self.deadline + self.grace_period:
            return self.Status.MISSED

        return self.Status.AUTO_WONT_DO

    def postpone(self, *, action: str = "postpone_single") -> None:
        """
        Postpone this task (§4.7).

        Two branches, both called "Postpone" in the UI:

        1. TODO/OVERDUE (deadline hasn't passed, or there is none active):
           sets due_date = today. deadline is untouched.
        2. Past the deadline (MISSED or AUTO_WONT_DO — deadline has
           passed either way): sets due_date = today AND turns
           deadline_enabled off. The stored deadline value itself is
           left untouched (not shifted, not cleared) — §10.1, resolved.

        Every deadline-related change is logged via Stage 1.5's
        log_deadline_change() seam instead of a domain history table
        (§4.8).

        `action` lets "Postpone All" (bulk) reuse this method while
        logging a distinguishable action ("postpone_all" vs
        "postpone_single" — §4.7, §4.8).
        """
        from core.logging_utils import log_deadline_change

        now = timezone.now()
        old_due_date = self.due_date
        old_deadline_enabled = self.deadline_enabled

        past_deadline = (
            self.deadline_enabled
            and self.deadline is not None
            and now > self.deadline
        )

        self.due_date = now
        if past_deadline:
            self.deadline_enabled = False
        self.save()

        log_deadline_change(
            task_id=self.pk,
            action=action,
            old_deadline=self.deadline,
            new_deadline=self.deadline,
            old_deadline_enabled=old_deadline_enabled,
            new_deadline_enabled=self.deadline_enabled,
            old_due_date=old_due_date,
            new_due_date=self.due_date,
        )


class Event(BaseEvent):
    """
    CTI child table (§4.2, §4.5). Independent of Task/Routine beyond the
    shared BaseEvent parent.

    Events use a purely time-driven three-state model — no stored status
    field at all, since events aren't "completed" the way tasks are.
    """

    class Status(models.TextChoices):
        UPCOMING = "UPCOMING", "Upcoming"
        ONGOING = "ONGOING", "Ongoing"
        PAST = "PAST", "Past"

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        db_table = "events"

    @property
    def status(self) -> str:
        """§4.5: UPCOMING / ONGOING / PAST, computed at read time."""
        now = timezone.now()
        if now < self.start_time:
            return self.Status.UPCOMING
        if now <= self.end_time:
            return self.Status.ONGOING
        return self.Status.PAST


class Routine(BaseEvent):
    """
    CTI child table (§4.2, §4.6). Independent of Task/Event beyond the
    shared BaseEvent parent.

    Each row is one occurrence (e.g. "today's" entry for a daily
    routine) — Stage 2 supports creating and completing individual
    occurrences by hand; full recurrence generation is Stage 3 (§4.9),
    which will generate rows of this same shape automatically.

    Uses the same NULL/DONE/WONT_DO explicit-field pattern as Task
    (§4.3), without the OVERDUE/MISSED distinction: a routine occurrence
    has one period, not a separate due date vs. deadline.
    """

    class UserStatus(models.TextChoices):
        DONE = "DONE", "Done"
        WONT_DO = "WONT_DO", "Won't Do"

    class Status(models.TextChoices):
        TODO = "TODO", "To Do"
        DONE = "DONE", "Done"
        WONT_DO = "WONT_DO", "Won't Do"
        AUTO_WONT_DO = "AUTO_WONT_DO", "Automatically Won't Do"

    user_status = models.CharField(
        max_length=16,
        choices=UserStatus.choices,
        null=True,
        blank=True,
        default=None,
    )
    period_end = models.DateTimeField(
        help_text="When this occurrence's period elapses without action, "
        "it becomes AUTO_WONT_DO (§4.6)."
    )

    class Meta:
        db_table = "routines"

    @property
    def status(self) -> str:
        """§4.6: TODO / DONE / WONT_DO / AUTO_WONT_DO, computed at read time."""
        if self.user_status == self.UserStatus.DONE:
            return self.Status.DONE
        if self.user_status == self.UserStatus.WONT_DO:
            return self.Status.WONT_DO

        if timezone.now() <= self.period_end:
            return self.Status.TODO
        return self.Status.AUTO_WONT_DO
