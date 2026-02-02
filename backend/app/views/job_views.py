"""
Job API Views
RESTful endpoints for job search and matching
"""
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.job_controller import JobController
from app.models.user import User
from app import limiter, cache

job_bp = Blueprint('jobs', __name__)

@job_bp.route('/health', methods=['GET'])
@limiter.exempt
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Job Search & Matching',
        'endpoints': {
            'POST /api/jobs/initialize': 'Initialize job database with mock data',
            'GET /api/jobs/match': 'Get matched jobs for user',
            'GET /api/jobs/search': 'Search jobs with filters',
            'GET /api/jobs/<id>': 'Get specific job details',
            'POST /api/jobs/<id>/save': 'Save job for later',
            'POST /api/jobs/<id>/apply': 'Apply to job',
            'GET /api/jobs/applications': 'Get user applications',
            'GET /api/jobs/<id>/match-explanation': 'Get match explanation'
        }
    }), 200


@job_bp.route('/initialize', methods=['POST'])
@jwt_required()
@limiter.limit("5 per minute")
def initialize_jobs():
    """Initialize job database with mock data"""
    user_id = get_jwt_identity()
    success, message, status = JobController.initialize_jobs()
    
    if success:
        return jsonify({'message': message}), status
    return jsonify({'error': message}), status


@job_bp.route('/match', methods=['GET'])
@jwt_required()
@limiter.limit(lambda: current_app.config.get('RATELIMIT_JOB_SEARCH', "30 per minute"))
@cache.cached(timeout=120, key_prefix=lambda: f"job_match_{get_jwt_identity()}")
def match_jobs():
    """
    Get matched jobs for user using NLP
    Query params:
        - role: Target role
        - location: Location filter
        - experience_level: Experience level filter
        - work_type: Work type filter
        - job_type: Job type filter
        - limit: Number of results (default: 20)
    """
    # Parse query parameters
    filters = {}
    
    if request.args.get('role'):
        filters['role'] = request.args.get('role')
    
    if request.args.get('location'):
        filters['location'] = request.args.get('location')
    
    if request.args.get('experience_level'):
        filters['experience_level'] = request.args.get('experience_level')
    
    if request.args.get('work_type'):
        filters['work_type'] = request.args.get('work_type')
    
    if request.args.get('job_type'):
        filters['job_type'] = request.args.get('job_type')
    
    limit = int(request.args.get('limit', 20))
    
    # Get matched jobs
    user_id = get_jwt_identity()
    success, data, status = JobController.match_jobs(
        user_id=user_id,
        filters=filters if filters else None,
        limit=limit
    )
    
    if success:
        return jsonify(data), status
    return jsonify({'error': data}), status


@job_bp.route('/search', methods=['GET'])
@limiter.limit(lambda: current_app.config.get('RATELIMIT_JOB_SEARCH', "30 per minute"))
@cache.cached(timeout=180, query_string=True)
def search_jobs():
    """
    Search jobs with filters (public endpoint)
    Query params:
        - q: Search query
        - location: Location filter
        - experience_level: Experience level filter
        - work_type: Work type filter
        - job_type: Job type filter
        - min_salary: Minimum salary
        - limit: Results limit (default: 50)
        - offset: Results offset for pagination (default: 0)
    """
    query = request.args.get('q')
    
    filters = {}
    if request.args.get('location'):
        filters['location'] = request.args.get('location')
    
    if request.args.get('experience_level'):
        filters['experience_level'] = request.args.get('experience_level')
    
    if request.args.get('work_type'):
        filters['work_type'] = request.args.get('work_type')
    
    if request.args.get('job_type'):
        filters['job_type'] = request.args.get('job_type')
    
    if request.args.get('min_salary'):
        filters['min_salary'] = int(request.args.get('min_salary'))
    
    limit = int(request.args.get('limit', 50))
    offset = int(request.args.get('offset', 0))
    
    success, data, status = JobController.search_jobs(
        query=query,
        filters=filters if filters else None,
        limit=limit,
        offset=offset
    )
    
    if success:
        return jsonify(data), status
    return jsonify({'error': data}), status


@job_bp.route('/<int:job_id>', methods=['GET'])
@limiter.limit("60 per minute")
@cache.cached(timeout=300, key_prefix=lambda: f"job_{job_id}")
def get_job(job_id):
    """Get specific job details"""
    # Get user ID if authenticated
    user_id = None
    auth_header = request.headers.get('Authorization')
    if auth_header:
        try:
            from flask_jwt_extended import decode_token, verify_jwt_in_request
            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity()
        except:
            pass
    
    success, data, status = JobController.get_job(job_id, user_id)
    
    if success:
        return jsonify(data), status
    return jsonify({'error': data}), status


@job_bp.route('/<int:job_id>/save', methods=['POST'])
@jwt_required()
@limiter.limit("20 per minute")
def save_job(job_id):
    """Save job for later"""
    user_id = get_jwt_identity()
    success, data, status = JobController.save_job(
        user_id=user_id,
        job_id=job_id
    )
    
    if success:
        return jsonify(data), status
    return jsonify({'error': data}), status


@job_bp.route('/<int:job_id>/apply', methods=['POST'])
@jwt_required()
@limiter.limit("10 per minute")
def apply_to_job(job_id):
    """
    Apply to job
    Body:
        - resume_id: Optional resume ID
        - cover_letter_id: Optional cover letter ID
        - match_score: Optional match score
    """
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    
    success, result, status = JobController.apply_to_job(
        user_id=user_id,
        job_id=job_id,
        resume_id=data.get('resume_id'),
        cover_letter_id=data.get('cover_letter_id'),
        match_score=data.get('match_score')
    )
    
    if success:
        return jsonify(result), status
    return jsonify({'error': result}), status


@job_bp.route('/applications', methods=['GET'])
@jwt_required()
@limiter.limit("30 per minute")
@cache.cached(timeout=120, key_prefix=lambda: f"applications_{get_jwt_identity()}")
def get_applications():
    """
    Get user's job applications
    Query params:
        - status: Optional status filter (saved, applied, interview, rejected, accepted)
    """
    user_id = get_jwt_identity()
    status_filter = request.args.get('status')
    
    success, data, status = JobController.get_user_applications(
        user_id=user_id,
        status=status_filter
    )
    
    if success:
        return jsonify(data), status
    return jsonify({'error': data}), status


@job_bp.route('/<int:job_id>/match-explanation', methods=['GET'])
@jwt_required()
@limiter.limit("20 per minute")
@cache.cached(timeout=300, key_prefix=lambda: f"match_explain_{get_jwt_identity()}_{job_id}")
def get_match_explanation(job_id):
    """Get explanation for why job was matched"""
    user_id = get_jwt_identity()
    success, data, status = JobController.get_match_explanation(
        user_id=user_id,
        job_id=job_id
    )
    
    if success:
        return jsonify(data), status
    return jsonify({'error': data}), status
