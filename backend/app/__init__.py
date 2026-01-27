from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    jwt.init_app(app)
    
    # Register blueprints
    from app.views.auth_views import auth_bp
    from app.views.user_views import user_bp
    from app.views.career_views import career_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(career_bp, url_prefix='/api/career')
    
    # Health check route
    @app.route('/api/health')
    def health_check():
        return {'status': 'healthy', 'message': 'HireSkill API is running'}, 200
    
    return app
