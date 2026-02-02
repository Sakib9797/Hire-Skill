"""
Job Controller
Business logic for job search and matching
"""
from typing import Dict, Tuple, List, Optional
from datetime import datetime
from app import db
from app.models.job import Job, JobApplication
from app.models.user import User, UserProfile
from app.services.job_scraper import JobScraper
from app.services.job_matcher import JobMatcher

class JobController:
    """Job search and matching controller"""
    
    @staticmethod
    def initialize_jobs():
        """Initialize database with mock jobs if empty"""
        try:
            # Check if jobs already exist
            existing_count = Job.query.count()
            if existing_count > 0:
                return True, f'{existing_count} jobs already exist', 200
            
            # Generate mock jobs
            mock_jobs = JobScraper.generate_mock_jobs(count=100)
            
            # Save to database
            for job_data in mock_jobs:
                job = Job(
                    title=job_data['title'],
                    company=job_data['company'],
                    location=job_data['location'],
                    work_type=job_data['work_type'],
                    job_type=job_data['job_type'],
                    experience_level=job_data['experience_level'],
                    salary_min=job_data['salary_min'],
                    salary_max=job_data['salary_max'],
                    description=job_data['description'],
                    requirements=job_data['requirements'],
                    responsibilities=job_data['responsibilities'],
                    skills_required=job_data['skills_required'],
                    benefits=job_data['benefits'],
                    source=job_data['source'],
                    source_url=job_data['source_url'],
                    company_logo=job_data['company_logo'],
                    posted_date=job_data['posted_date'],
                    application_deadline=job_data['application_deadline'],
                    is_active=job_data['is_active']
                )
                db.session.add(job)
            
            db.session.commit()
            return True, f'{len(mock_jobs)} jobs initialized successfully', 201
            
        except Exception as e:
            db.session.rollback()
            return False, f'Error initializing jobs: {str(e)}', 500
    
    @staticmethod
    def match_jobs(user_id: int, filters: Optional[Dict] = None, limit: int = 20) -> Tuple[bool, Dict, int]:
        """
        Find matching jobs for user using NLP
        Args:
            user_id: User ID
            filters: Optional filters (location, role, experience, work_type)
            limit: Maximum number of results
        Returns:
            Tuple of (success, data/error_message, status_code)
        """
        try:
            # Get user and profile
            user = User.query.get(user_id)
            if not user:
                return False, 'User not found', 404
            
            profile = UserProfile.query.filter_by(user_id=user_id).first()
            
            # Build user profile data
            user_data = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'target_role': filters.get('role') if filters and filters.get('role') else None,
                'skills': profile.skills if profile and profile.skills else [],
                'bio': profile.bio if profile else '',
                'experience': profile.experience if profile and profile.experience else [],
                'education': profile.education if profile and profile.education else []
            }
            
            # Get all active jobs from database
            query = Job.query.filter_by(is_active=True)
            
            # Apply basic database filters for efficiency
            if filters:
                if filters.get('location') and filters['location'].lower() != 'any':
                    query = query.filter(Job.location.ilike(f"%{filters['location']}%"))
                
                if filters.get('experience_level'):
                    query = query.filter_by(experience_level=filters['experience_level'])
                
                if filters.get('work_type'):
                    query = query.filter_by(work_type=filters['work_type'])
                
                if filters.get('job_type'):
                    query = query.filter_by(job_type=filters['job_type'])
            
            jobs_from_db = query.all()
            jobs_list = [job.to_dict() for job in jobs_from_db]
            
            # Use JobMatcher for NLP-based matching
            matcher = JobMatcher()
            matched_jobs = matcher.match_jobs(
                user_profile=user_data,
                jobs=jobs_list,
                filters=filters,
                top_k=limit
            )
            
            return True, {
                'jobs': matched_jobs,
                'total': len(matched_jobs),
                'filters_applied': filters or {}
            }, 200
            
        except Exception as e:
            import traceback
            print(f"ERROR in match_jobs: {str(e)}")
            print(traceback.format_exc())
            return False, f'Error matching jobs: {str(e)}', 500
    
    @staticmethod
    def search_jobs(query: Optional[str] = None, 
                   filters: Optional[Dict] = None,
                   limit: int = 50,
                   offset: int = 0) -> Tuple[bool, Dict, int]:
        """
        Search jobs with filters
        Args:
            query: Search query
            filters: Filter dictionary
            limit: Results limit
            offset: Results offset for pagination
        Returns:
            Tuple of (success, data/error_message, status_code)
        """
        try:
            # Start with base query
            db_query = Job.query.filter_by(is_active=True)
            
            # Apply text search
            if query:
                db_query = db_query.filter(
                    db.or_(
                        Job.title.ilike(f'%{query}%'),
                        Job.description.ilike(f'%{query}%'),
                        Job.company.ilike(f'%{query}%')
                    )
                )
            
            # Apply filters
            if filters:
                if filters.get('location') and filters['location'].lower() != 'any':
                    db_query = db_query.filter(Job.location.ilike(f"%{filters['location']}%"))
                
                if filters.get('experience_level'):
                    db_query = db_query.filter_by(experience_level=filters['experience_level'])
                
                if filters.get('work_type'):
                    db_query = db_query.filter_by(work_type=filters['work_type'])
                
                if filters.get('job_type'):
                    db_query = db_query.filter_by(job_type=filters['job_type'])
                
                if filters.get('min_salary'):
                    db_query = db_query.filter(Job.salary_min >= filters['min_salary'])
            
            # Get total count
            total = db_query.count()
            
            # Apply pagination and get results
            jobs = db_query.order_by(Job.posted_date.desc()).limit(limit).offset(offset).all()
            
            return True, {
                'jobs': [job.to_dict() for job in jobs],
                'total': total,
                'limit': limit,
                'offset': offset
            }, 200
            
        except Exception as e:
            return False, f'Error searching jobs: {str(e)}', 500
    
    @staticmethod
    def get_job(job_id: int, user_id: Optional[int] = None) -> Tuple[bool, Dict, int]:
        """
        Get specific job details
        Args:
            job_id: Job ID
            user_id: Optional user ID to check application status
        Returns:
            Tuple of (success, data/error_message, status_code)
        """
        try:
            job = Job.query.get(job_id)
            if not job:
                return False, 'Job not found', 404
            
            job_data = job.to_dict()
            
            # Check if user has applied
            if user_id:
                application = JobApplication.query.filter_by(
                    user_id=user_id,
                    job_id=job_id
                ).first()
                
                if application:
                    job_data['application_status'] = application.status
                    job_data['applied_date'] = application.applied_date.isoformat() if application.applied_date else None
            
            return True, {'job': job_data}, 200
            
        except Exception as e:
            return False, f'Error fetching job: {str(e)}', 500
    
    @staticmethod
    def save_job(user_id: int, job_id: int) -> Tuple[bool, Dict, int]:
        """
        Save job for later
        Args:
            user_id: User ID
            job_id: Job ID
        Returns:
            Tuple of (success, data/error_message, status_code)
        """
        try:
            # Check if already saved
            existing = JobApplication.query.filter_by(
                user_id=user_id,
                job_id=job_id
            ).first()
            
            if existing:
                return True, {'message': 'Job already saved', 'application': existing.to_dict()}, 200
            
            # Create new application
            application = JobApplication(
                user_id=user_id,
                job_id=job_id,
                status='saved'
            )
            
            db.session.add(application)
            db.session.commit()
            
            return True, {'message': 'Job saved successfully', 'application': application.to_dict()}, 201
            
        except Exception as e:
            db.session.rollback()
            return False, f'Error saving job: {str(e)}', 500
    
    @staticmethod
    def apply_to_job(user_id: int, job_id: int, resume_id: Optional[int] = None,
                    cover_letter_id: Optional[int] = None, match_score: Optional[float] = None) -> Tuple[bool, Dict, int]:
        """
        Apply to job
        Args:
            user_id: User ID
            job_id: Job ID
            resume_id: Optional resume ID
            cover_letter_id: Optional cover letter ID
            match_score: Optional match score
        Returns:
            Tuple of (success, data/error_message, status_code)
        """
        try:
            # Check if already applied
            existing = JobApplication.query.filter_by(
                user_id=user_id,
                job_id=job_id
            ).first()
            
            if existing:
                if existing.status == 'applied':
                    return False, 'Already applied to this job', 400
                
                # Update existing saved application
                existing.status = 'applied'
                existing.applied_date = datetime.utcnow()
                existing.resume_id = resume_id
                existing.cover_letter_id = cover_letter_id
                existing.match_score = match_score
                
                db.session.commit()
                return True, {'message': 'Application submitted successfully', 'application': existing.to_dict()}, 200
            
            # Create new application
            application = JobApplication(
                user_id=user_id,
                job_id=job_id,
                status='applied',
                applied_date=datetime.utcnow(),
                resume_id=resume_id,
                cover_letter_id=cover_letter_id,
                match_score=match_score
            )
            
            db.session.add(application)
            db.session.commit()
            
            return True, {'message': 'Application submitted successfully', 'application': application.to_dict()}, 201
            
        except Exception as e:
            db.session.rollback()
            return False, f'Error applying to job: {str(e)}', 500
    
    @staticmethod
    def get_user_applications(user_id: int, status: Optional[str] = None) -> Tuple[bool, Dict, int]:
        """
        Get user's job applications
        Args:
            user_id: User ID
            status: Optional status filter
        Returns:
            Tuple of (success, data/error_message, status_code)
        """
        try:
            query = JobApplication.query.filter_by(user_id=user_id)
            
            if status:
                query = query.filter_by(status=status)
            
            applications = query.order_by(JobApplication.created_at.desc()).all()
            
            return True, {
                'applications': [app.to_dict() for app in applications],
                'total': len(applications)
            }, 200
            
        except Exception as e:
            return False, f'Error fetching applications: {str(e)}', 500
    
    @staticmethod
    def get_match_explanation(user_id: int, job_id: int) -> Tuple[bool, Dict, int]:
        """
        Get explanation for job match
        Args:
            user_id: User ID
            job_id: Job ID
        Returns:
            Tuple of (success, data/error_message, status_code)
        """
        try:
            # Get user profile
            user = User.query.get(user_id)
            profile = UserProfile.query.filter_by(user_id=user_id).first()
            
            user_data = {
                'target_role': profile.target_role if profile else None,
                'skills': profile.skills if profile and profile.skills else [],
                'bio': profile.bio if profile else '',
                'experience': profile.experience if profile and profile.experience else [],
                'education': profile.education if profile and profile.education else []
            }
            
            # Get job
            job = Job.query.get(job_id)
            if not job:
                return False, 'Job not found', 404
            
            # Generate explanation
            matcher = JobMatcher()
            explanation = matcher.get_match_explanation(user_data, job.to_dict())
            
            return True, {'explanation': explanation}, 200
            
        except Exception as e:
            return False, f'Error generating explanation: {str(e)}', 500
