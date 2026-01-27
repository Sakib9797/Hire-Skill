from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.controllers import UserController
from app.utils import success_response, error_response, role_required

user_bp = Blueprint('users', __name__)

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user's profile"""
    user_id = get_jwt_identity()
    
    success, result, status = UserController.get_user_profile(user_id)
    
    if success:
        return success_response(result, 'Profile retrieved successfully', status)
    else:
        return error_response(result, status)

@user_bp.route('/profile', methods=['PUT', 'PATCH'])
@jwt_required()
def update_profile():
    """Update current user's profile"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data:
        return error_response('No data provided', 400)
    
    success, result, status = UserController.update_user_profile(user_id, data)
    
    if success:
        return success_response(result, result.get('message', 'Success'), status)
    else:
        return error_response(result, status)

@user_bp.route('/profile/theme', methods=['PUT'])
@jwt_required()
def update_theme():
    """Update user theme preference"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or 'theme' not in data:
        return error_response('Theme not provided', 400)
    
    success, result, status = UserController.update_theme_preference(
        user_id, 
        data['theme']
    )
    
    if success:
        return success_response(result, result.get('message', 'Success'), status)
    else:
        return error_response(result, status)

@user_bp.route('/', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_users():
    """Get all users (admin only)"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    role = request.args.get('role', None)
    
    success, result, status = UserController.get_all_users(page, per_page, role)
    
    if success:
        return success_response(result, 'Users retrieved successfully', status)
    else:
        return error_response(result, status)

@user_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_user_by_id(user_id):
    """Get user by ID (admin only)"""
    success, result, status = UserController.get_user_profile(user_id)
    
    if success:
        return success_response(result, 'User retrieved successfully', status)
    else:
        return error_response(result, status)
