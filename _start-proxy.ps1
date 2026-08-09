$ErrorActionPreference = 'Continue'
Write-Host '=== launching Clash Verge ==='
Start-Process -FilePath 'D:\clash\Clash Verge\clash-verge.exe' -WorkingDirectory 'D:\clash\Clash Verge'
Write-Host 'launched, waiting for port 7897...'

# Wait up to 90s for the proxy port to come up
$ok = $false
for ($i = 0; $i -lt 30; $i++) {
  Start-Sleep -Seconds 3
  $conn = Get-NetTCPConnection -LocalAddress '127.0.0.1' -LocalPort 7897 -State Listen -ErrorAction SilentlyContinue
  if ($conn) { $ok = $true; Write-Host "port 7897 LISTENING after $($i*3+3)s"; break }
  Write-Host "waiting... $($i*3+3)s"
}
if (-not $ok) {
  Write-Host 'PORT 7897 NOT UP - checking clash processes'
  Get-Process | Where-Object { $_.ProcessName -match 'clash|mihomo|verge' } | Select-Object Id, ProcessName
  exit 1
}
Write-Host 'PROXY READY'
