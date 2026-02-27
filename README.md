<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Flask-3.0-green?style=for-the-badge&logo=flask&logoColor=white" />
  <img src="https://img.shields.io/badge/React-18-blue?style=for-the-badge&logo=react&logoColor=white" />
  <img src="https://img.shields.io/badge/PostgreSQL-15-blue?style=for-the-badge&logo=postgresql&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Docker-Ready-blue?style=for-the-badge&logo=docker&logoColor=white" />
</p>

# HireSkillz — AI-Powered Career Platform

> A full-stack career management platform with AI-powered tools for job search, resume analysis, salary prediction, interview preparation, career recommendations, and more — built with Flask, React, and PostgreSQL.

---

## Architecture

```
┌──────────────────────────────────────────────────────┐
│                    Frontend (Vercel)                  │
│            React 18 · React Router · Context API     │
│            Dark Mode · ErrorBoundary · SPA            │
├──────────────────────────────────────────────────────┤
│                   REST API (JSON)                    │
│         CORS-locked · Security Headers · JWT         │
├──────────────────────────────────────────────────────┤
│              Backend (Render / Railway)               │
│      Flask 3.0 (MVC) · Gunicorn · Python Logging    │
│      Groq LLM · Scikit-learn ML · Web Scraping      │
├──────────────────────────────────────────────────────┤
│        PostgreSQL · Connection Pooling · ORM         │
└──────────────────────────────────────────────────────┘
```

---

## Features

### 1. Authentication & User Profiles
- JWT-based auth with access + refresh tokens and auto-refresh
- Secure registration with email validation and password strength enforcement
- Role-based access control (Candidate, Employer, Admin)
- Editable profile with professional details, skills, and education
- Profile completeness indicator

### 2. Multi-Source Job Search
- **14 job sources** (9 free + 5 API-keyed) including RemoteOK, Arbeitnow, Himalayas, Landing.jobs, Karriere.at, and more
- Real-time scraping with anti-ban measures (rotating user agents, rate limiting)
- Keyword and location-based filtering
- One-click job saving with application tracking
- Source badges showing where each job was found

### 3. ATS Resume Checker
- Upload PDF resumes for instant analysis
- Keyword match scoring against target job descriptions
- Section-by-section feedback (experience, skills, education, formatting)
- Role-specific suggestions powered by Groq LLM
- Actionable improvement tips to beat applicant tracking systems

### 4. Salary Predictor
- ML-powered salary estimation using trained scikit-learn models
- Predictions based on role, experience, location, and skills
- Confidence intervals and market range comparisons
- Visual salary range charts

### 5. Interview Preparation
- **73-question curated bank** across 12 categories (behavioral, technical, system design, etc.)
- LLM-generated questions tailored to specific job roles
- Source attribution for each question (curated vs. AI-generated)
- Category-coded color badges for easy navigation
- 15 well-rounded questions per session (mix of curated + generated)

### 6. Career Path Visualizer
- Interactive graph visualization of career progression
- Nodes and edges showing role transitions and skill requirements
- Explore paths from entry-level to senior/leadership positions
- Visual skill gap analysis

### 7. Cover Letter Generator
- AI-powered cover letters using Groq LLM (Llama 3.3 70B)
- Tailored to specific job descriptions and your resume
- ATS-friendly formatting
- Professional tone with customization options

### 8. Career Recommendations
- TF-IDF-based skill matching across **16 career paths**
- Personalized career suggestions based on your profile
- **100+ curated courses** (6-10 per career) with direct links
- Match percentage scores for each recommended career

### 9. Dark Mode & Theming
- System-wide light/dark mode toggle
- Persistent theme preference stored per user
- Smooth CSS variable transitions across all pages

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+

### Backend Setup

```bash
cd backend
python -m venv venv

# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database URL, secret keys, and API keys

python run.py
# Backend → http://localhost:5000
```

### Frontend Setup

```bash
cd frontend
npm install

# Configure environment
cp .env.example .env
# Edit .env with your API URL

npm start
# Frontend → http://localhost:3000
```

### Docker Setup (Alternative)

```bash
# Start all services (backend, frontend, database)
docker-compose up --build
```

---

## Project Structure

