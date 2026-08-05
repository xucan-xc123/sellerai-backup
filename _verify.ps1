$ErrorActionPreference = 'Continue'
Set-Location 'D:\AIAgent\sellerai-backup'

Write-Host '=== exact junk/sensitive staged check ==='
$staged = git diff --cached --name-only
$bad = $staged | Where-Object { $_ -eq '$null' -or $_ -match '^temp-repo' -or $_ -match '^tmp-push' -or $_ -eq '20260802/backend/.env' -or $_ -eq '20260802/backend/check_balance.py' -or $_ -eq '20260802/MEMORY.md' }
if ($bad) { $bad } else { Write-Host 'NONE - all clean' }

Write-Host '=== staged 20260802 top entries sample ==='
$staged | Where-Object { $_ -like '20260802*' } | Select-Object -First 8

Write-Host '=== untracked junk now ==='
git status --porcelain | Where-Object { $_ -match 'temp-repo|tmp-push|^\?\? \$null' } | Select-Object -First 6

Write-Host '=== tracked files count in HEAD ==='
(git ls-files).Count
