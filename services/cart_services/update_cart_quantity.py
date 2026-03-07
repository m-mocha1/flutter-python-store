from flask import g

def update_Cart_Quantity(Cart, qty, cart_id, db):

    if g.user is None:
        return "user not found"
    
    cart_item = Cart.query.filter_by(_id=cart_id, user_id=g.user._id).first()

    try:
        if cart_item and qty:
            cart_item.quantity = int(qty)
            db.session.commit()
            return("Quantity updated!")
        else:
            return("Error updating quantity!")
    except ValueError as e:
        return(str(e))            
        