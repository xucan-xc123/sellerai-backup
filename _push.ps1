$ErrorActionPreference = 'Continue'
Set-Location 'D:\AIAgent\sellerai-backup'

git -c user.name='sellerai-backup' -c user.email='backup@local' commit -m "Backup 2026-08-02 (exclude sensitive files, clean junk entries)"

if ($LASTEXITCODE -ne 0) {
  Write-Host 'COMMIT FAILED'
  exit 1
}

Write-Host '=== commit ok, pushing via proxy ==='
$env:HTTPS_PROXY = 'http://127.0.0.1:7897'
$env:HTTP_PROXY = 'http://127.0.0.1:7897'

git push github master 2>&1

if ($LASTEXITCODE -eq 0) {
  Write-Host 'PUSH OK'
} else {
  Write-Host 'PUSH FAILED'
  exit 1
}
