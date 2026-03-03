def removeFromCart(cart_id):
    if "username" not in session:
        return redirect(url_for("login"))
    
    user = User.query.filter_by(username=session["username"]).first()
    cart_item = Cart.query.filter_by(_id=cart_id, user_id=user._id).first()
    
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        flash("Item removed from cart!", "success")
    else:
        flash("Item not found!", "error")
    
    return redirect(url_for('myCart'))