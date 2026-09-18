$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$Frontend = Join-Path $RepoRoot "frontend"

Write-Host "== JUBA LISAN Desktop Build =="

if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    throw "Node.js is required to build the Windows desktop application."
}
if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    throw "npm is required to build the Windows desktop application."
}
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python is required only while building the bundled FastAPI backend."
}

& (Join-Path $PSScriptRoot "build-desktop-backend.ps1")

$BackendExe = Join-Path $Frontend "desktop-backend\juba-lisan-backend.exe"
if (-not (Test-Path $BackendExe)) {
    throw "Bundled backend executable was not produced: $BackendExe"
}

Set-Location $Frontend
if (Test-Path "package-lock.json") {
    npm ci
} else {
    npm install
}

$env:BUILD_TARGET = "desktop"
npm run build
npx electron-builder --win nsis portable

Write-Host ""
Write-Host "JUBA LISAN Windows artifacts are in: $Frontend\dist"
Get-ChildItem -Path (Join-Path $Frontend "dist") -File |
    Where-Object { $_.Extension -in ".exe", ".blockmap", ".yml" } |
    Select-Object Name, Length, LastWriteTime
