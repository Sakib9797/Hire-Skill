"""
Resume and Cover Letter Models
Stores generated resumes and cover letters with versioning
"""

from app import db
from datetime import datetime


class Resume(db.Model):
    """Resume model with versioning support"""
    __tablename__ = 'resumes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Resume content
    title = db.Column(db.String(200), nullable=False)
    target_role = db.Column(db.String(100), nullable=True)
    job_description = db.Column(db.Text, nullable=True)  # Job description used for generation
    content = db.Column(db.JSON, nullable=False)  # Structured JSON format (ATS-compliant)
    
    # Versioning
    version = db.Column(db.Integer, default=1)
    is_current = db.Column(db.Boolean, default=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=True)
    
    # ATS Metadata
    is_ats_optimized = db.Column(db.Boolean, default=True)
    template_name = db.Column(db.String(50), default='ats_professional')
    keywords_matched = db.Column(db.JSON, nullable=True)  # Matched keywords from job description
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='resumes')
    versions = db.relationship('Resume', backref=db.backref('parent', remote_side=[id]))
    
    def to_dict(self):
        """Convert resume to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'target_role': self.target_role,
            'job_description': self.job_description,
            'content': self.content,
            'version': self.version,
            'is_current': self.is_current,
            'parent_id': self.parent_id,
            'is_ats_optimized': self.is_ats_optimized,
            'template_name': self.template_name,
            'keywords_matched': self.keywords_matched,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class CoverLetter(db.Model):
    """Cover Letter model"""
    __tablename__ = 'cover_letters'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=True)
    
    # Cover letter content
    title = db.Column(db.String(200), nullable=False)
    company_name = db.Column(db.String(200), nullable=True)
    job_title = db.Column(db.String(200), nullable=True)
    content = db.Column(db.Text, nullable=False)  # Generated text
    
    # Versioning
    version = db.Column(db.Integer, default=1)
    is_current = db.Column(db.Boolean, default=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('cover_letters.id'), nullable=True)
    
    # Metadata
    tone = db.Column(db.String(50), default='professional')  # professional, friendly, formal
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='cover_letters')
    resume = db.relationship('Resume', backref='cover_letters')
    versions = db.relationship('CoverLetter', backref=db.backref('parent', remote_side=[id]))
    
    def to_dict(self):
        """Convert cover letter to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'resume_id': self.resume_id,
            'title': self.title,
            'company_name': self.company_name,
            'job_title': self.job_title,
            'content': self.content,
            'version': self.version,
            'is_current': self.is_current,
            'parent_id': self.parent_id,
            'tone': self.tone,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
