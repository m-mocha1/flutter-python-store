from flask import Blueprint, render_template, request
from utils.auth import require_login, get_logged_user
from models import Product

search_bp = Blueprint('search', __name__)

@search_bp.route("/search", methods=["GET"])
@require_login 
def search():
    query = request.args.get('q', '').strip()
    user = get_logged_user()
    if query:
        # Search products by name or description
        products = Product.query.filter(
            (Product.product_name.ilike(f'%{query}%')) |
            (Product.description.ilike(f'%{query}%'))
        ).all()
    else:
        products = []
    
    return render_template('search.html', 
                         username=user.username,
                         products=products,
                         query=query)