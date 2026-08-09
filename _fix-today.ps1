$ErrorActionPreference = 'Continue'
Write-Host '=== proxy port 7897 listening? ==='
$conn = Get-NetTCPConnection -LocalPort 7897 -State Listen -ErrorAction SilentlyContinue
if ($conn) { Write-Host 'LISTENING' } else { Write-Host 'NOT LISTENING' }

Write-Host '=== try direct github connectivity (no proxy) ==='
$env:HTTPS_PROXY = ''
$env:HTTP_PROXY = ''
try {
  $r = Invoke-WebRequest -Uri 'https://github.com' -Method Head -TimeoutSec 8 -UseBasicParsing
  Write-Host "DIRECT OK status=$($r.StatusCode)"
} catch {
  Write-Host "DIRECT FAIL: $($_.Exception.Message)"
}

Write-Host '=== tracked sensitive files remaining in 20260806-08 ==='
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Set-Location 'D:\AIAgent\sellerai-backup'
git -c core.quotepath=false ls-files -- '20260806' '20260807' '20260808' | Where-Object { $_ -match '\.env$|MEMORY\.md$|check_balance|VERCEL|环境变量|密钥' }
Write-Host '(empty = clean)'
