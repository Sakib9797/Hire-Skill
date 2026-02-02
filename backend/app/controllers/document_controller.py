"""
Document Controller
Handles business logic for resume and cover letter generation
"""

from app import db
from app.models import User, UserProfile, Resume, CoverLetter
from app.generators import ResumeGenerator, CoverLetterGenerator
from app.generators.ats_generator import ATSResumeGenerator
from app.utils.cv_parser import CVParser
from typing import Tuple, Dict, Optional
from datetime import datetime


class DocumentController:
    """Controller for document generation operations"""
    
    @staticmethod
    def generate_resume(user_id: int, target_role: Optional[str] = None, 
                       job_description: Optional[str] = None,
                       template: str = 'ats_professional') -> Tuple[bool, Dict, int]:
        """
        Generate a new ATS-compliant resume for user
        Args:
            user_id: User ID
            target_role: Target job role for customization
            job_description: Job description for keyword optimization
            template: Resume template (ats_professional by default)
        Returns:
            Tuple of (success, data/error_message, status_code)
        """
        try:
            # Get user and profile
            user = User.query.get(user_id)
            if not user:
                return False, 'User not found', 404
            
            if not user.profile:
                return False, 'User profile not found. Please complete your profile first.', 404
            
            # Prepare user profile data
            profile = user.profile
            user_data = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone': profile.phone or '',
                'location': profile.location or '',
                'linkedin_url': profile.linkedin_url or '',
                'github_url': profile.github_url or '',
                'portfolio_url': profile.portfolio_url or '',
                'bio': profile.bio or '',
                'skills': profile.skills or [],
                'interests': profile.interests or [],
                'experience': profile.experience or [],
                'education': profile.education or [],
                'certifications': [],
                'projects': []
            }
            
            # Generate ATS-compliant resume content using LLM
            success, resume_content, error_msg = ATSResumeGenerator.generate_ats_resume(
                user_profile=user_data,
                job_description=job_description,
                target_role=target_role
            )
            
            if not success:
                # Fallback to mock resume if LLM fails
                print(f"LLM generation failed: {error_msg}. Using mock resume.")
                resume_content = ATSResumeGenerator.generate_mock_resume(user_data, target_role)
            
            # Extract keywords if job description provided
            keywords_matched = None
            if job_description:
                from app.utils.keyword_extractor import KeywordExtractor
                keywords = KeywordExtractor.extract_keywords(job_description)
                match_analysis = KeywordExtractor.match_keywords_with_profile(
                    keywords, user_data.get('skills', [])
                )
                keywords_matched = {
                    'matched_skills': match_analysis.get('matched_required_skills', []),
                    'match_score': match_analysis.get('match_score', 0)
                }
            
            # Create resume title
            if target_role:
                title = f"Resume - {target_role}"
            else:
                title = f"Resume - {datetime.utcnow().strftime('%B %Y')}"
            
            # Mark previous resumes as not current
            Resume.query.filter_by(user_id=user_id, is_current=True).update({'is_current': False})
            
            # Save to database
            resume = Resume(
                user_id=user_id,
                title=title,
                target_role=target_role,
                job_description=job_description,
                content=resume_content,
                template_name=template,
                is_ats_optimized=True,
                keywords_matched=keywords_matched,
                version=1,
                is_current=True
            )
            
            db.session.add(resume)
            db.session.commit()
            
            return True, {
                'resume': resume.to_dict(),
                'message': 'ATS-compliant resume generated successfully'
            }, 201
            
        except Exception as e:
            db.session.rollback()
            import traceback
            print(f"ERROR in generate_resume: {str(e)}")
            print(traceback.format_exc())
            return False, f'Error generating resume: {str(e)}', 500
    
    @staticmethod
    def get_user_resumes(user_id: int, current_only: bool = False) -> Tuple[bool, Dict, int]:
        """
        Get all resumes for a user
        Args:
            user_id: User ID
            current_only: If True, return only current versions
        Returns:
            Tuple of (success, data/error_message, status_code)
        """
        try:
            query = Resume.query.filter_by(user_id=user_id)
            
            if current_only:
                query = query.filter_by(is_current=True)
            
            resumes = query.order_by(Resume.created_at.desc()).all()
            
            return True, {
                'resumes': [resume.to_dict() for resume in resumes],
                'total': len(resumes)
            }, 200
            
        except Exception as e:
            return False, f'Error fetching resumes: {str(e)}', 500
    
    @staticmethod
    def get_resume(resume_id: int, user_id: int) -> Tuple[bool, Dict, int]:
        """
        Get specific resume
        Args:
            resume_id: Resume ID
            user_id: User ID (for authorization)
        Returns:
            Tuple of (success, data/error_message, status_code)
        """
        try:
            resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
            
            if not resume:
                return False, 'Resume not found', 404
            
            return True, {'resume': resume.to_dict()}, 200
            
        except Exception as e:
            return False, f'Error fetching resume: {str(e)}', 500
    
    @staticmethod
    def update_resume(resume_id: int, user_id: int, updates: Dict) -> Tuple[bool, Dict, int]:
        """
        Update existing resume (creates new version)
        Args:
            resume_id: Resume ID
            user_id: User ID
            updates: Updates to apply
        Returns:
            Tuple of (success, data/error_message, status_code)
        """
        try:
            # Get current resume
            current_resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
            
            if not current_resume:
                return False, 'Resume not found', 404
            
            # Create new version
            new_content = ResumeGenerator.create_new_version(
                current_resume=current_resume.content,
                updates=updates
            )
            
            # Mark current as not current
            current_resume.is_current = False
            
            # Create new version
            new_resume = Resume(
                user_id=user_id,
                title=current_resume.title,
                target_role=current_resume.target_role,
                content=new_content,
                template_name=current_resume.template_name,
                version=current_resume.version + 1,
                is_current=True,
                parent_id=resume_id
            )
            
            db.session.add(new_resume)
            db.session.commit()
            
            return True, {
                'resume': new_resume.to_dict(),
                'message': f'Resume updated to version {new_resume.version}'
            }, 200
            
        except Exception as e:
            db.session.rollback()
            return False, f'Error updating resume: {str(e)}', 500
    
    @staticmethod
    def delete_resume(resume_id: int, user_id: int) -> Tuple[bool, Dict, int]:
        """
        Delete resume
        Args:
            resume_id: Resume ID
            user_id: User ID
        Returns:
            Tuple of (success, data/error_message, status_code)
        """
        try:
            resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
            
            if not resume:
                return False, 'Resume not found', 404
            
            db.session.delete(resume)
            db.session.commit()
            
            return True, {'message': 'Resume deleted successfully'}, 200
            
        except Exception as e:
            db.session.rollback()
            return False, f'Error deleting resume: {str(e)}', 500
    
    @staticmethod
    def generate_cover_letter(user_id: int, job_details: Dict, 
                            tone: str = 'professional',
                            resume_id: Optional[int] = None) -> Tuple[bool, Dict, int]:
        """
        Generate a new ATS-friendly cover letter
        Args:
            user_id: User ID
            job_details: Job information (company_name, job_title, job_description)
            tone: Tone of letter (professional, friendly, formal)
            resume_id: Optional resume ID to link
        Returns:
            Tuple of (success, data/error_message, status_code)
        """
        try:
            # Get user and profile
            user = User.query.get(user_id)
            if not user:
                return False, 'User not found', 404
            
            if not user.profile:
                return False, 'User profile not found. Please complete your profile first.', 404
            
            # Prepare user profile data
            profile = user.profile
            user_data = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone': profile.phone or '',
                'location': profile.location or '',
                'skills': profile.skills or [],
                'experience': profile.experience or [],
                'bio': profile.bio or ''
            }
            
            # Validate job details
            if not job_details.get('company_name') or not job_details.get('job_title'):
                return False, 'Company name and job title are required', 400
            
            # Generate ATS-friendly cover letter content using LLM
            success, content, error_msg = CoverLetterGenerator.generate_cover_letter(
                user_profile=user_data,
                job_details=job_details,
                tone=tone
            )
            
            if not success:
                # Fallback to mock cover letter if LLM fails
                print(f"LLM generation failed: {error_msg}. Using mock cover letter.")
                content = CoverLetterGenerator.generate_mock_cover_letter(user_data, job_details)
            
            # Create title
            title = f"Cover Letter - {job_details['job_title']} at {job_details['company_name']}"
            
            # Mark previous cover letters for this job as not current
            CoverLetter.query.filter_by(
                user_id=user_id,
                company_name=job_details['company_name'],
                job_title=job_details['job_title'],
                is_current=True
            ).update({'is_current': False})
            
            # Save to database
            cover_letter = CoverLetter(
                user_id=user_id,
                resume_id=resume_id,
                title=title,
                company_name=job_details['company_name'],
                job_title=job_details['job_title'],
                content=content,
                tone=tone,
                version=1,
                is_current=True
            )
            
            db.session.add(cover_letter)
            db.session.commit()
            
            return True, {
                'cover_letter': cover_letter.to_dict(),
                'message': 'Cover letter generated successfully'
            }, 201
            
        except Exception as e:
            db.session.rollback()
            return False, f'Error generating cover letter: {str(e)}', 500
    
    @staticmethod
    def generate_custom_cover_letter(user_id: int, custom_prompt: str,
                                    job_details: Optional[Dict] = None,
                                    tone: str = 'professional') -> Tuple[bool, Dict, int]:
        """
        Generate cover letter with custom instructions
        Args:
            user_id: User ID
            custom_prompt: Custom generation instructions
            job_details: Optional job details
            tone: Tone of letter
        Returns:
            Tuple of (success, data/error_message, status_code)
        """
        try:
            # Get user and profile
            user = User.query.get(user_id)
            if not user:
                return False, 'User not found', 404
            
            if not user.profile:
                return False, 'User profile not found', 404
            
            # Prepare user profile data
            profile = user.profile
            user_data = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'skills': profile.skills or [],
                'experience': profile.experience or [],
                'bio': profile.bio or ''
            }
            
            # Generate cover letter with custom prompt
            content = CoverLetterGenerator.generate_custom_cover_letter(
                user_profile=user_data,
                custom_prompt=custom_prompt,
                job_details=job_details,
                tone=tone
            )
            
            # Create title
            if job_details and job_details.get('company_name'):
                title = f"Custom Cover Letter - {job_details['company_name']}"
            else:
                title = f"Custom Cover Letter - {datetime.utcnow().strftime('%B %Y')}"
            
            # Save to database
            cover_letter = CoverLetter(
                user_id=user_id,
                title=title,
                company_name=job_details.get('company_name') if job_details else None,
                job_title=job_details.get('job_title') if job_details else None,
                content=content,
                tone=tone,
                version=1,
                is_current=True
            )
            
            db.session.add(cover_letter)
            db.session.commit()
            
            return True, {
                'cover_letter': cover_letter.to_dict(),
                'message': 'Custom cover letter generated successfully'
            }, 201
            
        except Exception as e:
            db.session.rollback()
            return False, f'Error generating custom cover letter: {str(e)}', 500
    
    @staticmethod
    def get_user_cover_letters(user_id: int, current_only: bool = False) -> Tuple[bool, Dict, int]:
        """
        Get all cover letters for a user
        Args:
            user_id: User ID
            current_only: If True, return only current versions
        Returns:
            Tuple of (success, data/error_message, status_code)
        """
        try:
            query = CoverLetter.query.filter_by(user_id=user_id)
            
            if current_only:
                query = query.filter_by(is_current=True)
            
            cover_letters = query.order_by(CoverLetter.created_at.desc()).all()
            
            return True, {
                'cover_letters': [cl.to_dict() for cl in cover_letters],
                'total': len(cover_letters)
            }, 200
            
        except Exception as e:
            return False, f'Error fetching cover letters: {str(e)}', 500
    
    @staticmethod
    def get_cover_letter(cover_letter_id: int, user_id: int) -> Tuple[bool, Dict, int]:
        """
        Get specific cover letter
        Args:
            cover_letter_id: Cover letter ID
            user_id: User ID (for authorization)
        Returns:
            Tuple of (success, data/error_message, status_code)
        """
        try:
            cover_letter = CoverLetter.query.filter_by(id=cover_letter_id, user_id=user_id).first()
            
            if not cover_letter:
                return False, 'Cover letter not found', 404
            
            return True, {'cover_letter': cover_letter.to_dict()}, 200
            
        except Exception as e:
            return False, f'Error fetching cover letter: {str(e)}', 500
    
    @staticmethod
    def delete_cover_letter(cover_letter_id: int, user_id: int) -> Tuple[bool, Dict, int]:
        """
        Delete cover letter
        Args:
            cover_letter_id: Cover letter ID
            user_id: User ID
        Returns:
            Tuple of (success, data/error_message, status_code)
        """
        try:
            cover_letter = CoverLetter.query.filter_by(id=cover_letter_id, user_id=user_id).first()
            
            if not cover_letter:
                return False, 'Cover letter not found', 404
            
            db.session.delete(cover_letter)
            db.session.commit()
            
            return True, {'message': 'Cover letter deleted successfully'}, 200
            
        except Exception as e:
            db.session.rollback()
            return False, f'Error deleting cover letter: {str(e)}', 500
    
    @staticmethod
    def parse_cv_file(pdf_file) -> Tuple[bool, Dict, int]:
        """
        Parse uploaded CV PDF file
        Args:
            pdf_file: PDF file object
        Returns:
            Tuple of (success, parsed_data/error_message, status_code)
        """
        try:
            parsed_data = CVParser.parse_cv(pdf_file)
            return True, {
                'data': parsed_data,
                'message': 'CV parsed successfully'
            }, 200
            
        except Exception as e:
            return False, f'Error parsing CV: {str(e)}', 500
    
    @staticmethod
    def generate_ats_resume(user_id: int, target_role: Optional[str] = None,
                          cv_file=None) -> Tuple[bool, Dict, int]:
        """
        Generate ATS-optimized resume
        Args:
            user_id: User ID
            target_role: Target job role
            cv_file: Optional uploaded CV file
        Returns:
            Tuple of (success, data/error_message, status_code)
        """
        try:
            # Get user and profile
            user = User.query.get(user_id)
            if not user:
                return False, 'User not found', 404
            
            # Parse CV if provided
            cv_data = None
            if cv_file:
                try:
                    cv_data = CVParser.parse_cv(cv_file)
                except Exception as e:
                    return False, f'Error parsing CV file: {str(e)}', 400
            
            # Prepare user profile data
            if user.profile:
                profile = user.profile
                user_data = {
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'phone': profile.phone or '',
                    'location': profile.location or '',
                    'linkedin_url': profile.linkedin_url or '',
                    'github_url': profile.github_url or '',
                    'portfolio_url': profile.portfolio_url or '',
                    'bio': profile.bio or '',
                    'skills': profile.skills or [],
                    'interests': profile.interests or [],
                    'experience': profile.experience or [],
                    'education': profile.education or [],
                }
            else:
                user_data = {
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'phone': '',
                    'location': '',
                    'skills': [],
                    'experience': [],
                    'education': []
                }
            
            # Generate ATS resume
            success, resume_content, error_msg = ATSResumeGenerator.generate_ats_resume(
                user_profile=user_data,
                target_role=target_role,
                job_description=None
            )
            
            if not success:
                print(f"LLM generation failed: {error_msg}. Using mock resume.")
                resume_content = ATSResumeGenerator.generate_mock_resume(user_data, target_role)
            
            # Use default ATS template
            template = 'ats_professional'
            
            # Create resume title
            if target_role:
                title = f"ATS Resume - {target_role}"
            else:
                title = f"ATS Resume - {datetime.utcnow().strftime('%B %Y')}"
            
            # Mark previous resumes with same title as not current
            Resume.query.filter_by(user_id=user_id, is_current=True).update({'is_current': False})
            
            # Save to database
            resume = Resume(
                user_id=user_id,
                title=title,
                target_role=target_role,
                content=resume_content,
                template_name=template,
                version=1,
                is_current=True
            )
            
            db.session.add(resume)
            db.session.commit()
            
            return True, {
                'resume': resume.to_dict(),
                'template': template,
                'message': 'ATS-optimized resume generated successfully'
            }, 201
            
        except Exception as e:
            db.session.rollback()
            import traceback
            print(f"ERROR in generate_ats_resume: {str(e)}")
            print(traceback.format_exc())
            return False, f'Error generating ATS resume: {str(e)}', 500
    
    @staticmethod
    def get_role_recommendations(role: str) -> Tuple[bool, Dict, int]:
        """
        Get template recommendations for a specific role
        Args:
            role: Target job role
        Returns:
            Tuple of (success, recommendations/error_message, status_code)
        """
        try:
            # Default recommendation for all roles
            recommendation = {
                'template': 'ats_professional',
                'description': 'ATS-optimized professional format',
                'best_for': 'All roles - optimized for Applicant Tracking Systems'
            }
            
            # Get all available templates
            templates = ResumeGenerator.TEMPLATES
            
            return True, {
                'role': role,
                'recommended': recommendation,
                'all_templates': {
                    name: {
                        'sections': config['sections'],
                        'style': config['style']
                    }
                    for name, config in templates.items()
                },
                'message': 'Recommendations retrieved successfully'
            }, 200
            
        except Exception as e:
            return False, f'Error getting recommendations: {str(e)}', 500
