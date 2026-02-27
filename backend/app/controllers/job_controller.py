"""
Job Controller
Business logic for job search and matching
"""
import logging
from typing import Dict, Tuple, List, Optional

logger = logging.getLogger(__name__)
from datetime import datetime, timezone
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
            
            # Fetch live jobs from real-time scraper using user's role as query
            target_role = (filters or {}).get('role') or user_data.get('target_role') or ''
            location    = (filters or {}).get('location', '')
            work_type   = (filters or {}).get('work_type', '')

            live_jobs = JobScraper.search_jobs(
                query=target_role,
                location=location if location and location.lower() != 'any' else '',
                work_type=work_type,
                limit=150,
            )
            # Serialise posted_date so NLP layer gets plain dicts
            for j in live_jobs:
                pd = j.get('posted_date')
                if pd and not isinstance(pd, str):
                    j['posted_date'] = pd.isoformat()
            jobs_list = live_jobs
            
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
            logger.exception('ERROR in match_jobs: %s', e)
            return False, f'Error matching jobs: {str(e)}', 500
    
    @staticmethod
    def search_jobs(query: Optional[str] = None,
                   filters: Optional[Dict] = None,
                   limit: int = 50,
                   offset: int = 0) -> Tuple[bool, Dict, int]:
        """
        Search real-time jobs from live APIs via JobScraper.
        Results are cached in-memory for 1 hour to avoid repeated calls.
        """
        try:
            location         = (filters or {}).get('location', '')
            experience_level = (filters or {}).get('experience_level', '')
            work_type        = (filters or {}).get('work_type', '')
            source_filter    = (filters or {}).get('source', '').lower()

            jobs = JobScraper.search_jobs(
                query=query or '',
                location=location if location and location.lower() != 'any' else '',
                experience_level=experience_level,
                work_type=work_type,
                limit=limit + offset,
            )

            # Optional filter by source name (LinkedIn, Indeed, RemoteOK, etc.)
            if source_filter and source_filter != 'all':
                jobs = [j for j in jobs
                        if source_filter in (j.get('source') or '').lower()]

            # Pagination (offset applied in-memory)
            paginated = jobs[offset: offset + limit]

            # Serialise posted_date to ISO string for JSON
            for j in paginated:
                pd = j.get('posted_date')
                if pd and not isinstance(pd, str):
                    j['posted_date'] = pd.isoformat()

            return True, {
                'jobs':   paginated,
                'total':  len(jobs),
                'limit':  limit,
                'offset': offset,
                'source': 'live',
            }, 200

        except Exception as e:
            logger.exception('Error searching jobs: %s', e)
            return False, f'Error searching jobs: {str(e)}', 500

    @staticmethod
    def upsert_and_save_job(user_id: int, job_data: Dict) -> Tuple[bool, Dict, int]:
        """
        Upsert a scraped job into the DB and create/return a saved-application record.
        Called when the user clicks Save on a live-scraped job card.
        """
        try:
            # Try to find an existing record by source_url
            existing_job = Job.query.filter_by(
                source_url=job_data.get('source_url', '')
            ).first()

            if not existing_job:
                from datetime import datetime as _dt
                posted_raw = job_data.get('posted_date')
                posted_dt  = (_dt.fromisoformat(posted_raw)
                              if isinstance(posted_raw, str) else None) or _dt.utcnow()

                existing_job = Job(
                    title            = job_data.get('title', 'Unknown'),
                    company          = job_data.get('company', 'Unknown'),
                    location         = job_data.get('location', ''),
                    work_type        = job_data.get('work_type', ''),
                    job_type         = job_data.get('job_type', 'Full-time'),
                    experience_level = job_data.get('experience_level', 'Mid'),
                    description      = job_data.get('description', ''),
                    skills_required  = job_data.get('skills_required', []),
                    requirements     = job_data.get('requirements', []),
                    responsibilities = job_data.get('responsibilities', []),
                    salary_min       = job_data.get('salary_min'),
                    salary_max       = job_data.get('salary_max'),
                    source           = job_data.get('source', ''),
                    source_url       = job_data.get('source_url', ''),
                    company_logo     = job_data.get('company_logo', ''),
                    posted_date      = posted_dt,
                    is_active        = True,
                )
                db.session.add(existing_job)
                db.session.flush()  # get the auto-assigned int ID

            # Check if already saved by this user
            app = JobApplication.query.filter_by(
                user_id=user_id, job_id=existing_job.id
            ).first()
            if app:
                return True, {'message': 'Job already saved', 'job_id': existing_job.id}, 200

            app = JobApplication(user_id=user_id, job_id=existing_job.id, status='saved')
            db.session.add(app)
            db.session.commit()
            return True, {'message': 'Job saved successfully', 'job_id': existing_job.id}, 201

        except Exception as e:
            db.session.rollback()
            return False, f'Error saving job: {str(e)}', 500
    
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
                existing.applied_date = datetime.now(timezone.utc)
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
                applied_date=datetime.now(timezone.utc),
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
