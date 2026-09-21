import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
API_ROOT = REPO_ROOT / "apps" / "api"
MANAGE_PY = API_ROOT / "manage.py"
sys.path.insert(0, str(API_ROOT))

from config.migration_checks import migration_history_violations  # noqa: E402


def run_manage_py(*args: str) -> int:
    result = subprocess.run(
        [sys.executable, str(MANAGE_PY), *args],
        cwd=REPO_ROOT,
        check=False,
    )
    return result.returncode


def check_append_only_migrations() -> int:
    base_ref = os.getenv("MIGRATION_BASE_REF", "").strip()
    if not base_ref or set(base_ref) == {"0"}:
        base_ref = "HEAD^"

    result = subprocess.run(
        [
            "git",
            "diff",
            "--name-status",
            "--find-renames",
            f"{base_ref}...HEAD",
            "--",
            "apps/api/dotick/*/migrations/*.py",
        ],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        return result.returncode

    violations = migration_history_violations(result.stdout)
    if violations:
        print("Historical migrations are immutable; add a new migration instead:", file=sys.stderr)
        for violation in violations:
            print(f"  {violation}", file=sys.stderr)
        return 1

    return 0


def main() -> int:
    history_exit_code = check_append_only_migrations()
    if history_exit_code != 0:
        return history_exit_code

    checks = [
        ("makemigrations", "--check", "--dry-run"),
        ("migrate", "--check"),
    ]

    for check in checks:
        exit_code = run_manage_py(*check)
        if exit_code != 0:
            return exit_code

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
