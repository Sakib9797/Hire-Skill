"""
Career Recommendation API Views
Endpoints for AI-powered career path recommendations
"""

from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.career_controller import CareerController
from app.utils import success_response, error_response
from app import limiter, cache

career_bp = Blueprint('career', __name__)


@career_bp.route('/recommend', methods=['GET'])
@jwt_required()
@limiter.limit(lambda: current_app.config.get('RATELIMIT_CAREER_RECOMMEND', "10 per minute"))
@cache.cached(timeout=300, key_prefix=lambda: f"career_recommend_{get_jwt_identity()}")
def get_recommendations():
    """
    Get AI-powered career recommendations for authenticated user
    Query Parameters:
        - top_n: Number of recommendations (default: 5, max: 15)
    Returns:
        List of recommended career paths with similarity scores and skill gaps
    """
    try:
        user_id = get_jwt_identity()
        top_n = request.args.get('top_n', default=5, type=int)
        
        # Limit to reasonable range
        top_n = max(1, min(top_n, 15))
        
        success, result, status = CareerController.get_career_recommendations(
            user_id=user_id,
            top_n=top_n
        )
        
        if success:
            return success_response(result, result.get('message', 'Success'), status)
        else:
            return error_response(result, status)
            
    except Exception as e:
        return error_response(f'Error processing request: {str(e)}', 500)


@career_bp.route('/skill-gap/<string:career_role>', methods=['GET'])
@jwt_required()
@limiter.limit(lambda: current_app.config.get('RATELIMIT_CAREER_RECOMMEND', "10 per minute"))
@cache.cached(timeout=300, key_prefix=lambda: f"skill_gap_{get_jwt_identity()}_{career_role}")
def get_skill_gap(career_role):
    """
    Get detailed skill gap analysis for a specific career
    Path Parameters:
        - career_role: Name of the target career role
    Returns:
        Detailed skill gap analysis and learning path
    """
    try:
        user_id = get_jwt_identity()
        
        success, result, status = CareerController.get_skill_gap_analysis(
            user_id=user_id,
            target_career=career_role
        )
        
        if success:
            return success_response(result, 'Skill gap analysis completed', status)
        else:
            return error_response(result, status)
            
    except Exception as e:
        return error_response(f'Error processing request: {str(e)}', 500)


@career_bp.route('/careers', methods=['GET'])
@limiter.limit("60 per minute")
@cache.cached(timeout=600, key_prefix="all_careers")
def get_all_careers():
    """
    Get list of all available career paths
    No authentication required
    Returns:
        List of all career paths with basic info
    """
    try:
        success, result, status = CareerController.get_all_careers()
        
        if success:
            return success_response(result, result.get('message', 'Success'), status)
        else:
            return error_response(result, status)
            
    except Exception as e:
        return error_response(f'Error processing request: {str(e)}', 500)


@career_bp.route('/careers/<string:role_name>', methods=['GET'])
@limiter.limit("60 per minute")
@cache.cached(timeout=600, key_prefix=lambda: f"career_details_{role_name}")
def get_career_details(role_name):
    """
    Get detailed information about a specific career
    Path Parameters:
        - role_name: Name of the career role
    Returns:
        Detailed career information including skills, salary, etc.
    """
    try:
        success, result, status = CareerController.get_career_details(role_name)
        
        if success:
            return success_response(result, result.get('message', 'Success'), status)
        else:
            return error_response(result, status)
            
    except Exception as e:
        return error_response(f'Error processing request: {str(e)}', 500)


@career_bp.route('/skills', methods=['GET'])
@limiter.limit("60 per minute")
@cache.cached(timeout=600, key_prefix="available_skills")
def get_available_skills():
    """
    Get list of all skills across careers
    Useful for autocomplete and skill suggestions
    Returns:
        List of all available skills
    """
    try:
        success, result, status = CareerController.get_available_skills()
        
        if success:
            return success_response(result, result.get('message', 'Success'), status)
        else:
            return error_response(result, status)
            
    except Exception as e:
        return error_response(f'Error processing request: {str(e)}', 500)


@career_bp.route('/health', methods=['GET'])
@limiter.exempt
def career_health_check():
    """
    Health check endpoint for career recommendation service
    Returns:
        Service status and model information
    """
    try:
        from app.ml.career_recommender import get_recommender
        recommender = get_recommender()
        
        return success_response({
            'status': 'healthy',
            'service': 'Career Recommendation Service',
            'model': 'TF-IDF + Cosine Similarity',
            'total_careers': len(recommender.career_paths),
            'total_skills': len(recommender.all_skills),
            'features': [
                'AI-powered career matching',
                'Skill gap analysis',
                'Learning path recommendations',
                'Similarity-based ranking'
            ]
        }, 'Career recommendation service is operational', 200)
        
    except Exception as e:
        return error_response(f'Service health check failed: {str(e)}', 500)
