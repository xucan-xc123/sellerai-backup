$ErrorActionPreference = 'Continue'
Set-Location 'D:\AIAgent\sellerai-backup'

Write-Host '---cost record real path---'
Get-ChildItem 'D:\AIAgent\sellerai-backup' -Filter '*.md' | ForEach-Object { $_.FullName }
Get-ChildItem 'D:\AIAgent\sellerai-backup' -Recurse -Depth 2 -Filter '成本记录.md' | ForEach-Object { $_.FullName }

Write-Host '---gitignore for 20260806-08 present?---'
Select-String -Path '.gitignore' -Pattern '2026080[6-9]' | ForEach-Object { $_.Line }

Write-Host '---tracked sensitive files in 20260806-08?---'
git ls-files | Where-Object { $_ -match '2026080[6-8].*(\.env|MEMORY|check_balance|VERCEL)' }

Write-Host '---cost record git history---'
git log --oneline --all -- '*成本记录*' | Select-Object -First 5

Write-Host '---last commit touched cost record---'
git log --oneline -3 -- '成本记录.md'
