from extensions import db

class User(db.Model):
    _id  = db.Column("id",db.Integer, primary_key=True)
    username = db.Column(db.String(30),nullable=False, unique = True)
    description = db.Column(db.String(30),nullable=False, unique = False)
    password= db.Column(db.String(200), nullable=False)

    def __init__(self, username, password, description):
        self.username = username
        self.password = password
        self.description = description

    def __repr__(self):
        """String representation for debugging"""
        return f'<User {self.username}>'