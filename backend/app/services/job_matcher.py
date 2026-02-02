"""
Job Matching Service using NLP and Embeddings
Matches user profiles with job postings using semantic similarity
"""
import numpy as np
from typing import List, Dict, Optional, Tuple
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

class JobMatcher:
    """NLP-based job matching with semantic similarity"""
    
    def __init__(self):
        """Initialize the job matcher"""
        self.vectorizer = TfidfVectorizer(
            max_features=500,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=1
        )
        self.job_vectors = None
        self.jobs_data = None
    
    def create_user_profile_text(self, user_data: Dict) -> str:
        """
        Create searchable text from user profile
        Args:
            user_data: User profile dictionary
        Returns:
            Combined text representation
        """
        text_parts = []
        
        # Add target role
        if user_data.get('target_role'):
            text_parts.append(user_data['target_role'])
        
        # Add skills (most important)
        skills = user_data.get('skills', [])
        if skills:
            text_parts.append(' '.join(str(s) for s in skills))
            # Repeat skills for higher weight
            text_parts.append(' '.join(str(s) for s in skills))
        
        # Add bio/summary
        if user_data.get('bio'):
            text_parts.append(str(user_data['bio']))
        
        # Add experience
        experience = user_data.get('experience', [])
        for exp in experience:
            if isinstance(exp, dict):
                if exp.get('title'):
                    text_parts.append(exp['title'])
                if exp.get('description'):
                    text_parts.append(exp['description'])
        
        # Add education
        education = user_data.get('education', [])
        for edu in education:
            if isinstance(edu, dict):
                if edu.get('degree'):
                    text_parts.append(edu['degree'])
                if edu.get('field'):
                    text_parts.append(edu['field'])
        
        return ' '.join(text_parts)
    
    def create_job_text(self, job: Dict) -> str:
        """
        Create searchable text from job posting
        Args:
            job: Job dictionary
        Returns:
            Combined text representation
        """
        text_parts = []
        
        # Add title (most important)
        if job.get('title'):
            text_parts.append(job['title'])
            # Repeat for higher weight
            text_parts.append(job['title'])
        
        # Add skills required
        skills = job.get('skills_required', [])
        if skills:
            text_parts.append(' '.join(str(s) for s in skills))
            # Repeat skills for higher weight
            text_parts.append(' '.join(str(s) for s in skills))
        
        # Add description
        if job.get('description'):
            text_parts.append(str(job['description']))
        
        # Add requirements
        requirements = job.get('requirements', [])
        if requirements:
            text_parts.append(' '.join(str(r) for r in requirements))
        
        # Add responsibilities
        responsibilities = job.get('responsibilities', [])
        if responsibilities:
            text_parts.append(' '.join(str(r) for r in responsibilities))
        
        return ' '.join(text_parts)
    
    def compute_embeddings(self, jobs: List[Dict]) -> np.ndarray:
        """
        Compute TF-IDF embeddings for job postings
        Args:
            jobs: List of job dictionaries
        Returns:
            Job embedding matrix
        """
        # Create text representations
        job_texts = [self.create_job_text(job) for job in jobs]
        
        # Fit and transform
        self.job_vectors = self.vectorizer.fit_transform(job_texts)
        self.jobs_data = jobs
        
        return self.job_vectors.toarray()
    
    def calculate_similarity(self, user_profile: Dict, jobs: List[Dict]) -> List[Tuple[Dict, float]]:
        """
        Calculate similarity scores between user profile and jobs
        Args:
            user_profile: User profile dictionary
            jobs: List of job dictionaries
        Returns:
            List of (job, similarity_score) tuples sorted by score
        """
        # Create embeddings if not already done
        if self.job_vectors is None or self.jobs_data != jobs:
            self.compute_embeddings(jobs)
        
        # Create user profile embedding
        user_text = self.create_user_profile_text(user_profile)
        user_vector = self.vectorizer.transform([user_text])
        
        # Calculate cosine similarity
        similarities = cosine_similarity(user_vector, self.job_vectors)[0]
        
        # Combine jobs with scores
        job_scores = list(zip(jobs, similarities))
        
        # Apply additional scoring factors
        enhanced_scores = []
        for job, base_score in job_scores:
            enhanced_score = self._enhance_score(user_profile, job, base_score)
            enhanced_scores.append((job, enhanced_score))
        
        # Sort by score descending
        enhanced_scores.sort(key=lambda x: x[1], reverse=True)
        
        return enhanced_scores
    
    def _enhance_score(self, user_profile: Dict, job: Dict, base_score: float) -> float:
        """
        Enhance base similarity score with additional factors
        Args:
            user_profile: User profile
            job: Job posting
            base_score: Base cosine similarity score
        Returns:
            Enhanced score
        """
        score = base_score
        
        # Skill matching bonus
        user_skills = set(str(s).lower() for s in user_profile.get('skills', []))
        job_skills = set(str(s).lower() for s in job.get('skills_required', []))
        
        if user_skills and job_skills:
            skill_overlap = len(user_skills.intersection(job_skills))
            skill_bonus = (skill_overlap / len(job_skills)) * 0.3
            score += skill_bonus
        
        # Experience level matching
        user_exp_years = len(user_profile.get('experience', []))
        job_exp_level = job.get('experience_level', '').lower()
        
        if job_exp_level == 'entry' and user_exp_years <= 2:
            score += 0.1
        elif job_exp_level == 'mid' and 2 <= user_exp_years <= 5:
            score += 0.1
        elif job_exp_level == 'senior' and user_exp_years >= 5:
            score += 0.1
        
        # Location preference (if remote/hybrid preferred)
        job_work_type = job.get('work_type', '').lower()
        if 'remote' in job_work_type or 'hybrid' in job_work_type:
            score += 0.05
        
        # Title matching bonus
        target_role = user_profile.get('target_role', '').lower()
        job_title = job.get('title', '').lower()
        if target_role and target_role in job_title:
            score += 0.15
        
        # Cap score at 1.0
        return min(score, 1.0)
    
    def match_jobs(self, 
                   user_profile: Dict, 
                   jobs: List[Dict],
                   filters: Optional[Dict] = None,
                   top_k: int = 20) -> List[Dict]:
        """
        Find best matching jobs for user
        Args:
            user_profile: User profile data
            jobs: List of available jobs
            filters: Optional filters (location, experience, etc.)
            top_k: Number of top matches to return
        Returns:
            List of matched jobs with scores
        """
        # Apply filters first
        if filters:
            jobs = self._apply_filters(jobs, filters)
        
        # Calculate similarities
        job_scores = self.calculate_similarity(user_profile, jobs)
        
        # Get top K matches
        top_matches = job_scores[:top_k]
        
        # Format results
        results = []
        for job, score in top_matches:
            job_with_score = {**job, 'match_score': round(float(score * 100), 2)}
            results.append(job_with_score)
        
        return results
    
    def _apply_filters(self, jobs: List[Dict], filters: Dict) -> List[Dict]:
        """
        Apply filters to job list
        Args:
            jobs: List of jobs
            filters: Filter dictionary
        Returns:
            Filtered job list
        """
        filtered = jobs
        
        # Location filter
        if filters.get('location') and filters['location'].lower() != 'any':
            location = filters['location'].lower()
            filtered = [
                job for job in filtered
                if location in job.get('location', '').lower()
            ]
        
        # Experience level filter
        if filters.get('experience_level'):
            exp_level = filters['experience_level']
            filtered = [
                job for job in filtered
                if job.get('experience_level') == exp_level
            ]
        
        # Work type filter
        if filters.get('work_type'):
            work_type = filters['work_type']
            filtered = [
                job for job in filtered
                if job.get('work_type') == work_type
            ]
        
        # Job type filter
        if filters.get('job_type'):
            job_type = filters['job_type']
            filtered = [
                job for job in filtered
                if job.get('job_type') == job_type
            ]
        
        # Salary filter
        if filters.get('min_salary'):
            min_sal = filters['min_salary']
            filtered = [
                job for job in filtered
                if job.get('salary_min', 0) >= min_sal
            ]
        
        return filtered
    
    def get_match_explanation(self, user_profile: Dict, job: Dict) -> Dict:
        """
        Generate explanation for job match
        Args:
            user_profile: User profile
            job: Job posting
        Returns:
            Explanation dictionary
        """
        explanation = {
            'matched_skills': [],
            'missing_skills': [],
            'experience_match': False,
            'title_match': False
        }
        
        # Check skill matches
        user_skills = set(str(s).lower() for s in user_profile.get('skills', []))
        job_skills = set(str(s).lower() for s in job.get('skills_required', []))
        
        explanation['matched_skills'] = list(user_skills.intersection(job_skills))
        explanation['missing_skills'] = list(job_skills - user_skills)
        
        # Check experience match
        user_exp_years = len(user_profile.get('experience', []))
        job_exp_level = job.get('experience_level', '').lower()
        
        if (job_exp_level == 'entry' and user_exp_years <= 2) or \
           (job_exp_level == 'mid' and 2 <= user_exp_years <= 5) or \
           (job_exp_level == 'senior' and user_exp_years >= 5):
            explanation['experience_match'] = True
        
        # Check title match
        target_role = user_profile.get('target_role', '').lower()
        job_title = job.get('title', '').lower()
        if target_role and target_role in job_title:
            explanation['title_match'] = True
        
        return explanation
