def remove_From_Cart(User,Cart,username,cart_id,db):
    
    user = User.query.filter_by(username=username).first()
    cart_item = Cart.query.filter_by(_id=cart_id, user_id=user._id).first()
    
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        return ("item removed")
    else:
        return ("Item not found!")
    