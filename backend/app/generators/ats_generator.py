"""
ATS Resume Generator
Creates Applicant Tracking System (ATS) optimized resumes using LLM
Produces clean, professional, single-column format optimized for ATS parsing
"""

import os
import json
import requests
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from app.utils.keyword_extractor import KeywordExtractor
from app.utils.json_schema_validator import JSONSchemaValidator
from app.utils.ats_prompt_builder import ATSPromptBuilder


class ATSResumeGenerator:
    """Generate ATS-optimized resumes with LLM"""
    
    # LLM Configuration
    LLM_API_URL = os.environ.get('LLM_API_URL', 'http://localhost:11434/api/generate')
    LLM_MODEL = os.environ.get('LLM_MODEL', 'llama2')
    LLM_API_KEY = os.environ.get('LLM_API_KEY', '')
    
    @staticmethod
    def generate_ats_resume(user_profile: Dict, job_description: Optional[str] = None,
                           target_role: Optional[str] = None) -> Tuple[bool, Dict, str]:
        """
        Generate ATS-compliant resume using LLM
        
        Args:
            user_profile: User profile data
            job_description: Job description text (optional)
            target_role: Target job role (optional)
            
        Returns:
            Tuple of (success, resume_json, error_message)
        """
        try:
            # Step 1: Extract keywords from job description
            keywords = None
            if job_description:
                keywords = KeywordExtractor.extract_keywords(job_description)
            
            # Step 2: Build ATS-optimized prompt
            prompt = ATSPromptBuilder.build_resume_prompt(
                user_profile=user_profile,
                job_description=job_description,
                target_role=target_role,
                keywords=keywords
            )
            
            # Step 3: Call LLM to generate resume
            resume_json_str = ATSResumeGenerator._call_llm(prompt)
            
            if not resume_json_str:
                return False, {}, "Failed to generate resume from LLM"
            
            # Step 4: Parse JSON response
            try:
                resume_data = json.loads(resume_json_str)
            except json.JSONDecodeError as e:
                # Try to extract JSON from response
                resume_data = ATSResumeGenerator._extract_json_from_text(resume_json_str)
                if not resume_data:
                    return False, {}, f"Invalid JSON response from LLM: {str(e)}"
            
            # Step 5: Validate against ATS schema
            is_valid, errors = JSONSchemaValidator.validate_resume(resume_data)
            
            if not is_valid:
                print(f"Resume validation errors: {errors}")
                # Try to fix common issues
                resume_data = ATSResumeGenerator._fix_common_issues(resume_data)
                is_valid, errors = JSONSchemaValidator.validate_resume(resume_data)
                
                if not is_valid:
                    return False, resume_data, f"Resume validation failed: {'; '.join(errors)}"
            
            # Step 6: Sanitize for ATS compliance
            _, resume_data, _ = JSONSchemaValidator.validate_and_sanitize(resume_data)
            
            return True, resume_data, ""
            
        except Exception as e:
            import traceback
            print(f"Error in generate_ats_resume: {str(e)}")
            print(traceback.format_exc())
            return False, {}, f"Error generating resume: {str(e)}"
    
    @staticmethod
    def _call_llm(prompt: str, max_retries: int = 3) -> Optional[str]:
        """
        Call LLM API to generate resume
        
        Args:
            prompt: Formatted prompt
            max_retries: Maximum number of retries
            
        Returns:
            Generated resume JSON as string
        """
        for attempt in range(max_retries):
            try:
                # Check if using OpenAI-compatible API
                if 'openai' in ATSResumeGenerator.LLM_API_URL.lower() or ATSResumeGenerator.LLM_API_KEY:
                    return ATSResumeGenerator._call_openai_api(prompt)
                else:
                    return ATSResumeGenerator._call_ollama_api(prompt)
                    
            except Exception as e:
                print(f"LLM API call attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_retries - 1:
                    raise
        
        return None
    
    @staticmethod
    def _call_openai_api(prompt: str) -> str:
        """Call OpenAI-compatible API"""
        headers = {
            'Content-Type': 'application/json',
        }
        
        if ATSResumeGenerator.LLM_API_KEY:
            headers['Authorization'] = f'Bearer {ATSResumeGenerator.LLM_API_KEY}'
        
        payload = {
            'model': ATSResumeGenerator.LLM_MODEL,
            'messages': [
                {
                    'role': 'system',
                    'content': 'You are an expert ATS resume writer. Output only valid JSON, no additional text.'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'temperature': 0.7,
            'max_tokens': 2000
        }
        
        response = requests.post(
            ATSResumeGenerator.LLM_API_URL,
            json=payload,
            headers=headers,
            timeout=60
        )
        
        response.raise_for_status()
        result = response.json()
        
        # Extract content from response
        if 'choices' in result and len(result['choices']) > 0:
            return result['choices'][0]['message']['content']
        elif 'response' in result:
            return result['response']
        else:
            raise ValueError("Unexpected API response format")
    
    @staticmethod
    def _call_ollama_api(prompt: str) -> str:
        """Call Ollama API"""
        payload = {
            'model': ATSResumeGenerator.LLM_MODEL,
            'prompt': prompt,
            'stream': False,
            'format': 'json'
        }
        
        response = requests.post(
            ATSResumeGenerator.LLM_API_URL,
            json=payload,
            timeout=60
        )
        
        response.raise_for_status()
        result = response.json()
        
        return result.get('response', '')
    
    @staticmethod
    def _extract_json_from_text(text: str) -> Optional[Dict]:
        """Extract JSON object from text that may contain additional content"""
        # Try to find JSON in code blocks
        import re
        
        # Remove markdown code blocks
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```\s*', '', text)
        
        # Find JSON object
        json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
        matches = re.finditer(json_pattern, text, re.DOTALL)
        
        for match in matches:
            try:
                json_obj = json.loads(match.group(0))
                # Check if it looks like a resume (has required fields)
                if 'personal_info' in json_obj or 'summary' in json_obj:
                    return json_obj
            except:
                continue
        
        return None
    
    @staticmethod
    def _fix_common_issues(resume_data: Dict) -> Dict:
        """Fix common validation issues in resume data"""
        fixed = resume_data.copy()
        
        # Ensure required fields exist
        if 'personal_info' not in fixed:
            fixed['personal_info'] = {}
        
        if 'summary' not in fixed or not fixed['summary']:
            fixed['summary'] = "Professional with experience in various domains."
        
        if 'skills' not in fixed:
            fixed['skills'] = {'technical': [], 'soft': [], 'tools': []}
        elif not isinstance(fixed['skills'], dict):
            fixed['skills'] = {'technical': [], 'soft': [], 'tools': []}
        
        if 'work_experience' not in fixed:
            fixed['work_experience'] = []
        
        if 'education' not in fixed:
            fixed['education'] = []
        
        if 'projects' not in fixed:
            fixed['projects'] = []
        
        if 'certifications' not in fixed:
            fixed['certifications'] = []
        
        # Fix work experience items
        if isinstance(fixed['work_experience'], list):
            for i, exp in enumerate(fixed['work_experience']):
                if not isinstance(exp.get('responsibilities'), list):
                    fixed['work_experience'][i]['responsibilities'] = []
                elif len(exp['responsibilities']) < 2:
                    # Add placeholder responsibilities
                    fixed['work_experience'][i]['responsibilities'].append("Performed job duties")
        
        return fixed
    
    @staticmethod
    def generate_mock_resume(user_profile: Dict, target_role: Optional[str] = None) -> Dict:
        """
        Generate a mock ATS-compliant resume without LLM (for testing)
        
        Args:
            user_profile: User profile data
            target_role: Target job role
            
        Returns:
            Mock resume data
        """
        return {
            "personal_info": {
                "full_name": f"{user_profile.get('first_name', '')} {user_profile.get('last_name', '')}".strip(),
                "email": user_profile.get('email', ''),
                "phone": user_profile.get('phone', ''),
                "location": user_profile.get('location', ''),
                "linkedin": user_profile.get('linkedin_url', ''),
                "github": user_profile.get('github_url', ''),
                "portfolio": user_profile.get('portfolio_url', '')
            },
            "summary": user_profile.get('bio', f"Experienced professional seeking {target_role or 'new opportunities'}. Skilled in various technologies and committed to delivering high-quality results."),
            "skills": {
                "technical": user_profile.get('skills', [])[:10],
                "soft": ["Communication", "Problem-solving", "Team collaboration"],
                "tools": ["Git", "VS Code", "Jira"]
            },
            "work_experience": user_profile.get('experience', [])[:5] if user_profile.get('experience') else [],
            "projects": user_profile.get('projects', [])[:5] if user_profile.get('projects') else [],
            "education": user_profile.get('education', [])[:3] if user_profile.get('education') else [],
            "certifications": user_profile.get('certifications', [])[:5] if user_profile.get('certifications') else []
        }
