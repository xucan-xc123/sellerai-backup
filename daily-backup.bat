@echo off
REM === SellerAI 每日自动备份 ===
REM 由 cron 每日 00:30 触发，备份到 D盘

set BACKUP_DIR=D:\AIAgent\sellerai-backup\%date:~0,4%%date:~5,2%%date:~8,2%
mkdir "%BACKUP_DIR%" 2>nul

REM 运营文档
xcopy "E:\QClaw\Work-QClaw\sellerai-deploy\*.md" "%BACKUP_DIR%\" /Y /Q >nul
xcopy "E:\QClaw\Work-QClaw\sellerai-deploy\*.csv" "%BACKUP_DIR%\" /Y /Q >nul

REM 后端核心
xcopy "E:\QClaw\Work-QClaw\sellerai-backend\app.py" "%BACKUP_DIR%\" /Y /Q >nul
xcopy "E:\QClaw\Work-QClaw\sellerai-backend\requirements.txt" "%BACKUP_DIR%\" /Y /Q >nul
xcopy "E:\QClaw\Work-QClaw\sellerai-backend\.env" "%BACKUP_DIR%\" /Y /Q >nul

REM 前端核心
xcopy "E:\QClaw\Work-QClaw\sellerai-frontend\package.json" "%BACKUP_DIR%\" /Y /Q >nul

REM MEMORY
xcopy "E:\QClaw\Work-QClaw\MEMORY.md" "%BACKUP_DIR%\" /Y /Q >nul

REM 每日内存
xcopy "E:\QClaw\Work-QClaw\memory\*.md" "%BACKUP_DIR%\memory\" /Y /Q >nul

REM 清理 30 天前的旧备份
forfiles /p "D:\AIAgent\sellerai-backup" /d -30 /c "cmd /c rmdir /s /q @path" 2>nul

echo %date% %time% Backup done >> "D:\AIAgent\sellerai-backup\backup-log.txt"
