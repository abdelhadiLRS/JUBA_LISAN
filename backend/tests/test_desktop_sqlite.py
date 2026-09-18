from pathlib import Path

from sqlalchemy.dialects.sqlite import dialect as sqlite_dialect
from sqlalchemy.schema import CreateIndex, CreateTable

from app.core.config import settings
from app.core.database import Base, get_database_url


def test_desktop_database_url_is_sqlite(monkeypatch, tmp_path):
    monkeypatch.setattr(settings, "DATABASE_URL", "")
    monkeypatch.setattr(settings, "DESKTOP_MODE", True)
    monkeypatch.setattr(settings, "DATA_DIR", str(tmp_path))

    url = get_database_url()
    assert url.startswith("sqlite+aiosqlite:///")
    assert url.endswith(".db")
    assert Path(url.removeprefix("sqlite+aiosqlite:///")).name == "juba_lisan.db"


def test_all_models_compile_for_sqlite():
    dialect = sqlite_dialect()

    for table in Base.metadata.sorted_tables:
        CreateTable(table).compile(dialect=dialect)
        for index in table.indexes:
            CreateIndex(index).compile(dialect=dialect)
