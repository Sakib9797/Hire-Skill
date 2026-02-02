"""
Keyword Extractor for ATS Optimization
Extracts relevant keywords from job descriptions for ATS matching
"""

import re
from typing import List, Dict, Set
from collections import Counter


class KeywordExtractor:
    """Extract and analyze keywords from job descriptions"""
    
    # Common ATS keywords categories
    TECHNICAL_INDICATORS = ['experience', 'skilled', 'proficient', 'expert', 'knowledge', 
                           'familiar', 'working knowledge', 'strong understanding']
    
    SOFT_SKILL_KEYWORDS = ['leadership', 'communication', 'teamwork', 'problem-solving', 
                          'analytical', 'collaborative', 'detail-oriented', 'organized',
                          'time management', 'adaptable', 'creative', 'innovative']
    
    # Common stop words to filter out
    STOP_WORDS = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
        'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should',
        'could', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those',
        'our', 'your', 'their', 'we', 'you', 'they', 'it', 'he', 'she', 'who', 'what',
        'where', 'when', 'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more',
        'most', 'other', 'some', 'such', 'no', 'not', 'only', 'own', 'same', 'so',
        'than', 'too', 'very', 'just', 'about', 'into', 'through', 'during', 'before',
        'after', 'above', 'below', 'between', 'under', 'again', 'further', 'then', 'once'
    }
    
    @staticmethod
    def extract_keywords(job_description: str, max_keywords: int = 50) -> Dict[str, List[str]]:
        """
        Extract keywords from job description
        
        Args:
            job_description: Job description text
            max_keywords: Maximum number of keywords to return
            
        Returns:
            Dictionary with categorized keywords:
            {
                'required_skills': [...],
                'preferred_skills': [...],
                'technical_terms': [...],
                'soft_skills': [...],
                'all_keywords': [...]
            }
        """
        if not job_description:
            return {
                'required_skills': [],
                'preferred_skills': [],
                'technical_terms': [],
                'soft_skills': [],
                'all_keywords': []
            }
        
        # Clean and normalize text
        text = KeywordExtractor._clean_text(job_description)
        
        # Extract different types of keywords
        required_skills = KeywordExtractor._extract_required_skills(job_description)
        preferred_skills = KeywordExtractor._extract_preferred_skills(job_description)
        technical_terms = KeywordExtractor._extract_technical_terms(text)
        soft_skills = KeywordExtractor._extract_soft_skills(text)
        
        # Extract general keywords
        all_keywords = KeywordExtractor._extract_general_keywords(text, max_keywords)
        
        return {
            'required_skills': list(required_skills),
            'preferred_skills': list(preferred_skills),
            'technical_terms': list(technical_terms)[:20],
            'soft_skills': list(soft_skills),
            'all_keywords': all_keywords[:max_keywords]
        }
    
    @staticmethod
    def _clean_text(text: str) -> str:
        """Clean and normalize text"""
        # Convert to lowercase
        text = text.lower()
        # Remove special characters but keep alphanumeric, spaces, and common punctuation
        text = re.sub(r'[^\w\s\-\+\#\.]', ' ', text)
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text
    
    @staticmethod
    def _extract_required_skills(job_description: str) -> Set[str]:
        """Extract required skills from job description"""
        skills = set()
        text_lower = job_description.lower()
        
        # Look for required/must-have sections
        required_patterns = [
            r'required skills?:?\s*(.+?)(?=preferred|desired|nice|responsibilities|qualifications|$)',
            r'must have:?\s*(.+?)(?=preferred|desired|nice|responsibilities|$)',
            r'requirements?:?\s*(.+?)(?=preferred|desired|nice|responsibilities|$)',
            r'required:?\s*(.+?)(?=preferred|desired|nice|responsibilities|$)'
        ]
        
        for pattern in required_patterns:
            matches = re.finditer(pattern, text_lower, re.DOTALL | re.IGNORECASE)
            for match in matches:
                section_text = match.group(1)
                # Extract bullet points and items
                items = re.findall(r'[•\-\*]\s*(.+?)(?=\n|$)', section_text)
                for item in items:
                    # Clean and extract skill
                    skill = KeywordExtractor._extract_skill_from_text(item)
                    if skill:
                        skills.add(skill)
        
        return skills
    
    @staticmethod
    def _extract_preferred_skills(job_description: str) -> Set[str]:
        """Extract preferred/nice-to-have skills"""
        skills = set()
        text_lower = job_description.lower()
        
        # Look for preferred/nice-to-have sections
        preferred_patterns = [
            r'preferred:?\s*(.+?)(?=responsibilities|qualifications|$)',
            r'nice to have:?\s*(.+?)(?=responsibilities|$)',
            r'desired:?\s*(.+?)(?=responsibilities|$)',
            r'bonus:?\s*(.+?)(?=responsibilities|$)'
        ]
        
        for pattern in preferred_patterns:
            matches = re.finditer(pattern, text_lower, re.DOTALL | re.IGNORECASE)
            for match in matches:
                section_text = match.group(1)
                items = re.findall(r'[•\-\*]\s*(.+?)(?=\n|$)', section_text)
                for item in items:
                    skill = KeywordExtractor._extract_skill_from_text(item)
                    if skill:
                        skills.add(skill)
        
        return skills
    
    @staticmethod
    def _extract_skill_from_text(text: str) -> str:
        """Extract clean skill name from text"""
        # Remove common phrases
        text = re.sub(r'experience (with|in)\s*', '', text, flags=re.IGNORECASE)
        text = re.sub(r'knowledge of\s*', '', text, flags=re.IGNORECASE)
        text = re.sub(r'proficiency in\s*', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\d+\+?\s*years?', '', text, flags=re.IGNORECASE)
        
        # Clean up
        text = text.strip(' .,;:-')
        
        # Take first meaningful part (before 'and', commas, etc.)
        parts = re.split(r'[,;]|\sand\s', text)
        if parts:
            skill = parts[0].strip()
            # Filter out very short or very long skills
            if 2 < len(skill) < 50:
                return skill
        
        return ''
    
    @staticmethod
    def _extract_technical_terms(text: str) -> Set[str]:
        """Extract technical terms (programming languages, frameworks, tools)"""
        technical_terms = set()
        
        # Common technical patterns
        # Programming languages, frameworks, tools
        tech_patterns = [
            r'\b(python|java|javascript|typescript|c\+\+|c#|ruby|go|rust|swift|kotlin|php)\b',
            r'\b(react|angular|vue|django|flask|spring|node\.?js|express|fastapi)\b',
            r'\b(sql|nosql|postgresql|mysql|mongodb|redis|elasticsearch|dynamodb)\b',
            r'\b(aws|azure|gcp|docker|kubernetes|jenkins|gitlab|github)\b',
            r'\b(rest|api|graphql|microservices|agile|scrum|devops|ci/cd)\b',
            r'\b(git|svn|jira|confluence|slack|teams)\b',
            r'\b(html|css|sass|less|webpack|babel|npm|yarn)\b',
            r'\b(tensorflow|pytorch|scikit-learn|pandas|numpy|jupyter)\b',
            r'\b(linux|unix|windows|macos|bash|shell|powershell)\b'
        ]
        
        for pattern in tech_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            technical_terms.update(match.lower() for match in matches)
        
        # Extract version numbers with technologies (e.g., "Python 3.x")
        version_matches = re.findall(r'([a-z]+)\s+\d+[\.\d]*', text, re.IGNORECASE)
        technical_terms.update(match.lower() for match in version_matches)
        
        return technical_terms
    
    @staticmethod
    def _extract_soft_skills(text: str) -> Set[str]:
        """Extract soft skills from text"""
        soft_skills = set()
        
        for skill in KeywordExtractor.SOFT_SKILL_KEYWORDS:
            if skill in text:
                soft_skills.add(skill)
        
        return soft_skills
    
    @staticmethod
    def _extract_general_keywords(text: str, max_keywords: int = 50) -> List[str]:
        """Extract general important keywords using frequency analysis"""
        # Tokenize
        words = text.split()
        
        # Filter stop words and short words
        meaningful_words = [
            word for word in words 
            if word not in KeywordExtractor.STOP_WORDS 
            and len(word) > 2 
            and not word.isdigit()
        ]
        
        # Count frequencies
        word_freq = Counter(meaningful_words)
        
        # Get most common keywords
        common_keywords = [word for word, count in word_freq.most_common(max_keywords)]
        
        return common_keywords
    
    @staticmethod
    def match_keywords_with_profile(keywords: Dict[str, List[str]], user_skills: List[str]) -> Dict[str, any]:
        """
        Match extracted keywords with user skills
        
        Args:
            keywords: Extracted keywords from job description
            user_skills: User's skills list
            
        Returns:
            Match analysis with scores and recommendations
        """
        user_skills_lower = [skill.lower() for skill in user_skills]
        
        # Match required skills
        required = keywords.get('required_skills', [])
        matched_required = [skill for skill in required if any(s in skill.lower() or skill.lower() in s for s in user_skills_lower)]
        
        # Match technical terms
        technical = keywords.get('technical_terms', [])
        matched_technical = [term for term in technical if any(term in s.lower() or s.lower() in term for s in user_skills_lower)]
        
        # Calculate match score
        total_required = len(required) if required else 1
        match_score = (len(matched_required) / total_required) * 100
        
        return {
            'match_score': round(match_score, 2),
            'matched_required_skills': matched_required,
            'matched_technical_terms': matched_technical,
            'missing_required_skills': [s for s in required if s not in matched_required],
            'recommendations': KeywordExtractor._generate_recommendations(keywords, user_skills_lower)
        }
    
    @staticmethod
    def _generate_recommendations(keywords: Dict[str, List[str]], user_skills_lower: List[str]) -> List[str]:
        """Generate recommendations for skill improvement"""
        recommendations = []
        
        required = keywords.get('required_skills', [])
        missing_required = [s for s in required if not any(s in skill or skill in s for skill in user_skills_lower)]
        
        if missing_required:
            recommendations.append(f"Consider highlighting experience with: {', '.join(missing_required[:3])}")
        
        preferred = keywords.get('preferred_skills', [])
        if preferred:
            recommendations.append(f"Adding these preferred skills would strengthen your application: {', '.join(preferred[:3])}")
        
        return recommendations
