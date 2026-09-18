# PyInstaller specification for the JUBA LISAN desktop backend.
from pathlib import Path

from PyInstaller.utils.hooks import collect_submodules

# PyInstaller executes .spec files as build configuration code, where
# __file__ is not guaranteed to be defined. The build script invokes
# PyInstaller from the backend directory, so cwd is the stable project root.
ROOT = Path.cwd().resolve()
if not (ROOT / "desktop_server.py").exists():
    raise RuntimeError(f"PyInstaller spec root is invalid: {ROOT}")

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
