"""
Career Recommendation Controller
Handles business logic for AI-powered career path recommendations
"""

from app.ml.career_recommender import get_recommender
from app.models import User, UserProfile
from typing import Tuple, Dict


class CareerController:
    """Controller for career recommendation operations"""
    
    @staticmethod
    def get_career_recommendations(user_id: int, top_n: int = 5) -> Tuple[bool, Dict, int]:
        """
        Get AI-powered career recommendations for a user
        Args:
            user_id: User ID
            top_n: Number of recommendations to return
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
            
            # Extract user profile data
            profile = user.profile
            user_data = {
                'skills': profile.skills or [],
                'interests': profile.interests or [],
                'experience': profile.experience or [],
                'education': profile.education or []
            }
            
            # Check if user has any skills
            if not user_data['skills'] and not user_data['interests']:
                return False, {
                    'message': 'Please add skills and interests to your profile to get personalized recommendations',
                    'suggestions': 'Add at least 3-5 skills related to your expertise or learning goals'
                }, 400
            
            # Get recommender instance
            recommender = get_recommender()
            
            # Generate recommendations
            recommendations = recommender.recommend_careers(
                user_profile=user_data,
                top_n=top_n
            )
            
            if not recommendations:
                return False, {
                    'message': 'Could not generate recommendations. Please add more skills to your profile.',
                    'available_skills': recommender.all_skills[:50]  # Show sample skills
                }, 404
            
            return True, {
                'recommendations': recommendations,
                'user_skills': user_data['skills'],
                'total_careers_analyzed': len(recommender.career_paths),
                'message': f'Found {len(recommendations)} career matches based on your profile'
            }, 200
            
        except Exception as e:
            return False, f'Error generating recommendations: {str(e)}', 500
    
    @staticmethod
    def get_skill_gap_analysis(user_id: int, target_career: str) -> Tuple[bool, Dict, int]:
        """
        Get detailed skill gap analysis for a specific career
        Args:
            user_id: User ID
            target_career: Target career role name
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
            
            profile = user.profile
            user_skills = profile.skills or []
            
            # Get recommender instance
            recommender = get_recommender()
            
            # Get skill recommendations
            analysis = recommender.get_skill_recommendations(user_skills, target_career)
            
            if 'error' in analysis:
                return False, analysis, 404
            
            return True, analysis, 200
            
        except Exception as e:
            return False, f'Error analyzing skill gaps: {str(e)}', 500
    
    @staticmethod
    def get_all_careers() -> Tuple[bool, Dict, int]:
        """
        Get list of all available career paths
        Returns:
            Tuple of (success, data/error_message, status_code)
        """
        try:
            recommender = get_recommender()
            
            careers = [
                {
                    'role': career['role'],
                    'category': career['category'],
                    'description': career['description'],
                    'required_skills_count': len(career['required_skills']),
                    'average_salary': career['average_salary'],
                    'growth_rate': career['growth_rate']
                }
                for career in recommender.career_paths
            ]
            
            # Group by category
            categories = {}
            for career in recommender.career_paths:
                category = career['category']
                if category not in categories:
                    categories[category] = []
                categories[category].append(career['role'])
            
            return True, {
                'careers': careers,
                'total_careers': len(careers),
                'categories': categories,
                'message': 'Available career paths retrieved successfully'
            }, 200
            
        except Exception as e:
            return False, f'Error fetching careers: {str(e)}', 500
    
    @staticmethod
    def get_career_details(role_name: str) -> Tuple[bool, Dict, int]:
        """
        Get detailed information about a specific career
        Args:
            role_name: Career role name
        Returns:
            Tuple of (success, data/error_message, status_code)
        """
        try:
            recommender = get_recommender()
            
            # Find career
            career = next(
                (c for c in recommender.career_paths if c['role'].lower() == role_name.lower()),
                None
            )
            
            if not career:
                return False, {
                    'error': f"Career '{role_name}' not found",
                    'available_careers': [c['role'] for c in recommender.career_paths]
                }, 404
            
            return True, {
                'career': career,
                'message': f'Details for {career["role"]} retrieved successfully'
            }, 200
            
        except Exception as e:
            return False, f'Error fetching career details: {str(e)}', 500
    
    @staticmethod
    def get_available_skills() -> Tuple[bool, Dict, int]:
        """
        Get list of all skills across careers (for autocomplete/suggestions)
        Returns:
            Tuple of (success, data/error_message, status_code)
        """
        try:
            recommender = get_recommender()
            
            return True, {
                'skills': recommender.all_skills,
                'total_skills': len(recommender.all_skills),
                'message': 'Available skills retrieved successfully'
            }, 200
            
        except Exception as e:
            return False, f'Error fetching skills: {str(e)}', 500
