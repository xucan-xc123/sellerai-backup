$ErrorActionPreference = 'Continue'
Set-Location 'D:\AIAgent\sellerai-backup'

# Test proxy connectivity first
Write-Host '=== test proxy HTTP to github ==='
try {
  $r = Invoke-WebRequest -Uri 'https://github.com' -Method Head -Proxy 'http://127.0.0.1:7897' -TimeoutSec 15 -UseBasicParsing
  Write-Host "PROXY OK status=$($r.StatusCode)"
} catch {
  Write-Host "PROXY TEST FAIL: $($_.Exception.Message)"
}

Write-Host '=== git push via proxy ==='
$env:HTTPS_PROXY = 'http://127.0.0.1:7897'
$env:HTTP_PROXY = 'http://127.0.0.1:7897'
git push github master 2>&1
if ($LASTEXITCODE -eq 0) { Write-Host 'PUSH OK' } else { Write-Host "PUSH FAILED exit=$LASTEXITCODE"; exit 1 }
