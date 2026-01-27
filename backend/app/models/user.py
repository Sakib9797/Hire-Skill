from datetime import datetime
from app import db
from enum import Enum

class UserRole(Enum):
    """User role enumeration"""
    USER = "user"
    ADMIN = "admin"
    EMPLOYER = "employer"
    CANDIDATE = "candidate"

class User(db.Model):
    """User model for authentication and profile"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    role = db.Column(db.String(20), default=UserRole.USER.value)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with profile
    profile = db.relationship('UserProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'profile': self.profile.to_dict() if self.profile else None
        }

class UserProfile(db.Model):
    """User profile model for additional information"""
    __tablename__ = 'user_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Profile fields
    bio = db.Column(db.Text)
    phone = db.Column(db.String(20))
    location = db.Column(db.String(100))
    avatar_url = db.Column(db.String(255))
    
    # Skills and experience
    skills = db.Column(db.JSON, default=list)  # Array of skills
    experience = db.Column(db.JSON, default=list)  # Array of experience objects
    education = db.Column(db.JSON, default=list)  # Array of education objects
    interests = db.Column(db.JSON, default=list)  # Array of interests
    
    # Social links
    linkedin_url = db.Column(db.String(255))
    github_url = db.Column(db.String(255))
    portfolio_url = db.Column(db.String(255))
    
    # Preferences
    theme_preference = db.Column(db.String(10), default='light')  # 'light' or 'dark'
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<UserProfile {self.user_id}>'
    
    def to_dict(self):
        """Convert profile object to dictionary"""
        return {
            'id': self.id,
            'bio': self.bio,
            'phone': self.phone,
            'location': self.location,
            'avatar_url': self.avatar_url,
            'skills': self.skills or [],
            'experience': self.experience or [],
            'education': self.education or [],
            'interests': self.interests or [],
            'linkedin_url': self.linkedin_url,
            'github_url': self.github_url,
            'portfolio_url': self.portfolio_url,
            'theme_preference': self.theme_preference
        }
