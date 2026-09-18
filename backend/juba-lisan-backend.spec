# PyInstaller specification for the JUBA LISAN desktop backend.
from pathlib import Path

from PyInstaller.utils.hooks import collect_submodules

ROOT = Path.cwd().resolve()\nif not (ROOT / "desktop_server.py").exists():\n    raise RuntimeError(f"PyInstaller must be invoked from the backend directory: {ROOT}")

hiddenimports = collect_submodules("app")

a = Analysis(
    ["desktop_server.py"],
    pathex=[str(ROOT)],
    binaries=[],
    datas=[
        (str(ROOT / "app" / "data"), "app/data"),
        (str(ROOT / "alembic"), "alembic"),
        (str(ROOT / "alembic.ini"), "."),
    ],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="juba-lisan-backend",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)
