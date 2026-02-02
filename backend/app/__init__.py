from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from config import config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address)
cache = Cache()

def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    jwt.init_app(app)
    
    # Initialize rate limiter
    limiter.init_app(app)
    
    # Initialize cache
    cache.init_app(app)
    
    # Error handler for rate limit exceeded
    @app.errorhandler(429)
    def ratelimit_handler(e):
        return jsonify({
            'success': False,
            'error': 'Rate limit exceeded',
            'message': str(e.description),
            'retry_after': e.description
        }), 429
    
    # Register blueprints
    from app.views.auth_views import auth_bp
    from app.views.user_views import user_bp
    from app.views.career_views import career_bp
    from app.views.document_views import document_bp
    from app.views.job_views import job_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(career_bp, url_prefix='/api/career')
    app.register_blueprint(document_bp, url_prefix='/api/documents')
    app.register_blueprint(job_bp, url_prefix='/api/jobs')
    
    # Health check route
    @app.route('/api/health')
    def health_check():
        return {'status': 'healthy', 'message': 'HireSkill API is running'}, 200
    
    return app
