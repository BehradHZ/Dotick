import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError, models, transaction
from dotick.items.models import Item, ItemSource
from dotick.organization.application import create_list
from dotick.tasks.models import Task

pytestmark = pytest.mark.django_db


def _user(email):
    return get_user_model().objects.create_user(
        email=email,
        password="Only-for-automated-tests-8!",
    )


def _item(owner):
    _, column = create_list(owner=owner, title="Tasks")
    item = Item.objects.create(
        kind=Item.Kind.TASK,
        owner=owner,
        created_by=owner,
        column=column,
        title="Composed Task",
        creation_operation_id="00000000-0000-0000-0000-000000000701",
        creation_intent_digest="0" * 64,
    )
    ItemSource.objects.create(item=item, platform=ItemSource.Platform.MANUAL)
    return item


def test_task_is_a_one_to_one_composed_subtype_not_model_inheritance():
    owner = _user("task-composition@example.test")
    item = _item(owner)

    task = Task.objects.create(item=item)

    relation = Task._meta.get_field("item")
    assert isinstance(relation, models.OneToOneField)
    assert relation.primary_key is True
    assert Task._meta.parents == {}
    assert Task._meta.db_table == "tasks"
    assert Item._meta.db_table == "items"
    assert task.pk == item.pk
    assert item.task == task


def test_deleting_an_item_cascades_to_its_task_subtype():
    owner = _user("task-composition-cascade@example.test")
    item = _item(owner)
    task = Task.objects.create(item=item)

    item.delete()

    assert not Task.objects.filter(pk=task.pk).exists()


def test_task_defaults_to_todo_and_exposes_only_increment_1_statuses():
    owner = _user("task-status-default@example.test")
    item = _item(owner)

    task = Task.objects.create(item=item)

    assert task.status == Task.Status.TODO
    assert {value for value, _ in Task.Status.choices} == {"todo", "done", "wont_do"}


@pytest.mark.parametrize("status", [Task.Status.TODO, Task.Status.DONE, Task.Status.WONT_DO])
def test_task_accepts_each_increment_1_status(status):
    owner = _user(f"task-status-{status}@example.test")
    item = _item(owner)

    task = Task.objects.create(item=item, status=status)

    task.refresh_from_db()
    assert task.status == status


def test_task_database_rejects_statuses_outside_increment_1():
    owner = _user("task-status-invalid@example.test")
    item = _item(owner)

    with pytest.raises(IntegrityError), transaction.atomic():
        Task.objects.create(item=item, status="in_progress")
