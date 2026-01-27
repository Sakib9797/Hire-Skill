from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers import AuthController
from app.utils import success_response, error_response

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    if not data:
        return error_response('No data provided', 400)
    
    success, result, status = AuthController.register_user(data)
    
    if success:
        return success_response(result, result.get('message', 'Success'), status)
    else:
        return error_response(result, status)

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user and return JWT tokens"""
    data = request.get_json()
    
    if not data:
        return error_response('No data provided', 400)
    
    success, result, status = AuthController.login_user(data)
    
    if success:
        return success_response(result, result.get('message', 'Success'), status)
    else:
        return error_response(result, status)

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token using refresh token"""
    user_id = get_jwt_identity()
    
    success, result, status = AuthController.refresh_access_token(user_id)
    
    if success:
        return success_response(result, result.get('message', 'Success'), status)
    else:
        return error_response(result, status)

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current authenticated user info"""
    from app.models import User
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return error_response('User not found', 404)
    
    return success_response({'user': user.to_dict()}, 'User retrieved successfully')
