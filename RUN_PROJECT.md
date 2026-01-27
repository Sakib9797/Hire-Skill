# 🚀 Quick Setup & Run Instructions

## Prerequisites Check

1. **Python 3.8+** - Check with: `python --version`
2. **Node.js 14+** - Check with: `node --version`
3. **PostgreSQL 12+** - Check with: `psql --version`

---

## Step 1: Create PostgreSQL Database

### Option A: Using psql Command Line

```powershell
# Connect to PostgreSQL (enter your postgres password when prompted)
psql -U postgres

# Inside psql, run:
CREATE DATABASE hireskill_db;

# List databases to verify
\l

# Exit psql
\q
```

### Option B: Using pgAdmin (GUI)

1. Open pgAdmin
2. Right-click on "Databases"
3. Select "Create" → "Database"
4. Enter name: `hireskill_db`
5. Click "Save"

---

## Step 2: Configure Backend

1. **Navigate to backend directory:**
```powershell
cd d:\Github\Hire-Skill\backend
```

2. **Copy environment file:**
```powershell
Copy-Item .env.example .env
```

3. **Edit `.env` file with your database credentials:**
```
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/hireskill_db
JWT_SECRET_KEY=your-secret-key-change-this-in-production
```

Replace `YOUR_PASSWORD` with your PostgreSQL password.

---

## Step 3: Setup & Run Backend

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Initialize database (creates tables)
python manage_db.py
# Select option 1 (Initialize database)

# Run the backend
python run.py
```

Backend will run at: **http://localhost:5000**

---

## Step 4: Setup & Run Frontend (New Terminal)

Open a **new PowerShell terminal** and run:

```powershell
# Navigate to frontend
cd d:\Github\Hire-Skill\frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend will run at: **http://localhost:3000**

---

## Verify Everything is Running

### 1. Check Backend API
Open browser or run:
```powershell
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "message": "HireSkill API is running"
}
```

### 2. Check Frontend
Open browser: **http://localhost:3000**

You should see the HireSkill landing page.

### 3. Check Database Tables

```powershell
# Connect to database
psql -U postgres -d hireskill_db

# List all tables
\dt

# View users table structure
\d users

# View user_profiles table structure
\d user_profiles

# Check if tables have any data
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM user_profiles;

# Exit
\q
```

---

## Common Issues & Solutions

### Issue: "Connection refused" to PostgreSQL
**Solution:** 
- Make sure PostgreSQL service is running
- Windows: Check Services → PostgreSQL should be "Running"
- Or run: `pg_ctl -D "C:\Program Files\PostgreSQL\16\data" start`

### Issue: "Database does not exist"
**Solution:**
```powershell
psql -U postgres
CREATE DATABASE hireskill_db;
\q
```

### Issue: Virtual environment activation fails
**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: Port 3000 or 5000 already in use
**Solution:**
```powershell
# Find process using port
netstat -ano | findstr :5000
netstat -ano | findstr :3000

# Kill process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

---

## Quick Database Checks

### View All Users
```sql
psql -U postgres -d hireskill_db -c "SELECT id, email, role, is_active FROM users;"
```

### View User Profiles
```sql
psql -U postgres -d hireskill_db -c "SELECT user_id, bio, theme_preference FROM user_profiles;"
```

### Create Test Admin User
```powershell
cd d:\Github\Hire-Skill\backend
python manage_db.py
# Select option 3 (Seed test data)
```

This creates:
- admin@hireskill.com / Admin123
- candidate@hireskill.com / Candidate123
- employer@hireskill.com / Employer123

---

## Test the Application

1. **Open Frontend:** http://localhost:3000
2. **Click "Get Started"** or navigate to Register
3. **Create Account:**
   - Email: test@example.com
   - Password: TestPass123
   - First Name: Test
   - Last Name: User
   - Role: Candidate
4. **Click "Create Account"**
5. **Login** with your credentials
6. **View Dashboard** - Update your profile, add skills, toggle theme

---

## Stop the Servers

### Stop Backend
Press `Ctrl + C` in the backend terminal

### Stop Frontend
Press `Ctrl + C` in the frontend terminal

---

## Database Management Commands

```powershell
# Backup database
pg_dump -U postgres hireskill_db > backup.sql

# Restore database
psql -U postgres hireskill_db < backup.sql

# Reset database (WARNING: Deletes all data)
cd d:\Github\Hire-Skill\backend
python manage_db.py
# Select option 2 (Reset database)
```

---

## Next Steps

- ✅ Create an account
- ✅ Login and view dashboard
- ✅ Update your profile
- ✅ Add skills and interests
- ✅ Toggle between light/dark theme
- ✅ Test API endpoints (see API_DOCUMENTATION.md)

---

**Need Help?** Check the detailed guides:
- [QUICKSTART.md](./QUICKSTART.md)
- [README.md](./README.md)
- [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)
