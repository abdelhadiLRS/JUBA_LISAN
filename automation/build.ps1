# automation/build.ps1
# JUBA LISAN - run the production build where supported
$ErrorActionPreference = 'Continue'
$root = Split-Path -Parent $PSScriptRoot
$frontend = Join-Path $root 'frontend'
$failed = $false

if (Test-Path (Join-Path $frontend 'package.json')) {
    $pkg = Get-Content (Join-Path $frontend 'package.json') -Raw | ConvertFrom-Json
    if ($pkg.scripts.build) {
        Push-Location $frontend
        if (-not (Test-Path (Join-Path $frontend 'node_modules'))) {
            Write-Host '[frontend] node_modules missing - run: npm ci' -ForegroundColor Yellow
            $failed = $true
        } else {
            Write-Host '[frontend] build...' -ForegroundColor Cyan
            npm run build
            if ($LASTEXITCODE -ne 0) { $failed = $true }
        }
        Pop-Location
    }
}

if ($failed) {
    Write-Host "`nBUILD: FAILED" -ForegroundColor Red
    exit 1
}
Write-Host "`nBUILD: OK" -ForegroundColor Green
exit 0
