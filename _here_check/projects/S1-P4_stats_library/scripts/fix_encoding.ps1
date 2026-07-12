chcp 65001 > $null
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$path = "D:\The Underhood\SEMESTERS\Sprint_Summer2026\Shadow-Oak-summer-sprint-2026\projects\S1-P4_stats_library\scripts\dashboard.py"
$bytes = [System.IO.File]::ReadAllBytes($path)
$text = [System.Text.Encoding]::UTF8.GetString($bytes)

$text = $text -replace 'Ã¢â‚¬â€', '-'
$text = $text -replace 'Ã¢â€šÂ¹', 'Rs '
$text = $text -replace 'â€”', '-'
$text = $text -replace 'â‚¹', 'Rs '
$text = $text -replace '"Nifty 50"\s*:\s*"\^NSEI"', '"Nifty 50": "^NSEI"'

[System.IO.File]::WriteAllText($path, $text, (New-Object System.Text.UTF8Encoding($false)))
Write-Host "Encoding cleaned." -ForegroundColor Green

$remaining = Select-String -Path $path -Pattern "Ã¢|â€"
if ($remaining) {
    Write-Host "STILL DIRTY - lines below need manual check:" -ForegroundColor Red
    $remaining | ForEach-Object { Write-Host $_.Line }
} else {
    Write-Host "File is clean. Safe to launch." -ForegroundColor Green
}