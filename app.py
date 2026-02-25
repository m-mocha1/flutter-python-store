from config import KEY
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

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif','webp'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)


# These class represents a table in the database
class User(db.Model):
    _id  = db.Column("id",db.Integer, primary_key=True)
    username = db.Column(db.String(30),nullable=False, unique = True)
    description = db.Column(db.String(30),nullable=False, unique = False)
    password= db.Column(db.String(200), nullable=False)

    def __init__(self, username, password, description):
        self.username = username
        self.password = password
        self.description = description

class Product(db.Model):
    _id  = db.Column("id",db.Integer, primary_key=True)
    product_name = db.Column(db.String(50),nullable=False)
    price = db.Column(db.Float, nullable = False)
    image_url = db.Column(db.String(500),nullable=False)
    description = db.Column(db.String(500), nullable=False)
    stock = db.Column(db.Integer, default=1)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, product_name, price, image_url, description, stock,user_id):
        self.product_name = product_name
        self.price = price
        self.image_url = image_url
        self.description = description
        self.stock = stock
        self.user_id = user_id

    @validates('stock')
    def validate_stock(self,key,value):
        if value <= 0:
            raise ValueError("Stock cannot be neg")
        return value

    def is_in_stock(self):
        return self.stock > 0 

    def can_add(self,quantity):
        return self.stock >= quantity

    def reduce_stock(self, amount):
        if not self.can_add(amount):
            raise ValueError(f"Only {self.stock} left in stock")
        self.stock -= amount
            
class Cart(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, default=1)
    product = db.relationship("Product")
    user = db.relationship("User")

    def __init__(self,user_id,product_id,quantity=1):
      self.user_id = user_id
      self.product_id = product_id
      self.quantity = quantity

    @validates('quantity')
    def validateQuantity(self,key,value):
      if value <= 0:
          raise ValueError("quantity must be at least 1")
      product = Product.query.filter_by(_id=self.product_id).first()
      if product and value > product.stock:
          raise ValueError(f"only{product.stock} left")
      return value
    

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

       user = User.query.filter_by(username=username).first()

       if user and check_password_hash(user.password, password):
            session["username"] = username
            return redirect(url_for("home"))
       else:
            flash("username or password is wrong")
            return render_template('login/login.html')

    else:
        return render_template('login/login.html')



@app.route("/sign",methods=["POST","GET"])
def sign():
    if "username" in session:
        return redirect(url_for("home"))
    
    if request.method == "POST":
        username = request.form["username"].strip().lower()
        password = request.form["password"]
        description = request.form["description"]
        try:
            hashed_pass = generate_password_hash(password=password, method='pbkdf2:sha256')
            new_user = User(username=username,password=hashed_pass,description=description)
            db.session.add(new_user)
            db.session.commit()
            session["username"] = username
            # session.permanent = True
            return redirect(url_for("home"))
        except IntegrityError:
            db.session.rollback()
            flash("username already exists!")
            return render_template('login/sign.html')

    else:
        return render_template('login/sign.html')



@app.route("/logout",methods=["POST"])
def log_out():
    session.pop("username",None)
    return redirect(url_for("login"))
     

@app.route("/profile",methods=["GET","POST"])
def profile():
    if "username" in session:
        user = User.query.filter_by(username=session["username"]).first()
        return render_template('profile.html', username=user.username, description=user.description)
    else: 
        return redirect(url_for("login"))
            




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
    
    

