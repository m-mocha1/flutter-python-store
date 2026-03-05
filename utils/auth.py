# utils/auth.py
from functools import wraps
from flask import g, redirect, url_for, session

# def name explains it
def get_user_by_username(User, username):
    return User.query.filter_by(username=username).first()

# to get the loged in user info and store them globaly
def load_logged_in_user(User):
    g.user = None
    if "username" in session:
        g.user = User.query.filter_by(username=session["username"]).first()

# return the global user info
def get_logged_user():
    return g.user


# a decorated func to check if the user is loged in and handle rerouting
def require_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

# a decorated func to check if the user is loged out to see the sign/login pages
def require_logout(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is not None:
            return redirect(url_for("home"))
        return f(*args, **kwargs)
    return decorated_function

# store the username in session
def login_user(username):
    session["username"] = username

# remove the username from session on logout
def logout_user():
    session.pop("username", None)