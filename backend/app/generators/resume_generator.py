"""
Resume Generator
Generates professional resumes based on user profile and target role
"""

from typing import Dict, List, Optional
from datetime import datetime


class ResumeGenerator:
    """Generate structured resume content"""
    
    # Resume templates
    TEMPLATES = {
        'professional': {
            'sections': ['contact', 'summary', 'experience', 'education', 'skills', 'certifications'],
            'style': 'clean and professional'
        },
        'modern': {
            'sections': ['contact', 'summary', 'skills', 'experience', 'education', 'projects'],
            'style': 'modern with emphasis on skills'
        },
        'creative': {
            'sections': ['contact', 'summary', 'portfolio', 'experience', 'skills', 'education'],
            'style': 'creative and visually appealing'
        },
        'executive': {
            'sections': ['contact', 'executive_summary', 'key_achievements', 'experience', 'education'],
            'style': 'executive level with achievements focus'
        }
    }
    
    @staticmethod
    def generate_resume(user_profile: Dict, target_role: Optional[str] = None, 
                       template: str = 'professional') -> Dict:
        """
        Generate structured resume content
        Args:
            user_profile: User profile data (from UserProfile model)
            target_role: Target job role for customization
            template: Template name (professional, modern, creative, executive)
        Returns:
            Structured resume in JSON format
        """
        template_config = ResumeGenerator.TEMPLATES.get(template, ResumeGenerator.TEMPLATES['professional'])
        
        resume = {
            'metadata': {
                'template': template,
                'generated_at': datetime.utcnow().isoformat(),
                'target_role': target_role,
                'version': 1
            },
            'contact': ResumeGenerator._generate_contact(user_profile),
            'sections': {}
        }
        
        # Generate sections based on template
        for section in template_config['sections']:
            if section == 'contact':
                continue  # Already added
            elif section == 'summary':
                resume['sections']['summary'] = ResumeGenerator._generate_summary(user_profile, target_role)
            elif section == 'executive_summary':
                resume['sections']['executive_summary'] = ResumeGenerator._generate_executive_summary(user_profile, target_role)
            elif section == 'experience':
                resume['sections']['experience'] = ResumeGenerator._format_experience(user_profile.get('experience', []))
            elif section == 'education':
                resume['sections']['education'] = ResumeGenerator._format_education(user_profile.get('education', []))
            elif section == 'skills':
                resume['sections']['skills'] = ResumeGenerator._format_skills(user_profile.get('skills', []), target_role)
            elif section == 'certifications':
                resume['sections']['certifications'] = ResumeGenerator._format_certifications(user_profile.get('certifications', []))
            elif section == 'projects':
                resume['sections']['projects'] = ResumeGenerator._format_projects(user_profile.get('projects', []))
            elif section == 'key_achievements':
                resume['sections']['key_achievements'] = ResumeGenerator._generate_achievements(user_profile)
            elif section == 'portfolio':
                resume['sections']['portfolio'] = ResumeGenerator._format_portfolio(user_profile)
        
        return resume
    
    @staticmethod
    def _generate_contact(user_profile: Dict) -> Dict:
        """Generate contact information section"""
        return {
            'full_name': f"{user_profile.get('first_name', '')} {user_profile.get('last_name', '')}".strip(),
            'email': user_profile.get('email', ''),
            'phone': user_profile.get('phone', ''),
            'location': user_profile.get('location', ''),
            'linkedin': user_profile.get('linkedin_url', ''),
            'github': user_profile.get('github_url', ''),
            'portfolio': user_profile.get('portfolio_url', ''),
            'website': user_profile.get('portfolio_url', '')
        }
    
    @staticmethod
    def _generate_summary(user_profile: Dict, target_role: Optional[str] = None) -> str:
        """Generate professional summary"""
        skills = user_profile.get('skills', [])
        experience = user_profile.get('experience', [])
        bio = user_profile.get('bio', '')
        
        # Calculate years of experience
        years_exp = len(experience) if experience else 0
        
        if target_role:
            summary = f"Results-driven professional with {years_exp}+ years of experience seeking {target_role} position. "
        else:
            summary = f"Accomplished professional with {years_exp}+ years of diverse experience. "
        
        if skills:
            top_skills = ', '.join(skills[:5])
            summary += f"Expertise in {top_skills}. "
        
        if bio:
            summary += bio[:200] + "..." if len(bio) > 200 else bio
        else:
            summary += "Proven track record of delivering high-quality results and driving business success."
        
        return summary
    
    @staticmethod
    def _generate_executive_summary(user_profile: Dict, target_role: Optional[str] = None) -> str:
        """Generate executive-level summary"""
        experience = user_profile.get('experience', [])
        years_exp = len(experience) if experience else 0
        
        summary = f"Senior executive with {years_exp}+ years of strategic leadership experience. "
        summary += "Proven ability to drive organizational growth, build high-performing teams, and deliver transformational results. "
        
        if target_role:
            summary += f"Seeking {target_role} position to leverage extensive expertise in business strategy and operational excellence."
        
        return summary
    
    @staticmethod
    def _format_experience(experience_list: List) -> List[Dict]:
        """Format work experience"""
        if not experience_list:
            return []
        
        formatted = []
        for exp in experience_list:
            if isinstance(exp, str):
                # If experience is just a string, parse it
                formatted.append({
                    'title': 'Position',
                    'company': exp,
                    'duration': 'Duration not specified',
                    'description': [],
                    'achievements': []
                })
            elif isinstance(exp, dict):
                formatted.append({
                    'title': exp.get('title', 'Position'),
                    'company': exp.get('company', 'Company'),
                    'location': exp.get('location', ''),
                    'start_date': exp.get('start_date', ''),
                    'end_date': exp.get('end_date', 'Present'),
                    'duration': exp.get('duration', ''),
                    'description': exp.get('description', []),
                    'achievements': exp.get('achievements', []),
                    'technologies': exp.get('technologies', [])
                })
        
        return formatted
    
    @staticmethod
    def _format_education(education_list: List) -> List[Dict]:
        """Format education"""
        if not education_list:
            return []
        
        formatted = []
        for edu in education_list:
            if isinstance(edu, str):
                formatted.append({
                    'degree': edu,
                    'institution': 'Institution',
                    'year': '',
                    'gpa': '',
                    'honors': []
                })
            elif isinstance(edu, dict):
                formatted.append({
                    'degree': edu.get('degree', 'Degree'),
                    'institution': edu.get('institution', 'Institution'),
                    'location': edu.get('location', ''),
                    'graduation_date': edu.get('graduation_date', ''),
                    'year': edu.get('year', ''),
                    'gpa': edu.get('gpa', ''),
                    'honors': edu.get('honors', []),
                    'relevant_courses': edu.get('relevant_courses', [])
                })
        
        return formatted
    
    @staticmethod
    def _format_skills(skills_list: List, target_role: Optional[str] = None) -> Dict:
        """Format skills by category"""
        if not skills_list:
            return {'technical': [], 'soft': [], 'other': []}
        
        # Categorize skills (basic categorization)
        technical_keywords = ['python', 'java', 'javascript', 'react', 'sql', 'aws', 'docker', 
                            'kubernetes', 'git', 'api', 'database', 'machine learning', 'ai',
                            'data', 'cloud', 'devops', 'testing', 'agile']
        
        soft_keywords = ['leadership', 'communication', 'teamwork', 'problem solving', 
                        'management', 'collaboration', 'analytical', 'creative']
        
        categorized = {
            'technical': [],
            'soft': [],
            'other': []
        }
        
        for skill in skills_list:
            skill_lower = skill.lower()
            if any(keyword in skill_lower for keyword in technical_keywords):
                categorized['technical'].append(skill)
            elif any(keyword in skill_lower for keyword in soft_keywords):
                categorized['soft'].append(skill)
            else:
                categorized['other'].append(skill)
        
        return categorized
    
    @staticmethod
    def _format_certifications(cert_list: List) -> List[Dict]:
        """Format certifications"""
        if not cert_list:
            return []
        
        formatted = []
        for cert in cert_list:
            if isinstance(cert, str):
                formatted.append({
                    'name': cert,
                    'issuer': '',
                    'date': '',
                    'credential_id': ''
                })
            elif isinstance(cert, dict):
                formatted.append(cert)
        
        return formatted
    
    @staticmethod
    def _format_projects(projects_list: List) -> List[Dict]:
        """Format projects"""
        if not projects_list:
            return []
        
        formatted = []
        for proj in projects_list:
            if isinstance(proj, dict):
                formatted.append({
                    'name': proj.get('name', 'Project'),
                    'description': proj.get('description', ''),
                    'technologies': proj.get('technologies', []),
                    'url': proj.get('url', ''),
                    'highlights': proj.get('highlights', [])
                })
        
        return formatted
    
    @staticmethod
    def _generate_achievements(user_profile: Dict) -> List[str]:
        """Generate key achievements"""
        achievements = []
        experience = user_profile.get('experience', [])
        
        # Extract achievements from experience
        for exp in experience:
            if isinstance(exp, dict) and 'achievements' in exp:
                achievements.extend(exp.get('achievements', []))
        
        # If no achievements, generate generic ones based on profile
        if not achievements:
            achievements = [
                "Demonstrated expertise in cross-functional team leadership",
                "Consistently delivered projects on time and within budget",
                "Implemented innovative solutions to complex business challenges"
            ]
        
        return achievements[:5]  # Top 5 achievements
    
    @staticmethod
    def _format_portfolio(user_profile: Dict) -> Dict:
        """Format portfolio section"""
        return {
            'website': user_profile.get('portfolio', ''),
            'github': user_profile.get('github', ''),
            'projects': user_profile.get('projects', [])
        }
    
    @staticmethod
    def create_new_version(current_resume: Dict, updates: Dict) -> Dict:
        """Create a new version of existing resume"""
        import copy
        new_resume = copy.deepcopy(current_resume)
        
        # Update version
        new_resume['metadata']['version'] = current_resume['metadata'].get('version', 1) + 1
        new_resume['metadata']['generated_at'] = datetime.utcnow().isoformat()
        
        # Apply updates
        for key, value in updates.items():
            if key in new_resume:
                new_resume[key] = value
            elif key in new_resume['sections']:
                new_resume['sections'][key] = value
        
        return new_resume
