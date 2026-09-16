import re

MIGRATION_PATH = re.compile(r"^apps/api/dotick/[^/]+/migrations/\d[^/]*\.py$")


def migration_history_violations(diff_output: str) -> list[str]:
    violations = []

    for line in diff_output.splitlines():
        status, *paths = line.split("\t")
        migration_paths = [path for path in paths if MIGRATION_PATH.fullmatch(path)]

        if migration_paths and status != "A":
            violations.extend(f"{status}\t{path}" for path in migration_paths)

    return violations
