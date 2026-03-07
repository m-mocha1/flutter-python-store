from flask import Blueprint, redirect, request, url_for, flash
from utils.auth import require_login, get_logged_user
from services import update_Cart_Quantity
from models import User, Cart
from extensions import db


update_cart_bp = Blueprint('update_cart',__name__)


@update_cart_bp.route('/updateCartQuantity/<int:cart_id>', methods=["POST"])
@require_login 
def updateCartQuantity(cart_id):
    user = get_logged_user()
    qty = request.form.get('quantity')

    message = update_Cart_Quantity(User, Cart, user.username, qty, cart_id, db)
    flash(message)    
    return redirect(url_for('cart.myCart'))