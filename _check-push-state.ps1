$ErrorActionPreference = 'Continue'
Set-Location 'D:\AIAgent\sellerai-backup'
$env:HTTPS_PROXY = 'http://127.0.0.1:7897'
$env:HTTP_PROXY = 'http://127.0.0.1:7897'

Write-Host '=== local HEAD ==='
git log --oneline -1
Write-Host '=== remote ref (proxy fetch) ==='
git ls-remote github master 2>&1 | Select-Object -First 3
Write-Host "ls-remote exit=$LASTEXITCODE"
Write-Host '=== status ==='
git status -sb | Select-Object -First 2
