$ErrorActionPreference = 'Continue'
Write-Host '=== D:\clash contents ==='
Get-ChildItem 'D:\clash' -Recurse -Depth 2 -ErrorAction SilentlyContinue | Select-Object -First 40 FullName
Write-Host ''
Write-Host '=== executable files ==='
Get-ChildItem 'D:\clash' -Recurse -Include '*.exe','*.bat','*.cmd','*.ps1','*.yml','*.yaml' -ErrorAction SilentlyContinue | Select-Object -First 20 FullName
