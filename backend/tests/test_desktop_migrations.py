import os
import subprocess
import sys
from pathlib import Path


def test_full_alembic_upgrade_works_on_sqlite(tmp_path):
    backend_dir = Path(__file__).resolve().parents[1]
    data_dir = tmp_path / "juba-lisan"
    db_path = data_dir / "database" / "juba_lisan.db"
    data_dir.mkdir(parents=True)
    db_path.parent.mkdir(parents=True)

    env = os.environ.copy()
    env.update(
        {
            "DESKTOP_MODE": "true",
            "DATA_DIR": str(data_dir),
            "DATABASE_URL": f"sqlite+aiosqlite:///{db_path}",
            "REDIS_ENABLED": "false",
            "REDIS_URL": "",
            "SECRET_KEY": "desktop-test-secret",
        }
    )

    result = subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        cwd=backend_dir,
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )

    assert result.returncode == 0, (
        "Alembic SQLite upgrade failed.\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )
    assert db_path.exists()



def test_full_alembic_upgrade_enforces_progress_and_competency_constraints(tmp_path):
    backend_dir = Path(__file__).resolve().parents[1]
    data_dir = tmp_path / "juba-lisan-constraints"
    db_path = data_dir / "database" / "juba_lisan.db"
    db_path.parent.mkdir(parents=True)

    env = os.environ.copy()
    env.update(
        {
            "DESKTOP_MODE": "true",
            "DATA_DIR": str(data_dir),
            "DATABASE_URL": f"sqlite+aiosqlite:///{db_path}",
            "REDIS_ENABLED": "false",
            "REDIS_URL": "",
            "SECRET_KEY": "desktop-test-secret",
        }
    )

    result = subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        cwd=backend_dir,
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    assert result.returncode == 0, (
        "Alembic SQLite upgrade failed.\\n"
        f"stdout:\\n{result.stdout}\\n"
        f"stderr:\\n{result.stderr}"
    )

    import sqlite3

    def unique_index_columns(connection, table_name):
        columns = set()
        for row in connection.execute(f"PRAGMA index_list({table_name})"):
            if row[2]:
                index_name = row[1]
                index_columns = tuple(
                    item[2]
                    for item in connection.execute(f"PRAGMA index_info({index_name})")
                )
                columns.add(index_columns)
        return columns

    with sqlite3.connect(db_path) as connection:
        progress_columns = {
            row[1]: row[3] for row in connection.execute("PRAGMA table_info(progress)")
        }
        competency_columns = {
            row[1]: row[3]
            for row in connection.execute("PRAGMA table_info(user_competencies)")
        }
        assert progress_columns["study_plan_id"] == 1
        assert competency_columns["study_plan_id"] == 1

        assert ("user_id", "study_plan_id", "date") in unique_index_columns(
            connection, "progress"
        )
        assert (
            "user_id",
            "study_plan_id",
            "unit_id",
            "competency_text",
        ) in unique_index_columns(connection, "user_competencies")
