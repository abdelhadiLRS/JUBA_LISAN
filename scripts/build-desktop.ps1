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

$NextStandalone = Join-Path $Frontend ".next\standalone"
if (-not (Test-Path (Join-Path $NextStandalone "server.js"))) {
    throw "Next.js standalone server was not produced: $NextStandalone\server.js"
}
$DesktopRenderer = Join-Path $Frontend "next-standalone"
if (Test-Path $DesktopRenderer) { Remove-Item $DesktopRenderer -Recurse -Force }
Copy-Item $NextStandalone $DesktopRenderer -Recurse -Force

$StaticSource = Join-Path $Frontend ".next\static"
$StaticTarget = Join-Path $DesktopRenderer ".next\static"
if (Test-Path $StaticSource) {
    New-Item -ItemType Directory -Force -Path (Split-Path $StaticTarget) | Out-Null
    Copy-Item $StaticSource $StaticTarget -Recurse -Force
}
$PublicSource = Join-Path $Frontend "public"
$PublicTarget = Join-Path $DesktopRenderer "public"
if (Test-Path $PublicSource) {
    Copy-Item $PublicSource $PublicTarget -Recurse -Force
}

npx electron-builder --win nsis portable

$Dist = Join-Path $Frontend "dist"
$Installer = Get-ChildItem -Path $Dist -Filter "*.exe" -File | Where-Object { $_.Name -notmatch '\.portable\.exe } | Select-Object -First 1
$Portable = Get-ChildItem -Path $Dist -Filter "*.portable.exe" -File | Select-Object -First 1
if (-not $Installer) { throw "Windows NSIS installer was not produced in: $Dist" }
if (-not $Portable) { throw "Windows portable executable was not produced in: $Dist" }

Write-Host ""
Write-Host "JUBA LISAN Windows artifacts are in: $Frontend\dist"
Get-ChildItem -Path (Join-Path $Frontend "dist") -File |
    Where-Object { $_.Extension -in ".exe", ".blockmap", ".yml" } |
    Select-Object Name, Length, LastWriteTime
 } | Select-Object -First 1
$Portable = Get-ChildItem -Path $Dist -Filter "*.portable.exe" -File | Select-Object -First 1
if (-not $Installer) { throw "Windows NSIS installer was not produced in: $Dist" }
if (-not $Portable) { throw "Windows portable executable was not produced in: $Dist" }

Write-Host ""
Write-Host "JUBA LISAN Windows artifacts are in: $Frontend\dist"
Get-ChildItem -Path (Join-Path $Frontend "dist") -File |
    Where-Object { $_.Extension -in ".exe", ".blockmap", ".yml" } |
    Select-Object Name, Length, LastWriteTime
