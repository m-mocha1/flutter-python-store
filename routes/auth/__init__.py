# routes/auth/__init__.py
from routes.auth.login_routes import login_bp
from routes.auth.signup_routes import signup_bp
from routes.auth.logout_routes import logout_bp

__all__ = ['login_bp', 'signup_bp', 'logout_bp']