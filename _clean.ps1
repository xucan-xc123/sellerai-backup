$ErrorActionPreference = 'Stop'
Set-Location 'D:\AIAgent\sellerai-backup'

# 1. Remove junk entries from index
git rm --cached -q -- '$null' 2>$null
git rm --cached -q -r -- temp-repo 2>$null
git rm --cached -q -r -- temp-repo- 2>$null
git rm --cached -q -r -- tmp-push 2>$null

# 2. Remove 20260802 sensitive files from index
git rm --cached -q -- '20260802/backend/.env' 2>$null
git rm --cached -q -- '20260802/backend/check_balance.py' 2>$null
git rm --cached -q -- '20260802/MEMORY.md' 2>$null

Write-Host '=== after removal: junk/sensitive still staged? ==='
git diff --cached --name-only | Where-Object { $_ -match 'temp-repo|tmp-push' -or $_ -eq '$null' -or $_ -match '20260802/(backend/\.env|backend/check_balance|MEMORY)' }

Write-Host '=== remaining staged count ==='
(git diff --cached --name-only).Count

Write-Host '=== working tree status (junk now untracked?) ==='
git status --porcelain | Where-Object { $_ -match 'temp-repo|tmp-push|^\?\? \$null|^\?\? temp' } | Select-Object -First 10
