from config import KEY
from services.cart_services.add_to_cart import add_to_cart
from extensions import db
from services.auth_services.login_service import auth_user
from services.auth_services.sign_up_service import create_user
from services.cart_services.update_cart_quantity import update_Cart_Quantity
from services.cart_services.remove_from_cart import remove_From_Cart
from services.product_services.add_product import add_Product
from services.product_services.remove_product import remove_Product

from flask import Flask, render_template, redirect, request, url_for, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
import os
from werkzeug.utils import secure_filename


app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key = KEY
# app.permanent_session_lifetime = timedelta(hours=1)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

UPLOAD_FOLDER = os.path.join(app.root_path, "static", "uploads")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif','webp'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db.init_app(app)

from models.user_model import User
from models.product_model import Product
from models.cart_model import Cart


# These class represents a table in the database
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route("/",methods=["GET", "POST"])
def home():
    if "username" in session:
        user = User.query.filter_by(username=session["username"]).first()
        cartItems = Cart.query.filter_by(user_id = user._id).all()
        cart_product_ids = [item.product_id for item in cartItems]
        products = Product.query.order_by(Product._id.desc()).all()  # no limit
        return render_template("index.html", products=products,username=user.username)
    else:
       return redirect(url_for("login")) 



@app.route("/login",methods=["POST","GET"])
def login():
    if "username" in session:
        return redirect(url_for("home"))

    if request.method == "POST":
    #    session.permanent = True
       username = request.form["username"].strip().lower()
       password = request.form["password"]

       ok,message = auth_user(User,username,password)

       if ok :
          session["username"] = username 
          return render_template("login/login.html") # if error
       
       flash(message,"error")

    return render_template("login/login.html") # if get
       

@app.route("/sign",methods=["POST","GET"])
def sign():
    if "username" in session:
        return redirect(url_for("home"))
    
    if request.method == "POST":
        username = request.form["username"].strip().lower()
        password = request.form["password"]
        description = request.form["description"]
        ok,message = create_user(User,username,password,description,db)

        if ok :
            session["username"] = username
            return redirect(url_for('home'))
        
        flash(message,"error")
        return render_template('login/sign.html')
    
    return render_template('login/sign.html')



@app.route("/logout",methods=["POST"])
def log_out():
    session.pop("username",None)
    return redirect(url_for("login"))
     

    #  ------------------------------------------



@app.route("/profile",methods=["GET","POST"])
def profile():
   if "username" not in session:
        return redirect(url_for("login"))
   
   user = get_username(User, username=session["username"])
   return render_template(
       'profile.html',
        username=user.username,
        description=user.description)


def get_username(User, username):
    return User.query.filter_by(username=username).first()
    
    #  ------------------------------------------




@app.route("/productPage/<product_id>",methods=["GET","POST"])
def productPage(product_id):
    if "username" not in session:
        return redirect(url_for("login"))
    
    product = Product.query.filter_by(_id=product_id).first()
    if not product:
        flash("Product no longer available")
        return redirect(url_for("home"))
   
    user = User.query.filter_by(username=session["username"]).first()
    related_products = Product.query.filter(Product._id != product_id).order_by(db.func.random()).limit(10).all()

    return render_template('productPage.html',
                            username=session["username"],
                            product=product,
                            products=related_products,
                            user_id=user._id)




@app.route("/myCart",methods=["GET","POST"])
def myCart():
    if "username" in session:
        user = User.query.filter_by(username=session["username"]).first()
        cartItems = Cart.query.filter_by(user_id = user._id).all()
        cart_product_ids = [item.product_id for item in cartItems]
        products_not_in_cart = Product.query.filter(~Product._id.in_(cart_product_ids)).order_by(db.func.random()).limit(10).all()
        subtotal = 0
        for item in cartItems:
            if item.product is None:
                continue  
            subtotal += item.product.price * item.quantity
        return render_template('myCart.html', username=session["username"],products=products_not_in_cart,cartItems=cartItems,subtotal=subtotal)
    else:
        return redirect(url_for("login"))
    
    
    #  ------------------------------------------

@app.route('/addToCart/<int:product_id>',methods=["POST"])
def add_to_cart_route(product_id): 
    if "username" not in session:
        return redirect(url_for("login"))
    
    qty_str = request.form.get("quantity", "1")

    try:
        requested_qty = int(qty_str)
    except:
        requested_qty = 1

    if requested_qty < 1: requested_qty = 1

    user = User.query.filter_by(username=session["username"]).first()
     
    ok,message = add_to_cart(db,User, Product, Cart, user._id,product_id, requested_qty) 
    flash(message,"ok" if ok else "error")
    
    if ok :
        return redirect(url_for("myCart"))
    else:
        return redirect(url_for("home"))

    #  ------------------------------------------

@app.route('/removeFromCart/<int:cart_id>', methods=["POST"])
def removeFromCart (cart_id):
    if "username" not in session:
        return redirect(url_for("login"))

    username=session["username"]
    message = remove_From_Cart(User, Cart, username,cart_id,db)
    flash(message)

    return redirect(url_for('myCart'))

    #  ------------------------------------------


@app.route('/updateCartQuantity/<int:cart_id>', methods=["POST"])
def updateCartQuantity(cart_id):
    if "username" not in session:
        return redirect(url_for("login"))
    
    username=session["username"]
    qty = request.form.get('quantity')

    message = update_Cart_Quantity(User, Cart, username, qty, cart_id, db)
    flash(message)    
    return redirect(url_for('myCart'))

    #  ------------------------------------------




@app.route("/addProduct",methods=["POST","GET"])
def addProduct():
    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]
    if request.method == "POST":
       product_name = request.form["product_name"]
       price = float(request.form["price"])
       description = request.form["description"]
       stock = int(request.form["stock"])

       file = request.files.get("image_file")
       if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_url = f"/static/uploads/{filename}"
       else:
            flash("Image is required", "error")
            return render_template('addProduct.html', username=session["username"])

       message = add_Product(db,Product,User,product_name,price,description,stock,username,image_url)
       flash(message)
       
    return redirect(url_for('home'))
    


@app.route("/removeProduct/<int:product_id>", methods=["POST"])
def removeProduct(product_id):
    if "username" not in session:
        return redirect(url_for("login"))
    
    username = session["username"]
    ok,message = remove_Product(User,Product,Cart,username,product_id,db,app.config["UPLOAD_FOLDER"])
    flash(message, "success" if ok else "error")
    return redirect(url_for("home"))




@app.route("/search", methods=["GET"])
def search():
    if "username" not in session:
        return redirect(url_for("login"))
    
    query = request.args.get('q', '').strip()
    
    if query:
        # Search products by name or description
        products = Product.query.filter(
            (Product.product_name.ilike(f'%{query}%')) |
            (Product.description.ilike(f'%{query}%'))
        ).all()
    else:
        products = []
    
    return render_template('search.html', 
                         username=session["username"],
                         products=products,
                         query=query)




@app.errorhandler(404)
def page_not_found(error):
    if "username" in session:
        return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))






if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)