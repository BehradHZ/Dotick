from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
ANALYSIS_ROOT = REPO_ROOT / "docs" / "reference" / "analysis"
OWNERSHIP_MODEL = ANALYSIS_ROOT / "ownership-creator-source-model.md"
TASK_STATE_MODEL = ANALYSIS_ROOT / "basic-task-state-diagram.md"
ERD_PATH = REPO_ROOT / "docs" / "design" / "increment-1-physical-erd.md"


def _read(path):
    return path.read_text(encoding="utf-8")


def test_ownership_creator_source_are_explicitly_distinct():
    document = _read(OWNERSHIP_MODEL)

    for phrase in (
        "whose Resource is this?",
        "who caused this Resource to be created in Dotick?",
        "how/from where did this Resource enter Dotick?",
        "Creator is not an authorization shortcut",
        "Source must not grant read/write permission",
        "must not be collapsed",
    ):
        assert phrase in document

    requirements = (
        "SRS-ITEM-006",
        "SRS-ITEM-007",
        "SRS-ITEM-008",
        "SRS-NFR-SEC-003",
    )
    for requirement in requirements:
        assert requirement in document


def test_basic_task_state_model_is_exactly_i1_user_driven_scope():
    document = _read(TASK_STATE_MODEL)

    for status in ("Todo", "Done", "Won't_Do"):
        assert status in document

    for transition in (
        "Todo --> Done",
        "Todo --> Won't_Do",
        "Done --> Todo",
        "Won't_Do --> Todo",
    ):
        assert transition in document

    assert "Overdue" in document
    assert "Missed" in document
    assert "Skipped" in document
    assert "deliberately excluded from I1" in document
    assert "Trash is a separate lifecycle axis" in document


def test_increment_1_erd_contains_required_physical_relationships():
    document = _read(ERD_PATH)

    for table in (
        "USERS",
        "USER_PREFERENCES",
        "FOLDERS",
        "LISTS",
        "COLUMNS",
        "ITEMS",
        "TASKS",
        "ITEM_SOURCES",
    ):
        assert table in document

    for field in (
        "owner_user_id",
        "created_by_user_id",
        "column_id",
        "version",
        "creation_operation_id",
        "creation_intent_digest",
        "platform",
        "external_account_id",
        "external_id",
    ):
        assert field in document

    assert "status IN ('todo', 'done', 'wont_do')" in document
    assert "one `items` row with `kind='task'` has exactly one `tasks` row" in document
    assert "Every I1 Item has exactly one `item_sources` row" in document


def test_increment_1_erd_does_not_pull_increment_2_plus_fields_into_schema():
    document = _read(ERD_PATH)

    forbidden_as_schema = (
        "due_at",
        "end_at",
        "deadline_at",
        "grace_period_days",
        "blocked_by",
    )

    absent_section = document.split(
        "## 10. Deliberately absent from I1 physical schema",
        1,
    )[1]
    for field in forbidden_as_schema:
        assert field in absent_section

    assert (
        "No scheduling, deadline, priority, dependency, hierarchy, recurrence, or "
        "reminder columns"
    ) in document
    assert "Group ownership/sharing/roles" in document
    assert "sync clocks, change branches, history/audit tables" in document


def test_erd_preserves_ownership_creator_provenance_separation():
    document = _read(ERD_PATH)

    assert "ownership         -> items.owner_user_id" in document
    assert "creator           -> items.created_by_user_id" in document
    assert "source/provenance -> item_sources" in document
    assert "Neither creator nor Source is used as an ownership shortcut" in document
