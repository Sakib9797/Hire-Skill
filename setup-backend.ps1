# HireSkill Backend Setup Script for Windows
# Run this script with: .\setup-backend.ps1

Write-Host "================================" -ForegroundColor Cyan
Write-Host "HireSkill Backend Setup" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Navigate to backend directory
Set-Location -Path "backend"

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.8+ from https://www.python.org/" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host ""
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists." -ForegroundColor Cyan
} else {
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host ""
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt
Write-Host "✓ Dependencies installed" -ForegroundColor Green

# Create .env file if it doesn't exist
Write-Host ""
Write-Host "Setting up environment variables..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host ".env file already exists." -ForegroundColor Cyan
} else {
    Copy-Item ".env.example" ".env"
    Write-Host "✓ .env file created from .env.example" -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠️  IMPORTANT: Please edit .env file and set your database credentials!" -ForegroundColor Yellow
    Write-Host "   DATABASE_URL=postgresql://your_username:your_password@localhost:5432/hireskill_db" -ForegroundColor Cyan
    Write-Host "   JWT_SECRET_KEY=your-secure-secret-key-here" -ForegroundColor Cyan
}

# Database setup instructions
Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "Database Setup Required" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Please ensure PostgreSQL is installed and running, then create the database:" -ForegroundColor Yellow
Write-Host "  1. Open PostgreSQL command line (psql)" -ForegroundColor White
Write-Host "  2. Run: CREATE DATABASE hireskill_db;" -ForegroundColor Cyan
Write-Host "  3. Exit: \q" -ForegroundColor White
Write-Host ""

# Ask if database is ready
$dbReady = Read-Host "Have you created the database? (y/n)"
if ($dbReady -eq "y" -or $dbReady -eq "Y") {
    Write-Host ""
    Write-Host "Starting Flask application..." -ForegroundColor Yellow
    Write-Host "Backend will be available at: http://localhost:5000" -ForegroundColor Green
    Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
    Write-Host ""
    python run.py
} else {
    Write-Host ""
    Write-Host "Setup completed! Next steps:" -ForegroundColor Green
    Write-Host "  1. Create PostgreSQL database" -ForegroundColor White
    Write-Host "  2. Edit .env file with your database credentials" -ForegroundColor White
    Write-Host "  3. Run: python run.py" -ForegroundColor White
    Write-Host ""
}
