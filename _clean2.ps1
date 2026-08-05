$ErrorActionPreference = 'Continue'
Set-Location 'D:\AIAgent\sellerai-backup'

# Unstage junk entries (they were never in HEAD, so reset is right)
git reset -q -- '$null' 2>&1 | Out-Null
git reset -q -- 'temp-repo' 2>&1 | Out-Null
git reset -q -- 'temp-repo-' 2>&1 | Out-Null
git reset -q -- 'tmp-push' 2>&1 | Out-Null

# Unstage 20260802 sensitive files
git reset -q -- '20260802/backend/.env' 2>&1 | Out-Null
git reset -q -- '20260802/backend/check_balance.py' 2>&1 | Out-Null
git reset -q -- '20260802/MEMORY.md' 2>&1 | Out-Null

Write-Host '=== junk/sensitive still staged? ==='
$still = git diff --cached --name-only | Where-Object { $_ -match 'temp-repo|tmp-push' -or $_ -eq '$null' -or $_ -match '20260802/(backend/\.env|backend/check_balance|MEMORY)' }
if ($still) { $still } else { Write-Host 'NONE - clean' }

Write-Host '=== remaining staged count ==='
(git diff --cached --name-only).Count

Write-Host '=== top-level staged entries ==='
git diff --cached --name-only | ForEach-Object { ($_ -split '/')[0] } | Group-Object | Sort-Object Count -Descending | Select-Object Name, Count | Format-Table -AutoSize
