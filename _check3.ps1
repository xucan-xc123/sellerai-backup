$ErrorActionPreference = 'Stop'
Set-Location 'D:\AIAgent\sellerai-backup'

Write-Host '=== 20260802 sensitive files present? ==='
$paths = @(
  '20260802/backend/.env',
  '20260802/backend/check_balance.py',
  '20260802/MEMORY.md',
  '20260802/reports/密钥安全审计-2026-07-22.md',
  '20260802/deploy/环境变量配置.md',
  '20260802/deploy/VERCEL部署规范_2026-07-16.md'
)
foreach ($p in $paths) {
  if (Test-Path -LiteralPath $p) { Write-Host ("EXISTS: " + $p) } else { Write-Host ("absent: " + $p) }
}

Write-Host '=== $null file content (literal path) ==='
Get-Content -LiteralPath 'D:\AIAgent\sellerai-backup\$null' -ErrorAction SilentlyContinue

Write-Host '=== staged sensitive check (20260802) ==='
git diff --cached --name-only | Where-Object { $_ -match '\.env$|check_balance|MEMORY\.md|密钥安全审计|环境变量配置|VERCEL部署规范' }
