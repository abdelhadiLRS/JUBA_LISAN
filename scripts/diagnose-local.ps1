[CmdletBinding()]
param(
    [int]$FrontendPort = 3000,
    [switch]$VerboseOutput
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root

try {
    Write-Host "JUBA LISAN local diagnostics" -ForegroundColor Cyan
    Write-Host "Root: $root" -ForegroundColor Gray
    Write-Host ""

    if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
        throw "Docker CLI was not found. Install/start Docker Desktop first."
    }

    if (-not (Test-Path '.env')) {
        Write-Host "[WARN] .env is missing. Run: .\scripts\setup-local.ps1" -ForegroundColor Yellow
    }

    Write-Host "[1/5] Validating Docker Compose configuration..." -ForegroundColor White
    docker compose config --quiet
    Write-Host "      OK" -ForegroundColor Green

    Write-Host "[2/5] Reading container status..." -ForegroundColor White
    docker compose ps
    Write-Host ""

    function Test-HttpEndpoint {
        param(
            [string]$Name,
            [string]$Uri,
            [int]$TimeoutSec = 10
        )

        try {
            $response = Invoke-WebRequest -Uri $Uri -Method Get -TimeoutSec $TimeoutSec -UseBasicParsing
            $status = [int]$response.StatusCode
            Write-Host "      $Name -> HTTP $status" -ForegroundColor Green
            if ($VerboseOutput -and $response.Content) {
                Write-Host "      $($response.Content.Substring(0, [Math]::Min(300, $response.Content.Length)))" -ForegroundColor Gray
            }
            return $true
        }
        catch {
            $status = $_.Exception.Response.StatusCode.value__
            if ($status) {
                Write-Host "      $Name -> HTTP $status" -ForegroundColor Yellow
            } else {
                Write-Host "      $Name -> unavailable: $($_.Exception.Message)" -ForegroundColor Red
            }
            return $false
        }
    }

    Write-Host "[3/5] Checking frontend/backend health bridge..." -ForegroundColor White
    $healthOk = Test-HttpEndpoint -Name 'Frontend /api/health' -Uri "http://localhost:$FrontendPort/api/health"

    Write-Host "[4/5] Checking public frontend routes..." -ForegroundColor White
    $homeOk = Test-HttpEndpoint -Name 'Frontend /' -Uri "http://localhost:$FrontendPort/"
    $loginOk = Test-HttpEndpoint -Name 'Frontend /login' -Uri "http://localhost:$FrontendPort/login"

    Write-Host "[5/5] Summary" -ForegroundColor White
    if ($healthOk -and $homeOk -and $loginOk) {
        Write-Host "      Core HTTP checks passed." -ForegroundColor Green
        Write-Host "      Open http://localhost:$FrontendPort and sign in/register." -ForegroundColor Cyan
        exit 0
    }

    Write-Host "      One or more HTTP checks failed." -ForegroundColor Red
    Write-Host "      Useful logs:" -ForegroundColor Yellow
    Write-Host "        docker compose logs --tail=200 backend" -ForegroundColor Gray
    Write-Host "        docker compose logs --tail=200 frontend" -ForegroundColor Gray
    exit 1
}
finally {
    Pop-Location
}
