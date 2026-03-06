from utils.auth import get_logged_user
from flask import g

def update_Cart_Quantity(User,Cart,username, qty, cart_id, db):
    user = get_logged_user()

    if g.user is None:
        return "user not found"
    
    cart_item = Cart.query.filter_by(_id=cart_id, user_id=user._id).first()

    try:
        if cart_item and qty:
            cart_item.quantity = int(qty)
            db.session.commit()
            return("Quantity updated!")
        else:
            return("Error updating quantity!")
    except ValueError as e:
        return(str(e))            
        