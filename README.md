# 🚀 HireSkill - Talent Connection Platform

> A modern, production-ready full-stack web application built with Flask and React, featuring JWT authentication, user profile management, and role-based access control.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![React](https://img.shields.io/badge/React-18.2.0-blue.svg)](https://reactjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-blue.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-Educational-yellow.svg)]()

## 🏗️ Architecture

- **Backend**: Flask (Python) with MVC architecture
- **Frontend**: React with Context API
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT-based with bcrypt password hashing
- **API**: RESTful endpoints
- **Styling**: Custom CSS with theme support (light/dark mode)

## 📋 Features

### Module 1: Authentication & User Profile

✅ **User Registration**
- Email and password validation
- Password strength requirements (8+ chars, uppercase, lowercase, number)
- Bcrypt password hashing
- Role selection (user, candidate, employer, admin)

✅ **User Login**
- JWT access and refresh tokens
- Token expiration and automatic refresh
- Secure session management

✅ **User Profile Management**
- Update personal information (name, bio, phone, location)
- Add/remove skills and interests
- Profile completeness tracking
- Theme preference storage

✅ **Role-Based Access Control**
- Different access levels for users, candidates, employers, and admins
- Protected routes and endpoints
- Role verification middleware

✅ **Theme Support**
- Light and dark mode toggle
- Persistent theme preference
- Smooth transitions and modern design

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+
- PostgreSQL 12+

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Mac/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**
   - Copy `.env.example` to `.env`
   - Update the following variables:
     ```
     DATABASE_URL=postgresql://your_username:your_password@localhost:5432/hireskill_db
     JWT_SECRET_KEY=your-secret-key-here
     ```

6. **Create PostgreSQL database**
   ```sql
   CREATE DATABASE hireskill_db;
   ```

7. **Run the application**
   ```bash
   python run.py
   ```
   Backend will be available at `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm start
   ```
   Frontend will be available at `http://localhost:3000`

## 📁 Project Structure

### Backend (MVC Architecture)

```
backend/
├── app/
│   ├── __init__.py           # App factory and initialization
│   ├── models/               # Database models (Model)
│   │   ├── __init__.py
│   │   └── user.py          # User and UserProfile models
│   ├── controllers/          # Business logic (Controller)
│   │   ├── __init__.py
│   │   ├── auth_controller.py
│   │   └── user_controller.py
│   ├── views/                # API routes (View)
│   │   ├── __init__.py
│   │   ├── auth_views.py
│   │   └── user_views.py
│   └── utils/                # Helper functions
│       ├── __init__.py
│       ├── validators.py
│       └── responses.py
├── config.py                 # Configuration settings
├── run.py                    # Application entry point
└── requirements.txt          # Python dependencies
```

### Frontend (Component-Based)

```
frontend/
├── public/
│   ├── index.html
│   └── manifest.json
├── src/
│   ├── components/           # Reusable components
│   │   ├── Navbar.js
│   │   └── PrivateRoute.js
│   ├── pages/                # Page components
│   │   ├── Home.js
│   │   ├── Login.js
│   │   ├── Register.js
│   │   └── Dashboard.js
│   ├── context/              # Context providers
│   │   ├── AuthContext.js
│   │   └── ThemeContext.js
│   ├── services/             # API services
│   │   ├── api.js
│   │   ├── authService.js
│   │   └── userService.js
│   ├── styles/               # CSS styles
│   │   ├── index.css
│   │   ├── Auth.css
│   │   └── Dashboard.css
│   ├── App.js                # Main app component
│   └── index.js              # Entry point
└── package.json              # Node dependencies
```

## 🔒 API Endpoints

### Authentication

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/refresh` - Refresh access token
- `GET /api/auth/me` - Get current user info

### User Profile

- `GET /api/users/profile` - Get current user's profile
- `PUT /api/users/profile` - Update user profile
- `PUT /api/users/profile/theme` - Update theme preference
- `GET /api/users/` - Get all users (admin only)
- `GET /api/users/<id>` - Get user by ID (admin only)

## 🔐 Security Features

- **Password Hashing**: Bcrypt with salt rounds
- **JWT Tokens**: Separate access and refresh tokens
- **Token Expiration**: Access tokens expire in 1 hour, refresh tokens in 30 days
- **Automatic Token Refresh**: Frontend automatically refreshes expired tokens
- **Input Validation**: Server-side validation for all inputs
- **Role-Based Access**: Decorator-based role verification
- **CORS Protection**: Configured CORS policies
- **SQL Injection Prevention**: SQLAlchemy ORM with parameterized queries

## 🎨 Design Features

- **Modern UI**: Clean, professional design inspired by top platforms
- **Responsive Layout**: Mobile-friendly design
- **Theme Support**: Light and dark modes with smooth transitions
- **Loading States**: User-friendly loading indicators
- **Error Handling**: Comprehensive error messages
- **Form Validation**: Client and server-side validation
- **Animations**: Smooth transitions and micro-interactions

## 🧪 Testing

### Test User Registration
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123",
    "first_name": "John",
    "last_name": "Doe",
    "role": "candidate"
  }'
```

### Test User Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123"
  }'
```

## 📝 Best Practices Implemented

1. **Password Security**
   - Minimum 8 characters
   - Requires uppercase, lowercase, and numbers
   - Bcrypt hashing with salt

2. **Token Management**
   - Short-lived access tokens (1 hour)
   - Long-lived refresh tokens (30 days)
   - Automatic token refresh on expiration

3. **Input Validation**
   - Email format validation
   - Password strength validation
   - Required field validation
   - Data sanitization

4. **Code Organization**
   - MVC architecture for backend
   - Component-based architecture for frontend
   - Separation of concerns
   - Reusable utilities and services

5. **Error Handling**
   - Comprehensive error messages
   - User-friendly error display
   - Proper HTTP status codes
   - Graceful degradation

## 🔧 Configuration

### Backend Configuration

Edit `backend/.env`:

```env
FLASK_ENV=development
DATABASE_URL=postgresql://username:password@localhost:5432/hireskill_db
JWT_SECRET_KEY=your-secret-key
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=2592000
```

### Frontend Configuration

Edit `frontend/.env`:

```env
REACT_APP_API_URL=http://localhost:5000/api
```

## 🚀 Deployment

### Backend Deployment

1. Set `FLASK_ENV=production`
2. Use a production WSGI server (e.g., Gunicorn)
3. Set up PostgreSQL on production server
4. Configure environment variables
5. Use HTTPS for secure communication

### Frontend Deployment

1. Build production bundle: `npm run build`
2. Deploy to static hosting (Netlify, Vercel, etc.)
3. Update API URL to production endpoint
4. Configure CORS on backend for production domain

## 📄 License

This project is for educational purposes.

## 👥 Support

For issues or questions, please create an issue in the repository.

## 🎯 Future Enhancements

- Email verification
- Password reset functionality
- Social authentication (Google, LinkedIn)
- File upload for avatars
- Advanced search and filtering
- Real-time notifications
- Job posting and application system
- Messaging system
- Analytics dashboard
