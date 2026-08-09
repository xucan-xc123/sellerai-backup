$ErrorActionPreference = 'Continue'
Write-Host '=== clash/verge processes ==='
Get-Process | Where-Object { $_.ProcessName -match 'clash|mihomo|verge' } | Select-Object Id, ProcessName, StartTime
Write-Host ''
Write-Host '=== verge config dir ==='
$vergeDir = "$env:APPDATA\io.github.clash-verge-rev.clash-verge-rev"
if (-not (Test-Path $vergeDir)) { $vergeDir = "$env:APPDATA\clash-verge" }
if (Test-Path $vergeDir) {
  Write-Host "CFG DIR: $vergeDir"
  Get-ChildItem $vergeDir -Depth 1 -ErrorAction SilentlyContinue | Select-Object -First 25 FullName
  Write-Host '--- profiles ---'
  Get-ChildItem "$vergeDir\profiles" -ErrorAction SilentlyContinue | Select-Object Name, Length, LastWriteTime
} else {
  Write-Host 'no verge config dir found'
}
Write-Host ''
Write-Host '=== any port listening by clash pid? ==='
$p = Get-Process | Where-Object { $_.ProcessName -match 'clash|mihomo' } | Select-Object -First 1
if ($p) {
  Get-NetTCPConnection -OwningProcess $p.Id -State Listen -ErrorAction SilentlyContinue | Select-Object LocalAddress, LocalPort
}
