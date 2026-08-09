$ErrorActionPreference = 'Continue'
Set-Location 'D:\AIAgent\sellerai-backup'

Write-Host '=== 20260809 full file list ==='
Get-ChildItem '20260809' -Recurse -File | ForEach-Object { $_.FullName.Replace('D:\AIAgent\sellerai-backup\','') }

Write-Host ''
Write-Host '=== branch status ==='
git status -sb | Select-Object -First 3

Write-Host ''
Write-Host '=== 20260809 reports dir ==='
if (Test-Path '20260809\reports') { Get-ChildItem '20260809\reports' -File | ForEach-Object { $_.Name } }

Write-Host ''
Write-Host '=== 20260809 deploy 环境变量/密钥 files ==='
Get-ChildItem '20260809\deploy' -File | Where-Object { $_.Name -match '环境变量|密钥|VERCEL' } | ForEach-Object { $_.Name }

Write-Host ''
Write-Host '=== gitignore: does it have 20260806-08 sections? ==='
Select-String -Path '.gitignore' -Pattern '^# 2026080[6-9]' | ForEach-Object { $_.Line }
Write-Host '(empty = missing)'
