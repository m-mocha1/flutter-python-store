from config import KEY
from services.cart_services.add_to_cart import add_to_cart
from extensions import db
from services.auth_services.login_service import auth_user
from services.auth_services.sign_up_service import create_user
from services.cart_services.update_cart_quantity import update_Cart_Quantity
from services.cart_services.remove_from_cart import remove_From_Cart
from services.product_services.add_product import add_Product,save_product_image
from services.product_services.remove_product import remove_Product
from utils.auth import require_login,require_logout,login_user,logout_user,get_user_by_username,load_logged_in_user,get_logged_user
from utils.cart import get_user_cart_products_id,get_products_not_in_cart,get_user_cart,sub_total
from utils.product import get_all_products,get_product_info,get_other_products

from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
from flask import Flask, g, session


app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key = KEY
# app.permanent_session_lifetime = timedelta(hours=1)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

UPLOAD_FOLDER = os.path.join(app.root_path, "static", "uploads")

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db.init_app(app)

from models.user_model import User
from models.product_model import Product
from models.cart_model import Cart


# -------------------------------------------------------------
# These class represents a table in the database

# -------------------------------------------------------------

app.before_request(load_logged_in_user)

# -------------------------------------------------------------
@app.route("/",methods=["GET", "POST"])
@require_login 
def home():
   cart_product_ids = get_user_cart_product_ids(Cart)
   products = get_all_products(Product)

   return render_template(
        "index.html", 
        products=products,
        username=g.user.username,
        cart_product_ids=cart_product_ids  # for product page
    )
# -------------------------------------------------------------


# -------------------------------------------------------------
@app.route("/login",methods=["POST","GET"])
@require_logout
def login():
    if request.method == "POST":
       username = request.form["username"].strip().lower()
       password = request.form["password"]

       ok,message = auth_user(User,username,password)

       if ok :
          login_user(username) 
          return render_template("login/login.html") # if error
       
       flash(message,"error")

    return render_template("login/login.html") # if GET
# -------------------------------------------------------------
       

# -------------------------------------------------------------

@app.route("/sign",methods=["POST","GET"])
@require_logout
def sign():
    if request.method == "POST":
        username = request.form["username"].strip().lower()
        password = request.form["password"]
        description = request.form["description"]
        ok,message = create_user(User,username,password,description,db)

        if ok :
            login_user(username)
            return redirect(url_for('home'))
        
        flash(message,"error")
        return render_template('login/sign.html')
    
    return render_template('login/sign.html')
# -------------------------------------------------------------


# -------------------------------------------------------------
@app.route("/logout",methods=["POST"])
@require_login 
def log_out():
    logout_user()
    return redirect(url_for("login"))    
# -------------------------------------------------------------



# -------------------------------------------------------------
@app.route("/profile",methods=["GET","POST"])
@require_login 
def profile():

  user = get_logged_user()
  return render_template(
  'profile.html',
   username=user.username,
   description=user.description)
# -------------------------------------------------------------





@app.route("/productPage/<product_id>",methods=["GET","POST"])
@require_login 
def productPage(product_id):
    product = get_product_info(Product,product_id)
    if product is None:
        flash("Product no longer available")
        return redirect(url_for("home"))
   
    user = get_logged_user()
    related_products = get_other_products(db, Product, product_id)

    return render_template('productPage.html',
                            username=user.username,
                            product=product,
                            products=related_products,
                            user_id=user._id)




@app.route("/myCart",methods=["GET","POST"])
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

    #  ------------------------------------------

@app.route('/addToCart/<int:product_id>',methods=["POST"])
@require_login 
def add_to_cart_route(product_id): 
    if "username" not in session:
        return redirect(url_for("login"))
    
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
        return redirect(url_for("myCart"))
    else:
        return redirect(url_for("home"))

    #  ------------------------------------------

@app.route('/removeFromCart/<int:cart_id>', methods=["POST"])
@require_login 
def removeFromCart (cart_id):
    user= get_logged_user()
    
    message = remove_From_Cart(User, Cart, user.username,cart_id,db)
    flash(message)

    return redirect(url_for('myCart'))

    #  ------------------------------------------


@app.route('/updateCartQuantity/<int:cart_id>', methods=["POST"])
@require_login 
def updateCartQuantity(cart_id):
    user = get_logged_user()
    qty = request.form.get('quantity')

    message = update_Cart_Quantity(User, Cart, user.username, qty, cart_id, db)
    flash(message)    
    return redirect(url_for('myCart'))

    #  ------------------------------------------




@app.route("/addProduct",methods=["POST","GET"])
@require_login 
def addProduct():
    if request.method == "POST":
       user = get_logged_user()

       product_name = request.form["product_name"]
       price = float(request.form["price"])
       description = request.form["description"]
       stock = int(request.form["stock"])

       file = request.files.get("image_file")
       upload_folder = app.config['UPLOAD_FOLDER']
    
       ok,result = save_product_image(file, upload_folder)
       if not ok :
           return render_template('addProduct.html', username=user.username) #error
       image_url = result

       ok,message = add_Product(db,Product,User,product_name,price,description,stock,user,image_url)

       if ok :   
        flash(message,"success")
        return redirect(url_for('home'))
       else:
           flash(message, "error")
           return render_template('addProduct.html', username=user.username)
    
    user = get_logged_user()
    return render_template('addProduct.html', username=user.username)


@app.route("/removeProduct/<int:product_id>", methods=["POST"])
@require_login 
def removeProduct(product_id):
    if "username" not in session:
        return redirect(url_for("login"))
    
    username = session["username"]
    ok,message = remove_Product(User,Product,Cart,username,product_id,db,app.config["UPLOAD_FOLDER"])
    flash(message, "success" if ok else "error")
    return redirect(url_for("home"))




@app.route("/search", methods=["GET"])
@require_login 
def search():
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