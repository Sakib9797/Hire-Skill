# Quick Start Guide

## ⚡ Fast Setup (5 minutes)

### 1. Backend Setup

```bash
# Navigate to backend
cd backend

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env  # Windows
# cp .env.example .env  # Mac/Linux

# Edit .env and set your database credentials
# DATABASE_URL=postgresql://your_username:your_password@localhost:5432/hireskill_db
# JWT_SECRET_KEY=your-secret-key-change-this

# Create database in PostgreSQL
# psql -U postgres
# CREATE DATABASE hireskill_db;
# \q

# Run the backend
python run.py
```

Backend runs at: **http://localhost:5000**

### 2. Frontend Setup

```bash
# Open new terminal and navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend runs at: **http://localhost:3000**

## 🎯 Default Test Flow

1. **Open** http://localhost:3000
2. **Click** "Get Started" or "Register"
3. **Create Account**:
   - Email: test@example.com
   - Password: TestPass123
   - First Name: Test
   - Last Name: User
   - Role: Candidate
4. **Login** with credentials
5. **View Dashboard** and update profile
6. **Toggle Theme** using moon/sun icon

## 🔑 API Health Check

Test if backend is running:
```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "message": "HireSkill API is running"
}
```

## 🐛 Common Issues

### Backend won't start
- ✅ Make sure PostgreSQL is running
- ✅ Database `hireskill_db` exists
- ✅ `.env` file has correct database URL
- ✅ Virtual environment is activated

### Frontend won't start
- ✅ Run `npm install` first
- ✅ Check if port 3000 is available
- ✅ Make sure backend is running on port 5000

### CORS errors
- ✅ Backend should be on port 5000
- ✅ Frontend should be on port 3000
- ✅ Restart both servers

## 📊 User Roles

- **user**: Basic access
- **candidate**: Job seeker profile
- **employer**: Company/recruiter profile
- **admin**: Full system access

## 🎨 Theme Toggle

The app supports light and dark themes:
- Click the moon 🌙 icon for dark mode
- Click the sun ☀️ icon for light mode
- Preference is saved to your profile

## 📱 Features to Try

1. ✅ Register with different roles
2. ✅ Login and logout
3. ✅ Update profile information
4. ✅ Add skills and interests
5. ✅ Switch between themes
6. ✅ View profile changes in real-time

## 🔒 Password Requirements

- Minimum 8 characters
- At least 1 uppercase letter
- At least 1 lowercase letter
- At least 1 number

Example: `SecurePass123`

## 📚 API Documentation

### Register
```bash
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123",
  "first_name": "John",
  "last_name": "Doe",
  "role": "candidate"
}
```

### Login
```bash
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

### Update Profile (requires token)
```bash
PUT /api/users/profile
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "bio": "Full-stack developer",
  "skills": ["Python", "React", "PostgreSQL"],
  "interests": ["AI", "Web Development"]
}
```

## 🎓 Learning Resources

This project demonstrates:
- ✅ MVC architecture pattern
- ✅ RESTful API design
- ✅ JWT authentication
- ✅ React Context API
- ✅ Protected routes
- ✅ Form validation
- ✅ Theme management
- ✅ Database relationships
- ✅ Password hashing
- ✅ Token refresh mechanism

## 💡 Next Steps

1. Try creating multiple accounts with different roles
2. Update your profile with skills and interests
3. Test the theme toggle functionality
4. Explore the code structure
5. Add new features!

## 🆘 Need Help?

Check the main README.md for:
- Detailed setup instructions
- Complete API documentation
- Architecture explanation
- Security features
- Deployment guide
