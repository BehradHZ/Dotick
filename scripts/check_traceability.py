"""Fail on duplicate normative SRS IDs or missing/extra matrix family coverage."""

import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    srs = (ROOT / "docs/requirements/srs.md").read_text(encoding="utf-8")
    matrix = (ROOT / "docs/requirements/traceability-matrix.md").read_text(encoding="utf-8")
    ids = re.findall(r"^\| (SRS-[A-Z-]+-\d{3}) \|", srs, re.MULTILINE)
    duplicates = [key for key, count in Counter(ids).items() if count != 1]
    family_section = matrix.split("# 5.", 1)[1].split("# 6.", 1)[0]
    covered = []
    for prefix, start, end, count in re.findall(
        r"^\| `(SRS-[A-Z-]+)-(\d{3})(?:\.\.(\d{3}))?` \| (\d+) \|", family_section, re.MULTILINE
    ):
        family = [f"{prefix}-{number:03}" for number in range(int(start), int(end or start) + 1)]
        if len(family) != int(count):
            raise SystemExit(f"Incorrect matrix count: {prefix}")
        covered.extend(family)
    missing, extra = set(ids) - set(covered), set(covered) - set(ids)
    if not ids or duplicates or missing or extra or len(covered) != len(set(covered)):
        raise SystemExit(
            f"Traceability failed: duplicates={duplicates}; "
            f"missing={sorted(missing)}; extra={sorted(extra)}"
        )
    register = (ROOT / "docs/decision-register.md").read_text(encoding="utf-8")
    decisions = set(re.findall(r"^## (DR-\d+)", register, re.MULTILINE))
    unresolved = set(re.findall(r"DR-\d{3}", matrix)) - decisions
    if unresolved:
        raise SystemExit(f"Unresolved decision references: {sorted(unresolved)}")
    print(
        f"Traceability verified: {len(ids)} unique requirements; exact coverage; valid decisions."
    )


if __name__ == "__main__":
    main()
