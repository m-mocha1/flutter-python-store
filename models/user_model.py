from extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    _id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(500), default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    products = db.relationship("Product", backref="owner", cascade="all, delete-orphan")
    cart_items = db.relationship("Cart", backref="user", cascade="all, delete-orphan")

    def __init__(self, username, password, description):
        self.username = username
        self.password = password
        self.description = description

    def __repr__(self):
        """String representation for debugging"""
        return f'<User {self.username}>'