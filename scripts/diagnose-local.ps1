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

    Write-Host "[1/6] Validating Docker Compose configuration..." -ForegroundColor White
    docker compose config --quiet
    Write-Host "      OK" -ForegroundColor Green

    Write-Host "[2/6] Reading container status..." -ForegroundColor White
    docker compose ps
    Write-Host ""

    function Test-HttpEndpoint {
        param(
            [string]$Name,
            [string]$Uri,
            [ValidateSet('GET', 'POST')]
            [string]$Method = 'GET',
            [int[]]$ExpectedStatus = @(200),
            [int]$TimeoutSec = 10
        )

        try {
            $response = Invoke-WebRequest -Uri $Uri -Method $Method -TimeoutSec $TimeoutSec -UseBasicParsing
            $status = [int]$response.StatusCode
            if ($ExpectedStatus -contains $status) {
                Write-Host "      $Name -> HTTP $status (expected)" -ForegroundColor Green
                if ($VerboseOutput -and $response.Content) {
                    Write-Host "      $($response.Content.Substring(0, [Math]::Min(300, $response.Content.Length)))" -ForegroundColor Gray
                }
                return $true
            }

            Write-Host "      $Name -> HTTP $status (expected $($ExpectedStatus -join ', '))" -ForegroundColor Red
            return $false
        }
        catch {
            $status = $null
            if ($_.Exception.Response) {
                try { $status = [int]$_.Exception.Response.StatusCode.value__ } catch {}
            }
            if ($status -and ($ExpectedStatus -contains $status)) {
                Write-Host "      $Name -> HTTP $status (expected)" -ForegroundColor Green
                return $true
            }
            if ($status) {
                Write-Host "      $Name -> HTTP $status (expected $($ExpectedStatus -join ', '))" -ForegroundColor Red
            } else {
                Write-Host "      $Name -> unavailable: $($_.Exception.Message)" -ForegroundColor Red
            }
            return $false
        }
    }

    Write-Host "[3/6] Checking frontend/backend health bridge..." -ForegroundColor White
    $healthOk = Test-HttpEndpoint -Name 'Frontend /api/health' -Uri "http://localhost:$FrontendPort/api/health"

    Write-Host "[4/6] Checking public frontend routes..." -ForegroundColor White
    $homeOk = Test-HttpEndpoint -Name 'Frontend /' -Uri "http://localhost:$FrontendPort/"
    $loginOk = Test-HttpEndpoint -Name 'Frontend /login' -Uri "http://localhost:$FrontendPort/login"

    Write-Host "[5/6] Checking auth/config bootstrap endpoints..." -ForegroundColor White
    $configOk = Test-HttpEndpoint -Name 'Frontend /api/config' -Uri "http://localhost:$FrontendPort/api/config"
    # A clean local install has no refresh cookie yet, so 401 is the expected response.
    # The important check is that the endpoint responds promptly instead of hanging.
    $refreshOk = Test-HttpEndpoint -Name 'Frontend /api/auth/refresh' -Uri "http://localhost:$FrontendPort/api/auth/refresh" -Method POST -ExpectedStatus @(401)

    Write-Host "[6/6] Summary" -ForegroundColor White
    if ($healthOk -and $homeOk -and $loginOk -and $configOk -and $refreshOk) {
        Write-Host "      Core HTTP and auth bootstrap checks passed." -ForegroundColor Green
        Write-Host "      Open http://localhost:$FrontendPort and sign in/register." -ForegroundColor Cyan
        exit 0
    }

    Write-Host "      One or more HTTP checks failed." -ForegroundColor Red
    Write-Host "      Backend logs (tail 120):" -ForegroundColor Yellow
    docker compose logs --tail=120 backend
    Write-Host ""
    Write-Host "      Frontend logs (tail 120):" -ForegroundColor Yellow
    docker compose logs --tail=120 frontend
    exit 1
}
finally {
    Pop-Location
}
