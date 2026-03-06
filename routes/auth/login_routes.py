from flask import Blueprint, render_template, redirect, request, url_for, flash
from utils import require_logout, login_user
from services.auth_services import auth_user
from models import User

login_bp = Blueprint('login', __name__)


@login_bp.route("/login",methods=["POST","GET"])
@require_logout
def login():
    if request.method == "POST":
       username = request.form["username"].strip().lower()
       password = request.form["password"]

       ok,message = auth_user(User,username,password)

       if ok :
          login_user(username) 
          return redirect(url_for('home')) # if error
       
       flash(message,"error")

    return render_template("login/login.html") # if GET