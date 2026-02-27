import os
import logging
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from config import config

logger = logging.getLogger(__name__)

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address)
cache = Cache()


def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG if app.config.get('DEBUG') else logging.INFO,
        format='%(asctime)s %(levelname)s [%(name)s] %(message)s',
    )

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # CORS — restrict origins in production
    allowed_origins = os.environ.get(
        'CORS_ORIGINS',
        'http://localhost:3000,http://127.0.0.1:3000'
    ).split(',')
    CORS(app, resources={r"/api/*": {"origins": allowed_origins}},
         supports_credentials=True)

    jwt.init_app(app)

    # Initialize rate limiter
    limiter.init_app(app)

    # Initialize cache
    cache.init_app(app)

    # Security headers
    @app.after_request
    def set_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        if not app.debug:
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response

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
    from app.views.salary_views import salary_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(career_bp, url_prefix='/api/career')
    app.register_blueprint(document_bp, url_prefix='/api/documents')
    app.register_blueprint(job_bp, url_prefix='/api/jobs')
    app.register_blueprint(salary_bp, url_prefix='/api/salary')

    # Health check route
    @app.route('/api/health')
    def health_check():
        return {'status': 'healthy', 'message': 'HireSkill API is running'}, 200

    logger.info('HireSkill app created (config=%s)', config_name)
    return app
