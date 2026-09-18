from pathlib import Path

from sqlalchemy.dialects.sqlite import dialect as sqlite_dialect
from sqlalchemy.schema import CreateIndex, CreateTable

from app.core.database import Base, get_database_url


def test_default_database_url_is_desktop_sqlite():
    url = get_database_url()
    assert url.startswith("sqlite+aiosqlite:///")
    assert url.endswith(".db")


def test_all_models_compile_for_sqlite():
    dialect = sqlite_dialect()

    for table in Base.metadata.sorted_tables:
        CreateTable(table).compile(dialect=dialect)
        for index in table.indexes:
            CreateIndex(index).compile(dialect=dialect)


def test_database_path_uses_juba_lisan_data_directory():
    url = get_database_url()
    assert Path(url.removeprefix("sqlite+aiosqlite:///")).name == "juba_lisan.db"
