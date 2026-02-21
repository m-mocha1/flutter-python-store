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
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)


# These class represents a table in the database
class users(db.Model):
    _id  = db.Column("id",db.Integer, primary_key=True)
    username = db.Column(db.String(30),nullable=False, unique = True)
    description = db.Column(db.String(30),nullable=False, unique = False)
    password= db.Column(db.String(20), nullable=False)

    def __init__(self, username, password, description):
        self.username = username
        self.password = password
        self.description = description

class proudcts(db.Model):
    _id  = db.Column("id",db.Integer, primary_key=True)
    product_name = db.Column(db.String(50),nullable=False)
    price = db.Column(db.Float, nullable = False)
    image_url = db.Column(db.String(500),nullable=False)
    description = db.Column(db.String(500), nullable=False)
    stock = db.Column(db.Integer, default=1)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, product_name, price, image_url, description, stock,user_id):
        self.product_name = product_name
        self.price = price
        self.image_url = image_url
        self.description = description
        self.stock = stock
        self.user_id = user_id

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route("/")
def home():
    if "username" in session:
        all_products = proudcts.query.order_by(db.func.random()).limit(10).all()
        return render_template('index.html', username=session["username"], products=all_products)
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

       user = users.query.filter_by(username=username).first()

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
            new_user = users(username=username,password=hashed_pass,description=description)
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
        user = users.query.filter_by(username=session["username"]).first()
        return render_template('profile.html', username=user.username, description=user.description)
    else: 
        return redirect(url_for("login"))
            




@app.route("/productPage/<product_id>",methods=["GET","POST"])
def productPage(product_id):
    if "username" not in session:
        return redirect(url_for("login"))
    
    product = proudcts.query.filter_by(_id=product_id).first()
    if not product:
        flash("Proudct no longer available")
        return redirect(url_for("home"))
   
    user = users.query.filter_by(username=session["username"]).first()
    related_products = proudcts.query.filter(proudcts._id != product_id).order_by(db.func.random()).limit(10).all()

    return render_template('productPage.html',
                            username=session["username"],
                            product=product,
                            related_products=related_products,
                            user_id=user._id)




@app.route("/myCart",methods=["GET","POST"])
def myCart():
    if "username" in session:
        all_products = proudcts.query.all()
        return render_template('myCart.html', username=session["username"],products=all_products)
    else:
        return redirect(url_for("login"))
    



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

       user = users.query.filter_by(username=session["username"]).first()
       new_proudct = proudcts(
           product_name=product_name,
           price=price,
           image_url=image_url,
           description=description,
           stock=stock,
           user_id=user._id)
       
       db.session.add(new_proudct)
       db.session.commit()
       flash("your last product has been added successfully!", "success")
    return render_template('addProudct.html', username=session["username"])
    



@app.route("/removeProduct/<int:product_id>", methods=["POST"])
def removeProduct(product_id):
    if "username" not in session:
        return redirect(url_for("login"))
    user = users.query.filter_by(username=session["username"]).first()
    product = proudcts.query.filter_by(_id=product_id).first()
    if product and product.user_id == user._id:
        db.session.delete(product)
        db.session.commit()
        flash("Product removed successfully!", "success")
    else:
        flash("You can only remove products you added.", "error")
    return redirect(url_for("home"))




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