from config import KEY
from flask import Flask
from extensions import db

def create_app():
   app = Flask(__name__, static_folder='static', static_url_path='/static')
   app.secret_key = KEY
   app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
   app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
   UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'uploads')
   ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif','webp'}
   app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
   return app
   
 




app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)