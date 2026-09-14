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
        docker compose up -d --build
        Write-Host "JUBA LISAN is starting at http://localhost:3000" -ForegroundColor Cyan
        Write-Host "Check services with: docker compose ps" -ForegroundColor Gray
    }
    finally {
        Pop-Location
    }
}
