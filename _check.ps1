$ErrorActionPreference = 'Stop'
Set-Location 'D:\AIAgent\sellerai-backup'

Write-Host '=== git status (porcelain) count ==='
$all = git status --porcelain
Write-Host ("total lines: " + $all.Count)

Write-Host '=== staged A entries mentioning temp/null/tmp ==='
$all | Where-Object { $_ -match 'temp-repo|tmp-push|null' } | Select-Object -First 20

Write-Host '=== tracked files mentioning temp/null/tmp ==='
$tracked = git ls-files
$tracked | Where-Object { $_ -match 'temp-repo|tmp-push' } | Select-Object -First 20
$tracked | Where-Object { $_ -eq '$null' }

Write-Host '=== untracked files (not ignored) ==='
git ls-files --others --exclude-standard | Select-Object -First 20

Write-Host '=== last commits ==='
git log --oneline -5
