from flask import g

def remove_From_Cart(Cart,cart_id,db):
    
   

    if g.user is None:
        return "user not found"

    cart_item = Cart.query.filter_by(_id=cart_id, user_id=g.user._id).first()
    
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        return ("item removed")
    else:
        return ("Item not found!")
    