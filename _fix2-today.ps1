$ErrorActionPreference = 'Continue'
Set-Location 'D:\AIAgent\sellerai-backup'

# Remove remaining tracked VERCEL files via glob (avoid CJK encoding issue in args)
git rm --cached --ignore-unmatch '20260806/deploy/VERCEL*.md' '20260807/deploy/VERCEL*.md' '20260808/deploy/VERCEL*.md' 2>&1
Write-Host '=== rm done ==='

# Verify index clean of sensitive for 06-08 + 09
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Write-Host '=== sensitive still tracked in 20260806-09? ==='
git -c core.quotepath=false ls-files -- '20260806' '20260807' '20260808' '20260809' | Where-Object { $_ -match '\.env$|MEMORY\.md$|check_balance|VERCEL|环境变量|密钥' }
Write-Host '(empty = clean)'

# Amend the previous commit so the fix ships in one commit
git -c user.name='sellerai-backup' -c user.email='backup@local' commit --amend --no-edit 2>&1
if ($LASTEXITCODE -ne 0) { Write-Host 'AMEND FAILED'; exit 1 }
Write-Host '=== amend done ==='

Write-Host '=== new HEAD ==='
git log --oneline -1
