from app import db
from app.models import User, UserProfile

class UserController:
    """Controller for user profile operations"""
    
    @staticmethod
    def get_user_profile(user_id):
        """
        Get user profile by ID
        Args:
            user_id: User ID
        Returns:
            Tuple of (success, message/user_data, status_code)
        """
        user = User.query.get(user_id)
        
        if not user:
            return False, 'User not found', 404
        
        return True, {
            'user': user.to_dict()
        }, 200
    
    @staticmethod
    def update_user_profile(user_id, data):
        """
        Update user profile
        Args:
            user_id: User ID
            data: Dictionary containing profile fields to update
        Returns:
            Tuple of (success, message/user_data, status_code)
        """
        user = User.query.get(user_id)
        
        if not user:
            return False, 'User not found', 404
        
        try:
            # Update user basic info
            if 'first_name' in data:
                user.first_name = data['first_name'].strip()
            if 'last_name' in data:
                user.last_name = data['last_name'].strip()
            
            # Get or create profile
            profile = user.profile
            if not profile:
                profile = UserProfile(user_id=user.id)
                db.session.add(profile)
            
            # Update profile fields
            profile_fields = [
                'bio', 'phone', 'location', 'avatar_url',
                'skills', 'experience', 'education', 'interests',
                'linkedin_url', 'github_url', 'portfolio_url',
                'theme_preference'
            ]
            
            for field in profile_fields:
                if field in data:
                    setattr(profile, field, data[field])
            
            # Validate theme preference
            if 'theme_preference' in data:
                if data['theme_preference'] not in ['light', 'dark']:
                    return False, 'Invalid theme preference. Must be "light" or "dark"', 422
            
            db.session.commit()
            
            return True, {
                'user': user.to_dict(),
                'message': 'Profile updated successfully'
            }, 200
            
        except Exception as e:
            db.session.rollback()
            return False, f'Update failed: {str(e)}', 500
    
    @staticmethod
    def update_theme_preference(user_id, theme):
        """
        Update user theme preference
        Args:
            user_id: User ID
            theme: 'light' or 'dark'
        Returns:
            Tuple of (success, message/data, status_code)
        """
        if theme not in ['light', 'dark']:
            return False, 'Invalid theme. Must be "light" or "dark"', 422
        
        user = User.query.get(user_id)
        
        if not user:
            return False, 'User not found', 404
        
        try:
            profile = user.profile
            if not profile:
                profile = UserProfile(user_id=user.id)
                db.session.add(profile)
            
            profile.theme_preference = theme
            db.session.commit()
            
            return True, {
                'theme_preference': theme,
                'message': 'Theme updated successfully'
            }, 200
            
        except Exception as e:
            db.session.rollback()
            return False, f'Update failed: {str(e)}', 500
    
    @staticmethod
    def get_all_users(page=1, per_page=10, role=None):
        """
        Get all users with pagination
        Args:
            page: Page number
            per_page: Items per page
            role: Filter by role (optional)
        Returns:
            Tuple of (success, message/users_data, status_code)
        """
        try:
            query = User.query
            
            if role:
                query = query.filter_by(role=role)
            
            pagination = query.paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )
            
            users = [user.to_dict() for user in pagination.items]
            
            return True, {
                'users': users,
                'total': pagination.total,
                'pages': pagination.pages,
                'current_page': page,
                'per_page': per_page
            }, 200
            
        except Exception as e:
            return False, f'Failed to fetch users: {str(e)}', 500
