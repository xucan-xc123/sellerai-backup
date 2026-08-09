$ErrorActionPreference = 'Continue'
Write-Host '=== find proxy processes ==='
Get-Process | Where-Object { $_.ProcessName -match 'clash|shadowsock|v2ray|proxy|proxifier|trojan' } | Select-Object Id, ProcessName, Path
Write-Host '=== netstat for common proxy ports ==='
Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Where-Object { $_.LocalPort -in @(7890,7891,7892,7897,7898,8080,1080,1086,1087,3128,8118,9090,9050,9051,10808) } | Select-Object LocalAddress, LocalPort, OwningProcess
Write-Host '=== also check 127.0.0.1:7897 specifically ==='
Get-NetTCPConnection -LocalAddress '127.0.0.1' -LocalPort 7897 -ErrorAction SilentlyContinue
