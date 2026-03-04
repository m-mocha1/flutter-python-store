from werkzeug.security import check_password_hash
def auth_user(User,username,password):
    user = User.query.filter_by(username=username).first()
    
    if user and check_password_hash(user.password, password):
        return (True,"success")
    else:
        return(False,"username or password are incorrect")
