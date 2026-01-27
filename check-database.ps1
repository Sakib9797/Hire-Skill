# Database Check Script
# This script helps you verify your PostgreSQL database setup

Write-Host "================================" -ForegroundColor Cyan
Write-Host "PostgreSQL Database Checker" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check if psql is available
Write-Host "Checking PostgreSQL installation..." -ForegroundColor Yellow
try {
    $pgVersion = psql --version
    Write-Host "✓ PostgreSQL found: $pgVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ PostgreSQL not found. Please install PostgreSQL first." -ForegroundColor Red
    Write-Host "Download from: https://www.postgresql.org/download/windows/" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "Database Options:" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host "1. Create hireskill_db database" -ForegroundColor White
Write-Host "2. Check if database exists" -ForegroundColor White
Write-Host "3. List all tables in database" -ForegroundColor White
Write-Host "4. View all users in database" -ForegroundColor White
Write-Host "5. View all user profiles" -ForegroundColor White
Write-Host "6. Check database connection" -ForegroundColor White
Write-Host "7. Exit" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Select an option (1-7)"

switch ($choice) {
    "1" {
        Write-Host "`nCreating database..." -ForegroundColor Yellow
        Write-Host "Enter your PostgreSQL username (default: postgres):" -ForegroundColor Cyan
        $username = Read-Host
        if ([string]::IsNullOrWhiteSpace($username)) { $username = "postgres" }
        
        $createCmd = "CREATE DATABASE hireskill_db;"
        echo $createCmd | psql -U $username -d postgres
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Database 'hireskill_db' created successfully!" -ForegroundColor Green
        } else {
            Write-Host "✗ Failed to create database. It may already exist." -ForegroundColor Red
        }
    }
    
    "2" {
        Write-Host "`nChecking database..." -ForegroundColor Yellow
        Write-Host "Enter your PostgreSQL username (default: postgres):" -ForegroundColor Cyan
        $username = Read-Host
        if ([string]::IsNullOrWhiteSpace($username)) { $username = "postgres" }
        
        $checkCmd = "SELECT datname FROM pg_database WHERE datname='hireskill_db';"
        $result = echo $checkCmd | psql -U $username -d postgres -t
        
        if ($result -match "hireskill_db") {
            Write-Host "✓ Database 'hireskill_db' exists!" -ForegroundColor Green
        } else {
            Write-Host "✗ Database 'hireskill_db' does not exist." -ForegroundColor Red
            Write-Host "Run option 1 to create it." -ForegroundColor Yellow
        }
    }
    
    "3" {
        Write-Host "`nListing tables..." -ForegroundColor Yellow
        Write-Host "Enter your PostgreSQL username (default: postgres):" -ForegroundColor Cyan
        $username = Read-Host
        if ([string]::IsNullOrWhiteSpace($username)) { $username = "postgres" }
        
        psql -U $username -d hireskill_db -c "\dt"
    }
    
    "4" {
        Write-Host "`nViewing users..." -ForegroundColor Yellow
        Write-Host "Enter your PostgreSQL username (default: postgres):" -ForegroundColor Cyan
        $username = Read-Host
        if ([string]::IsNullOrWhiteSpace($username)) { $username = "postgres" }
        
        $query = "SELECT id, email, first_name, last_name, role, is_active, created_at FROM users ORDER BY id;"
        psql -U $username -d hireskill_db -c $query
    }
    
    "5" {
        Write-Host "`nViewing user profiles..." -ForegroundColor Yellow
        Write-Host "Enter your PostgreSQL username (default: postgres):" -ForegroundColor Cyan
        $username = Read-Host
        if ([string]::IsNullOrWhiteSpace($username)) { $username = "postgres" }
        
        $query = "SELECT up.id, up.user_id, u.email, up.bio, up.theme_preference FROM user_profiles up JOIN users u ON up.user_id = u.id ORDER BY up.id;"
        psql -U $username -d hireskill_db -c $query
    }
    
    "6" {
        Write-Host "`nTesting database connection..." -ForegroundColor Yellow
        Write-Host "Enter your PostgreSQL username (default: postgres):" -ForegroundColor Cyan
        $username = Read-Host
        if ([string]::IsNullOrWhiteSpace($username)) { $username = "postgres" }
        
        $query = "SELECT version();"
        psql -U $username -d hireskill_db -c $query
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "`n✓ Database connection successful!" -ForegroundColor Green
        } else {
            Write-Host "`n✗ Database connection failed!" -ForegroundColor Red
        }
    }
    
    "7" {
        Write-Host "`nExiting..." -ForegroundColor Yellow
        exit 0
    }
    
    default {
        Write-Host "`n✗ Invalid option selected." -ForegroundColor Red
    }
}

Write-Host "`nPress any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
