$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$Frontend = Join-Path $RepoRoot "frontend"

& (Join-Path $PSScriptRoot "build-desktop-backend.ps1")

Set-Location $Frontend
npm install
npm run build
npx electron-builder --win

Write-Host ""
Write-Host "JUBA LISAN Windows artifacts are in: $Frontend\dist"
