import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MANAGE_PY = REPO_ROOT / "apps" / "api" / "manage.py"


def run_manage_py(*args: str) -> int:
    result = subprocess.run(
        [sys.executable, str(MANAGE_PY), *args],
        cwd=REPO_ROOT,
        check=False,
    )
    return result.returncode


def main() -> int:
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
