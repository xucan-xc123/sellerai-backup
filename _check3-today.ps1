$ErrorActionPreference = 'Continue'
Set-Location 'D:\AIAgent\sellerai-backup'

Write-Host '=== recent commits touching sensitive files ==='
git log --oneline -8

Write-Host ''
Write-Host '=== files in last 3 commits (sensitive check) ==='
git log --name-only --format='COMMIT %h %s' -3 | Where-Object { $_ -match '\.env$|MEMORY|check_balance|VERCEL|环境变量|密钥' -or $_ -match '^COMMIT' }

Write-Host ''
Write-Host '=== is .env content in repo history? ==='
git log --all --oneline -- '20260808/backend/.env' '20260807/backend/.env' '20260806/backend/.env' | Select-Object -First 5

Write-Host ''
Write-Host '=== 20260809 gitignore check: what would be added ==='
git add -n --dry-run 20260809/ 2>&1 | Select-Object -First 40
