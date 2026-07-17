# SellerAI 每日自动备份 PowerShell 脚本
# Cron 每日 00:30 触发

$dateStr = Get-Date -Format "yyyyMMdd"
$backupDir = "D:\AIAgent\sellerai-backup\$dateStr"

# 创建今日备份目录
New-Item -ItemType Directory -Force -Path $backupDir | Out-Null

# 复制各类文件
$sources = @(
    @{Src="E:\QClaw\Work-QClaw\sellerai-deploy\*";       Dest="$backupDir\deploy\"},
    @{Src="E:\QClaw\Work-QClaw\sellerai-backend\*.py";   Dest="$backupDir\backend\"},
    @{Src="E:\QClaw\Work-QClaw\sellerai-backend\.env";   Dest="$backupDir\backend\"},
    @{Src="E:\QClaw\Work-QClaw\sellerai-backend\*.txt";  Dest="$backupDir\backend\"},
    @{Src="E:\QClaw\Work-QClaw\sellerai-reports\*.md";   Dest="$backupDir\reports\"},
    @{Src="E:\QClaw\Work-QClaw\MEMORY.md";               Dest="$backupDir\"},
    @{Src="E:\QClaw\Work-QClaw\memory\2026-07-*.md";     Dest="$backupDir\memory\"}
)

foreach ($s in $sources) {
    New-Item -ItemType Directory -Force -Path $s.Dest | Out-Null
    Copy-Item -Path $s.Src -Destination $s.Dest -Force -ErrorAction SilentlyContinue
}

# 清理 30 天前的旧备份
$cutoff = (Get-Date).AddDays(-30)
Get-ChildItem -Path "D:\AIAgent\sellerai-backup" -Directory | 
    Where-Object { $_.Name -match '^\d{8}$' -and [datetime]::ParseExact($_.Name, 'yyyyMMdd', $null) -lt $cutoff } |
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

# 记录日志
"$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') | Backup OK | Files: $(Get-ChildItem $backupDir -Recurse -File | Measure-Object | Select-Object -ExpandProperty Count) | Size: $(Get-ChildItem $backupDir -Recurse -File | Measure-Object -Property Length -Sum | Select-Object -ExpandProperty Sum) bytes" |
    Out-File -Append -FilePath "D:\AIAgent\sellerai-backup\backup-log.txt" -Encoding UTF8

Write-Output "Backup done: $backupDir"
