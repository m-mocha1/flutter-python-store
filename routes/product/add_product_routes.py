from flask import Blueprint, render_template, redirect, request, url_for, flash, current_app
from utils.auth import require_login, get_logged_user
from services.product_serviecs import add_Product, save_product_image
from models.product_model import Product
from models.user_model import User
from extensions import db

add_product_bp = Blueprint('add_product', __name__)

@add_product_bp.route("/addProduct", methods=["POST", "GET"])
@require_login 
def addProduct():
    if request.method == "POST":
        user = get_logged_user()

        product_name = request.form["product_name"].strip()
        price = float(request.form["price"])
        description = request.form["description"].strip()
        stock = int(request.form["stock"])

        file = request.files.get("image_file")
        upload_folder = current_app.config['UPLOAD_FOLDER']
    
        ok, result = save_product_image(file, upload_folder)
        if not ok:
            flash("Failed to save image", "error")
            return render_template('addProduct.html', username=user.username)
        image_url = result

        ok, message = add_Product(db, Product, product_name, price, description, stock, user, image_url)

        if ok:   
            flash(message, "success")
            return redirect(url_for('home.home'))
        else:
            flash(message, "error")
            return render_template('addProduct.html', username=user.username)
    
    user = get_logged_user()
    return render_template('addProduct.html', username=user.username)