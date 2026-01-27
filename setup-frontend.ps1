# HireSkill Frontend Setup Script for Windows
# Run this script with: .\setup-frontend.ps1

Write-Host "================================" -ForegroundColor Cyan
Write-Host "HireSkill Frontend Setup" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Navigate to frontend directory
Set-Location -Path "frontend"

# Check if Node.js is installed
Write-Host "Checking Node.js installation..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "✓ Node.js found: $nodeVersion" -ForegroundColor Green
    
    $npmVersion = npm --version
    Write-Host "✓ npm found: v$npmVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Node.js not found. Please install Node.js from https://nodejs.org/" -ForegroundColor Red
    exit 1
}

# Install dependencies
Write-Host ""
Write-Host "Installing npm dependencies..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Cyan
npm install

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Check if .env exists
Write-Host ""
Write-Host "Checking environment configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "✓ .env file found" -ForegroundColor Green
} else {
    Write-Host "⚠️  .env file not found, using defaults" -ForegroundColor Yellow
    Write-Host "   API URL: http://localhost:5000/api" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting development server..." -ForegroundColor Yellow
Write-Host "Frontend will be available at: http://localhost:3000" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""
Write-Host "⚠️  Make sure the backend is running on port 5000!" -ForegroundColor Yellow
Write-Host ""

# Start the development server
npm start
