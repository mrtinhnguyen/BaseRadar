# PowerShell script to completely clean up for vercel dev
# This removes ALL pyproject.toml files and uv.lock to ensure Vercel uses requirements.txt

Write-Host "Cleaning up for Vercel dev..." -ForegroundColor Cyan
Write-Host ""

# Remove Vercel cache
if (Test-Path ".vercel") {
    Write-Host "Removing Vercel cache..." -ForegroundColor Yellow
    Remove-Item ".vercel" -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "Cache cleared" -ForegroundColor Green
}

# Remove uv.lock if it exists
if (Test-Path "uv.lock") {
    Write-Host "Removing uv.lock..." -ForegroundColor Yellow
    Remove-Item "uv.lock" -Force
    Write-Host "Deleted uv.lock" -ForegroundColor Green
}

# Remove ALL pyproject.toml files (including .bak and .hidden)
$pyprojectFiles = Get-ChildItem -Filter "pyproject.toml*" -ErrorAction SilentlyContinue
if ($pyprojectFiles) {
    Write-Host "Removing pyproject.toml files..." -ForegroundColor Yellow
    foreach ($file in $pyprojectFiles) {
        Write-Host "  Removing: $($file.Name)" -ForegroundColor Gray
        Remove-Item $file.FullName -Force -ErrorAction SilentlyContinue
    }
    Write-Host "All pyproject.toml files removed" -ForegroundColor Green
} else {
    Write-Host "No pyproject.toml files found" -ForegroundColor Green
}

# Verify requirements.txt exists
if (Test-Path "requirements.txt") {
    Write-Host "requirements.txt found" -ForegroundColor Green
} else {
    Write-Host "Warning: requirements.txt not found!" -ForegroundColor Red
}

Write-Host ""
Write-Host "Cleanup complete! Now you can run:" -ForegroundColor Cyan
Write-Host "  vercel dev" -ForegroundColor White
Write-Host ""
Write-Host "Note: pyproject.toml has been removed. Restore it from git if needed" -ForegroundColor Yellow
Write-Host "  git checkout pyproject.toml" -ForegroundColor DarkGray
Write-Host ""
