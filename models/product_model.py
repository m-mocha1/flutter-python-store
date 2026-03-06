from extensions import db
from sqlalchemy.orm import validates

class Product(db.Model):
    _id  = db.Column("id",db.Integer, primary_key=True)
    product_name = db.Column(db.String(50),nullable=False)
    price = db.Column(db.Float, nullable = False)
    image_url = db.Column(db.String(500),nullable=False)
    description = db.Column(db.String(500), nullable=False)
    stock = db.Column(db.Integer, default=1)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, product_name, price, image_url, description, stock,user_id):
        self.product_name = product_name
        self.price = price
        self.image_url = image_url
        self.description = description
        self.stock = stock
        self.user_id = user_id

    @validates('stock')
    def validate_stock(self,key,value):
        if value <= 0:
            raise ValueError("Stock cannot be neg")
        return value

    def is_in_stock(self):
        return self.stock > 0 

    def can_add(self,quantity):
        return self.stock >= quantity

    def reduce_stock(self, amount):
        if not self.can_add(amount):
            raise ValueError(f"Only {self.stock} left in stock")
        self.stock -= amount