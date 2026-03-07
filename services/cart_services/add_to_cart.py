def add_to_cart(db, Product, Cart, user_id, product_id, requested_qty):   
    
    product = Product.query.filter_by(_id=product_id).first()
    if not product:
        return(False,"Product not found")
    
    if not product.is_in_stock():
        return(False,"this product out of stock")
    
    existing = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()

    try:
        if existing:
            new_total = existing.quantity + requested_qty
            if not product.can_add(new_total):
                return(False,f"only {product.stock} left in stock")
            existing.quantity = new_total
        else:
            if not product.can_add(requested_qty):
                return (False,f"only {product.stock} left in stock")
            newCartItem = Cart(user_id=user_id,product_id=product_id,quantity=requested_qty)
            db.session.add(newCartItem)
        
        db.session.commit()
        return(True,"item added to cart")   
    except ValueError as e:
        return (False,"error")