# Import views
from app.views.auth_views import auth_bp
from app.views.user_views import user_bp

__all__ = ['auth_bp', 'user_bp']
