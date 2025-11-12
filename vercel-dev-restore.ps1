# PowerShell script to restore pyproject.toml after vercel dev

Write-Host "Restoring pyproject.toml..." -ForegroundColor Cyan
Write-Host ""

if (Test-Path "pyproject.toml.hidden") {
    Rename-Item "pyproject.toml.hidden" "pyproject.toml" -Force
    Write-Host "Restored pyproject.toml" -ForegroundColor Green
} else {
    Write-Host "pyproject.toml.hidden not found" -ForegroundColor Yellow
    if (Test-Path "pyproject.toml.bak") {
        Write-Host "Found backup file, restoring from backup..." -ForegroundColor Yellow
        Copy-Item "pyproject.toml.bak" "pyproject.toml" -Force
        Write-Host "Restored pyproject.toml from backup" -ForegroundColor Green
    }
}

if (Test-Path "pyproject.toml.bak") {
    Write-Host "Backup file exists: pyproject.toml.bak" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Restore complete!" -ForegroundColor Green
Write-Host ""
