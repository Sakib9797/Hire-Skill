"""
Cover Letter Generator
Generates ATS-friendly personalized cover letters using LLM
"""

import os
import json
import requests
from typing import Dict, Optional, Tuple
from datetime import datetime
from app.utils.ats_prompt_builder import ATSPromptBuilder


class CoverLetterGenerator:
    """Generate ATS-friendly personalized cover letters"""
    
    # LLM Configuration
    LLM_API_URL = os.environ.get('LLM_API_URL', 'http://localhost:11434/api/generate')
    LLM_MODEL = os.environ.get('LLM_MODEL', 'llama2')
    LLM_API_KEY = os.environ.get('LLM_API_KEY', '')
    
    @staticmethod
    def generate_cover_letter(user_profile: Dict, job_details: Dict, 
                             tone: str = 'professional') -> Tuple[bool, str, str]:
        """
        Generate ATS-friendly cover letter using LLM
        
        Args:
            user_profile: User profile data
            job_details: Job details (company_name, job_title, job_description)
            tone: Tone of the letter (professional, friendly, formal)
            
        Returns:
            Tuple of (success, cover_letter_text, error_message)
        """
        try:
            company_name = job_details.get('company_name', 'Company')
            job_title = job_details.get('job_title', 'Position')
            job_description = job_details.get('job_description', '')
            
            # Build prompt for cover letter
            prompt = ATSPromptBuilder.build_cover_letter_prompt(
                user_profile=user_profile,
                job_description=job_description,
                company_name=company_name,
                job_title=job_title
            )
            
            # Call LLM to generate cover letter
            cover_letter_text = CoverLetterGenerator._call_llm(prompt)
            
            if not cover_letter_text:
                return False, "", "Failed to generate cover letter from LLM"
            
            # Sanitize for ATS compliance (remove emojis, special chars)
            cover_letter_text = CoverLetterGenerator._sanitize_text(cover_letter_text)
            
            return True, cover_letter_text, ""
            
        except Exception as e:
            import traceback
            print(f"Error in generate_cover_letter: {str(e)}")
            print(traceback.format_exc())
            return False, "", f"Error generating cover letter: {str(e)}"
    
    @staticmethod
    def _call_llm(prompt: str, max_retries: int = 3) -> Optional[str]:
        """Call LLM API to generate cover letter"""
        for attempt in range(max_retries):
            try:
                # Check if using OpenAI-compatible API
                if 'openai' in CoverLetterGenerator.LLM_API_URL.lower() or CoverLetterGenerator.LLM_API_KEY:
                    return CoverLetterGenerator._call_openai_api(prompt)
                else:
                    return CoverLetterGenerator._call_ollama_api(prompt)
                    
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
        
        if CoverLetterGenerator.LLM_API_KEY:
            headers['Authorization'] = f'Bearer {CoverLetterGenerator.LLM_API_KEY}'
        
        payload = {
            'model': CoverLetterGenerator.LLM_MODEL,
            'messages': [
                {
                    'role': 'system',
                    'content': 'You are a professional cover letter writer. Create ATS-friendly, professional cover letters without emojis or special formatting.'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'temperature': 0.7,
            'max_tokens': 1000
        }
        
        response = requests.post(
            CoverLetterGenerator.LLM_API_URL,
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
            'model': CoverLetterGenerator.LLM_MODEL,
            'prompt': prompt,
            'stream': False
        }
        
        response = requests.post(
            CoverLetterGenerator.LLM_API_URL,
            json=payload,
            timeout=60
        )
        
        response.raise_for_status()
        result = response.json()
        
        return result.get('response', '')
    
    @staticmethod
    def _sanitize_text(text: str) -> str:
        """Remove ATS-unfriendly content from text"""
        # Remove emojis and non-ASCII characters except basic punctuation
        sanitized = ''.join(char for char in text if ord(char) < 128 or char in ['\n', '\t'])
        
        # Remove multiple line breaks
        while '\n\n\n' in sanitized:
            sanitized = sanitized.replace('\n\n\n', '\n\n')
        
        return sanitized.strip()
    
    @staticmethod
    def generate_mock_cover_letter(user_profile: Dict, job_details: Dict) -> str:
        """
        Generate a mock cover letter without LLM (for testing)
        
        Args:
            user_profile: User profile data
            job_details: Job details
            
        Returns:
            Mock cover letter text
        """
        full_name = f"{user_profile.get('first_name', '')} {user_profile.get('last_name', '')}".strip()
        company_name = job_details.get('company_name', 'Company')
        job_title = job_details.get('job_title', 'Position')
        
        today = datetime.utcnow().strftime('%B %d, %Y')
        
        experience_list = user_profile.get('experience', [])
        experience_text = ""
        if experience_list and isinstance(experience_list, list) and len(experience_list) > 0:
            exp = experience_list[0]
            if isinstance(exp, dict):
                experience_text = f"- {exp.get('title', 'Position')} at {exp.get('company', 'Company')}"
        
        cover_letter = f"""{today}

Dear Hiring Manager,

I am writing to express my strong interest in the {job_title} position at {company_name}. With my background and experience, I am confident in my ability to contribute effectively to your team.

Throughout my career, I have developed expertise in {', '.join(user_profile.get('skills', ['various technologies'])[:3])}. I am particularly drawn to {company_name} because of your commitment to innovation and excellence in the industry.

{experience_text if experience_text else 'My professional experience has equipped me with the skills necessary for this role.'}

I am excited about the opportunity to bring my skills and passion to your team. I would welcome the chance to discuss how my background aligns with your needs.

Thank you for considering my application. I look forward to the possibility of contributing to {company_name}.

Sincerely,
{full_name}
"""
        
        return cover_letter
