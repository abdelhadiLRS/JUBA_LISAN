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

$StaticSource = Join-Path $Frontend ".next\static"
if (-not (Test-Path $StaticSource)) {
    throw "Next.js static assets were not produced: $StaticSource"
}

$StaticChunks = Get-ChildItem -Path $StaticSource -Recurse -File -ErrorAction SilentlyContinue |
    Where-Object { $_.Extension -in ".js", ".css" } |
    Select-Object -First 1
if (-not $StaticChunks) {
    throw "Next.js standalone build contains no JavaScript or CSS static assets: $StaticSource"
}

$DesktopRenderer = Join-Path $Frontend "next-standalone"
if (Test-Path $DesktopRenderer) {
    Remove-Item $DesktopRenderer -Recurse -Force
}
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

# next-intl message files live at the repository root. They are loaded at
# runtime so Turbopack does not need to resolve modules outside the frontend
# workspace; package them beside the standalone Next.js server.
$MessagesSource = Join-Path $RepoRoot "messages"
$MessagesTarget = Join-Path $DesktopRenderer "messages"
if (-not (Test-Path $MessagesSource)) {
    throw "Locale messages directory was not found: $MessagesSource"
}
Copy-Item $MessagesSource $MessagesTarget -Recurse -Force

$RequiredLocales = @("en", "es", "fr", "pt", "de", "it", "pl", "nl", "ro", "ru")
foreach ($Locale in $RequiredLocales) {
    $LocaleFile = Join-Path $MessagesTarget ($Locale + ".json")
    if (-not (Test-Path $LocaleFile)) {
        throw "Required locale message file was not packaged: $LocaleFile"
    }
}

$RendererServer = Join-Path $DesktopRenderer "server.js"
if (-not (Test-Path $RendererServer)) {
    throw "Desktop renderer server was not copied to the packaging directory: $RendererServer"
}

npx electron-builder --win nsis portable

$Dist = Join-Path $Frontend "dist"
$Installer = Get-ChildItem -Path $Dist -Filter "*.exe" -File |
    Where-Object { $_.Name -match "Setup .*\.exe$" -and $_.Name -notmatch "__uninstaller\.exe$" } |
    Select-Object -First 1
$Portable = Get-ChildItem -Path $Dist -Filter "*.exe" -File |
    Where-Object { $_.Name -notmatch "Setup .*\.exe$" -and $_.Name -notmatch "__uninstaller\.exe$" } |
    Select-Object -First 1

if (-not $Installer) {
    throw "Windows NSIS installer was not produced in: $Dist"
}
if (-not $Portable) {
    throw "Windows portable executable was not produced in: $Dist"
}

Write-Host ""
Write-Host "JUBA LISAN Windows artifacts are in: $Frontend\dist"
Get-ChildItem -Path $Dist -File |
    Where-Object { $_.Extension -in ".exe", ".blockmap", ".yml" } |
    Select-Object Name, Length, LastWriteTime
