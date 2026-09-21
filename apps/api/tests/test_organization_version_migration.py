import uuid

import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError, connection, transaction
from django.db.migrations.executor import MigrationExecutor

pytestmark = pytest.mark.django_db(transaction=True)

OLD_MIGRATION = ("organization", "0002_list_folder_position")
NEW_MIGRATION = ("organization", "0004_organization_create_operation")


def test_organization_schema_migrates_existing_rows_and_preserves_uniqueness():
    executor = MigrationExecutor(connection)
    leaf_nodes = executor.loader.graph.leaf_nodes()

    try:
        executor.migrate([OLD_MIGRATION])
        old_apps = executor.loader.project_state([OLD_MIGRATION]).apps
        Folder = old_apps.get_model("organization", "Folder")
        List = old_apps.get_model("organization", "List")
        Column = old_apps.get_model("organization", "Column")

        user = get_user_model().objects.create_user(
            email="organization-version-migration@example.test",
            password="Only-for-automated-tests-8!",
        )
        folder = Folder.objects.create(owner_id=user.id, title="Existing Folder")
        row = List.objects.create(owner_id=user.id, folder_id=folder.id, title="Existing List")
        column = Column.objects.create(list_id=row.id, title="Existing Column", is_default=True)

        executor = MigrationExecutor(connection)
        executor.migrate([NEW_MIGRATION])
        new_apps = executor.loader.project_state([NEW_MIGRATION]).apps
        Folder = new_apps.get_model("organization", "Folder")
        List = new_apps.get_model("organization", "List")
        Column = new_apps.get_model("organization", "Column")
        OrganizationCreateOperation = new_apps.get_model(
            "organization",
            "OrganizationCreateOperation",
        )

        assert Folder.objects.get(pk=folder.id).version == 1
        assert List.objects.get(pk=row.id).version == 1
        assert Column.objects.get(pk=column.id).version == 1

        List.objects.create(owner_id=user.id, title="Inbox", is_inbox=True)
        with pytest.raises(IntegrityError), transaction.atomic():
            List.objects.create(owner_id=user.id, title="Second Inbox", is_inbox=True)

        with pytest.raises(IntegrityError), transaction.atomic():
            Column.objects.create(list_id=row.id, title="Second Default", is_default=True)

        operation_id = uuid.uuid4()
        OrganizationCreateOperation.objects.create(
            owner_id=user.id,
            resource_type="folder",
            operation_id=operation_id,
            intent_digest="a" * 64,
            resource_id=folder.id,
        )
        with pytest.raises(IntegrityError), transaction.atomic():
            OrganizationCreateOperation.objects.create(
                owner_id=user.id,
                resource_type="folder",
                operation_id=operation_id,
                intent_digest="b" * 64,
                resource_id=folder.id,
            )
        with pytest.raises(IntegrityError), transaction.atomic():
            OrganizationCreateOperation.objects.create(
                owner_id=user.id,
                resource_type="unsupported",
                operation_id=uuid.uuid4(),
                intent_digest="a" * 64,
                resource_id=folder.id,
            )
        with pytest.raises(IntegrityError), transaction.atomic():
            OrganizationCreateOperation.objects.create(
                owner_id=user.id,
                resource_type="folder",
                operation_id=uuid.uuid4(),
                intent_digest="",
                resource_id=folder.id,
            )
    finally:
        MigrationExecutor(connection).migrate(leaf_nodes)
