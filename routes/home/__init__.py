# routes/home/__init__.py
from routes.home.home_routes import home_bp
from routes.home.profile_routes import profile_bp

__all__ = ['home_bp', 'profile_bp']