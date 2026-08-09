$ErrorActionPreference = 'Continue'
Write-Host '=== git global proxy config ==='
git config --global --get http.proxy
git config --global --get https.proxy
Write-Host '=== system proxy (WinINET) ==='
$reg = Get-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings' -ErrorAction SilentlyContinue
Write-Host "ProxyEnable=$($reg.ProxyEnable) ProxyServer=$($reg.ProxyServer)"
Write-Host '=== env proxies ==='
Write-Host "HTTP_PROXY=$env:HTTP_PROXY HTTPS_PROXY=$env:HTTPS_PROXY"
Write-Host '=== try git push via system (no proxy env) ==='
Set-Location 'D:\AIAgent\sellerai-backup'
Remove-Item Env:HTTPS_PROXY -ErrorAction SilentlyContinue
Remove-Item Env:HTTP_PROXY -ErrorAction SilentlyContinue
git push github master 2>&1 | Select-Object -First 5
Write-Host "exit=$LASTEXITCODE"
