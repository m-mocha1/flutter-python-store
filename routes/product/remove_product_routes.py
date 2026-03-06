from flask import Blueprint, redirect, url_for, flash, current_app
from utils.auth import require_login, get_logged_user
from services.product_serviecs.remove_product import remove_Product
from models import User, Product, Cart
from extensions import db

remove_product_bp = Blueprint('remove_product', __name__)

@remove_product_bp.route("/removeProduct/<int:product_id>", methods=["POST"])
@require_login 
def removeProduct(product_id):
    user = get_logged_user()
    ok,message = remove_Product(User,Product,Cart,user.username,product_id,db,current_app.config["UPLOAD_FOLDER"])
    flash(message, "success" if ok else "error")
    return redirect(url_for("home.home"))
