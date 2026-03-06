from flask import Blueprint, redirect, url_for
from utils.auth import require_login, logout_user

logout_bp = Blueprint('logout', __name__)

@logout_bp.route("/logout",methods=["POST"])
@require_login 
def log_out():
    logout_user()
    return redirect(url_for("login.login"))    