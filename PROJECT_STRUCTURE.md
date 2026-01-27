# 📂 HireSkill Project Structure

```
Hire-Skill/
│
├── 📄 README.md                      # Main project documentation
├── 📄 QUICKSTART.md                  # Fast setup guide
├── 📄 API_DOCUMENTATION.md           # Complete API reference
├── 📄 PROJECT_OVERVIEW.md            # Comprehensive project overview
├── 📄 DESIGN_SYSTEM.md               # Design guidelines and patterns
├── 📄 TESTING_GUIDE.md               # Testing procedures and checklist
├── 📄 COMPLETION_SUMMARY.md          # Project completion report
├── 📄 .gitignore                     # Git ignore rules
├── ⚙️ setup-backend.ps1              # Backend setup script (PowerShell)
├── ⚙️ setup-frontend.ps1             # Frontend setup script (PowerShell)
│
├── 🔙 backend/                       # Flask Backend (Python)
│   ├── 📄 run.py                     # Application entry point
│   ├── 📄 config.py                  # Configuration management
│   ├── 📄 manage_db.py               # Database management utility
│   ├── 📄 requirements.txt           # Python dependencies
│   ├── 📄 .env.example               # Environment variables template
│   ├── 📄 .gitignore                 # Backend Git ignore
│   │
│   └── 📁 app/                       # Main application package
│       ├── 📄 __init__.py            # App factory (Flask app creation)
│       │
│       ├── 📁 models/                # Database Models (ORM)
│       │   ├── 📄 __init__.py        # Models package initialization
│       │   └── 📄 user.py            # User and UserProfile models
│       │
│       ├── 📁 controllers/           # Business Logic (Controllers)
│       │   ├── 📄 __init__.py        # Controllers package
│       │   ├── 📄 auth_controller.py # Authentication logic
│       │   └── 📄 user_controller.py # User profile logic
│       │
│       ├── 📁 views/                 # API Endpoints (Views/Routes)
│       │   ├── 📄 __init__.py        # Views package
│       │   ├── 📄 auth_views.py      # Authentication endpoints
│       │   └── 📄 user_views.py      # User profile endpoints
│       │
│       └── 📁 utils/                 # Helper Functions
│           ├── 📄 __init__.py        # Utils package
│           ├── 📄 validators.py      # Validation functions
│           └── 📄 responses.py       # Response formatters
│
└── 🎨 frontend/                      # React Frontend
    ├── 📄 package.json               # Node.js dependencies
    ├── 📄 .env                       # Environment configuration
    ├── 📄 .gitignore                 # Frontend Git ignore
    │
    ├── 📁 public/                    # Static Public Files
    │   ├── 📄 index.html             # HTML template
    │   └── 📄 manifest.json          # PWA manifest
    │
    └── 📁 src/                       # Source Code
        ├── 📄 index.js               # React entry point
        ├── 📄 App.js                 # Main app component with routing
        │
        ├── 📁 components/            # Reusable Components
        │   ├── 📄 Navbar.js          # Navigation bar with theme toggle
        │   └── 📄 PrivateRoute.js    # Protected route wrapper
        │
        ├── 📁 pages/                 # Page Components
        │   ├── 📄 Home.js            # Landing page
        │   ├── 📄 Login.js           # User login page
        │   ├── 📄 Register.js        # User registration page
        │   └── 📄 Dashboard.js       # User dashboard/profile
        │
        ├── 📁 context/               # React Context (State Management)
        │   ├── 📄 AuthContext.js     # Authentication state
        │   └── 📄 ThemeContext.js    # Theme state (light/dark)
        │
        ├── 📁 services/              # API Service Layer
        │   ├── 📄 api.js             # Axios instance with interceptors
        │   ├── 📄 authService.js     # Authentication API calls
        │   └── 📄 userService.js     # User profile API calls
        │
        └── 📁 styles/                # CSS Stylesheets
            ├── 📄 index.css          # Global styles and theme variables
            ├── 📄 Auth.css           # Authentication page styles
            └── 📄 Dashboard.css      # Dashboard page styles
```

## 📊 File Count by Category

### Documentation (7 files)
- README.md
- QUICKSTART.md
- API_DOCUMENTATION.md
- PROJECT_OVERVIEW.md
- DESIGN_SYSTEM.md
- TESTING_GUIDE.md
- COMPLETION_SUMMARY.md

### Backend (18 files)
- Entry Points: 2 files (run.py, manage_db.py)
- Configuration: 2 files (config.py, .env.example)
- Models: 2 files
- Controllers: 3 files
- Views: 3 files
- Utils: 3 files
- Config: 3 files (requirements.txt, .gitignore, __init__.py files)

