$ErrorActionPreference = 'Continue'
Write-Host '=== verge-mihomo listening ports ==='
Get-NetTCPConnection -OwningProcess 23764 -State Listen -ErrorAction SilentlyContinue | Select-Object LocalAddress, LocalPort, State
Write-Host ''
Write-Host '=== all verge-related ports ==='
Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Where-Object { $_.OwningProcess -in @(21856,23764) } | Select-Object LocalAddress, LocalPort, OwningProcess
Write-Host ''
Write-Host '=== profiles dir full ==='
$vergeDir = 'C:\Users\Administrator\AppData\Roaming\io.github.clash-verge-rev.clash-verge-rev'
Get-ChildItem "$vergeDir\profiles" -ErrorAction SilentlyContinue | Select-Object Name, Length
Write-Host '--- profile.yaml? ---'
Get-ChildItem "$vergeDir\profiles" -Filter '*.yaml' -ErrorAction SilentlyContinue | ForEach-Object { $_.FullName }
Write-Host '=== current config locations ==='
Get-ChildItem "$vergeDir" -ErrorAction SilentlyContinue | Select-Object Name, Length | Format-Table -AutoSize
