import os
import subprocess
import sys
from pathlib import Path


def test_full_alembic_upgrade_works_on_sqlite(tmp_path):
    backend_dir = Path(__file__).resolve().parents[1]
    data_dir = tmp_path / "juba-lisan"
    db_path = data_dir / "database" / "juba_lisan.db"
    data_dir.mkdir(parents=True)

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
