import os
import sys
from dotenv import load_dotenv

load_dotenv()


def _require_secret(key: str, default: str = '') -> str:
    """Return env var; crash in production when the value is the insecure default."""
    value = os.environ.get(key, default)
    if os.environ.get('FLASK_ENV') == 'production' and value in ('', 'change-me-in-production'):
        sys.exit(f'FATAL: {key} must be set in production. Exiting.')
    return value


class Config:
    """Base configuration"""
    SECRET_KEY = _require_secret('FLASK_SECRET_KEY', 'flask-dev-secret')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://localhost/hireskillz_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Database connection pool (production-safe defaults)
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': int(os.environ.get('DB_POOL_SIZE', 5)),
        'max_overflow': int(os.environ.get('DB_MAX_OVERFLOW', 10)),
        'pool_timeout': int(os.environ.get('DB_POOL_TIMEOUT', 30)),
        'pool_recycle': int(os.environ.get('DB_POOL_RECYCLE', 1800)),
        'pool_pre_ping': True,
    }

    # JWT Configuration
    JWT_SECRET_KEY = _require_secret('JWT_SECRET_KEY', 'change-me-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 3600))
    JWT_REFRESH_TOKEN_EXPIRES = int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRES', 2592000))

    # CORS
    CORS_HEADERS = 'Content-Type'

    # Rate Limiting Configuration
    RATELIMIT_STORAGE_URI = os.environ.get('RATELIMIT_STORAGE_URI') or 'memory://'
    RATELIMIT_STRATEGY = 'fixed-window'
    RATELIMIT_DEFAULT = '100 per minute'
    RATELIMIT_HEADERS_ENABLED = True

    # Caching Configuration
    CACHE_TYPE = os.environ.get('CACHE_TYPE') or 'simple'
    CACHE_DEFAULT_TIMEOUT = int(os.environ.get('CACHE_DEFAULT_TIMEOUT', 300))
    CACHE_REDIS_URL = os.environ.get('CACHE_REDIS_URL') or None

    # Custom Rate Limits
    RATELIMIT_AI_GENERATION = os.environ.get('RATELIMIT_AI_GENERATION') or '5 per minute'
    RATELIMIT_JOB_SEARCH = os.environ.get('RATELIMIT_JOB_SEARCH') or '30 per minute'
    RATELIMIT_CAREER_RECOMMEND = os.environ.get('RATELIMIT_CAREER_RECOMMEND') or '10 per minute'


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    # Use Redis for rate limiting in production when available
    RATELIMIT_STORAGE_URI = os.environ.get('RATELIMIT_STORAGE_URI') or 'memory://'
    CACHE_TYPE = os.environ.get('CACHE_TYPE') or 'simple'


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'TEST_DATABASE_URL',
        'sqlite://'  # in-memory SQLite — no external DB needed
    )
    SQLALCHEMY_ENGINE_OPTIONS = {}  # SQLite doesn't support pool options


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
