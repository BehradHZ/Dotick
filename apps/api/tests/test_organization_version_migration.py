import pytest
from django.contrib.auth import get_user_model
from django.db import connection
from django.db.migrations.executor import MigrationExecutor

pytestmark = pytest.mark.django_db(transaction=True)

OLD_MIGRATION = ("organization", "0002_list_folder_position")
NEW_MIGRATION = ("organization", "0003_folder_list_column_version")


def test_existing_organization_rows_receive_version_one():
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

        assert Folder.objects.get(pk=folder.id).version == 1
        assert List.objects.get(pk=row.id).version == 1
        assert Column.objects.get(pk=column.id).version == 1
    finally:
        MigrationExecutor(connection).migrate(leaf_nodes)
