# automation/status.ps1
# JUBA LISAN - repository status summary
$ErrorActionPreference = 'Continue'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

Write-Host "=== JUBA LISAN - STATUS ===" -ForegroundColor Cyan

$branch = git branch --show-current
Write-Host "Branch: $branch"

$sync = git status -sb | Select-Object -First 1
Write-Host $sync

$changes = git status --porcelain
if ($changes) {
    Write-Host "`nWorking tree (not clean):" -ForegroundColor Yellow
    $changes | ForEach-Object { Write-Host "  $_" }
} else {
    Write-Host "`nWorking tree clean." -ForegroundColor Green
}

$roadmap = Join-Path $root 'DEVELOPMENT_ROADMAP.md'
if (Test-Path $roadmap) {
    Write-Host "`nRoadmap phase summary:"
    Select-String -Path $roadmap -Pattern '^### Phase' | ForEach-Object {
        Write-Host "  $($_.Line)"
    }
}

$versionLine = (Get-Content (Join-Path $root 'specs/version.md') -TotalCount 4)[2]
$version = $versionLine.Trim('*', ' ')
$version = $version.Trim()
Write-Host ''
Write-Host "Version: $version"
