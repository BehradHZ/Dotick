from config.migration_checks import migration_history_violations


def test_append_only_gate_allows_new_migrations():
    diff = "A\tapps/api/dotick/organization/migrations/0002_add_index.py\n"

    assert migration_history_violations(diff) == []


def test_append_only_gate_rejects_changed_deleted_and_renamed_migrations():
    diff = "\n".join(
        [
            "M\tapps/api/dotick/identity/migrations/0001_initial.py",
            "D\tapps/api/dotick/items/migrations/0001_initial.py",
            "R100\tapps/api/dotick/tasks/migrations/0001_initial.py"
            "\tapps/api/dotick/tasks/migrations/0001_rewritten.py",
        ]
    )

    assert migration_history_violations(diff) == [
        "M\tapps/api/dotick/identity/migrations/0001_initial.py",
        "D\tapps/api/dotick/items/migrations/0001_initial.py",
        "R100\tapps/api/dotick/tasks/migrations/0001_initial.py",
        "R100\tapps/api/dotick/tasks/migrations/0001_rewritten.py",
    ]


def test_append_only_gate_ignores_non_migration_python_files():
    diff = "\n".join(
        [
            "M\tapps/api/dotick/items/models.py",
            "M\tapps/api/dotick/items/migrations/__init__.py",
        ]
    )

    assert migration_history_violations(diff) == []
