from flask import Blueprint, render_template
from utils.auth import require_login, get_logged_user
from utils.cart import get_user_cart, get_user_cart_products_id, get_products_not_in_cart, sub_total
from models import Cart, Product
from extensions import db

cart_bp = Blueprint('cart', __name__)

@cart_bp.route("/myCart",methods=["GET","POST"])
@require_login 
def myCart():
        
        user =get_logged_user()
        cartItems = get_user_cart(Cart)
        cart_product_ids = get_user_cart_products_id(Cart)
        products_not_in_cart = get_products_not_in_cart(Product,cart_product_ids,db)
        subtotal = sub_total(cartItems)
        

        return render_template('myCart.html',
                                username=user.username,
                                products=products_not_in_cart,
                                cartItems=cartItems,
                                subtotal=subtotal)