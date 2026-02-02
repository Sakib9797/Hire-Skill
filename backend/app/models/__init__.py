# Import models here for easier access
from app.models.user import User, UserProfile, UserRole
from app.models.document import Resume, CoverLetter

__all__ = ['User', 'UserProfile', 'UserRole', 'Resume', 'CoverLetter']
