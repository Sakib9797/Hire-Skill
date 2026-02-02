# Module 3: ATS-Friendly Resume & Cover Letter Generator

## Overview
This module implements AI-powered ATS (Applicant Tracking System) compliant resume and cover letter generation using LLM technology. All resumes follow strict ATS compliance rules to ensure maximum compatibility with automated screening systems.

## Features

### ✅ ATS-Compliant Resume Generation
- **Single-column layout** - No tables, graphics, or complex formatting
- **Standard section headings** - SUMMARY, SKILLS, WORK EXPERIENCE, PROJECTS, EDUCATION, CERTIFICATIONS
- **Keyword optimization** - Extracts and matches keywords from job descriptions
- **JSON schema validation** - Strict validation ensures ATS compatibility
- **Version tracking** - Maintains history of all generated resumes
- **PDF export** - ATS-friendly PDF format for download

### ✅ Cover Letter Generation
- **AI-powered personalization** - Tailored to job role and company
- **Professional tone** - ATS-neutral, no emojis or special formatting
- **Keyword integration** - Natural incorporation of job-relevant keywords
- **Multiple formats** - Text output optimized for ATS systems

### ✅ Keyword Extraction & Matching
- **Intelligent parsing** - Extracts technical skills, soft skills, and requirements
- **Match scoring** - Calculates compatibility between profile and job description
- **Recommendations** - Suggests skills to highlight or acquire

## Architecture

### Backend Structure
```
backend/
├── app/
│   ├── models/
│   │   └── document.py              # Resume & CoverLetter models with versioning
│   ├── controllers/
│   │   └── document_controller.py   # Business logic for document generation
│   ├── views/
│   │   └── document_views.py        # API endpoints
│   ├── generators/
│   │   ├── ats_generator.py         # ATS-compliant resume generator with LLM
│   │   └── cover_letter_generator.py # Cover letter generator with LLM
│   └── utils/
│       ├── keyword_extractor.py     # Extract keywords from job descriptions
│       ├── json_schema_validator.py # Validate resume JSON against ATS schema
│       ├── ats_prompt_builder.py    # Build optimized prompts for LLM
│       └── pdf_generator.py         # Generate ATS-friendly PDFs
```

## API Endpoints

### 1. Generate Resume
**POST** `/api/resume/generate`

Generate a new ATS-compliant resume.

**Request Body:**
```json
{
  "target_role": "Software Engineer",
  "job_description": "We are looking for a Software Engineer with Python...",
  "template": "ats_professional"
}
```

**Response:**
```json
{
  "success": true,
  "message": "ATS-compliant resume generated successfully",
  "data": {
    "resume": {
      "id": 1,
      "title": "Resume - Software Engineer",
      "target_role": "Software Engineer",
      "content": {
        "personal_info": {...},
        "summary": "...",
        "skills": {...},
        "work_experience": [...],
        "education": [...]
      },
      "is_ats_optimized": true,
      "keywords_matched": {
        "matched_skills": ["Python", "Django", "REST API"],
        "match_score": 85.5
      }
    }
  }
}
```

### 2. Get All Resumes
**GET** `/api/resume?current_only=false`

Retrieve all user resumes or only current versions.

**Response:**
```json
{
  "success": true,
  "message": "Resumes retrieved successfully",
  "data": {
    "resumes": [...],
    "total": 5
  }
}
```

### 3. Get Specific Resume
**GET** `/api/resume/<resume_id>`

Retrieve a specific resume by ID.

### 4. Download Resume as PDF
**GET** `/api/resume/<resume_id>/download`

Download resume as ATS-friendly PDF.

**Response:** PDF file download

### 5. Get Resume Versions
**GET** `/api/resume/versions/<user_id>`

Get all resume versions for a user (version history).

### 6. Generate Cover Letter
**POST** `/api/cover-letter/generate`

Generate an ATS-friendly cover letter.

**Request Body:**
```json
{
  "company_name": "Tech Corp",
  "job_title": "Software Engineer",
  "job_description": "We are seeking...",
  "tone": "professional",
  "resume_id": 1
}
```

