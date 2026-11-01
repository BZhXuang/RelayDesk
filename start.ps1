param([switch]$Down, [switch]$Logs)
$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
if ($Down) {
    & docker compose -f (Join-Path $root 'docker-compose.yml') down
    if ($LASTEXITCODE -ne 0) { throw 'Docker Compose stop failed.' }
    return
}
if ($Logs) {
    & docker compose -f (Join-Path $root 'docker-compose.yml') logs -f --tail 100
    if ($LASTEXITCODE -ne 0) { throw 'Docker Compose logs failed.' }
    return
}
if (!(Get-Command docker -ErrorAction SilentlyContinue)) { throw 'Docker Desktop / Docker Engine is required.' }
if (!(Test-Path -LiteralPath (Join-Path $root '.env'))) { throw 'Copy .env.example to .env and set ANTHROPIC_API_KEY and REDIS_PASSWORD first.' }
& docker compose -f (Join-Path $root 'docker-compose.yml') up --build -d
if ($LASTEXITCODE -ne 0) { throw 'Docker Compose startup failed.' }
Write-Host 'RelayDesk is starting. Open http://localhost:5173; API docs: http://localhost:8000/docs.'
