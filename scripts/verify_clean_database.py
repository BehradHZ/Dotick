import os
import subprocess
import sys
import uuid
from pathlib import Path

import psycopg
from dotenv import load_dotenv
from psycopg import sql

REPO_ROOT = Path(__file__).resolve().parents[1]
MANAGE_PY = REPO_ROOT / "apps" / "api" / "manage.py"
REQUIRED_POSTGRES_SETTINGS = ("PGHOST", "PGPORT", "PGUSER", "PGPASSWORD")


def postgres_settings() -> dict[str, str]:
    load_dotenv(REPO_ROOT / ".env")

    missing = [name for name in REQUIRED_POSTGRES_SETTINGS if not os.getenv(name)]
    if missing:
        names = ", ".join(missing)
        raise RuntimeError(f"Missing required PostgreSQL settings: {names}")

    return {name: os.environ[name] for name in REQUIRED_POSTGRES_SETTINGS}


def connect(database: str, settings: dict[str, str]):
    return psycopg.connect(
        dbname=database,
        host=settings["PGHOST"],
        port=settings["PGPORT"],
        user=settings["PGUSER"],
        password=settings["PGPASSWORD"],
        autocommit=True,
    )


def run_manage_py(database: str, *args: str) -> None:
    environment = os.environ.copy()
    environment["PGDATABASE"] = database

    subprocess.run(
        [sys.executable, str(MANAGE_PY), *args],
        cwd=REPO_ROOT,
        env=environment,
        check=True,
    )


def main() -> int:
    settings = postgres_settings()
    admin_database = os.getenv("PGADMIN_DATABASE", "postgres")
    verification_database = f"dotick_verify_{uuid.uuid4().hex[:12]}"
    created = False

    try:
        with connect(admin_database, settings) as connection:
            connection.execute(
                sql.SQL("CREATE DATABASE {}").format(sql.Identifier(verification_database))
            )
            created = True

        print(f"Created fresh PostgreSQL database: {verification_database}")
        run_manage_py(verification_database, "migrate", "--noinput")
        run_manage_py(verification_database, "migrate", "--check")
        run_manage_py(verification_database, "showmigrations")
        print("Clean PostgreSQL migration verification passed.")
        return 0
    finally:
        if created:
            with connect(admin_database, settings) as connection:
                connection.execute(
                    "SELECT pg_terminate_backend(pid) FROM pg_stat_activity "
                    "WHERE datname = %s AND pid <> pg_backend_pid()",
                    (verification_database,),
                )
                connection.execute(
                    sql.SQL("DROP DATABASE {}").format(sql.Identifier(verification_database))
                )
            print(f"Dropped verification database: {verification_database}")


if __name__ == "__main__":
    raise SystemExit(main())
