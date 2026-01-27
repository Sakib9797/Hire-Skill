# AI Career Path Recommendation API - Testing Guide

## Module 2: AI Career Path Recommendation - IMPLEMENTATION COMPLETE ✓

### Overview
AI-powered career recommendation system using:
- **Machine Learning**: Scikit-learn with TF-IDF vectorization
- **Algorithm**: Cosine similarity for matching user profiles to careers
- **Features**: Skill gap analysis, learning path generation, personalized recommendations

---

## API Endpoints

### 1. Health Check
**GET** `/api/career/health`

Check if the career recommendation service is running.

```bash
curl http://localhost:5000/api/career/health
```

**Response:**
```json
{
  "success": true,
  "message": "Career recommendation service is operational",
  "data": {
    "status": "healthy",
    "service": "Career Recommendation Service",
    "model": "TF-IDF + Cosine Similarity",
    "total_careers": 15,
    "total_skills": 150+,
    "features": [
      "AI-powered career matching",
      "Skill gap analysis",
      "Learning path recommendations",
      "Similarity-based ranking"
    ]
  }
}
```

---

### 2. Get Career Recommendations (Protected)
**GET** `/api/career/recommend?top_n=5`

Get personalized career recommendations based on user profile.

**Authentication Required**: Bearer Token

**Query Parameters:**
- `top_n` (optional): Number of recommendations (default: 5, max: 15)

```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  "http://localhost:5000/api/career/recommend?top_n=5"
```

**Response:**
```json
{
  "success": true,
  "message": "Found 5 career matches based on your profile",
  "data": {
    "recommendations": [
      {
        "role": "Full Stack Developer",
        "category": "Software Development",
        "similarity_score": 85.5,
        "skill_match_percentage": 70.0,
        "description": "Develops both frontend and backend of web applications",
        "average_salary": "$85,000 - $130,000",
        "growth_rate": "High",
        "required_skills": ["JavaScript", "React", "Node.js", "Python", "..."],
        "optional_skills": ["AWS", "GraphQL", "Kubernetes", "..."],
        "skill_gaps": {
          "missing_required": ["Docker", "TypeScript"],
          "missing_optional": ["AWS", "Kubernetes"],
          "matched_required": ["JavaScript", "React", "Python"],
          "required_match_percentage": 75.0
        },
        "reasoning": "Excellent fit based on your skills and interests. You already have 8 out of 15 required skills (53%). Focus on learning: Docker, TypeScript, REST API. High demand career with excellent growth prospects."
      }
    ],
    "user_skills": ["JavaScript", "Python", "React", "..."],
    "total_careers_analyzed": 15
  }
}
```

---

### 3. Skill Gap Analysis (Protected)
**GET** `/api/career/skill-gap/<career_role>`

Get detailed skill gap analysis for a specific career path.

**Authentication Required**: Bearer Token

```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  "http://localhost:5000/api/career/skill-gap/Data%20Scientist"
```

**Response:**
```json
{
  "success": true,
  "message": "Skill gap analysis completed",
  "data": {
    "career": "Data Scientist",
    "category": "Data Science",
    "current_match": "45.5%",
    "skills_you_have": ["Python", "SQL", "Statistics"],
    "skills_needed": ["Machine Learning", "TensorFlow", "Pandas", "NumPy"],
    "bonus_skills": ["PyTorch", "Deep Learning", "NLP"],
    "learning_path": [
      {
        "phase": "Phase 1: Essential Skills",
        "priority": "High",
        "skills": ["Machine Learning", "Pandas", "NumPy", "Scikit-learn"],
        "timeline": "3-6 months"
      },
      {
        "phase": "Phase 2: Advanced Skills",
        "priority": "Low",
        "skills": ["PyTorch", "Deep Learning"],
        "timeline": "12+ months"
      }
    ],
    "estimated_time_to_ready": "6-12 months of dedicated study"
  }
}
```

---

### 4. List All Careers
**GET** `/api/career/careers`

Get list of all available career paths.

**No Authentication Required**

```bash
curl http://localhost:5000/api/career/careers
```

**Response:**
```json
{
  "success": true,
  "message": "Available career paths retrieved successfully",
  "data": {
    "careers": [
      {
        "role": "Full Stack Developer",
        "category": "Software Development",
        "description": "Develops both frontend and backend...",
        "required_skills_count": 15,
        "average_salary": "$85,000 - $130,000",
        "growth_rate": "High"
      }
    ],
    "total_careers": 15,
    "categories": {
      "Software Development": ["Full Stack Developer", "Frontend Developer", "Backend Developer"],
      "Data Science": ["Data Scientist", "Data Engineer"],
      "AI/ML": ["Machine Learning Engineer"],
      "...": ["..."]
    }
  }
}
```

---

### 5. Get Career Details
**GET** `/api/career/careers/<role_name>`

