$root = $PSScriptRoot
$projects = @(
    "projects\sovereignfinance",
    "projects\S1-P2_nifftyvault",
    "projects\S1-P3_oakledger",
    "projects\S1-P4_stats_library"
)

foreach ($p in $projects) {
    $full = Join-Path $root $p
    Write-Host "`n===== VERIFYING $p =====" -ForegroundColor Cyan
    Push-Location $full

    Write-Host "-- pytest --" -ForegroundColor Yellow
    pytest

    Write-Host "-- ruff --" -ForegroundColor Yellow
    ruff check .

    Write-Host "-- black --" -ForegroundColor Yellow
    black --check .

    Write-Host "-- mypy --" -ForegroundColor Yellow
    mypy src

    Pop-Location
}
Write-Host "`n===== VERIFICATION LOOP COMPLETE =====" -ForegroundColor Green
