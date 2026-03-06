from routes.product.product_detail_routes import product_detail_bp
from routes.product.add_product_routes import add_product_bp
from routes.product.remove_product_routes import remove_product_bp
from routes.product.search_routes import search_bp

__all__ = ['product_detail_bp', 'add_product_bp', 'remove_product_bp', 'search_bp']