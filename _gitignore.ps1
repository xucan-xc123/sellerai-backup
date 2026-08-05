$ErrorActionPreference = 'Continue'
Set-Location 'D:\AIAgent\sellerai-backup'

# Append 20260802 ignore rules if not present
$gitignore = 'D:\AIAgent\sellerai-backup\.gitignore'
$content = Get-Content -LiteralPath $gitignore -Raw -Encoding UTF8

$newRules = @'

# 20260802
20260802/backend/.env
20260802/backend/check_balance.py
20260802/MEMORY.md
20260802/reports/密钥安全审计-2026-07-22.md
20260802/deploy/环境变量配置.md
20260802/deploy/VERCEL部署规范_2026-07-16.md

# junk / temp dirs - never commit
$null
temp-repo
temp-repo-
tmp-push/
'@

if ($content -match '# 20260802') {
  Write-Host '20260802 rules already present'
} else {
  Add-Content -LiteralPath $gitignore -Value $newRules -Encoding UTF8
  Write-Host '20260802 rules appended'
}

Write-Host '=== verify ignore works ==='
git check-ignore -v '20260802/backend/.env' '20260802/MEMORY.md' '$null' 'temp-repo' 'tmp-push/x' 2>&1

Write-Host '=== git status short after ignore ==='
$st = git status --porcelain
Write-Host ("total: " + $st.Count)
$st | Where-Object { $_ -match 'temp-repo|tmp-push|^\?\? \$null' } | Select-Object -First 6
