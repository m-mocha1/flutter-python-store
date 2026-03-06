from flask import Blueprint, render_template
from utils.auth import require_login, get_logged_user

profile_bp = Blueprint('profile', __name__)

@profile_bp.route("/profile",methods=["GET","POST"])
@require_login 
def profile():
  user = get_logged_user()
  return render_template(
  'profile.html',
   username=user.username,
   description=user.description)