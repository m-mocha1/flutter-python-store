from flask import g

def get_user_cart(Cart):
    user = g.user
    if user is None:
        return []
    return Cart.query.filter_by(user_id= user._id).all()

def get_user_cart_products_id(Cart):
    cart_items = get_user_cart(Cart)
    return [item.product_id for item in cart_items]

def get_products_not_in_cart(Product,cart_product_ids,db):
    return Product.query.filter(~Product._id.in_(cart_product_ids)).order_by(db.func.random()).limit(10).all()

def sub_total(cart_items):
    subtotal = 0
    for item in cart_items:
            if item.product is None:
                continue  
            subtotal += item.product.price * item.quantity
    return subtotal