**Response:**
```json
{
  "success": true,
  "message": "Cover letter generated successfully",
  "data": {
    "cover_letter": {
      "id": 1,
      "title": "Cover Letter - Software Engineer at Tech Corp",
      "content": "Dear Hiring Manager,\n\n...",
      "company_name": "Tech Corp",
      "job_title": "Software Engineer"
    }
  }
}
```

## ATS Compliance Rules

### ✅ Required Format Rules
1. **Single-column layout** - No tables or multi-column formats
2. **Standard fonts** - Helvetica, Arial (no custom fonts)
3. **Standard headings** - Use ONLY: SUMMARY, SKILLS, WORK EXPERIENCE, PROJECTS, EDUCATION, CERTIFICATIONS
4. **Simple bullets** - Use • for lists, no graphics
5. **No special characters** - ASCII only, no emojis
6. **No headers/footers** - All content in main body
7. **Black text on white** - No colors or backgrounds

### ✅ Content Rules
1. **Keyword optimization** - Include relevant keywords naturally
2. **Action verbs** - Start bullet points with action verbs
3. **Quantified achievements** - Use numbers, percentages, metrics
4. **Consistent tense** - Present for current, past for previous roles
5. **Standard job titles** - Use industry-standard terminology

## Resume JSON Schema

All generated resumes follow this strict schema:

```json
{
  "personal_info": {
    "full_name": "string (required)",
    "email": "string (required)",
    "phone": "string",
    "location": "string",
    "linkedin": "string",
    "github": "string",
    "portfolio": "string"
  },
  "summary": "string (50-500 chars, professional summary)",
  "skills": {
    "technical": ["array of technical skills"],
    "soft": ["array of soft skills"],
    "tools": ["array of tools/technologies"]
  },
  "work_experience": [
    {
      "title": "string",
      "company": "string",
      "location": "string",
      "duration": "string",
      "responsibilities": ["array of 2-5 bullet points"]
    }
  ],
  "projects": [
    {
      "name": "string",
      "description": "string",
      "technologies": ["array"],
      "link": "string"
    }
  ],
  "education": [
    {
      "degree": "string",
      "institution": "string",
      "location": "string",
      "year": "string",
      "gpa": "string (optional)"
    }
  ],
  "certifications": [
    {
      "name": "string",
      "issuer": "string",
      "year": "string",
      "credential_id": "string"
    }
  ]
}
```

## LLM Configuration

### Supported LLM Providers

#### Option 1: Ollama (Recommended for Development)
```bash
# Install Ollama
# Visit: https://ollama.ai

# Pull a model
ollama pull llama2

# Configure .env
LLM_API_URL=http://localhost:11434/api/generate
LLM_MODEL=llama2
LLM_API_KEY=
```

#### Option 2: OpenAI
```bash
# Get API key from https://platform.openai.com/api-keys

# Configure .env
LLM_API_URL=https://api.openai.com/v1/chat/completions
LLM_MODEL=gpt-3.5-turbo
LLM_API_KEY=sk-your-api-key-here
```

#### Option 3: LM Studio (Local)
```bash
# Download LM Studio from https://lmstudio.ai
# Download and load a model
# Start local server

# Configure .env
LLM_API_URL=http://localhost:1234/v1/chat/completions
LLM_MODEL=your-model-name
LLM_API_KEY=
```

## Setup Instructions

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy example env file
cp .env.example .env

# Edit .env and configure:
# - DATABASE_URL
# - JWT_SECRET_KEY
# - LLM_API_URL, LLM_MODEL, LLM_API_KEY
```

### 3. Run Database Migrations
```bash
# Create database
python create_db.py

# Run migrations (if using Flask-Migrate)
flask db upgrade
```

### 4. Start the Server
```bash
python run.py
```

## Testing

### Test Resume Generation
```bash
# Test with mock data (no LLM required)
python test_resume_gen.py
```

### Test API Endpoints
```bash
# Test document API
python test_document_api.py
```

### Manual Testing with cURL

```bash
# 1. Register/Login to get JWT token
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password"}'

