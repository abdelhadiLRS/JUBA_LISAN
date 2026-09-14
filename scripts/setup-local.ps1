[CmdletBinding()]
param(
    [switch]$Force,
    [switch]$Start
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$envExample = Join-Path $root '.env.example'
$envPath = Join-Path $root '.env'

if (-not (Test-Path $envExample)) {
    throw "Missing .env.example at $envExample"
}

if ((Test-Path $envPath) -and -not $Force) {
    Write-Host "`.env already exists. Keeping the existing local configuration." -ForegroundColor Yellow
} else {
    function New-LocalSecret {
        param([int]$Length = 48)
        $raw = (([guid]::NewGuid().ToString('N')) + ([guid]::NewGuid().ToString('N')))
        return $raw.Substring(0, [Math]::Min($Length, $raw.Length))
    }

    $content = Get-Content -Raw -Path $envExample
    $content = $content.Replace('CHANGE_ME_DB_PASSWORD', (New-LocalSecret))
    $content = $content.Replace('CHANGE_ME_REDIS_PASSWORD', (New-LocalSecret))
    $content = $content.Replace('CHANGE_ME_SECRET_KEY_32_CHARS_MINIMUM', (New-LocalSecret))

    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($envPath, $content, $utf8NoBom)

    Write-Host "Created local environment: $envPath" -ForegroundColor Green
    Write-Host "Generated unique PostgreSQL, Redis, and JWT secrets." -ForegroundColor Green
}

if ($Start) {
    if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
        throw "Docker CLI was not found. Install/start Docker Desktop first."
    }

    Push-Location $root
    try {
        Write-Host "Building and starting JUBA LISAN; waiting for healthy services..." -ForegroundColor White
        docker compose up -d --build --wait --wait-timeout 180
        Write-Host "JUBA LISAN is ready at http://localhost:3000" -ForegroundColor Green
        Write-Host "Run diagnostics with: powershell -ExecutionPolicy Bypass -File .\scripts\diagnose-local.ps1" -ForegroundColor Gray
        docker compose ps
    }
    finally {
        Pop-Location
    }
}
