# automation/test.ps1
# JUBA LISAN - run available checks (lint, typecheck, unit tests)
# Discovers what exists in the repo instead of assuming commands.
$ErrorActionPreference = 'Continue'
$root = Split-Path -Parent $PSScriptRoot
$frontend = Join-Path $root 'frontend'
$backend  = Join-Path $root 'backend'

$failed = $false

# ?? Frontend ??????????????????????????????????????????????????????????????
if (Test-Path (Join-Path $frontend 'package.json')) {
    $pkg = Get-Content (Join-Path $frontend 'package.json') -Raw | ConvertFrom-Json
    Push-Location $frontend

    if (-not (Test-Path (Join-Path $frontend 'node_modules'))) {
        Write-Host '[frontend] node_modules missing - run: npm ci' -ForegroundColor Yellow
    } else {
        if ($pkg.scripts.lint -and (Get-Command npx -ErrorAction SilentlyContinue)) {
            Write-Host '[frontend] lint...' -ForegroundColor Cyan
            npx eslint src/ --max-warnings=0
            if ($LASTEXITCODE -ne 0) { $failed = $true }
        }
        if (Test-Path (Join-Path $frontend 'tsconfig.json')) {
            Write-Host '[frontend] typecheck...' -ForegroundColor Cyan
            npx tsc --noEmit
            if ($LASTEXITCODE -ne 0) { $failed = $true }
        }
        if ($pkg.scripts.'test:run') {
            Write-Host '[frontend] unit tests...' -ForegroundColor Cyan
            npm run test:run
            if ($LASTEXITCODE -ne 0) { $failed = $true }
        }
    }
    Pop-Location
}

# ?? Backend (only when a local environment is available) ?????????????????
$pytestCandidates = @(
    (Join-Path $root '.venv/Scripts/python.exe'),
    (Join-Path $root 'backend/.venv/Scripts/python.exe')
) | Where-Object { Test-Path $_ }

if ($pytestCandidates.Count -gt 0 -and (Test-Path (Join-Path $backend 'tests'))) {
    $python = $pytestCandidates[0]
    Write-Host "[backend] pytest via $python..." -ForegroundColor Cyan
    Push-Location $backend
    & $python -m pytest -q
    if ($LASTEXITCODE -ne 0) { $failed = $true }
    Pop-Location
} else {
    Write-Host '[backend] no local Python env detected - skipped (CI runs backend tests).' -ForegroundColor DarkGray
}

if ($failed) {
    Write-Host "`nRESULT: FAILED" -ForegroundColor Red
    exit 1
}
Write-Host "`nRESULT: ALL PASSED" -ForegroundColor Green
exit 0