### Frontend (21 files)
- Entry Points: 2 files (index.js, App.js)
- Components: 2 files
- Pages: 4 files
- Context: 2 files
- Services: 3 files
- Styles: 3 files
- Configuration: 3 files (package.json, .env, .gitignore)
- Public: 2 files

### Scripts & Config (4 files)
- Setup Scripts: 2 files
- Root Config: 2 files (.gitignore, this file)

**Total: 50 files**

## 🎯 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         FRONTEND                            │
│                      (React SPA)                            │
├─────────────────────────────────────────────────────────────┤
│  Components  │  Pages  │  Context  │  Services  │  Styles  │
│     ↓            ↓         ↓           ↓            ↓       │
│  Reusable   Pages     State Mgmt   API Layer   Themes      │
└────────────────────────┬────────────────────────────────────┘
                         │
                    HTTP/HTTPS
                    (REST API)
                         │
┌────────────────────────┴────────────────────────────────────┐
│                         BACKEND                             │
│                    (Flask REST API)                         │
├─────────────────────────────────────────────────────────────┤
│   Views      │  Controllers  │   Models   │    Utils       │
│     ↓              ↓              ↓            ↓           │
│  Endpoints   Business Logic   Database    Helpers         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │
                         ↓
              ┌──────────────────┐
              │   PostgreSQL     │
              │    Database      │
              │                  │
              │  • users         │
              │  • user_profiles │
              └──────────────────┘
```

## 🔄 Data Flow

```
User Action (Frontend)
    ↓
React Component
    ↓
Context API (State Management)
    ↓
Service Layer (API calls)
    ↓
Axios (HTTP Client with Interceptors)
    ↓
Flask Routes (Views)
    ↓
Controllers (Business Logic)
    ↓
Models (Database ORM)
    ↓
PostgreSQL Database
    ↓
Response ← ← ← ← ← ← ←
```

## 🔐 Authentication Flow

```
1. User Registration/Login
   ↓
2. Backend validates credentials
   ↓
3. Generate JWT tokens (access + refresh)
   ↓
4. Store tokens in localStorage
   ↓
5. Include token in all API requests
   ↓
6. Backend verifies token
   ↓
7. If expired, auto-refresh using refresh token
   ↓
8. Continue with authenticated request
```

## 🎨 Component Hierarchy

```
App.js (Main Router)
├── Home
├── Login
├── Register
└── Dashboard (Protected)
    ├── Navbar
    │   ├── User Avatar
    │   ├── Theme Toggle
    │   └── Logout Button
    │
    └── Dashboard Content
        ├── Account Info Card
        └── Profile Details Card
            ├── View Mode
            └── Edit Mode
```

## 📡 API Endpoint Structure

```
/api
├── /auth
│   ├── POST   /register      (Public)
│   ├── POST   /login         (Public)
│   ├── POST   /refresh       (Requires Refresh Token)
│   └── GET    /me            (Protected)
│
└── /users
    ├── GET    /profile       (Protected)
    ├── PUT    /profile       (Protected)
    ├── PUT    /profile/theme (Protected)
    ├── GET    /              (Admin Only)
    └── GET    /<id>          (Admin Only)
```

## 💾 Database Schema

```
┌─────────────────────────┐
│        users            │
├─────────────────────────┤
│ • id (PK)               │
│ • email (Unique)        │
│ • password_hash         │
│ • first_name            │
│ • last_name             │
│ • role                  │
│ • is_active             │
│ • created_at            │
│ • updated_at            │
└──────────┬──────────────┘
           │ 1:1
           │
┌──────────▼──────────────┐
│    user_profiles        │
├─────────────────────────┤
│ • id (PK)               │
│ • user_id (FK)          │
│ • bio                   │
│ • phone                 │
│ • location              │
│ • avatar_url            │
│ • skills (JSON)         │
│ • experience (JSON)     │
│ • education (JSON)      │
│ • interests (JSON)      │
│ • linkedin_url          │
│ • github_url            │
│ • portfolio_url         │
│ • theme_preference      │
│ • created_at            │
│ • updated_at            │
└─────────────────────────┘
```

## 🎯 Key Features by File

### Authentication
- `auth_controller.py` - Registration, login, token refresh logic
- `auth_views.py` - Authentication API endpoints
- `AuthContext.js` - Frontend auth state management
- `authService.js` - Auth API calls

### User Profile
- `user_controller.py` - Profile management logic
- `user_views.py` - Profile API endpoints
- `Dashboard.js` - Profile UI and editing
- `userService.js` - Profile API calls

### Security
- `validators.py` - Password hashing, validation
- `api.js` - Token interceptors
- `PrivateRoute.js` - Route protection

### Theme System
- `ThemeContext.js` - Theme state management
- `index.css` - CSS variables for theming
- `Navbar.js` - Theme toggle button

---

**This structure follows industry best practices with clear separation of concerns, making the codebase maintainable and scalable.**
