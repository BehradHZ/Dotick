from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
MODEL_PATH = (
    REPO_ROOT
    / "docs"
    / "reference"
    / "analysis"
    / "folder-list-column-navigation-model.md"
)


def _document():
    return MODEL_PATH.read_text(encoding="utf-8")


def test_navigation_model_traces_increment_1_organization_requirements():
    document = _document()

    for requirement in (
        "SRS-ORG-001",
        "SRS-ORG-002",
        "SRS-ORG-003",
        "SRS-ORG-004",
        "SRS-ORG-005",
        "SRS-ORG-006",
        "SRS-NFR-SEC-003",
    ):
        assert requirement in document


def test_navigation_model_preserves_canonical_hierarchy_and_folder_optionality():
    document = _document()

    required_phrases = (
        "Folder is optional",
        "A List may exist without a Folder",
        "Every List must have a default Column",
        "Folder itself is not a direct Task placement target",
        "Task's direct placement is the Column",
    )
    for phrase in required_phrases:
        assert phrase in document


def test_navigation_model_formalizes_inbox_and_default_column_resolution():
    document = _document()

    required_phrases = (
        "Inbox is a special root-level navigation destination",
        "Inbox/default Column",
        "Create Task with no destination",
        "that List's default Column",
        "placement null",
    )
    for phrase in required_phrases:
        assert phrase in document


def test_navigation_model_keeps_legacy_terms_out_of_domain_hierarchy():
    document = _document()

    assert "`Tab` and `Section` are legacy names for `Column`" in document
    assert "`not_sectioned`" in document
    assert "must not appear as separate domain/navigation entity types" in document


def test_navigation_model_requires_owner_scoped_resource_resolution():
    document = _document()

    required_phrases = (
        "Root discovery is owner-scoped",
        "Navigation cannot bypass ownership validation",
        "foreign List/Column",
        "Column/List mismatch is rejected server-side",
        "reject cross-user access",
    )
    for phrase in required_phrases:
        assert phrase in document


def test_navigation_model_does_not_pull_later_navigation_scope_into_i1():
    document = _document()

    required_exclusions = (
        "Increment 5",
        "List/Kanban/Timeline",
        "Group-owned/shared Folder/List/Column navigation",
        "Increment 7",
        "offline navigation/sync conflict behavior",
        "Increment 6",
        "structural child/hierarchy navigation",
        "Increment 2",
    )
    for phrase in required_exclusions:
        assert phrase in document

    assert "This model does not decide whether I5 uses a sidebar, bottom bar" in document
