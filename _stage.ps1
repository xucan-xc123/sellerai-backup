$ErrorActionPreference = 'Continue'
Set-Location 'D:\AIAgent\sellerai-backup'

# Stage .gitignore update
git add .gitignore

Write-Host '=== final staged count ==='
(git diff --cached --name-only).Count

Write-Host '=== staged top-level summary ==='
git diff --cached --name-only | ForEach-Object { ($_ -split '/')[0] } | Group-Object | Sort-Object Count -Descending | Select-Object Name, Count | Format-Table -AutoSize

Write-Host '=== confirm no junk/sensitive staged ==='
$bad = git diff --cached --name-only | Where-Object { $_ -eq '$null' -or $_ -match '^temp-repo' -or $_ -match '^tmp-push' -or $_ -match '\.env$' -or $_ -match 'check_balance|MEMORY\.md|密钥安全审计|VERCEL部署规范' }
if ($bad) { Write-Host 'WARNING:'; $bad } else { Write-Host 'CLEAN' }
