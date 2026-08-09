$ErrorActionPreference = 'Continue'
Set-Location 'D:\AIAgent\sellerai-backup'
$env:HTTPS_PROXY = 'http://127.0.0.1:7897'
$env:HTTP_PROXY = 'http://127.0.0.1:7897'
git push github master 2>&1
Write-Host "PUSH_EXIT=$LASTEXITCODE"
if ($LASTEXITCODE -eq 0) { Write-Host 'PUSH OK' } else { Write-Host 'PUSH FAILED' }
