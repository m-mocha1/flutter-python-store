# Flask E-Commerce Application - SOLID Principles Refactoring Guide

## 📚 Table of Contents
1. [Project Overview](#project-overview)
2. [SOLID Principles](#solid-principles)
3. [Project Architecture](#project-architecture)
4. [Key Concepts Learned](#key-concepts-learned)
5. [File Structure](#file-structure)
6. [Setup & Installation](#setup--installation)
7. [Key Features](#key-features)
8. [Code Examples](#code-examples)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)

---

## Project Overview

This is a **Flask-based E-Commerce Application** refactored using **SOLID design principles**. The project demonstrates professional-grade code organization, separation of concerns, and clean architecture patterns.

### What This Project Does
- User authentication (login, signup, logout)
- Product management (add, view, remove products)
- Shopping cart functionality (add, remove, update items)
- Product search
- User profiles

### Technologies Used
- **Backend:** Flask, SQLAlchemy
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript
- **Security:** Werkzeug password hashing

---

## SOLID Principles

SOLID is a set of 5 design principles that make code clean, maintainable, and scalable.

### S - Single Responsibility Principle
**Each class/function should have ONE reason to change and do ONE thing.**

**Bad Example:**
```python
def handle_user(username, password, email):
    # Authenticates, saves to database, AND sends email
    authenticate_user(username, password)
    save_user(username, email)
    send_email(email)
```

**Good Example:**
```python
# Three separate functions
def auth_user(username, password):
    # Only handles authentication
    pass

def create_user(username, password, email):
    # Only handles user creation
    pass

def send_email(email):
    # Only handles email sending
    pass
```

**In This Project:**
- `routes/` = Handle HTTP requests
- `services/` = Business logic
- `utils/` = Helper functions
- `models/` = Database definitions

---

### O - Open/Closed Principle
**Classes should be OPEN for extension but CLOSED for modification.**

**Meaning:** Add new features WITHOUT changing existing code.

**In This Project:**
- Add new routes in separate files without modifying existing routes
- Add new utils without changing existing code

---

### L - Liskov Substitution Principle
**Derived classes must be substitutable for their base classes.**

**Meaning:** Child classes should work the same way as parent classes.

**In This Project:**
- All models inherit from `db.Model` consistently
- All blueprints follow the same pattern
- Relationships work the same way across all models

---

### I - Interface Segregation Principle
**Clients should not depend on interfaces they don't use.**

**In This Project:**
- `utils/auth.py` = Only auth functions
- `utils/product.py` = Only product functions
- `utils/cart.py` = Only cart functions
- Each module has a single, clear purpose

---

### D - Dependency Inversion Principle
**High-level modules should not depend on low-level modules. Both should depend on abstractions.**

**Bad Example:**
```python
@app.route('/home')
def home():
    # Routes directly query database
    products = Product.query.all()
    return render_template('home.html', products=products)
```

**Good Example:**
```python
@app.route('/home')
def home():
    # Routes use utility functions (abstraction)
    products = get_all_products(Product)
    return render_template('home.html', products=products)
```

**In This Project:**
- Routes depend on `utils/` functions, not direct database queries
- Services handle business logic
- Routes stay clean and focused on HTTP handling

---

## Project Architecture

### Folder Structure
```
project/
├── app.py                          # Main Flask app
├── config.py                       # Configuration
├── extensions.py                   # Database initialization
│
├── models/
│   ├── __init__.py                # Import all models
│   ├── user_model.py              # User database model
│   ├── product_model.py           # Product database model
│   └── cart_model.py              # Cart database model
│
├── routes/
│   ├── __init__.py                # Import all blueprints
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── login_routes.py        # Login endpoint
│   │   ├── signup_routes.py       # Signup endpoint
│   │   └── logout_routes.py       # Logout endpoint
│   ├── home/
│   │   ├── __init__.py
│   │   ├── home_routes.py         # Home page
│   │   └── profile_routes.py      # User profile
│   ├── product/
│   │   ├── __init__.py
│   │   ├── product_detail_routes.py    # View product
│   │   ├── add_product_routes.py       # Add product
│   │   ├── remove_product_routes.py    # Delete product
│   │   └── search_routes.py            # Search products
│   └── cart/
│       ├── __init__.py
│       ├── cart_routes.py              # View cart
│       ├── add_to_cart_routes.py       # Add to cart
│       ├── remove_from_cart_routes.py  # Remove from cart
│       └── update_cart_routes.py       # Update quantity
│
├── utils/
│   ├── __init__.py                # Import all utilities
│   ├── auth.py                    # Authentication helpers
│   ├── product.py                 # Product helpers
│   └── cart.py                    # Cart helpers
│
├── services/
│   ├── __init__.py
│   ├── auth_services/
│   │   ├── __init__.py
│   │   ├── login_service.py       # Login business logic
│   │   └── sign_up_service.py     # Signup business logic
│   ├── cart_services/
│   │   ├── __init__.py
│   │   ├── add_to_cart.py
│   │   ├── remove_from_cart.py
│   │   └── update_cart_quantity.py
│   └── product_serviecs/
│       ├── __init__.py
│       ├── add_product.py
│       └── remove_product.py
│
├── templates/
│   ├── index.html                 # Home page
│   ├── base.html                  # Base template
│   ├── login/
│   │   ├── login.html
│   │   └── sign.html
│   ├── profile.html
│   ├── productPage.html
│   ├── myCart.html
│   └── search.html
│
├── static/
│   ├── css/                       # Stylesheets
│   ├── js/                        # JavaScript
│   └── uploads/                   # User uploaded images
│
└── README.md                       # This file
```

### Architecture Flow
```
User Request
    ↓
routes/ (HTTP handlers)
    ↓
utils/ (Get/process data)
    ↓
services/ (Business logic)
    ↓
models/ (Database)
    ↓
Database
```

---

## Key Concepts Learned

### 1. __init__.py Pattern
**Purpose:** Makes folders into Python packages and defines what can be imported.

**Without __init__.py:**
```python
# This doesn't work
from models import User
```

**With __init__.py:**
```python
# models/__init__.py
from models.user_model import User
from models.product_model import Product
from models.cart_model import Cart

__all__ = ['User', 'Product', 'Cart']

# Now this works!
from models import User, Product, Cart
```

**Benefits:**
- Clean imports
- Centralized exports
- Easy to refactor
- Professional structure

---

### 2. Flask Blueprints
**Purpose:** Organize routes into groups.

**Basic Blueprint:**
```python
# routes/auth/login_routes.py
from flask import Blueprint

login_bp = Blueprint('login', __name__)

@login_bp.route("/login", methods=["POST", "GET"])
def login():
    return render_template("login/login.html")
```

**Using url_for():**
```html
<!-- In templates -->
<a href="{{ url_for('login.login') }}">Login</a>
<!-- Blueprint name: 'login', Function name: 'login' -->
```

**Format: `"blueprint_name.function_name"`**

| Blueprint | Function | url_for() |
|-----------|----------|-----------|
| `login_bp` | `login()` | `"login.login"` |
| `home_bp` | `home()` | `"home.home"` |
| `cart_bp` | `my_cart()` | `"cart.my_cart"` |
| `add_product_bp` | `add_product()` | `"add_product.add_product"` |

---

### 3. Flask's g Object
**Purpose:** Store request-specific data (like logged-in user).

**How It Works:**
```python
# In app.py
@app.before_request
def before_request():
    g.user = None
    if "username" in session:
        g.user = User.query.filter_by(username=session["username"]).first()

# Now g.user is available in ALL routes without importing
@app.route('/home')
def home():
    username = g.user.username  # No import needed!
    return render_template('home.html', username=username)
```

**Key Points:**
- `g` is request-specific (new for each request)
- Automatically destroyed after request
- Perfect for storing current user
- Loaded in `@app.before_request` hook

---

### 4. Decorators for Code Reuse
**Purpose:** Add functionality without repeating code.

**Example - @require_login:**
```python
# Instead of checking in every route:
@app.route('/profile')
def profile():
    if g.user is None:
        return redirect(url_for('login.login'))
    # ... rest of code

# Use decorator:
@require_login
def profile():
    # Already checked! g.user guaranteed to exist
    return render_template('profile.html')
```

**How it works:**
```python
from functools import wraps

def require_login(f):  # f is the func being decorated
    @wraps(f) # keep the original func name 
    def decorated_function(*args, **kwargs): # capture any args passed to route
        if g.user is None: 
            return redirect(url_for("login.login")) #the check start before running the func (if None) redirect
        return f(*args, **kwargs) # if logged in we run the original route 
    return decorated_function # return the original func
    
```

---

### 5. Separation of Concerns
**Routes are for HTTP handling, not business logic.**

**Bad:**
```python
# Route doing too much
@app.route('/addProduct', methods=["POST"])
def addProduct():
    user = User.query.filter_by(username=session["username"]).first()
    product_name = request.form["product_name"]
    price = float(request.form["price"])
    
    # File handling
    file = request.files.get("image_file")
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    # Database operation
    new_product = Product(
        product_name=product_name,
        price=price,
        user_id=user._id
    )
    db.session.add(new_product)
    db.session.commit()
    
    return redirect(url_for('home'))
```

**Good:**
```python
# Route is simple and clean
@app.route("/addProduct", methods=["POST", "GET"])
@require_login
def add_product():
    user = get_logged_user()
    
    if request.method == "POST":
        product_name = request.form["product_name"].strip()
        price = float(request.form["price"].strip())
        description = request.form["description"].strip()
        stock = int(request.form["stock"].strip())
        
        file = request.files.get("image_file")
        ok, result = save_product_image(file, app.config['UPLOAD_FOLDER'])
        
        if not ok:
            flash(result, "error")
            return render_template('addProduct.html', username=user.username)
        
        image_url = result
        ok, message = add_Product(db, Product, User, product_name, price, description, stock, user, image_url)
        
        if ok:
            flash(message, "success")
            return redirect(url_for('home.home'))
        else:
            flash(message, "error")
    
    return render_template('addProduct.html', username=user.username)
```

**Benefits:**
- Routes are readable
- Easy to test
- Reusable functions
- Easy to modify logic

---

## Key Features

### Authentication
- User registration with password hashing
- Login with session management
- Logout functionality
- Protected routes with @require_login decorator

### Product Management
- Add products with image upload
- View product details
- Delete products
- Search products
- Track inventory/stock

### Shopping Cart
- Add items to cart
- Remove items from cart
- Update quantities
- Calculate subtotal
- View cart items

### User Profiles
- View user information
- View user's listings
- User-specific data isolation

---

## Code Examples

### 1. Clean Route Example
```python
# routes/home/home_routes.py
from flask import Blueprint, render_template, g
from utils import require_login, get_all_products
from models import Product

home_bp = Blueprint('home', __name__)

@home_bp.route("/", methods=["GET", "POST"])
@require_login
def home():
    """Display home page with all products"""
    products = get_all_products(Product)
    return render_template(
        "index.html",
        products=products,
        username=g.user.username
    )
```

**Why it's good:**
- Uses @require_login decorator
- Uses utility function get_all_products()
- Uses g.user instead of session query
- Simple and readable

---

### 2. Utility Function Example
```python
# utils/auth.py
from functools import wraps
from flask import g, redirect, url_for, session

def load_logged_in_user(User):
    """Load user into g.user before each request"""
    g.user = None
    if "username" in session:
        g.user = User.query.filter_by(username=session["username"]).first()

def get_logged_user():
    """Get current logged-in user"""
    return g.user

def require_login(f):
    """Decorator to require user to be logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("login.login"))
        return f(*args, **kwargs)
    return decorated_function
```

**Why it's good:**
- Centralized authentication logic
- Reusable across all routes
- DRY principle (Don't Repeat Yourself)
- Easy to test

---

### 3. Model Example
```python
# models/user_model.py
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    
    _id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(500), default="")
    
    # Relationships
    products = db.relationship("Product", backref="owner", cascade="all, delete-orphan")
    cart_items = db.relationship("Cart", backref="user", cascade="all, delete-orphan")
    
    def set_password(self, password):
        """Hash password before storing"""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f'<User {self.username}>'
```

**Why it's good:**
- Password is hashed (security!)
- Relationships defined clearly
- Helper methods for common tasks
- Easy to understand

---

## Best Practices

### ✅ DO:

1. **Use utilities for repeated code**
```python
# Good - use utility
@app.route('/profile')
def profile():
    user = get_logged_user()
    return render_template('profile.html', user=user)
```

2. **Use decorators for repeated checks**
```python
# Good - use decorator
@require_login
def protected_route():
    pass
```

3. **Organize by responsibility**
```
models/ = Database
routes/ = HTTP
utils/ = Helpers
services/ = Business logic
```

4. **Keep routes simple**
```python
# Good - route is simple
@app.route('/add')
@require_login
def add_item():
    ok, msg = add_to_database(data)
    flash(msg)
    return redirect(url_for('home.home'))
```

5. **Use g.user instead of session queries**
```python
# Good
user = g.user

# Bad
user = User.query.filter_by(username=session["username"]).first()
```

### ❌ DON'T:

1. **Don't repeat code**
```python
# Bad - repeated in multiple routes
if g.user is None:
    return redirect(url_for('login'))
```

2. **Don't put business logic in routes**
```python
# Bad
@app.route('/process')
def process():
    # Don't do heavy logic here
    for i in range(1000000):
        # Complex calculations
        pass
```

3. **Don't mix concerns**
```python
# Bad - file handling in database function
def add_product():
    # Handle file upload
    # Save to database
    # Send email
```

4. **Don't use plaintext passwords**
```python
# Bad
user.password = password  # Store plaintext!

# Good
user.set_password(password)  # Hash it!
```

5. **Don't import from deep paths**
```python
# Bad
from routes.cart.add_to_cart_routes import add_to_cart_bp

# Good
from routes import add_to_cart_bp
```

---

## Setup & Installation

### 1. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install flask flask-sqlalchemy werkzeug
```

### 3. Create Database
```python
# In Python shell
from app import app, db
with app.app_context():
    db.create_all()
```

### 4. Run Application
```bash
python app.py
```

---

## Common Mistakes & Fixes

### ❌ Error: ImportError: cannot import name 'X'
**Cause:** Missing `__init__.py` or wrong import path

**Fix:**
```python
# Make sure each folder has __init__.py
# Use from imports/__init__.py instead of deep paths
from models import User  # ✅
from models.user_model import User  # ❌ (unless necessary)
```

### ❌ Error: circular import
**Cause:** Module A imports B, B imports A

**Fix:**
```python
# Bad - circular
# utils/auth.py imports from services
# services imports from utils/auth

# Good - remove unnecessary imports
# Use g.user directly instead of importing get_logged_user
```

### ❌ Error: g.user is None in route
**Cause:** @app.before_request not loading user

**Fix:**
```python
# Make sure in app.py:
@app.before_request
def before_request():
    from models import User
    from utils import load_logged_in_user
    load_logged_in_user(User)  # This must run!
```

### ❌ Error: Foreign key constraint fails
**Cause:** Foreign key column names don't match

**Fix:**
```python
# Make sure table names and columns match exactly:
user_id = db.Column(db.Integer, db.ForeignKey('users._id'), nullable=False)
                                               ↑ table name
                                                    ↑ column name (must exist in users table)
```

---

## What You've Learned

### Design Principles
✅ SOLID principles
✅ Separation of concerns
✅ DRY (Don't Repeat Yourself)
✅ Single Responsibility Principle

### Python/Flask Concepts
✅ Blueprints for route organization
✅ Decorators for code reuse
✅ Flask's g object for request data
✅ SQLAlchemy ORM and relationships

### Project Structure
✅ Organizing code by responsibility
✅ Using __init__.py for clean imports
✅ Creating reusable utility functions
✅ Separating business logic from routes

### Best Practices
✅ Password hashing with werkzeug
✅ Clean architecture patterns
✅ Error handling and validation
✅ Professional code organization

---

## Next Steps

1. **Add more features:**
   - Order history
   - Payment processing
   - Email notifications
   - Admin panel

2. **Improve security:**
   - Add CSRF protection
   - Rate limiting
   - Input validation
   - SQL injection prevention

3. **Scale the application:**
   - Use PostgreSQL instead of SQLite
   - Add caching (Redis)
   - Add API endpoints (REST/GraphQL)
   - Containerize with Docker

4. **Add testing:**
   - Unit tests for utilities
   - Integration tests for routes
   - Database tests

---

## Resources

- **Flask Documentation:** https://flask.palletsprojects.com/
- **SQLAlchemy Documentation:** https://docs.sqlalchemy.org/
- **SOLID Principles:** https://en.wikipedia.org/wiki/SOLID
---

## Summary

- **Code is easier to understand** - Each file has one responsibility
- **Code is easier to test** - Utilities are isolated and testable
- **Code is easier to modify** - Changes don't break other parts
- **Code is easier to scale** - Adding features doesn't require rewriting

The key insight: **Organize by responsibility, not by feature.**
---

*Last Updated: March 2026*
