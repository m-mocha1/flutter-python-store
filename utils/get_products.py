from flask import g
def get_all_products(Product):
    return Product.query.order_by(Proudct._id.decs()).all
# this to return all products newset first

def get_product_info(Product, product_id):
    return Product.query.filter_by(_id=product_id).first()

def get_other_products(db,Product,product_id):
        return Product.query.filter(Product._id != product_id).order_by(db.func.random()).limit(10).all()