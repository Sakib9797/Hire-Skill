"""
ATS Prompt Builder
Builds optimized prompts for LLM to generate ATS-compliant resumes
"""

from typing import Dict, List, Optional


class ATSPromptBuilder:
    """Build ATS-optimized prompts for resume generation"""
    
    # Standard ATS section headings
    ATS_SECTION_HEADINGS = {
        'summary': 'SUMMARY',
        'skills': 'SKILLS',
        'work_experience': 'WORK EXPERIENCE',
        'projects': 'PROJECTS',
        'education': 'EDUCATION',
        'certifications': 'CERTIFICATIONS'
    }
    
    @staticmethod
    def build_resume_prompt(user_profile: Dict, job_description: Optional[str] = None, 
                           target_role: Optional[str] = None, keywords: Optional[Dict] = None) -> str:
        """
        Build optimized prompt for ATS-compliant resume generation
        
        Args:
            user_profile: User profile data
            job_description: Job description text (optional)
            target_role: Target job role (optional)
            keywords: Extracted keywords from job description (optional)
            
        Returns:
            Formatted prompt for LLM
        """
        prompt_parts = []
        
        # System instruction
        prompt_parts.append(ATSPromptBuilder._get_system_instruction())
        
        # User profile section
        prompt_parts.append(ATSPromptBuilder._format_user_profile(user_profile))
        
        # Target role and job description
        if target_role:
            prompt_parts.append(f"\n**TARGET ROLE**: {target_role}")
        
        if job_description:
            prompt_parts.append(f"\n**JOB DESCRIPTION**:\n{job_description[:1000]}")  # Limit length
        
        # Keywords to emphasize
        if keywords:
            prompt_parts.append(ATSPromptBuilder._format_keywords(keywords))
        
        # JSON schema requirement
        prompt_parts.append(ATSPromptBuilder._get_json_schema_instruction())
        
        # Final instructions
        prompt_parts.append(ATSPromptBuilder._get_generation_instructions())
        
        return '\n\n'.join(prompt_parts)
    
    @staticmethod
    def _get_system_instruction() -> str:
        """Get system instruction for ATS compliance"""
        return """You are an expert ATS (Applicant Tracking System) resume writer. Your task is to create a strictly ATS-compliant resume that will pass automated screening systems.

**CRITICAL ATS RULES - MUST FOLLOW**:
1. Single-column layout (no tables, columns, or complex formatting)
2. Standard section headings ONLY: SUMMARY, SKILLS, WORK EXPERIENCE, PROJECTS, EDUCATION, CERTIFICATIONS
3. Use bullet points (•) for lists, never tables or graphics
4. No special characters, emojis, or icons
5. Include relevant keywords naturally (no keyword stuffing)
6. Use action verbs and quantified achievements
7. Keep formatting simple and clean
8. Output as structured JSON only

**ATS BEST PRACTICES**:
- Use standard job titles and skill names
- Include industry-standard terminology
- Quantify achievements with numbers, percentages, or metrics
- Use present tense for current roles, past tense for previous roles
- Be specific and concise
- Match keywords from job description when applicable"""
    
    @staticmethod
    def _format_user_profile(user_profile: Dict) -> str:
        """Format user profile data for prompt"""
        sections = ["**USER PROFILE DATA**:"]
        
        # Personal info
        sections.append(f"Name: {user_profile.get('first_name', '')} {user_profile.get('last_name', '')}")
        sections.append(f"Email: {user_profile.get('email', '')}")
        if user_profile.get('phone'):
            sections.append(f"Phone: {user_profile['phone']}")
        if user_profile.get('location'):
            sections.append(f"Location: {user_profile['location']}")
        if user_profile.get('linkedin_url'):
            sections.append(f"LinkedIn: {user_profile['linkedin_url']}")
        if user_profile.get('github_url'):
            sections.append(f"GitHub: {user_profile['github_url']}")
        if user_profile.get('portfolio_url'):
            sections.append(f"Portfolio: {user_profile['portfolio_url']}")
        
        # Bio/summary
        if user_profile.get('bio'):
            sections.append(f"\nBio: {user_profile['bio']}")
        
        # Skills
        if user_profile.get('skills'):
            skills_str = ', '.join(user_profile['skills'])
            sections.append(f"\nSkills: {skills_str}")
        
        # Experience
        if user_profile.get('experience'):
            sections.append("\nWork Experience:")
            for exp in user_profile['experience']:
                sections.append(f"- {exp.get('title', 'N/A')} at {exp.get('company', 'N/A')}")
                sections.append(f"  Duration: {exp.get('duration', 'N/A')}")
                if exp.get('description'):
                    sections.append(f"  Description: {exp['description']}")
        
        # Education
        if user_profile.get('education'):
            sections.append("\nEducation:")
            for edu in user_profile['education']:
                sections.append(f"- {edu.get('degree', 'N/A')} from {edu.get('institution', 'N/A')}")
                sections.append(f"  Year: {edu.get('year', 'N/A')}")
        
        # Projects
        if user_profile.get('projects'):
            sections.append("\nProjects:")
            for proj in user_profile['projects']:
                sections.append(f"- {proj.get('name', 'N/A')}: {proj.get('description', 'N/A')}")
        
        # Certifications
        if user_profile.get('certifications'):
            sections.append("\nCertifications:")
            for cert in user_profile['certifications']:
                sections.append(f"- {cert.get('name', 'N/A')} from {cert.get('issuer', 'N/A')}")
        
        return '\n'.join(sections)
    
    @staticmethod
    def _format_keywords(keywords: Dict) -> str:
        """Format keywords for emphasis"""
        sections = ["**KEYWORDS TO EMPHASIZE**:"]
        
        if keywords.get('required_skills'):
            sections.append(f"Required Skills: {', '.join(keywords['required_skills'][:10])}")
        
        if keywords.get('technical_terms'):
            sections.append(f"Technical Terms: {', '.join(keywords['technical_terms'][:10])}")
        
        if keywords.get('soft_skills'):
            sections.append(f"Soft Skills: {', '.join(keywords['soft_skills'][:5])}")
        
        sections.append("\nNaturally incorporate these keywords where they match the user's experience.")
        
        return '\n'.join(sections)
    
    @staticmethod
    def _get_json_schema_instruction() -> str:
        """Get JSON schema instruction"""
        return """**REQUIRED JSON OUTPUT SCHEMA**:

```json
{
  "personal_info": {
    "full_name": "string (required)",
    "email": "string (required)",
    "phone": "string (optional)",
    "location": "string (optional)",
    "linkedin": "string (optional)",
    "github": "string (optional)",
    "portfolio": "string (optional)"
  },
  "summary": "string (50-500 chars, professional summary tailored to role)",
  "skills": {
    "technical": ["array of technical skills"],
    "soft": ["array of soft skills"],
    "tools": ["array of tools/technologies"]
  },
  "work_experience": [
    {
      "title": "string (job title)",
      "company": "string (company name)",
      "location": "string (optional)",
      "duration": "string (e.g., 'Jan 2020 - Present')",
      "responsibilities": [
        "Bullet point 1 with quantified achievement",
        "Bullet point 2 with action verb and impact",
        "At least 2-5 responsibilities per role"
      ]
    }
  ],
  "projects": [
    {
      "name": "string (project name)",
      "description": "string (concise description with impact)",
      "technologies": ["array of technologies used"],
      "link": "string (optional)"
    }
  ],
  "education": [
    {
      "degree": "string (degree name)",
      "institution": "string (school/university)",
      "location": "string (optional)",
      "year": "string (graduation year or expected)",
      "gpa": "string (optional, only if > 3.5)"
    }
  ],
  "certifications": [
    {
      "name": "string (certification name)",
      "issuer": "string (issuing organization)",
      "year": "string (year obtained)",
      "credential_id": "string (optional)"
    }
  ]
}
```"""
    
    @staticmethod
    def _get_generation_instructions() -> str:
        """Get final generation instructions"""
        return """**GENERATION INSTRUCTIONS**:

1. **Summary**: Write a compelling 50-100 word professional summary that:
   - Highlights key qualifications for the target role
   - Incorporates relevant keywords naturally
   - Quantifies years of experience and key achievements
   - Uses action-oriented language

2. **Skills**: Organize skills into categories:
   - Technical: programming languages, frameworks, databases
   - Soft: communication, leadership, problem-solving
   - Tools: software, platforms, methodologies
   - Prioritize skills matching the job description

3. **Work Experience**: For each role:
   - Use strong action verbs (Led, Developed, Implemented, Achieved)
   - Quantify achievements with metrics (%, $, numbers)
   - Focus on impact and results, not just duties
   - Tailor to highlight relevant experience
   - Use 3-5 bullet points per role

4. **Projects**: Highlight relevant projects that:
   - Demonstrate applicable skills
   - Show initiative and problem-solving
   - Include specific technologies and outcomes

5. **Education**: List degrees with:
   - Degree name and major
   - Institution name
   - Graduation year
   - GPA only if 3.5 or higher

6. **Certifications**: Include relevant certifications that:
   - Are industry-recognized
   - Match job requirements
   - Are current/not expired

**CRITICAL**: 
- Output ONLY the JSON object, no additional text
- No markdown formatting, no code blocks
- Ensure all required fields are present
- Keep content ATS-friendly (no special characters, emojis)
- Be honest - only use information from the user profile
- If information is missing, use empty strings or empty arrays"""
    
    @staticmethod
    def build_cover_letter_prompt(user_profile: Dict, job_description: str, 
                                  company_name: str, job_title: str) -> str:
        """
        Build prompt for ATS-compliant cover letter generation
        
        Args:
            user_profile: User profile data
            job_description: Job description text
            company_name: Company name
            job_title: Job title
            
        Returns:
            Formatted prompt for LLM
        """
        prompt = f"""You are a professional cover letter writer. Create an ATS-friendly cover letter that is:
- Professional and neutral in tone
- Tailored to the specific job and company
- Concise (250-400 words)
- Free of emojis, special characters, and excessive formatting
- Focused on value proposition and relevant experience

**USER PROFILE**:
Name: {user_profile.get('first_name', '')} {user_profile.get('last_name', '')}
Email: {user_profile.get('email', '')}
Phone: {user_profile.get('phone', '')}
Location: {user_profile.get('location', '')}

Bio: {user_profile.get('bio', '')}

Skills: {', '.join(user_profile.get('skills', []))}

Recent Experience:
{ATSPromptBuilder._format_recent_experience(user_profile.get('experience', []))}

**TARGET POSITION**:
Company: {company_name}
Job Title: {job_title}
Job Description: {job_description[:800]}

**COVER LETTER STRUCTURE**:
1. Opening: Express interest in the specific role and company
2. Body (2-3 paragraphs):
   - Highlight relevant experience and achievements
   - Connect skills to job requirements
   - Show knowledge of the company
3. Closing: Express enthusiasm and call to action

**OUTPUT FORMAT**:
Return ONLY plain text, no special formatting.
Use standard business letter format with:
- Date
- Hiring Manager / Recruiting Team
- Company Name
- Body paragraphs
- Professional closing

No emojis, no special characters, no excessive formatting.
Be professional, concise, and genuine."""
        
        return prompt
    
    @staticmethod
    def _format_recent_experience(experience: List[Dict]) -> str:
        """Format recent experience for cover letter"""
        if not experience:
            return "No experience listed"
        
        formatted = []
        for exp in experience[:3]:  # Only recent 3
            formatted.append(f"- {exp.get('title', 'N/A')} at {exp.get('company', 'N/A')} ({exp.get('duration', 'N/A')})")
            if exp.get('description'):
                formatted.append(f"  {exp['description'][:150]}")
        
        return '\n'.join(formatted)
