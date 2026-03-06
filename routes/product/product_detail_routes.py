from flask import Blueprint, render_template, redirect, url_for, flash
from utils.auth import require_login, get_logged_user
from utils.product import get_product_info, get_other_products
from models import Product
from extensions import db


product_detail_bp = Blueprint('product_detail', __name__)

@product_detail_bp.route("/productPage/<product_id>",methods=["GET","POST"])
@require_login 
def productPage(product_id):
    product = get_product_info(Product,product_id)
    if product is None:
        flash("Product no longer available")
        return redirect(url_for("home.home"))
   
    user = get_logged_user()
    related_products = get_other_products(db, Product, product_id)

    return render_template('productPage.html',
                            username=user.username,
                            product=product,
                            products=related_products,
                            user_id=user._id)