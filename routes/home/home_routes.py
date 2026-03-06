from flask import Blueprint, render_template, g
from utils import require_login, get_all_products
from models import Product

home_bp = Blueprint('home', __name__)

@home_bp.route("/",methods=["GET", "POST"])
@require_login 
def home():
   products = get_all_products(Product)
#    cart_product_ids = get_user_cart_product_ids(Cart)

   return render_template(
        "index.html", 
        products=products,
        username=g.user.username,
        # cart_product_ids=cart_product_ids  # for product page
    )