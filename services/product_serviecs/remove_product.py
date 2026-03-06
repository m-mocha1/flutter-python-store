import os
from utils.auth import get_logged_user
from flask import g

def remove_Product(User, Product, Cart, username, product_id, db, upload_folder):
    
    user = get_loged_user()

    if g.user is None:
        return "user not found"

    if user is None:
        return(False,"user not found")

    product = Product.query.filter_by(_id=product_id).first()
    
    if product is None:
        return(False,"product not found")

    if product and product.user_id == user._id:
        delete_image_file(product.image_url,upload_folder)
        
        Cart.query.filter_by(product_id=product._id).delete()

        db.session.delete(product)
        db.session.commit()
        return (True,"Product removed successfully!")
    else:
        return(False,"You can only remove products you added.")


def delete_image_file(image_url: str,upload_folder):
    """Delete image file from disk given its URL like /static/uploads/filename.jpg"""
    if not image_url:
        return
    try:
        # we only handle files under /static/uploads/
        prefix = "/static/uploads/"
        if not image_url.startswith(prefix):
            return
        
        filename = image_url[len(prefix):]
        file_path = os.path.join(upload_folder, filename)

        if os.path.exists(file_path):
            os.remove(file_path)

    except Exception as e:
        # optional: log error instead of crashing
        print(f"Error deleting file {image_url}: {e}")