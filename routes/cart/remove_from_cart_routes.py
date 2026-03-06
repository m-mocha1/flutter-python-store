from flask import Blueprint, redirect, url_for, flash
from utils.auth import require_login, get_logged_user
from services.cart_services.remove_from_cart import remove_From_Cart
from models import User, Cart
from extensions import db


remove_from_cart_bp = Blueprint('remove_cart', __name__)

@remove_from_cart_bp.route('/removeFromCart/<int:cart_id>', methods=["POST"])
@require_login 
def removeFromCart (cart_id):
    user= get_logged_user()
    
    message = remove_From_Cart(User, Cart, user.username,cart_id,db)
    flash(message)

    return redirect(url_for('cart.myCart'))