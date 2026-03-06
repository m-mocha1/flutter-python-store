from routes.auth import login_bp, signup_bp, logout_bp
from routes.home import home_bp, profile_bp
from routes.product import product_detail_bp, add_product_bp, remove_product_bp, search_bp
from routes.cart import cart_bp, add_to_cart_bp, remove_from_cart_bp, update_cart_bp

__all__ = [
    # Auth
    'login_bp',
    'signup_bp',
    'logout_bp',
    # Home
    'home_bp',
    'profile_bp',
    # Product
    'product_detail_bp',
    'add_product_bp',
    'remove_product_bp',
    'search_bp',
    # Cart
    'cart_bp',
    'add_to_cart_bp',
    'remove_from_cart_bp',
    'update_cart_bp'
]