@app.route('/addToCart/<int:product_id>',methods=["POST"])
def addToCart(product_id):
    if "username" not in session:
        return redirect(url_for("login"))
    
    user = User.query.filter_by(username=session["username"]).first()
    product = Product.query.filter_by(_id = product_id).first()
    
    if not product:
        flash("Product not found", "error")
        return redirect(url_for("home"))
    
    if not product.is_in_stock():
        flash("this product out of stock")    
        return redirect(url_for('productPage',product_id=product_id))
    
    # get requested quantity (from product page form or default 1)
    try:
        requested_qty = int(request.form.get("quantity", 1))
    except ValueError:
        requested_qty = 1

    if requested_qty <= 0:
        flash("Quantity must be at least 1", "error")
        return redirect(url_for('productPage', product_id=product_id))

    existing = Cart.query.filter_by(user_id = user._id,product_id = product_id).first()

    try:
        if existing:
            new_total = existing.quantity + requested_qty
            if not product.can_add(new_total):
                flash(f"only {product.stock} left in stock")
                return redirect(url_for("myCart"))
            existing.quantity = new_total
        else:
            if not product.can_add(requested_qty):
                flash(f"only {product.stock} left in stock")
                return redirect(url_for("productPage", product_id=product_id))
            newCartItem = Cart(user_id=user._id,product_id=product_id,quantity=requested_qty)
            db.session.add(newCartItem)
        
        db.session.commit()
        flash("item added to cart", "success")   
        return redirect(url_for('myCart'))
    except ValueError as e:
        flash(str(e),"error")
        return redirect(url_for("myCart"))



@app.route('/removeFromCart/<int:cart_id>', methods=["POST"])
def removeFromCart(cart_id):
    if "username" not in session:
        return redirect(url_for("login"))
    
    user = User.query.filter_by(username=session["username"]).first()
    cart_item = Cart.query.filter_by(_id=cart_id, user_id=user._id).first()
    
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        flash("Item removed from cart!", "success")
    else:
        flash("Item not found!", "error")
    
    return redirect(url_for('myCart'))


@app.route('/updateCartQuantity/<int:cart_id>', methods=["POST"])
def updateCartQuantity(cart_id):
    if "username" not in session:
        return redirect(url_for("login"))
    
    user = User.query.filter_by(username=session["username"]).first()
    cart_item = Cart.query.filter_by(_id=cart_id, user_id=user._id).first()
    quantity = request.form.get('quantity')
    

    try:
        if cart_item and quantity:
            cart_item.quantity = int(quantity)
            db.session.commit()
            flash("Quantity updated!", "success")
        else:
            flash("Error updating quantity!", "error")
    except ValueError as e:
        flash(str(e),"error")            
        
    return redirect(url_for('myCart'))




@app.route("/addProduct",methods=["POST","GET"])
def addProduct():
    if "username" not in session:
        return redirect(url_for("login"))

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

       user = User.query.filter_by(username=session["username"]).first()

       try:
           new_Product = Product(
               product_name=product_name,
               price=price,
               image_url=image_url,
               description=description,
               stock=stock,          
               user_id=user._id
           )
           db.session.add(new_Product)
           db.session.commit()
           flash("your last product has been added successfully!", "success")
       except ValueError as e:
           db.session.rollback()
           flash(str(e), "error")

    return render_template('addProduct.html', username=session["username"])
    


@app.route("/removeProduct/<int:product_id>", methods=["POST"])
def removeProduct(product_id):
    if "username" not in session:
        return redirect(url_for("login"))
    user = User.query.filter_by(username=session["username"]).first()
    product = Product.query.filter_by(_id=product_id).first()
    if product and product.user_id == user._id:
        delete_image_file(product.image_url)
        
        Cart.query.filter_by(product_id=product._id).delete()

        db.session.delete(product)
        db.session.commit()
        flash("Product removed successfully!", "success")
    else:
        flash("You can only remove products you added.", "error")
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



def delete_image_file(image_url: str):
    """Delete image file from disk given its URL like /static/uploads/filename.jpg"""
    if not image_url:
        return
    try:
        # we only handle files under /static/uploads/
        prefix = "/static/uploads/"
        if not image_url.startswith(prefix):
            return
        filename = image_url[len(prefix):]
        file_path = os.path.join(app.root_path, "static", "uploads", filename)
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        # optional: log error instead of crashing
        print(f"Error deleting file {image_url}: {e}")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)