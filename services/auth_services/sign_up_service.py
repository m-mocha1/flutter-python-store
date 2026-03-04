from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError

def create_user(User,username,password,description,db):
    try:
        hashed_pass = generate_password_hash(password=password, method='pbkdf2:sha256')
        new_user = User(
        username=username,
        password=hashed_pass,
        description=description
         )
        
        db.session.add(new_user)
        db.session.commit()
        return (True,"user created")
    
    except IntegrityError:
        db.session.rollback()
        return (False,"user already exists!")



