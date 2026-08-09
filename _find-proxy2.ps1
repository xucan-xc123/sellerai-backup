$ErrorActionPreference = 'Continue'
Write-Host '=== try SSH push (no proxy) ==='
Set-Location 'D:\AIAgent\sellerai-backup'
$env:GIT_SSH_COMMAND = 'ssh -o ConnectTimeout=15 -o StrictHostKeyChecking=accept-new'
git push github-ssh master 2>&1 | Select-Object -First 8
Write-Host "ssh exit=$LASTEXITCODE"

Write-Host ''
Write-Host '=== common proxy app installs ==='
$paths = @(
  "$env:LOCALAPPDATA\Programs\Clash for Windows",
  "$env:LOCALAPPDATA\Clash for Windows",
  "$env:APPDATA\Clash for Windows",
  'C:\Program Files\Clash for Windows',
  'D:\Program Files\Clash for Windows',
  'D:\Clash for Windows',
  'D:\Software\Clash*',
  "$env:LOCALAPPDATA\Programs\v2rayN",
  'C:\Program Files\v2rayN',
  'D:\v2rayN',
  'D:\Software\v2rayN',
  "$env:LOCALAPPDATA\Programs\mihomo",
  'D:\mihomo',
  'D:\Software\mihomo'
)
foreach ($p in $paths) {
  if (Test-Path $p) { Write-Host "FOUND: $p" }
}
Write-Host '=== search common exes in D:\ ==='
Get-ChildItem 'D:\' -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name -match 'clash|v2ray|mihomo|proxy|surge' } | ForEach-Object { $_.FullName }
Get-ChildItem "$env:USERPROFILE\Desktop" -Filter '*.lnk' -ErrorAction SilentlyContinue | Where-Object { $_.Name -match 'clash|v2ray|proxy' } | ForEach-Object { $_.FullName }
