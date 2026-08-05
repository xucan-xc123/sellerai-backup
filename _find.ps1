$ErrorActionPreference = 'Continue'

Write-Host '=== find 成本记录.md ==='
Get-ChildItem -Path 'D:\AIAgent' -Filter '成本记录.md' -Recurse -ErrorAction SilentlyContinue | Select-Object FullName

Write-Host '=== find sellerai-deploy dir ==='
Get-ChildItem -Path 'D:\AIAgent' -Directory -Filter 'sellerai-deploy' -Recurse -ErrorAction SilentlyContinue | Select-Object FullName

Write-Host '=== find sellerai-deploy anywhere ==='
Get-ChildItem -Path 'D:\' -Directory -Filter 'sellerai-deploy' -Recurse -Depth 3 -ErrorAction SilentlyContinue | Select-Object FullName