# 2. Generate resume
curl -X POST http://localhost:5000/api/resume/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "target_role": "Software Engineer",
    "job_description": "Looking for Python developer with Django experience..."
  }'

# 3. Download PDF
curl -X GET http://localhost:5000/api/resume/1/download \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  --output resume.pdf
```

## Key Components

### 1. Keyword Extractor (`keyword_extractor.py`)
- Extracts required vs preferred skills
- Identifies technical terms and soft skills
- Calculates match scores
- Provides recommendations

### 2. JSON Schema Validator (`json_schema_validator.py`)
- Validates resume structure
- Ensures ATS compliance
- Sanitizes content (removes emojis, special chars)
- Provides detailed error messages

### 3. ATS Prompt Builder (`ats_prompt_builder.py`)
- Builds optimized prompts for LLM
- Includes ATS compliance instructions
- Incorporates job keywords
- Formats user profile data

### 4. ATS Resume Generator (`ats_generator.py`)
- Calls LLM API with optimized prompts
- Validates generated JSON
- Handles API errors with retries
- Falls back to mock data if LLM fails

### 5. PDF Generator (`pdf_generator.py`)
- Generates ATS-friendly PDFs
- Uses simple single-column layout
- Standard fonts (Helvetica)
- Clean formatting without graphics

## Database Schema

### Resume Table
```sql
CREATE TABLE resumes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    title VARCHAR(200) NOT NULL,
    target_role VARCHAR(100),
    job_description TEXT,
    content JSONB NOT NULL,
    version INTEGER DEFAULT 1,
    is_current BOOLEAN DEFAULT TRUE,
    parent_id INTEGER REFERENCES resumes(id),
    is_ats_optimized BOOLEAN DEFAULT TRUE,
    template_name VARCHAR(50),
    keywords_matched JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Cover Letter Table
```sql
CREATE TABLE cover_letters (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    resume_id INTEGER REFERENCES resumes(id),
    title VARCHAR(200) NOT NULL,
    company_name VARCHAR(200),
    job_title VARCHAR(200),
    content TEXT NOT NULL,
    version INTEGER DEFAULT 1,
    is_current BOOLEAN DEFAULT TRUE,
    parent_id INTEGER REFERENCES cover_letters(id),
    tone VARCHAR(50) DEFAULT 'professional',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

## Error Handling

The system implements comprehensive error handling:

1. **LLM Failures**: Falls back to mock resume generation
2. **Validation Errors**: Returns detailed error messages
3. **Missing Data**: Provides helpful prompts for users
4. **API Timeouts**: Implements retry logic with exponential backoff

## Best Practices

### For Resume Generation
1. Always provide job description for better keyword matching
2. Complete user profile before generating resumes
3. Review and customize generated content
4. Test PDF output for ATS compatibility

### For Cover Letters
1. Provide detailed job descriptions
2. Use professional tone for ATS systems
3. Keep content concise (250-400 words)
4. Include specific company research

## Troubleshooting

### LLM Not Responding
- Check LLM_API_URL is correct
- Verify LLM service is running (Ollama/LM Studio)
- Check API key if using OpenAI
- Review server logs for detailed errors

### Invalid JSON from LLM
- System automatically attempts to fix common issues
- Falls back to mock data if unfixable
- Check LLM model quality (try different model)

### PDF Generation Fails
- Ensure reportlab is installed
- Check resume content is valid JSON
- Review error logs for specific issues

## Future Enhancements

- [ ] Support for multiple languages
- [ ] Custom template builder
- [ ] A/B testing for resume variations
- [ ] Integration with job boards
- [ ] Real-time ATS score preview
- [ ] Industry-specific templates
- [ ] Cover letter templates library

## License
Part of Hire-Skill AI Career Guidance Platform

## Support
For issues or questions, please refer to the main project documentation.
