import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
USE_CASE_PATH = REPO_ROOT / "docs" / "reference" / "analysis" / "authentication-use-cases.md"

EXPECTED_USE_CASE_IDS = {f"UC-AUTH-{number:03}" for number in range(1, 13)}
IN_SCOPE_AUTH_REQUIREMENTS = {f"SRS-AUTH-{number:03}" for number in range(1, 14)}
PRESENTATION_ONLY_REQUIREMENTS = {"SRS-AUTH-014", "SRS-AUTH-015"}


def _document():
    return USE_CASE_PATH.read_text(encoding="utf-8")


def test_authentication_use_case_ids_are_stable_and_complete():
    document = _document()
    headings = set(re.findall(r"^## (UC-AUTH-\d{3}) — ", document, re.MULTILINE))

    assert headings == EXPECTED_USE_CASE_IDS

    for use_case_id in EXPECTED_USE_CASE_IDS:
        assert document.count(f"## {use_case_id} — ") == 1


def test_authentication_srs_family_has_explicit_analysis_trace():
    document = _document()
    referenced = set(re.findall(r"SRS-AUTH-\d{3}", document))

    assert IN_SCOPE_AUTH_REQUIREMENTS <= referenced
    assert PRESENTATION_ONLY_REQUIREMENTS <= referenced
    assert "Profile Picture" in document
    assert "rather than authentication" in document


def test_current_scope_exclusions_are_explicit():
    document = _document()

    assert "TOTP" in document
    assert "SMS-based second-factor" in document
    assert "external identity provider other than Google" in document
    assert "authorization for shared/group resources" in document


def test_cross_method_identity_and_revocation_invariants_are_formalized():
    document = _document()

    required_phrases = (
        "stable internal User identity",
        "none replaces it",
        "server-revocable",
        "do **not** silently merge/link",
        "same internal User/session boundary",
    )
    for phrase in required_phrases:
        assert phrase in document
