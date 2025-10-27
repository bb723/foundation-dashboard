# START-HERE.ps1
# Complete setup script - run this first!

Write-Host ""
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "     FOUNDATION DASHBOARD - COMPLETE SETUP" -ForegroundColor White
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Virtual Environment
Write-Host "[1/5] Setting up virtual environment..." -ForegroundColor Yellow
Write-Host ""

if (Test-Path "venv") {
    Write-Host "Virtual environment already exists. Skipping creation." -ForegroundColor Green
} else {
    Write-Host "Creating virtual environment..." -ForegroundColor White
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
    Write-Host "Virtual environment created!" -ForegroundColor Green
}

Write-Host ""

# Step 2: Activate Virtual Environment
Write-Host "[2/5] Activating virtual environment..." -ForegroundColor Yellow
Write-Host ""
& .\venv\Scripts\Activate.ps1

# Step 3: Install Dependencies
Write-Host "[3/5] Installing dependencies (this may take a minute)..." -ForegroundColor Yellow
Write-Host ""
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
    Write-Host "Try running manually: pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "Dependencies installed successfully!" -ForegroundColor Green
Write-Host ""

# Step 4: Configure Environment
Write-Host "[4/5] Configuring environment..." -ForegroundColor Yellow
Write-Host ""

if (Test-Path ".env") {
    Write-Host ".env file already exists." -ForegroundColor Yellow
    $overwrite = Read-Host "Overwrite with credentials from _scripts? (y/N)"
    if ($overwrite -eq 'y' -or $overwrite -eq 'Y') {
        Remove-Item .env
        & .\set-local-env.ps1
    } else {
        Write-Host "Keeping existing .env file." -ForegroundColor Green
    }
} else {
    Write-Host "Creating .env file with shared credentials..." -ForegroundColor White
    & .\set-local-env.ps1
}

Write-Host ""

# Step 5: Verify Setup
Write-Host "[5/5] Verifying setup..." -ForegroundColor Yellow
Write-Host ""
python setup_check.py

Write-Host ""
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "     SETUP COMPLETE!" -ForegroundColor Green
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "You're ready to run the application!" -ForegroundColor White
Write-Host ""
Write-Host "Start the app:" -ForegroundColor Cyan
Write-Host "  python app.py" -ForegroundColor White
Write-Host ""
Write-Host "Then visit:" -ForegroundColor Cyan
Write-Host "  http://localhost:5000" -ForegroundColor White
Write-Host ""
Write-Host "To activate the virtual environment in future sessions:" -ForegroundColor Cyan
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host ""
Write-Host "Having issues? Check TROUBLESHOOTING.md" -ForegroundColor Yellow
Write-Host ""
