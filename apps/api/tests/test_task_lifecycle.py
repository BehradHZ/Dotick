from datetime import UTC, datetime, timedelta

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from dotick.items.models import Item
from dotick.organization.application import create_list
from dotick.tasks.application import advance_task_lifecycle, create_task, update_task
from dotick.tasks.models import Task

pytestmark = pytest.mark.django_db


def _user(email):
    return get_user_model().objects.create_user(
        email=email,
        password="Only-for-automated-tests-8!",
    )


def _task(owner, *, operation_id, due_at=None, deadline_at=None, grace_period_days=0):
    _, column = create_list(owner=owner, title=f"Tasks {operation_id[-3:]}")
    item, _ = create_task(
        actor_id=owner.id,
        title="Scheduled Task",
        operation_id=operation_id,
        column_id=column.id,
        due_at=due_at,
        deadline_at=deadline_at,
        grace_period_days=grace_period_days,
    )
    return item


def test_lifecycle_boundaries_advance_todo_overdue_missed_and_skipped():
    owner = _user("task-lifecycle-boundaries@example.test")
    due = datetime(2026, 10, 1, 8, tzinfo=UTC)
    deadline = datetime(2026, 10, 2, 8, tzinfo=UTC)
    item = _task(
        owner,
        operation_id="00000000-0000-0000-0000-000000000901",
        due_at=due,
        deadline_at=deadline,
        grace_period_days=2,
    )

    assert advance_task_lifecycle(now=due - timedelta(microseconds=1)) == 0
    assert advance_task_lifecycle(now=due) == 1
    item.refresh_from_db()
    assert item.task.status == Task.Status.OVERDUE
    assert item.version == 2

    assert advance_task_lifecycle(now=deadline) == 1
    item.refresh_from_db()
    assert item.task.status == Task.Status.MISSED
    assert item.version == 3

    assert advance_task_lifecycle(now=deadline + timedelta(days=2)) == 1
    item.refresh_from_db()
    assert item.task.status == Task.Status.SKIPPED
    assert item.version == 4


def test_zero_grace_skips_at_deadline_without_observable_missed_state():
    owner = _user("task-lifecycle-zero-grace@example.test")
    deadline = datetime(2026, 10, 2, 8, tzinfo=UTC)
    item = _task(
        owner,
        operation_id="00000000-0000-0000-0000-000000000902",
        deadline_at=deadline,
    )

    assert advance_task_lifecycle(now=deadline) == 1
    item.refresh_from_db()
    assert item.task.status == Task.Status.SKIPPED


def test_lifecycle_does_not_touch_user_results_trash_or_historical_reads_and_edits():
    owner = _user("task-lifecycle-preservation@example.test")
    past = datetime(2026, 10, 1, 8, tzinfo=UTC)
    done = _task(
        owner,
        operation_id="00000000-0000-0000-0000-000000000903",
        due_at=past,
    )
    done = update_task(
        actor_id=owner.id,
        task_id=done.id,
        version=1,
        status=Task.Status.DONE,
    )
    wont_do = _task(
        owner,
        operation_id="00000000-0000-0000-0000-000000000904",
        due_at=past,
    )
    wont_do = update_task(
        actor_id=owner.id,
        task_id=wont_do.id,
        version=1,
        status=Task.Status.WONT_DO,
    )
    historical = _task(
        owner,
        operation_id="00000000-0000-0000-0000-000000000905",
        due_at=past,
    )
    historical = update_task(
        actor_id=owner.id,
        task_id=historical.id,
        version=1,
        title="Edited without time transition",
    )
    trashed = _task(
        owner,
        operation_id="00000000-0000-0000-0000-000000000906",
        due_at=past,
    )
    Item.objects.filter(pk=trashed.id).update(is_trashed=True, trashed_at=past)

    assert historical.task.status == Task.Status.TODO
    assert advance_task_lifecycle(now=past + timedelta(days=1)) == 1
    assert Task.objects.get(pk=done.id).status == Task.Status.DONE
    assert Task.objects.get(pk=wont_do.id).status == Task.Status.WONT_DO
    assert Task.objects.get(pk=historical.id).status == Task.Status.OVERDUE
    assert Task.objects.get(pk=trashed.id).status == Task.Status.TODO


def test_management_command_runs_the_explicit_lifecycle(capsys):
    call_command("advance_task_lifecycle")

    assert "Advanced 0 Task lifecycle state(s)." in capsys.readouterr().out
