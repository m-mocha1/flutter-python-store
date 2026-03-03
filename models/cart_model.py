from app.extensions import db

class Cart(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, default=1)
    product = db.relationship("Product")
    user = db.relationship("User")


    def __init__(self,user_id,product_id,quantity=1):
      self.user_id = user_id
      self.product_id = product_id
      self.quantity = quantity
