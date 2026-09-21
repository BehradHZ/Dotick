import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
USE_CASE_PATH = REPO_ROOT / "docs" / "reference" / "analysis" / "basic-task-use-cases.md"

EXPECTED_USE_CASE_IDS = {f"UC-TASK-{number:03}" for number in range(1, 4)}
REQUIRED_I1_TRACE = {
    "SRS-ORG-002",
    "SRS-ORG-003",
    "SRS-ITEM-002",
    "SRS-ITEM-003",
    "SRS-ITEM-005",
    "SRS-ITEM-006",
    "SRS-ITEM-007",
    "SRS-ITEM-008",
    "SRS-TASK-001",
    "SRS-TASK-014",
    "SRS-TASK-020",
    "SRS-NFR-SEC-003",
}


def _document():
    return USE_CASE_PATH.read_text(encoding="utf-8")


def test_basic_task_use_case_ids_are_stable_and_complete():
    document = _document()
    headings = set(re.findall(r"^## (UC-TASK-\d{3}) — ", document, re.MULTILINE))

    assert headings == EXPECTED_USE_CASE_IDS
    for use_case_id in EXPECTED_USE_CASE_IDS:
        assert document.count(f"## {use_case_id} — ") == 1


def test_basic_task_use_cases_trace_required_i1_behavior():
    document = _document()
    referenced = set(re.findall(r"SRS-(?:ORG|ITEM|TASK|NFR-SEC)-\d{3}", document))

    assert REQUIRED_I1_TRACE <= referenced


def test_basic_task_use_cases_freeze_i1_status_and_unscheduled_scope():
    document = _document()

    for status in ("Todo", "Done", "Won't_Do"):
        assert status in document

    required_scope_phrases = (
        "Task can exist and remain **unscheduled**",
        "Overdue",
        "Missed",
        "Skipped",
        "dependency / `blocked_by`",
        "priority",
        "recurrence and reminders",
        "outside these use cases",
    )
    for phrase in required_scope_phrases:
        assert phrase in document


def test_basic_task_use_cases_formalize_security_and_concurrency_invariants():
    document = _document()

    required_phrases = (
        "stable UUID identity",
        "server-controlled concepts",
        "foreign/private destination",
        "stale edit must not silently overwrite",
        "stable operation identity/idempotency rule",
        "Unknown/server-owned request fields are rejected",
    )
    for phrase in required_phrases:
        assert phrase in document


def test_each_requested_flow_has_preconditions_trigger_and_postconditions():
    document = _document()

    sections = re.split(r"^## UC-TASK-\d{3} — ", document, flags=re.MULTILINE)[1:]
    assert len(sections) == 3

    for section in sections:
        assert "### Preconditions" in section
        assert "### Trigger" in section
        assert "### Postconditions" in section
        assert "flow" in section.lower()
