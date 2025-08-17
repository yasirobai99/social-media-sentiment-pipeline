# Creates a timestamped compressed dump in .\backups
$ErrorActionPreference = "Stop"
$date = Get-Date -Format "yyyyMMdd_HHmmss"
if (!(Test-Path -Path ".\backups")) { New-Item -ItemType Directory -Path ".\backups" | Out-Null }
$dumpPath = ".\backups\sentiment_$date.dump"
# Prefer .env value if available in the shell; fallback to default
$env:PGPASSWORD = $env:POSTGRES_PASSWORD
if (-not $env:PGPASSWORD) { $env:PGPASSWORD = "postgres123" }
docker exec -e PGPASSWORD=$env:PGPASSWORD -t social-media-sentiment-pipeline-postgres-1 pg_dump -U postgres -Fc sentiment > $dumpPath
Write-Host "Backup created:" $dumpPath
