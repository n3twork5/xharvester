# XHARVESTOR Updater for Windows (conceptual)
$repoUrl = "https://github.com/n3tworkh4x/xharvestor.git"
$installDir = "$env:USERPROFILE\Tools\xharvestor"

# Check if Git is available
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "Git is not installed. Please install Git for Windows." -ForegroundColor Red
    exit 1
}

# Clone or update repository
if (Test-Path $installDir) {
    Set-Location $installDir
    git pull
} else {
    git clone $repoUrl $installDir
}

# Install Python dependencies
python -m pip install colorama requests

Write-Host "XHARVESTER has been updated successfully!" -ForegroundColor Green