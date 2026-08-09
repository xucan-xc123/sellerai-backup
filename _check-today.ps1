$ErrorActionPreference = 'Continue'
Write-Host '---20260809 sensitive files---'
Get-ChildItem 'D:\AIAgent\sellerai-backup\20260809' -Recurse -File | Where-Object { $_.Name -match '\.env$|check_balance|MEMORY|VERCEL|环境变量|密钥|token|secret|\.pem$' } | ForEach-Object { $_.FullName }
Write-Host '---sellerai-deploy dirs---'
Get-ChildItem 'D:\AIAgent' -Directory | ForEach-Object { $_.Name }
Write-Host '---cost record candidates---'
@('D:\AIAgent\sellerai-deploy\成本记录.md','D:\AIAgent\sellerai-backup\deploy\成本记录.md','D:\AIAgent\sellerai-backup\成本记录.md') | ForEach-Object { Write-Host "$_ => $(Test-Path $_)" }
Write-Host '---git status full---'
Set-Location 'D:\AIAgent\sellerai-backup'
git status --short
Write-Host '---gitignore tail---'
Get-Content '.gitignore' -Tail 8
