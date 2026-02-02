# Module 3 Quick Reference Card

## 📡 API Endpoints

```
BASE URL: http://localhost:5000/api

Authentication: Bearer Token (JWT) in Authorization header
```

### Resume APIs

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/resume/generate` | Generate ATS resume | ✅ Yes |
| GET | `/resume` | Get all resumes | ✅ Yes |
| GET | `/resume/<id>` | Get specific resume | ✅ Yes |
| GET | `/resume/<id>/download` | Download PDF | ✅ Yes |
| GET | `/resume/versions/<user_id>` | Get version history | ✅ Yes |
| PUT | `/resume/<id>` | Update resume | ✅ Yes |
| DELETE | `/resume/<id>` | Delete resume | ✅ Yes |

### Cover Letter APIs

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/cover-letter/generate` | Generate cover letter | ✅ Yes |
| GET | `/cover-letter` | Get all cover letters | ✅ Yes |
| GET | `/cover-letter/<id>` | Get specific | ✅ Yes |
| DELETE | `/cover-letter/<id>` | Delete | ✅ Yes |

## 🔧 Request Examples

### Generate Resume

```bash
curl -X POST http://localhost:5000/api/resume/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "target_role": "Software Engineer",
    "job_description": "We are looking for a Python developer with Django experience..."
  }'
```

### Download PDF

```bash
curl -X GET http://localhost:5000/api/resume/1/download \
  -H "Authorization: Bearer YOUR_TOKEN" \
  --output resume.pdf
```

### Generate Cover Letter

```bash
curl -X POST http://localhost:5000/api/cover-letter/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "company_name": "Tech Corp",
    "job_title": "Software Engineer",
    "job_description": "We are seeking...",
    "tone": "professional"
  }'
```

## 📦 Required Fields

### Resume Generation
- ✅ None required (uses profile data)
- 📝 Optional: `target_role`, `job_description`, `template`

### Cover Letter Generation
- ✅ Required: `company_name`, `job_title`
- 📝 Optional: `job_description`, `tone`, `resume_id`

## 🎯 Response Format

```json
{
  "success": true,
  "message": "Resume generated successfully",
  "data": {
    "resume": {
      "id": 1,
      "title": "Resume - Software Engineer",
      "target_role": "Software Engineer",
      "content": { /* JSON resume */ },
      "is_ats_optimized": true,
      "keywords_matched": {
        "matched_skills": ["Python", "Django"],
        "match_score": 85.5
      },
      "created_at": "2026-01-28T10:30:00",
      "version": 1
    }
  }
}
```

## ⚙️ Environment Variables

```bash
# LLM Configuration (Using Groq - Fast & Free)
LLM_API_URL=https://api.groq.com/openai/v1/chat/completions
LLM_MODEL=llama-3.3-70b-versatile
LLM_API_KEY=your-groq-api-key

# Database
DATABASE_URL=postgresql://user:pass@localhost/hireskill_db

# JWT
JWT_SECRET_KEY=your-secret-key
JWT_ACCESS_TOKEN_EXPIRES=3600
```

## 🧪 Testing

```bash
# Run test suite
cd backend
python test_module3.py

# Expected output
✅ Keyword Extraction - Passed
✅ JSON Validation - Passed
✅ Prompt Building - Passed
✅ Mock Resume Generation - Passed
✅ Mock Cover Letter - Passed
```

## 🚨 Common Errors

| Error Code | Message | Solution |
|------------|---------|----------|
| 401 | Unauthorized | Include valid JWT token |
| 404 | User profile not found | Complete user profile first |
| 400 | Invalid input | Check required fields |
| 500 | LLM generation failed | Check LLM service, fallback to mock |

## 📋 Resume JSON Schema

```json
{
  "personal_info": {
    "full_name": "string",
    "email": "string",
    "phone": "string"
  },
  "summary": "string (50-500 chars)",
  "skills": {
    "technical": ["array"],
    "soft": ["array"],
    "tools": ["array"]
  },
  "work_experience": [
    {
      "title": "string",
      "company": "string",
      "duration": "string",
      "responsibilities": ["array"]
    }
  ],
  "education": [{...}],
  "projects": [{...}],
  "certifications": [{...}]
}
```

## 🔒 Security

- ✅ JWT authentication required
- ✅ User authorization (own data only)
- ✅ Input validation
- ✅ SQL injection protection
- ✅ XSS prevention
- ✅ Schema validation

## 📈 Performance

- ⚡ LLM timeout: 60 seconds
- ⚡ Retry logic: 3 attempts
- ⚡ Fallback: Mock generation if LLM fails
- ⚡ PDF generation: < 1 second
- ⚡ Keyword extraction: < 100ms

## 🎨 ATS Compliance Checklist

- ✅ Single-column layout
- ✅ Standard fonts (Helvetica, Arial)
- ✅ No tables or graphics
- ✅ Standard section headings
- ✅ Simple bullet points (•)
- ✅ No emojis or special characters
- ✅ Black text on white background
- ✅ Keyword-optimized content

## 💡 Best Practices

1. **Always provide job description** for better keyword matching
2. **Complete user profile** before generating resumes
3. **Review generated content** before downloading
4. **Test PDF output** with actual ATS systems
5. **Use professional tone** for cover letters
6. **Keep cover letters** concise (250-400 words)
7. **Download PDFs** for final submission
8. **Track versions** for different job applications

## 🛠️ Troubleshooting

### Groq API not responding?
```bash
# Test the API connection
python test_groq_api.py

# Check if API key is set
echo $env:LLM_API_KEY  # Windows
# Should show: gsk_...

# Verify in .env file
cat .env | Select-String "LLM_API"
```

### Invalid JSON from LLM?
- System auto-fixes common issues
- Falls back to mock data
- Try different temperature setting

### PDF download fails?
```bash
# Install reportlab
pip install reportlab==4.0.7

# Check resume content
curl -X GET http://localhost:5000/api/resume/1 \
  -H "Authorization: Bearer TOKEN"
```

## 📚 Documentation

- 📖 Full Documentation: `MODULE_3_DOCUMENTATION.md`
- 📋 Implementation Summary: `MODULE_3_IMPLEMENTATION_SUMMARY.md`
- 🎨 Frontend Guide: `FRONTEND_INTEGRATION_GUIDE.md`
- 🧪 Test Suite: `backend/test_module3.py`

## 🚀 Quick Start Commands

```bash
# 1. Setup
cd backend
pip install -r requirements.txt
cp .env.example .env

# 2. Configure database
# Edit .env and update DATABASE_URL with your PostgreSQL password

# 3. Groq API is already configured!
# Test it:
python test_groq_api.py

# 4. Run database migrations
flask db migrate -m "Add ATS fields to Resume model"
flask db upgrade

# 5. Start server
python run.py

# 6. Test Module 3
python test_module3.py

# 7. Generate resume (after login)
curl -X POST http://localhost:5000/api/resume/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{"target_role": "Software Engineer"}'
```

---

**Version:** 1.0
**Date:** January 28, 2026
**Status:** ✅ Production Ready
