$ErrorActionPreference = 'Continue'

Write-Host '=== search E: for sellerai-deploy ==='
Get-ChildItem -Path 'E:\' -Directory -Filter 'sellerai-deploy' -Recurse -Depth 4 -ErrorAction SilentlyContinue | Select-Object FullName

Write-Host '=== search C:\Users for sellerai-deploy ==='
Get-ChildItem -Path 'C:\Users' -Directory -Filter 'sellerai-deploy' -Recurse -Depth 5 -ErrorAction SilentlyContinue | Select-Object FullName

Write-Host '=== search D:\ root depth 2 for 成本记录.md ==='
Get-ChildItem -Path 'D:\' -Filter '成本记录.md' -Recurse -Depth 3 -ErrorAction SilentlyContinue | Select-Object FullName

Write-Host '=== search workdir ==='
Get-ChildItem -Path 'E:\QClaw\Work-QClaw' -Filter '成本记录.md' -Recurse -Depth 3 -ErrorAction SilentlyContinue | Select-Object FullName
