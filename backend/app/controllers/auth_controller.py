from app import db
from app.models import User, UserProfile, UserRole
from app.utils import (
    hash_password,
    verify_password,
    validate_email,
    validate_password,
    validate_required_fields
)
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import datetime

class AuthController:
    """Controller for authentication operations"""
    
    @staticmethod
    def register_user(data):
        """
        Register a new user
        Args:
            data: Dictionary containing email, password, first_name, last_name, role
        Returns:
            Tuple of (success, message/user_data, status_code)
        """
        # Validate required fields
        required_fields = ['email', 'password']
        is_valid, message = validate_required_fields(data, required_fields)
        if not is_valid:
            return False, message, 422
        
        email = data.get('email', '').strip().lower()
        password = data.get('password')
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        role = data.get('role', UserRole.USER.value)
        
        # Validate email
        if not validate_email(email):
            return False, 'Invalid email format', 422
        
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            return False, 'Email already registered', 409
        
        # Validate password
        is_valid, message = validate_password(password)
        if not is_valid:
            return False, message, 422
        
        # Validate role
        valid_roles = [r.value for r in UserRole]
        if role not in valid_roles:
            return False, f'Invalid role. Must be one of: {", ".join(valid_roles)}', 422
        
        try:
            # Create user
            user = User(
                email=email,
                password_hash=hash_password(password),
                first_name=first_name,
                last_name=last_name,
                role=role
            )
            
            db.session.add(user)
            db.session.flush()  # Get user ID
            
            # Create default profile
            profile = UserProfile(
                user_id=user.id,
                theme_preference='light'
            )
            
            db.session.add(profile)
            db.session.commit()
            
            return True, {
                'user': user.to_dict(),
                'message': 'User registered successfully'
            }, 201
            
        except Exception as e:
            db.session.rollback()
            return False, f'Registration failed: {str(e)}', 500
    
    @staticmethod
    def login_user(data):
        """
        Authenticate user and generate JWT tokens
        Args:
            data: Dictionary containing email and password
        Returns:
            Tuple of (success, message/token_data, status_code)
        """
        # Validate required fields
        required_fields = ['email', 'password']
        is_valid, message = validate_required_fields(data, required_fields)
        if not is_valid:
            return False, message, 422
        
        email = data.get('email', '').strip().lower()
        password = data.get('password')
        
        # Find user
        user = User.query.filter_by(email=email).first()
        
        if not user or not verify_password(password, user.password_hash):
            return False, 'Invalid email or password', 401
        
        if not user.is_active:
            return False, 'Account is deactivated', 403
        
        # Generate tokens
        additional_claims = {
            'role': user.role,
            'email': user.email
        }
        
        access_token = create_access_token(
            identity=user.id,
            additional_claims=additional_claims
        )
        
        refresh_token = create_refresh_token(
            identity=user.id,
            additional_claims=additional_claims
        )
        
        return True, {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict(),
            'message': 'Login successful'
        }, 200
    
    @staticmethod
    def refresh_access_token(user_id):
        """
        Generate new access token
        Args:
            user_id: User ID from refresh token
        Returns:
            Tuple of (success, message/token_data, status_code)
        """
        user = User.query.get(user_id)
        
        if not user:
            return False, 'User not found', 404
        
        if not user.is_active:
            return False, 'Account is deactivated', 403
        
        additional_claims = {
            'role': user.role,
            'email': user.email
        }
        
        access_token = create_access_token(
            identity=user.id,
            additional_claims=additional_claims
        )
        
        return True, {
            'access_token': access_token,
            'message': 'Token refreshed successfully'
        }, 200
