# PowerShell script to setup environment for vercel dev
# This temporarily hides pyproject.toml so Vercel uses requirements.txt

Write-Host "Setting up Vercel dev environment..." -ForegroundColor Cyan
Write-Host ""

# Remove uv.lock if it exists (Vercel will try to use it and cause errors)
if (Test-Path "uv.lock") {
    Write-Host "Removing uv.lock to prevent Vercel from using it..." -ForegroundColor Yellow
    Remove-Item "uv.lock" -Force
    Write-Host "✓ Deleted uv.lock" -ForegroundColor Green
}

# Check if pyproject.toml exists
if (-not (Test-Path "pyproject.toml")) {
    Write-Host "pyproject.toml not found, nothing to do" -ForegroundColor Yellow
    exit 0
}

# Backup pyproject.toml if it exists
if (Test-Path "pyproject.toml.bak") {
    Write-Host "Backup already exists, skipping backup..." -ForegroundColor Yellow
} else {
    Copy-Item "pyproject.toml" "pyproject.toml.bak" -Force
    Write-Host "✓ Backed up pyproject.toml" -ForegroundColor Green
}

# Hide pyproject.toml
Rename-Item "pyproject.toml" "pyproject.toml.hidden" -Force
Write-Host "✓ Hidden pyproject.toml (renamed to pyproject.toml.hidden)" -ForegroundColor Green

# Verify requirements.txt exists
if (Test-Path "requirements.txt") {
    Write-Host "✓ requirements.txt found" -ForegroundColor Green
} else {
    Write-Host "⚠ Warning: requirements.txt not found!" -ForegroundColor Red
}

Write-Host ""
Write-Host "Setup complete! Now you can run:" -ForegroundColor Cyan
Write-Host "  vercel dev" -ForegroundColor White
Write-Host ""
Write-Host "To restore pyproject.toml later, run:" -ForegroundColor Cyan
Write-Host "  .\vercel-dev-restore.ps1" -ForegroundColor White
Write-Host ""

