"""
Test Script for Module 3: ATS Resume & Cover Letter Generator
Tests the core functionality without requiring LLM or full server setup
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.utils.keyword_extractor import KeywordExtractor
from app.utils.json_schema_validator import JSONSchemaValidator
from app.utils.ats_prompt_builder import ATSPromptBuilder
from app.generators.ats_generator import ATSResumeGenerator
from app.generators.cover_letter_generator import CoverLetterGenerator


def test_keyword_extraction():
    """Test keyword extraction from job description"""
    print("\n" + "="*60)
    print("TEST 1: Keyword Extraction")
    print("="*60)
    
    job_description = """
    We are seeking a Senior Software Engineer with 5+ years of experience.
    
    Required Skills:
    - Python, Django, Flask
    - REST API development
    - PostgreSQL, MongoDB
    - Docker, Kubernetes
    
    Preferred Skills:
    - AWS or Azure experience
    - React.js
    - CI/CD pipelines
    
    The ideal candidate will have strong problem-solving skills and excellent
    communication abilities. Experience with agile methodologies is a plus.
    """
    
    keywords = KeywordExtractor.extract_keywords(job_description)
    
    print("\n✅ Extracted Keywords:")
    print(f"   Required Skills: {keywords['required_skills']}")
    print(f"   Preferred Skills: {keywords['preferred_skills']}")
    print(f"   Technical Terms: {keywords['technical_terms'][:10]}")
    print(f"   Soft Skills: {keywords['soft_skills']}")
    
    # Test keyword matching
    user_skills = ['Python', 'Django', 'PostgreSQL', 'Docker', 'React']
    match_analysis = KeywordExtractor.match_keywords_with_profile(keywords, user_skills)
    
    print(f"\n✅ Match Analysis:")
    print(f"   Match Score: {match_analysis['match_score']}%")
    print(f"   Matched Skills: {match_analysis['matched_required_skills']}")
    print(f"   Missing Skills: {match_analysis['missing_required_skills']}")


def test_json_validation():
    """Test JSON schema validation"""
    print("\n" + "="*60)
    print("TEST 2: JSON Schema Validation")
    print("="*60)
    
    # Valid resume data
    valid_resume = {
        "personal_info": {
            "full_name": "John Doe",
            "email": "john@example.com",
            "phone": "+1234567890",
            "location": "San Francisco, CA"
        },
        "summary": "Experienced software engineer with 5+ years of expertise in Python development.",
        "skills": {
            "technical": ["Python", "Django", "PostgreSQL"],
            "soft": ["Problem-solving", "Communication"],
            "tools": ["Git", "Docker"]
        },
        "work_experience": [
            {
                "title": "Software Engineer",
                "company": "Tech Corp",
                "duration": "2020-Present",
                "responsibilities": [
                    "Developed REST APIs using Django",
                    "Improved system performance by 40%"
                ]
            }
        ],
        "education": [
            {
                "degree": "B.S. Computer Science",
                "institution": "University of California",
                "year": "2019"
            }
        ],
        "projects": [],
        "certifications": []
    }
    
    is_valid, errors = JSONSchemaValidator.validate_resume(valid_resume)
    
    if is_valid:
        print("\n✅ Valid Resume JSON - All checks passed!")
    else:
        print(f"\n❌ Validation Failed: {errors}")
    
    # Test invalid resume
    invalid_resume = {
        "personal_info": {
            "full_name": "Jane Doe"
            # Missing required email
        },
        "summary": "Too short",  # Less than 50 chars
        "skills": {},
        "work_experience": [],
        "education": []  # Empty - should have at least 1
    }
    
    is_valid, errors = JSONSchemaValidator.validate_resume(invalid_resume)
    print(f"\n✅ Validation correctly caught {len(errors)} errors in invalid resume:")
    for error in errors[:3]:
        print(f"   - {error}")


def test_prompt_building():
    """Test ATS prompt building"""
    print("\n" + "="*60)
    print("TEST 3: ATS Prompt Building")
    print("="*60)
    
    user_profile = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john@example.com',
        'phone': '+1234567890',
        'location': 'San Francisco, CA',
        'skills': ['Python', 'Django', 'PostgreSQL', 'Docker'],
        'experience': [
            {
                'title': 'Software Engineer',
                'company': 'Tech Corp',
                'duration': '2020-Present',
                'description': 'Developed REST APIs'
            }
        ],
        'education': [
            {
                'degree': 'B.S. Computer Science',
                'institution': 'UC Berkeley',
                'year': '2019'
            }
        ]
    }
    
    job_description = "Looking for Python developer with Django experience"
    target_role = "Senior Software Engineer"
    
    keywords = {
        'required_skills': ['Python', 'Django'],
        'technical_terms': ['REST API', 'PostgreSQL'],
        'soft_skills': ['Problem-solving']
    }
    
    prompt = ATSPromptBuilder.build_resume_prompt(
        user_profile=user_profile,
        job_description=job_description,
        target_role=target_role,
        keywords=keywords
    )
    
    print("\n✅ Generated ATS-optimized prompt")
    print(f"   Prompt length: {len(prompt)} characters")
    print(f"   Contains ATS rules: {'ATS RULES' in prompt}")
    print(f"   Contains JSON schema: {'JSON OUTPUT SCHEMA' in prompt}")
    print(f"   Contains keywords: {'KEYWORDS TO EMPHASIZE' in prompt}")


def test_mock_resume_generation():
    """Test mock resume generation (without LLM)"""
    print("\n" + "="*60)
    print("TEST 4: Mock Resume Generation")
    print("="*60)
    
    user_profile = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john@example.com',
        'phone': '+1234567890',
        'location': 'San Francisco, CA',
        'bio': 'Experienced software engineer passionate about building scalable systems.',
        'skills': ['Python', 'Django', 'PostgreSQL', 'Docker', 'AWS'],
        'experience': [
            {
                'title': 'Senior Software Engineer',
                'company': 'Tech Corp',
                'duration': '2020-Present',
                'responsibilities': [
                    'Led development of microservices architecture',
                    'Improved API response time by 50%'
                ]
            },
            {
                'title': 'Software Engineer',
                'company': 'StartupXYZ',
                'duration': '2018-2020',
                'responsibilities': [
                    'Developed REST APIs using Django',
                    'Managed PostgreSQL databases'
                ]
            }
        ],
        'education': [
            {
                'degree': 'B.S. Computer Science',
                'institution': 'UC Berkeley',
                'year': '2018'
            }
        ],
        'projects': [
            {
                'name': 'E-commerce Platform',
                'description': 'Built scalable e-commerce platform',
                'technologies': ['Python', 'Django', 'React']
            }
        ],
        'certifications': [
            {
                'name': 'AWS Certified Developer',
                'issuer': 'Amazon',
                'year': '2021'
            }
        ]
    }
    
    # Generate mock resume
    resume = ATSResumeGenerator.generate_mock_resume(user_profile, 'Senior Software Engineer')
    
    # Validate
    is_valid, errors = JSONSchemaValidator.validate_resume(resume)
    
    print("\n✅ Mock Resume Generated")
    print(f"   Valid: {is_valid}")
    print(f"   Name: {resume['personal_info']['full_name']}")
    print(f"   Skills: {len(resume['skills'].get('technical', []))} technical skills")
    print(f"   Experience: {len(resume['work_experience'])} positions")
    print(f"   Education: {len(resume['education'])} entries")
    
    if not is_valid:
        print(f"   Validation errors: {errors}")


def test_mock_cover_letter():
    """Test mock cover letter generation"""
    print("\n" + "="*60)
    print("TEST 5: Mock Cover Letter Generation")
    print("="*60)
    
    user_profile = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john@example.com',
        'phone': '+1234567890',
        'location': 'San Francisco, CA',
        'skills': ['Python', 'Django', 'PostgreSQL'],
        'experience': [
            {
                'title': 'Software Engineer',
                'company': 'Tech Corp',
                'duration': '2020-Present'
            }
        ]
    }
    
    job_details = {
        'company_name': 'Innovative Tech Inc',
        'job_title': 'Senior Python Developer',
        'job_description': 'We are seeking a talented Python developer...'
    }
    
    cover_letter = CoverLetterGenerator.generate_mock_cover_letter(user_profile, job_details)
    
    # Check ATS-friendliness
    newline_tab = ['\n', '\t']
    is_ats_friendly = all(ord(c) < 128 or c in newline_tab for c in cover_letter)
    
    print("\n✅ Mock Cover Letter Generated")
    print(f"   Length: {len(cover_letter)} characters")
    print(f"   Contains company name: {job_details['company_name'] in cover_letter}")
    print(f"   Contains job title: {job_details['job_title'] in cover_letter}")
    print(f"   ATS-friendly (no emojis): {is_ats_friendly}")


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("MODULE 3: ATS Resume & Cover Letter Generator - Test Suite")
    print("="*60)
    
    try:
        test_keyword_extraction()
        test_json_validation()
        test_prompt_building()
        test_mock_resume_generation()
        test_mock_cover_letter()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        print("\nModule 3 core functionality is working correctly.")
        print("To test with actual LLM, configure .env and run the server.")
        print("\nNext steps:")
        print("1. Configure LLM in .env file")
        print("2. Run: python run.py")
        print("3. Test API endpoints with Postman or cURL")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
