$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$Backend = Join-Path $RepoRoot "backend"
$Venv = Join-Path $Backend ".venv"

Set-Location $Backend

if (!(Test-Path $Venv)) {
  python -m venv .venv
}

& "$Venv\Scripts\python.exe" -m pip install --upgrade pip
& "$Venv\Scripts\python.exe" -m pip install -r requirements.txt pyinstaller

if (Test-Path "build") { Remove-Item "build" -Recurse -Force }
if (Test-Path "dist") { Remove-Item "dist" -Recurse -Force }

& "$Venv\Scripts\pyinstaller.exe" --clean --noconfirm "juba-lisan-backend.spec"

$Target = Join-Path $RepoRoot "frontend\desktop-backend"
if (Test-Path $Target) { Remove-Item $Target -Recurse -Force }
New-Item -ItemType Directory -Path $Target | Out-Null
Copy-Item (Join-Path $Backend "dist\juba-lisan-backend.exe") $Target

Write-Host "Desktop backend ready: $Target\juba-lisan-backend.exe"
