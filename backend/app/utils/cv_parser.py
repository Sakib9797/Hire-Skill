"""
CV Parser
Extract information from PDF resumes using PyPDF2 and regular expressions
"""

import re
from typing import Dict, List, Optional
import PyPDF2
from io import BytesIO


class CVParser:
    """Parse PDF CVs and extract structured information"""
    
    # Common section headers
    SECTION_PATTERNS = {
        'contact': r'(email|phone|mobile|address|linkedin|github)',
        'summary': r'(summary|profile|objective|about)',
        'experience': r'(experience|employment|work history|professional experience)',
        'education': r'(education|academic|qualification)',
        'skills': r'(skills|technical skills|competencies|expertise)',
        'certifications': r'(certifications?|certificates?|licenses?)',
        'projects': r'(projects?|portfolio)',
        'achievements': r'(achievements?|accomplishments?|awards?)'
    }
    
    @staticmethod
    def extract_text_from_pdf(pdf_file) -> str:
        """
        Extract text from PDF file
        Args:
            pdf_file: File object or bytes
        Returns:
            Extracted text as string
        """
        try:
            if isinstance(pdf_file, bytes):
                pdf_file = BytesIO(pdf_file)
            
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text
        except Exception as e:
            raise Exception(f"Error extracting PDF text: {str(e)}")
    
    @staticmethod
    def extract_email(text: str) -> Optional[str]:
        """Extract email address"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return emails[0] if emails else None
    
    @staticmethod
    def extract_phone(text: str) -> Optional[str]:
        """Extract phone number"""
        # Match various phone formats
        phone_patterns = [
            r'\+?[\d\s\-\(\)]{10,}',  # International format
            r'\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{4}',  # US format
            r'\d{3}[\s\-]\d{3}[\s\-]\d{4}'  # Simple format
        ]
        
        for pattern in phone_patterns:
            phones = re.findall(pattern, text)
            if phones:
                # Clean up the phone number
                phone = re.sub(r'[^\d+]', '', phones[0])
                if len(phone) >= 10:
                    return phones[0].strip()
        return None
    
    @staticmethod
    def extract_name(text: str) -> str:
        """
        Extract name (usually first few lines)
        """
        lines = text.strip().split('\n')
        # Name is typically in the first 3 lines
        for line in lines[:3]:
            line = line.strip()
            # Filter out email, phone, location patterns
            if line and len(line) < 50 and not re.search(r'@|http|www|\d{3}[\-\s]\d{3}', line):
                # Check if it looks like a name (2-4 words, titlecase)
                words = line.split()
                if 1 <= len(words) <= 4 and all(w[0].isupper() for w in words if w):
                    return line
        return ""
    
    @staticmethod
    def extract_linkedin(text: str) -> Optional[str]:
        """Extract LinkedIn URL"""
        linkedin_pattern = r'linkedin\.com/in/[\w\-]+'
        matches = re.findall(linkedin_pattern, text, re.IGNORECASE)
        return f"https://{matches[0]}" if matches else None
    
    @staticmethod
    def extract_github(text: str) -> Optional[str]:
        """Extract GitHub URL"""
        github_pattern = r'github\.com/[\w\-]+'
        matches = re.findall(github_pattern, text, re.IGNORECASE)
        return f"https://{matches[0]}" if matches else None
    
    @staticmethod
    def extract_skills(text: str) -> List[str]:
        """
        Extract skills from CV
        Look for skills section and extract keywords
        """
        skills = []
        
        # Common technical skills keywords
        skill_keywords = [
            'python', 'java', 'javascript', 'typescript', 'c\\+\\+', 'c#', 'ruby', 'php', 'swift', 'kotlin',
            'react', 'angular', 'vue', 'node', 'django', 'flask', 'spring', 'express',
            'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git',
            'machine learning', 'deep learning', 'ai', 'data science', 'nlp',
            'agile', 'scrum', 'devops', 'ci/cd', 'tdd', 'rest', 'graphql', 'api'
        ]
        
        text_lower = text.lower()
        
        for skill in skill_keywords:
            if re.search(r'\b' + skill + r'\b', text_lower):
                # Capitalize properly
                skills.append(skill.upper() if skill in ['sql', 'api', 'ai', 'nlp', 'aws', 'gcp', 'php', 'tdd'] else skill.title())
        
        return list(set(skills))  # Remove duplicates
    
    @staticmethod
    def extract_section(text: str, section_name: str) -> str:
        """
        Extract a specific section from the CV
        Args:
            text: Full CV text
            section_name: Section to extract (experience, education, etc.)
        Returns:
            Section content as string
        """
        pattern = CVParser.SECTION_PATTERNS.get(section_name)
        if not pattern:
            return ""
        
        # Find section start
        section_regex = rf'(?i)\b{pattern}\b'
        matches = list(re.finditer(section_regex, text))
        
        if not matches:
            return ""
        
        start_pos = matches[0].end()
        
        # Find next section (or end of text)
        remaining_text = text[start_pos:]
        
        # Look for next major section header
        next_section_patterns = '|'.join([f"({p})" for p in CVParser.SECTION_PATTERNS.values()])
        next_section = re.search(rf'(?i)\b({next_section_patterns})\b', remaining_text)
        
        if next_section:
            section_content = remaining_text[:next_section.start()]
        else:
            section_content = remaining_text
        
        return section_content.strip()
    
    @staticmethod
    def parse_cv(pdf_file) -> Dict:
        """
        Parse CV and extract all information
        Args:
            pdf_file: PDF file object or bytes
        Returns:
            Dictionary with extracted information
        """
        try:
            # Extract text from PDF
            text = CVParser.extract_text_from_pdf(pdf_file)
            
            # Extract basic info
            name = CVParser.extract_name(text)
            names = name.split() if name else []
            
            result = {
                'first_name': names[0] if len(names) > 0 else '',
                'last_name': ' '.join(names[1:]) if len(names) > 1 else '',
                'email': CVParser.extract_email(text) or '',
                'phone': CVParser.extract_phone(text) or '',
                'linkedin_url': CVParser.extract_linkedin(text) or '',
                'github_url': CVParser.extract_github(text) or '',
                'skills': CVParser.extract_skills(text),
                'bio': CVParser.extract_section(text, 'summary')[:500],  # Limit to 500 chars
                'raw_text': text,
                'sections': {
                    'experience': CVParser.extract_section(text, 'experience'),
                    'education': CVParser.extract_section(text, 'education'),
                    'certifications': CVParser.extract_section(text, 'certifications'),
                    'projects': CVParser.extract_section(text, 'projects')
                }
            }
            
            return result
            
        except Exception as e:
            raise Exception(f"Error parsing CV: {str(e)}")
    
    @staticmethod
    def parse_experience(experience_text: str) -> List[Dict]:
        """Parse experience section into structured format"""
        experiences = []
        
        # Split by common patterns (dates, job titles)
        # This is a simplified parser - can be enhanced
        lines = experience_text.split('\n')
        current_exp = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                if current_exp:
                    experiences.append(current_exp)
                    current_exp = {}
                continue
            
            # Try to identify job title, company, dates
            # Date pattern: 2020-2023, Jan 2020 - Dec 2023, etc.
            date_pattern = r'(\d{4}|\w+\s\d{4})\s*[-–]\s*(\d{4}|\w+\s\d{4}|present|current)'
            if re.search(date_pattern, line, re.IGNORECASE):
                current_exp['period'] = line
            elif not current_exp.get('title'):
                current_exp['title'] = line
            elif not current_exp.get('company'):
                current_exp['company'] = line
            else:
                current_exp['description'] = current_exp.get('description', '') + ' ' + line
        
        if current_exp:
            experiences.append(current_exp)
        
        return experiences
    
    @staticmethod
    def parse_education(education_text: str) -> List[Dict]:
        """Parse education section into structured format"""
        education = []
        
        lines = education_text.split('\n')
        current_edu = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                if current_edu:
                    education.append(current_edu)
                    current_edu = {}
                continue
            
            # Try to identify degree, institution, dates
            if not current_edu.get('degree'):
                current_edu['degree'] = line
            elif not current_edu.get('institution'):
                current_edu['institution'] = line
            else:
                current_edu['details'] = current_edu.get('details', '') + ' ' + line
        
        if current_edu:
            education.append(current_edu)
        
        return education
