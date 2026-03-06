# app.py
from config import KEY
from extensions import db
from flask import Flask, g
import os

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key = KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

UPLOAD_FOLDER = os.path.join(app.root_path, "static", "uploads")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db.init_app(app)

# Import models
from models import User, Product, Cart

# Import auth
from utils import load_logged_in_user

@app.before_request
def before_request():
    load_logged_in_user(User)

@app.errorhandler(404)
def page_not_found(error):
    from flask import redirect, url_for
    if g.user:
        return redirect(url_for("home.home"))
    else:
        return redirect(url_for("login.login"))

# Import and register blueprints
from routes import (
    login_bp,
    signup_bp,
    logout_bp,

    home_bp,
    profile_bp,

    product_detail_bp,
    add_product_bp,
    remove_product_bp,
    search_bp,

    cart_bp,
    add_to_cart_bp,
    remove_from_cart_bp,
    update_cart_bp
)

blueprints = [
    login_bp, signup_bp, logout_bp,
    home_bp, profile_bp,
    product_detail_bp, add_product_bp, remove_product_bp, search_bp,
    cart_bp, add_to_cart_bp, remove_from_cart_bp, update_cart_bp
]

for blueprint in blueprints:
    app.register_blueprint(blueprint)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)