from utils.get_loged_user import logged_user
from werkzeug.utils import secure_filename

from flask import g
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif','webp'}


def add_Product(db,Product, product_name, price, description, stock, user, image_url):
    if g.user is None:
        return "user not found"

    try:
           new_Product = Product(
               product_name=product_name,
               price=price,
               image_url=image_url,
               description=description,
               stock=stock,          
               user_id=user._id
           )
           db.session.add(new_Product)
           db.session.commit()
           return(True,"your last product has been added successfully!")
    except ValueError as e:
           db.session.rollback()
           return (str(e))



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_product_image(file,upload_folder):
    """Save product image and return URL or error message"""
    if not file:
        return False, "Image is required"
    
    if not allowed_file(file.filename):
        return False, "Invalid file type. Allowed: png, jpg, jpeg, gif, webp"
    
    try:
        filename = secure_filename(file.filename)
        # Add timestamp to avoid filename conflicts
        import time
        filename = f"{int(time.time())}_{filename}"
        
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        
        file.save(os.path.join(upload_folder, filename))
        image_url = f"/static/uploads/{filename}"
        return True, image_url
    except Exception as e:
        return False, f"Error saving image: {str(e)}"