```
HireSkillz/
├── backend/
│   ├── app/
│   │   ├── __init__.py              # App factory, CORS, security headers
│   │   ├── models/                  # SQLAlchemy models
│   │   │   ├── user.py             # User + UserProfile
│   │   │   ├── job.py              # SavedJob + JobApplication
│   │   │   └── document.py         # Resume + CoverLetter
│   │   ├── controllers/            # Business logic
│   │   │   ├── auth_controller.py  # Registration, login, JWT
│   │   │   ├── user_controller.py  # Profile CRUD
│   │   │   ├── job_controller.py   # Job search + save
│   │   │   └── document_controller.py # ATS + document mgmt
│   │   ├── views/                  # API route blueprints
│   │   │   ├── auth_views.py       # /api/auth/*
│   │   │   ├── user_views.py       # /api/users/*
│   │   │   ├── job_views.py        # /api/jobs/*
│   │   │   ├── document_views.py   # /api/documents/*
│   │   │   ├── career_views.py     # /api/career/*
│   │   │   └── salary_views.py     # /api/salary/*
│   │   ├── generators/             # AI content generation
│   │   │   ├── ats_generator.py    # ATS resume analysis
│   │   │   ├── resume_generator.py # Resume building
│   │   │   └── cover_letter_generator.py
│   │   ├── services/               # External integrations
│   │   │   └── job_scraper.py      # 14-source job scraper
│   │   ├── ml/                     # Machine learning models
│   │   └── utils/                  # Validators, responses
│   ├── tests/                      # pytest test suite
│   ├── config.py                   # Env-aware configuration
│   ├── run.py                      # Entry point
│   ├── Procfile                    # Gunicorn (Heroku/Railway)
│   ├── Dockerfile                  # Multi-stage container
│   └── requirements.txt
├── frontend/
│   ├── public/
│   │   ├── favicon.ico             # Custom HireSkillz icon
│   │   ├── logo192.png / logo512.png
│   │   └── robots.txt
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.js           # Navigation + avatar
│   │   │   ├── PrivateRoute.js     # Auth guard
│   │   │   └── ErrorBoundary.js    # React error boundary
│   │   ├── pages/
│   │   │   ├── Home.js
│   │   │   ├── Login.js / Register.js
│   │   │   ├── Dashboard.js
│   │   │   ├── JobSearch.js
│   │   │   ├── ATSChecker.js
│   │   │   ├── SalaryPredictor.js
│   │   │   ├── InterviewPrep.js
│   │   │   ├── CareerPath.js
│   │   │   ├── CoverLetter.js
│   │   │   ├── CareerRecommendations.js
│   │   │   └── NotFound.js         # 404 page
│   │   ├── context/                # AuthContext, ThemeContext
│   │   ├── services/               # API + auth + user services
│   │   └── styles/                 # CSS per component
│   ├── vercel.json                 # Vercel SPA config + headers
│   ├── Dockerfile                  # Multi-stage node → nginx
│   └── package.json
├── docker-compose.yml              # Full-stack orchestration
├── .github/workflows/ci.yml        # GitHub Actions CI
├── LICENSE                         # MIT License
└── CONTRIBUTING.md                 # Contribution guidelines
```

---

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login with JWT |
| POST | `/api/auth/refresh` | Refresh access token |
| GET | `/api/auth/me` | Get current user |

### User Profile
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users/profile` | Get profile |
| PUT | `/api/users/profile` | Update profile |
| PUT | `/api/users/profile/theme` | Update theme |
| GET | `/api/users/` | List users (admin) |

### Jobs
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/jobs/search` | Search jobs across sources |
| POST | `/api/jobs/save` | Save a job listing |
| GET | `/api/jobs/saved` | Get saved jobs |
| DELETE | `/api/jobs/saved/<id>` | Remove saved job |

### Documents & AI
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/documents/ats-check` | ATS resume analysis |
| POST | `/api/documents/cover-letter` | Generate cover letter |
| GET | `/api/documents/interview-questions` | Get interview questions |

### Career & Salary
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/salary/predict` | Predict salary range |
| GET | `/api/career/paths` | Get career paths |
| POST | `/api/career/recommend` | Get career recommendations |

---

## Security

- **CORS Lockdown** — Origin whitelist via `CORS_ORIGINS` env variable
- **Security Headers** — X-Content-Type-Options, X-Frame-Options, X-XSS-Protection, Referrer-Policy, HSTS (production)
- **Secret Key Safety** — App refuses to start in production with default secrets
- **Password Hashing** — Bcrypt with salt rounds
- **JWT Tokens** — Separate access (1h) and refresh (30d) tokens with auto-refresh
- **Input Validation** — Server-side validation on all endpoints
- **SQL Injection Prevention** — SQLAlchemy ORM with parameterized queries
- **DB Connection Pooling** — Pool size, overflow, timeout, and pre-ping configured

---

## Testing

Run the backend test suite:

```bash
cd backend
pytest tests/ -v
```

Tests cover:
- Health endpoint availability
- Security headers on every response
- User registration and login flow
- Authentication error handling
- Interview question bank integrity

---

## Deployment

### Frontend → Vercel

1. Connect your GitHub repo to [Vercel](https://vercel.com)
2. Set root directory to `frontend`
3. Add environment variable: `REACT_APP_API_URL=https://your-backend.com/api`
4. Deploy — `vercel.json` handles SPA routing and security headers

### Backend → Render / Railway

1. Connect your GitHub repo
2. Set root directory to `backend`
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn run:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
5. Add environment variables:
   ```
   FLASK_ENV=production
   DATABASE_URL=postgresql://...
   JWT_SECRET_KEY=<strong-random-key>
   GROQ_API_KEY=<your-groq-key>
   CORS_ORIGINS=https://your-frontend.vercel.app
   ```

### Docker (Self-hosted)

```bash
docker-compose up --build -d
# Backend  → http://localhost:5000
# Frontend → http://localhost:3000
# Database → localhost:5432
```

---

## Environment Variables

### Backend (`backend/.env`)

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `JWT_SECRET_KEY` | Secret for JWT signing | Yes (production) |
| `GROQ_API_KEY` | Groq API key for LLM features | Yes |
| `FLASK_ENV` | `development` or `production` | No (default: development) |
| `CORS_ORIGINS` | Comma-separated allowed origins | No (default: localhost) |
| `PORT` | Server port | No (default: 5000) |

### Frontend (`frontend/.env`)

| Variable | Description |
|----------|-------------|
| `REACT_APP_API_URL` | Backend API base URL |

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React 18, React Router, Context API, CSS3 |
| Backend | Flask 3.0, SQLAlchemy, Flask-JWT-Extended |
| Database | PostgreSQL 15 with connection pooling |
| AI / ML | Groq LLM (Llama 3.3 70B), scikit-learn, TF-IDF |
| Scraping | Requests, BeautifulSoup, rotating user agents |
| Auth | JWT (access + refresh), Bcrypt |
| DevOps | Docker, GitHub Actions CI, Gunicorn |
| Deployment | Vercel (frontend), Render / Railway (backend) |

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please read the [Contributing Guidelines](CONTRIBUTING.md) before submitting a pull request.