Get detailed information about a specific career.

```bash
curl "http://localhost:5000/api/career/careers/Full%20Stack%20Developer"
```

**Response:**
```json
{
  "success": true,
  "message": "Details for Full Stack Developer retrieved successfully",
  "data": {
    "career": {
      "role": "Full Stack Developer",
      "category": "Software Development",
      "required_skills": ["JavaScript", "React", "Node.js", "..."],
      "optional_skills": ["AWS", "GraphQL", "..."],
      "description": "Develops both frontend and backend of web applications",
      "average_salary": "$85,000 - $130,000",
      "growth_rate": "High"
    }
  }
}
```

---

### 6. Get Available Skills
**GET** `/api/career/skills`

Get list of all skills across careers (for autocomplete/suggestions).

```bash
curl http://localhost:5000/api/career/skills
```

**Response:**
```json
{
  "success": true,
  "message": "Available skills retrieved successfully",
  "data": {
    "skills": ["A/B Testing", "AWS", "Agile", "Angular", "Ansible", "..."],
    "total_skills": 150
  }
}
```

---

## Testing Instructions

### Step 1: Start the Backend
```bash
cd d:\Github\Hire-Skill\backend
python run.py
```

### Step 2: Test Health Endpoint (No Auth)
Open browser: http://localhost:5000/api/career/health

### Step 3: Login and Get Token
1. Go to http://localhost:3000/login
2. Login with your credentials
3. Open browser DevTools (F12) → Application → Local Storage
4. Copy the `accessToken` value

### Step 4: Test Recommendations (With Auth)
```bash
# Replace YOUR_TOKEN with the actual token
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:5000/api/career/recommend?top_n=5"
```

### Step 5: Add Skills to Your Profile
1. Go to http://localhost:3000/dashboard
2. Edit your profile
3. Add skills like: Python, JavaScript, React, Machine Learning, etc.
4. Save profile

### Step 6: Get Recommendations Again
The recommendations will now be personalized based on your skills!

---

## Career Paths Available (15 Total)

### Software Development
- Full Stack Developer
- Frontend Developer
- Backend Developer
- Mobile Developer

### Data & AI
- Data Scientist
- Machine Learning Engineer
- Data Engineer

### Infrastructure & Security
- DevOps Engineer
- Cloud Architect
- Cybersecurity Analyst

### Design & Product
- UI/UX Designer
- Product Manager

### Other
- QA Engineer
- Blockchain Developer
- Business Analyst

---

## Machine Learning Implementation

### Feature Extraction
- Extracts skills and interests from user profile
- Converts to TF-IDF feature vectors
- Handles multi-word skills (e.g., "Machine Learning", "CI/CD")

### Recommendation Algorithm
1. **Vectorization**: User skills → TF-IDF vector
2. **Similarity**: Cosine similarity with 15 career vectors
3. **Ranking**: Sort by similarity score + skill match %
4. **Gap Analysis**: Identify missing required/optional skills
5. **Reasoning**: Generate human-readable explanations

### Skill Gap Analysis
- Calculates % of required skills matched
- Identifies missing required & optional skills
- Generates learning path with phases and timelines
- Estimates time to become job-ready

---

## Error Handling

### No Skills in Profile
```json
{
  "success": false,
  "error": "Please add skills and interests to your profile to get personalized recommendations",
  "message": "Add at least 3-5 skills related to your expertise or learning goals"
}
```

### Career Not Found
```json
{
  "success": false,
  "error": "Career 'XYZ Developer' not found",
  "available_careers": ["Full Stack Developer", "..."]
}
```

### No Authentication Token
```json
{
  "msg": "Missing Authorization Header"
}
```

---

## Success Criteria ✓

✅ **Feature extraction from user profile** - Implemented with TF-IDF vectorization
✅ **ML-based recommendation** - Cosine similarity with skill matching
✅ **API endpoint: /api/career/recommend** - Created with authentication
✅ **Recommended career roles** - Returns top N matches with scores
✅ **Reasoning** - Generates skill gap explanation and learning paths
✅ **Scikit-learn integration** - TfidfVectorizer + cosine_similarity
✅ **Pretrained dataset** - 15 careers with 150+ unique skills
✅ **No errors** - All endpoints tested and working

---

## Next Steps (Optional Enhancements)

1. **Frontend Integration**: Create React component to display recommendations
2. **Skill Autocomplete**: Use /api/career/skills for typeahead
3. **Learning Resources**: Add course recommendations for skill gaps
4. **Career Roadmap**: Visualize learning path with timeline
5. **Model Training**: Add user feedback to improve recommendations
6. **Advanced ML**: Implement collaborative filtering or neural networks

---

**Status**: ✅ **MODULE 2 COMPLETE - AI Career Recommendation System Fully Implemented**
