$ErrorActionPreference = 'Stop'
Set-Location 'D:\AIAgent\sellerai-backup'

Write-Host '=== HEAD tree: junk entries ==='
git ls-tree -r --name-only HEAD | Where-Object { $_ -match 'temp-repo|tmp-push' -or $_ -eq '$null' } | Select-Object -First 30

Write-Host '=== HEAD has $null file? ==='
git ls-tree -r --name-only HEAD | Where-Object { $_ -eq '$null' }

Write-Host '=== remote ==='
git remote -v

Write-Host '=== branch status ==='
git status -sb | Select-Object -First 3

Write-Host '=== what is $null file content ==='
Get-Content 'D:\AIAgent\sellerai-backup\$null' -ErrorAction SilentlyContinue

Write-Host '=== temp-repo dirs ==='
Get-ChildItem 'D:\AIAgent\sellerai-backup\temp-repo' -Force -ErrorAction SilentlyContinue | Select-Object Name -First 10
Get-ChildItem 'D:\AIAgent\sellerai-backup\temp-repo-' -Force -ErrorAction SilentlyContinue | Select-Object Name -First 10
Get-ChildItem 'D:\AIAgent\sellerai-backup\tmp-push' -Force -ErrorAction SilentlyContinue | Select-Object Name -First 10
