"""
Job Model
"""
from datetime import datetime
from app import db

class Job(db.Model):
    """Job posting model"""
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200))
    work_type = db.Column(db.String(50))  # Remote, Hybrid, On-site
    job_type = db.Column(db.String(50))  # Full-time, Part-time, Contract
    experience_level = db.Column(db.String(50))  # Entry, Mid, Senior
    salary_min = db.Column(db.Integer)
    salary_max = db.Column(db.Integer)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.JSON)  # List of requirements
    responsibilities = db.Column(db.JSON)  # List of responsibilities
    skills_required = db.Column(db.JSON)  # List of required skills
    benefits = db.Column(db.JSON)  # List of benefits
    source = db.Column(db.String(100))  # LinkedIn, Indeed, etc.
    source_url = db.Column(db.String(500))
    company_logo = db.Column(db.String(500))
    posted_date = db.Column(db.DateTime, default=datetime.utcnow)
    application_deadline = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    embedding = db.Column(db.LargeBinary)  # Store job embedding for similarity
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert job to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'company': self.company,
            'location': self.location,
            'work_type': self.work_type,
            'job_type': self.job_type,
            'experience_level': self.experience_level,
            'salary_min': self.salary_min,
            'salary_max': self.salary_max,
            'description': self.description,
            'requirements': self.requirements,
            'responsibilities': self.responsibilities,
            'skills_required': self.skills_required,
            'benefits': self.benefits,
            'source': self.source,
            'source_url': self.source_url,
            'company_logo': self.company_logo,
            'posted_date': self.posted_date.isoformat() if self.posted_date else None,
            'application_deadline': self.application_deadline.isoformat() if self.application_deadline else None,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Job {self.title} at {self.company}>'


class JobApplication(db.Model):
    """Job application tracking model"""
    __tablename__ = 'job_applications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    status = db.Column(db.String(50), default='saved')  # saved, applied, interview, rejected, accepted
    applied_date = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'))
    cover_letter_id = db.Column(db.Integer, db.ForeignKey('cover_letters.id'))
    match_score = db.Column(db.Float)  # Relevance score
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='job_applications')
    job = db.relationship('Job', backref='applications')
    resume = db.relationship('Resume', backref='job_applications')
    cover_letter = db.relationship('CoverLetter', backref='job_applications')
    
    def to_dict(self):
        """Convert job application to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'job_id': self.job_id,
            'job': self.job.to_dict() if self.job else None,
            'status': self.status,
            'applied_date': self.applied_date.isoformat() if self.applied_date else None,
            'notes': self.notes,
            'resume_id': self.resume_id,
            'cover_letter_id': self.cover_letter_id,
            'match_score': self.match_score,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<JobApplication user={self.user_id} job={self.job_id}>'
