# automation/develop.ps1
# JUBA LISAN - one-click development cycle:
#   pull main -> verify tree -> tests -> build -> commit -> push
# Safety rules:
#   - never force push
#   - never push when tests or build fail
#   - never discard unexpected local changes
$ErrorActionPreference = 'Continue'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

function Step($msg) { Write-Host "`n==> $msg" -ForegroundColor Cyan }
function Fail($msg)  { Write-Host "!!  $msg" -ForegroundColor Red }

# 1. Check git
if (-not (Test-Path (Join-Path $root '.git'))) {
    Write-Host 'Not a git repository - aborting.' -ForegroundColor Red
    exit 1
}

# 2. Pull main
$branch = git branch --show-current
if ($branch -ne 'main') {
    Write-Host "Branch is '$branch', expected 'main'. Switching is left to the operator." -ForegroundColor Yellow
}
Write-Host '==> Pulling latest main...'
git pull --ff-only origin main
if ($LASTEXITCODE -ne 0) {
    Write-Host 'Pull failed (diverged or network). Resolve manually - aborting.' -ForegroundColor Red
    exit 1
}

# 3. Check working tree
$status = git status --porcelain
if ($status) {
    Write-Host '==> Working tree has local changes:' -ForegroundColor Yellow
    $status | ForEach-Object { Write-Host "    $_" }
    $answer = Read-Host 'Continue with these changes? (y/N)'
    if ($answer -ne 'y') { Write-Host 'Aborting - nothing was modified.'; exit 0 }
}

# 4. Run checks (test then build)
& (Join-Path $PSScriptRoot 'test.ps1')
if ($LASTEXITCODE -ne 0) {
    Write-Host "`nChecks failed - NOT committing, NOT pushing." -ForegroundColor Red
    exit 1
}
& (Join-Path $PSScriptRoot 'build.ps1')
if ($LASTEXITCODE -ne 0) {
    Write-Host "`nBuild failed - NOT committing, NOT pushing." -ForegroundColor Red
    exit 1
}

# 5. Commit (only if there is something to commit)
$pending = git status --porcelain
if ($pending) {
    $msg = Read-Host 'Commit message (empty = skip commit)'
    if ($msg) {
        git add -A
        git commit -m $msg
        if ($LASTEXITCODE -ne 0) { Write-Host 'Commit failed - aborting.' -ForegroundColor Red; exit 1 }
    }
} else {
    Write-Host 'Nothing to commit.'
}

# 6. Push
$pushAnswer = Read-Host 'Push to origin/main? (y/N)'
if ($pushAnswer -eq 'y') {
    git push origin main
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`nPUSHED OK." -ForegroundColor Green
    } else {
        Write-Host "`nPush FAILED - check network/credentials." -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host 'Push skipped.'
}
