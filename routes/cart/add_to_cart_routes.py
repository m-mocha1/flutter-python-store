from flask import Blueprint, redirect, request, url_for, flash
from utils.auth import require_login, get_logged_user
from services.cart_services import add_to_cart
from models import User, Product, Cart
from extensions import db


add_to_cart_bp = Blueprint('add_cart', __name__)

@add_to_cart_bp.route('/addToCart/<int:product_id>',methods=["POST"])
@require_login 
def add_to_cart_route(product_id): 
    
    qty_str = request.form.get("quantity", "1")
    try:
        requested_qty = int(qty_str)
    except:
        requested_qty = 1

    if requested_qty < 1: requested_qty = 1

    user = get_logged_user()
     
    ok,message = add_to_cart(db,User, Product, Cart, user._id,product_id, requested_qty) 
    flash(message,"ok" if ok else "error")
    
    if ok :
        return redirect(url_for("cart.myCart"))
    else:
        return redirect(url_for("home.home"))