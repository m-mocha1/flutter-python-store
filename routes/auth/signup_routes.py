from flask import Blueprint, render_template, redirect, request, url_for, flash
from utils.auth import require_logout, login_user
from services.auth_services import create_user
from models import User
from extensions import db

signup_bp = Blueprint('signup', __name__)

@signup_bp.route("/sign",methods=["POST","GET"])
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