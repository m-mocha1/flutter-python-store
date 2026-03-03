def updateCartQuantity(cart_id):
    if "username" not in session:
        return redirect(url_for("login"))
    
    user = User.query.filter_by(username=session["username"]).first()
    cart_item = Cart.query.filter_by(_id=cart_id, user_id=user._id).first()
    quantity = request.form.get('quantity')
    

    try:
        if cart_item and quantity:
            cart_item.quantity = int(quantity)
            db.session.commit()
            flash("Quantity updated!", "success")
        else:
            flash("Error updating quantity!", "error")
    except ValueError as e:
        flash(str(e),"error")            
        
    return redirect(url_for('myCart'))