$ErrorActionPreference = 'Continue'
Set-Location 'D:\AIAgent\sellerai-backup'

# 1) Remove already-tracked sensitive files from the index (use --cached so local files stay)
$sensitive = @(
  '20260806/backend/.env','20260806/backend/check_balance.py','20260806/MEMORY.md','20260806/deploy/VERCEL部署规范_2026-07-16.md','20260806/deploy/环境变量配置.md','20260806/reports/密钥安全审计-2026-07-22.md',
  '20260807/backend/.env','20260807/backend/check_balance.py','20260807/MEMORY.md','20260807/deploy/VERCEL部署规范_2026-07-16.md','20260807/deploy/环境变量配置.md','20260807/reports/密钥安全审计-2026-07-22.md',
  '20260808/backend/.env','20260808/backend/check_balance.py','20260808/MEMORY.md','20260808/deploy/VERCEL部署规范_2026-07-16.md','20260808/deploy/环境变量配置.md','20260808/reports/密钥安全审计-2026-07-22.md'
)
foreach ($f in $sensitive) {
  git rm --cached --quiet --ignore-unmatch $f 2>&1
}
Write-Host '=== staged removal of old sensitive files done ==='

# 2) Stage everything (gitignore now excludes sensitive for 06-09 + future)
git add -A
Write-Host '=== git add -A done ==='

# 3) Verify no sensitive file in index for 06-09
Write-Host '=== check: sensitive files still staged? ==='
git diff --cached --name-only | Where-Object { $_ -match '2026080[6-9].*(\.env$|MEMORY|check_balance|VERCEL|环境变量|密钥)' }
Write-Host '(empty above = safe)'

# 4) Commit
git -c user.name='sellerai-backup' -c user.email='backup@local' commit -m "Daily backup 20260809 + fix: remove leaked sensitive files (08-06/07/08) from tracking, harden gitignore" 2>&1
if ($LASTEXITCODE -ne 0) { Write-Host 'COMMIT FAILED'; exit 1 }
Write-Host '=== commit ok ==='

# 5) Push via proxy
$env:HTTPS_PROXY = 'http://127.0.0.1:7897'
$env:HTTP_PROXY = 'http://127.0.0.1:7897'
git push github master 2>&1
if ($LASTEXITCODE -eq 0) { Write-Host 'PUSH OK' } else { Write-Host 'PUSH FAILED'; exit 1 }
