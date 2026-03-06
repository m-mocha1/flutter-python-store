# models/cart_model.py
from extensions import db
from datetime import datetime

class Cart(db.Model):
    __tablename__ = 'cart'
    
    _id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users._id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products._id'), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship("User", backref="cart_items")
    product = db.relationship("Product", backref="in_cart")
    
    def __init__(self, user_id, product_id, quantity=1):
        """Initialize cart item"""
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity
    
    def __repr__(self):
        """String representation for debugging"""
        return f'<Cart user_id={self.user_id}, product_id={self.product_id}, qty={self.quantity}>'
    
    def get_total_price(self):
        """Calculate total price for this item"""
        if self.product:
            return self.product.price * self.quantity
        return 0